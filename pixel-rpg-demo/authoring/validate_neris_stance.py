"""Validate measured runtime stance drift; no inference of final gait quality."""
from pathlib import Path
import json,sys
contact="--contact" in sys.argv
weighted="--weight" in sys.argv or contact
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/pixel-rpg/model-wave-01/guided/neris-stance'
if '--rear' in sys.argv:BASE=BASE.parent/'neris-rear-stance'
trace=json.loads((BASE/('contact-runtime-trace.json' if contact else 'weight-runtime-trace.json' if weighted else 'runtime-trace.json')).read_text());groups={}
for row in trace:groups.setdefault(row['stance'],[]).append(row)
results=[]
for stance,rows in groups.items():
 if len({r['frame'] for r in rows})!=4:continue
 result={'stance':stance,'samples':len(rows)}
 for kind in ['naive','locked']:
  ys=[r[kind+'_y'] for r in rows];result[kind+'_drift']=max(ys)-min(ys)
 results.append(result)
assert len(results)>=4
assert max(r['locked_drift'] for r in results)<=2.05
if weighted:
 assert all(r['naive_y']==r['locked_y'] for r in trace)
else:
 assert max(r['naive_drift'] for r in results)>4
assert all(trace[i+1]['time']>trace[i]['time'] for i in range(len(trace)-1))
report={'complete_stances':len(results),'naive_max_drift':max(r['naive_drift'] for r in results),'locked_max_drift':max(r['locked_drift'] for r in results),'stance_results':results,'scope':'Actual engine support marker tracks verified sprite sole; max 2.05 px hold drift at 24px/s and12fps. Does not validate natural gait.'}
report['comparison']=['weighted','coordinated-weighted'] if contact else ['locked','weighted'] if weighted else ['naive','locked']
report['identical_support_trajectories']=all(r['naive_y']==r['locked_y'] for r in trace)
(BASE/('contact-runtime-validation.json' if contact else 'weight-runtime-validation.json' if weighted else 'runtime-validation.json')).write_text(json.dumps(report,indent=2))
frames=[Image.open(BASE/(f'contact-travel-{i:02d}.png' if contact else f'weight-travel-{i:02d}.png' if weighted else f'travel-{i:02d}.png')).convert('RGB') for i in range(32)]
frames[0].save(BASE/('contact-comparison.gif' if contact else 'weight-comparison.gif' if weighted else 'travel-comparison.gif'),save_all=True,append_images=frames[1:],duration=83,loop=0)
print(json.dumps(report))
