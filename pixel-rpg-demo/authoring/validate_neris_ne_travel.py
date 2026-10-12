"""Validate both axes and Euclidean heel drift from actual NE runtime traces."""
from pathlib import Path
import json,math
from PIL import Image
BASE=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided/neris-NE-travel'
trace=json.loads((BASE/'runtime-trace.json').read_text());meta=json.loads((BASE/'manifest.json').read_text());groups={}
assert abs(math.hypot(*meta['velocity'])-24)<1e-8 and meta['fps']==12
assert all(trace[i+1]['time']>trace[i]['time'] for i in range(len(trace)-1))
for row in trace:
 groups.setdefault(row['stance'],[]).append(row)
 for kind in ['original','calibrated']:
  anchor=meta['frames'][row['frame']][kind+'_anchor' if kind=='original' else 'corrected_anchor']
  assert all(abs(row[kind][axis]-(anchor[axis]+meta['velocity'][axis]*row['time']))<0.001 for axis in range(2))
results=[]
for key,rows in groups.items():
 if len({r['frame'] for r in rows})!=4:continue
 result={'stance':key}
 for kind in ['original','calibrated']:
  pts=[r[kind] for r in rows]
  result[kind]={'x':max(p[0] for p in pts)-min(p[0] for p in pts),'y':max(p[1] for p in pts)-min(p[1] for p in pts),'distance':max(math.dist(a,b) for a in pts for b in pts)}
 results.append(result)
assert len(results)>=4
original=max(r['original']['distance'] for r in results);corrected=max(r['calibrated']['distance'] for r in results)
# 2px travel during a held frame plus <=0.83px phase-rounding spread.
assert corrected<original and corrected<=2.9
report={'stances':len(results),'original_max_distance':original,'corrected_max_distance':corrected,'tolerance':2.9,'status':'contact-marker calibration only; art unapproved','results':results}
(BASE/'runtime-validation.json').write_text(json.dumps(report,indent=2))
frames=[Image.open(BASE/f'travel-{i:02}.png').convert('RGB') for i in range(32)];frames[0].save(BASE/'comparison.gif',save_all=True,append_images=frames[1:],duration=83,loop=0)
print(json.dumps(report))
