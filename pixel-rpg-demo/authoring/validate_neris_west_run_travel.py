"""Validate live east heel drift with explicit held-frame tolerance."""
from pathlib import Path
import json,sys

from PIL import Image
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/pixel-rpg/model-wave-01/guided/neris-west-run-travel'
trace=json.loads((BASE/'runtime-trace.json').read_text());groups={}
for row in trace:
 if row['planted']:groups.setdefault(row['stance'],[]).append(row)
results=[]
for key,rows in groups.items():
 if len({r['frame'] for r in rows})!=3:continue
 result={'stance':key}
 for kind in ['original','calibrated']:
  xs=[r[kind+'_x'] for r in rows];result[kind]=max(xs)-min(xs)
 results.append(result)
assert len(results)>=4
assert all(trace[i+1]['time']>trace[i]['time'] for i in range(len(trace)-1))
original=max(r['original'] for r in results);calibrated=max(r['calibrated'] for r in results)
assert original>calibrated and calibrated<=3.05
report={'complete_stances':len(results),'original_max_drift':original,'calibrated_max_drift':calibrated,'tolerance':3.05,'limitation':'16fps at48px/s permits3px held-frame residual; flight excluded; heel marker only, art unapproved','results':results}
(BASE/'runtime-validation.json').write_text(json.dumps(report,indent=2))
frames=[Image.open(BASE/f'travel-{i:02d}.png').convert('RGB') for i in range(32)]
frames[0].save(BASE/'comparison.gif',save_all=True,append_images=frames[1:],duration=83,loop=0)
print(json.dumps(report))
