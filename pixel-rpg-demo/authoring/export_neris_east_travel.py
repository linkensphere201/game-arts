"""Calibrate east stride speed from pixel heels; bounded lower-leg shift candidate."""
from pathlib import Path
import json,hashlib,sys
compact="--compact" in sys.argv
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
OUT=BASE/('neris-east-compact-travel' if compact else 'neris-east-travel');OUT.mkdir(exist_ok=True)
path=BASE/('neris-east-compact-phase-study.png' if compact else 'neris-east-complete-phase-study.png');sheet=Image.open(path).convert('RGBA');out=Image.new('RGBA',sheet.size);records=[]
for i in range(8):
 a=np.array(sheet.crop((i*96,0,(i+1)*96,144)))
 xs=np.where(a[120,:,3]>0)[0]
 if i%4==0:xs=xs[xs>(52 if compact else 55)]
 heel=int(xs.min());target=(53-2*(i%4)) if compact else (59-6*(i%4));shift=target-heel
 assert abs(shift)<=(4 if compact else 2)
 b=np.zeros_like(a)
 for y in range(144):
  dx=round(shift*np.clip((y-100)/14,0,1))
  for x in range(96):
   if 0<=x+dx<96:b[y,x+dx]=a[y,x]
 assert np.array_equal(a[:101],b[:101])
 assert np.array_equal(a[114:,max(0,-shift):min(96,96-shift)],b[114:,max(0,shift):min(96,96+shift)])
 assert b[120,target,3]==255
 out.paste(Image.fromarray(b),(96*i,0))
 records.append({'frame':i,'original_heel':heel,'corrected_heel':target,'lower_shift':shift})
sheet.save(OUT/'original.png');out.save(OUT/'calibrated.png')
(OUT/'manifest.json').write_text(json.dumps({'fps':12 if compact else 8,'original_speed':24,'calibrated_speed':24 if compact else 48,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'frames':records,'status':'unapproved east stride calibration','limits':['held-frame residual drift up to2px' if compact else 'held-frame residual drift up to6px','both feet shift in adjusted lower rows','upper/lower join and art remain unapproved']},indent=2))
print('NERIS_EAST_TRAVEL_EXPORT_OK: measured heel progression, bounded lower shift')
