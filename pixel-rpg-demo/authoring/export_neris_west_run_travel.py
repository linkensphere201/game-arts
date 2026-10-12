"""Bounded running heel calibration; airborne slots have no planted anchor."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/pixel-rpg/model-wave-01/guided';OUT=BASE/'neris-west-run-travel';OUT.mkdir(exist_ok=True)
path=BASE/'neris-west-run-arm-middle.png';sheet=Image.open(path).convert('RGBA');out=Image.new('RGBA',sheet.size);records=[]
for i in range(8):
 a=np.array(sheet.crop((i*96,0,(i+1)*96,144)));planted=i%4<3
 heel=int(np.where(a[119,:,3]>0)[0].max()) if planted else None
 target=42+3*(i%4) if planted else None
 shift=target-heel if planted else 0;assert abs(shift)<=2
 b=np.zeros_like(a)
 for y in range(144):
  dx=round(shift*np.clip((y-100)/14,0,1))
  for x in range(96):
   if 0<=x+dx<96:b[y,x+dx]=a[y,x]
 assert np.array_equal(a[:101],b[:101])
 assert np.count_nonzero(a[:,:,3])==np.count_nonzero(b[:,:,3]),'Clipped pixel'
 assert np.array_equal(a[114:,max(0,-shift):min(96,96-shift)],b[114:,max(0,shift):min(96,96+shift)])
 if planted:assert b[119,target,3]==255
 else:assert np.array_equal(a,b)
 out.paste(Image.fromarray(b),(96*i,0));records.append({'frame':i,'planted':planted,'original_heel':heel,'corrected_heel':target,'lower_shift':shift})
sheet.save(OUT/'original.png');out.save(OUT/'calibrated.png')
(OUT/'manifest.json').write_text(json.dumps({'fps':16,'original_speed':-48,'calibrated_speed':-48,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'frames':records,'status':'unapproved running calibration','limits':['support marker only, not full sole or biomechanics','both feet shift below adjusted rows','flight excluded from planted-foot drift','3px per held frame residual permitted']},indent=2))
print('NERIS_WEST_RUN_TRAVEL_EXPORT_OK: bound2px, upper101 unchanged, airborne frames unchanged')
