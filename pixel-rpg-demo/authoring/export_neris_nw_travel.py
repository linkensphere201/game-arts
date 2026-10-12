"""NW two-axis heel calibration at normalized 24px/s; preserve rigid shoe pixels."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/pixel-rpg/model-wave-01/guided';OUT=BASE/'neris-NW-travel';OUT.mkdir(exist_ok=True)
path=BASE/'neris-NW-complete-phase-study.png';sheet=Image.open(path).convert('RGBA');out=Image.new('RGBA',sheet.size);records=[]
# Anatomical rear edge of each support shoe, checked against the actual alpha.
anchors=[(41,119),(42,120),(43,121),(44,121),(49,116),(50,117),(52,117),(53,118)]
for i,(hx,hy) in enumerate(anchors):
 a=np.array(sheet.crop((i*96,0,(i+1)*96,144)));assert a[hy,hx,3]==255
 step=round(math.sqrt(2)*(i%4));target=((41 if i<4 else 49)+step,(118 if i<4 else 115)+step)
 dx,dy=target[0]-hx,target[1]-hy;assert max(abs(dx),abs(dy))<=2
 b=np.zeros_like(a)
 for y in range(144):
  sy=y if y<=100 else (y+dy*100/12)/(1+dy/12) if y<112+dy else y-dy
  sy=round(sy);sx_shift=round(dx*np.clip((sy-100)/12,0,1))
  if 0<=sy<144:
   for x in range(96):
    if 0<=x-sx_shift<96:b[y,x]=a[sy,x-sx_shift]
 assert np.array_equal(a[:101],b[:101]);assert b[target[1],target[0],3]==255
 for y in range(112,140):
  assert np.array_equal(a[y,max(0,-dx):min(96,96-dx)],b[y+dy,max(0,dx):min(96,96+dx)])
 out.paste(Image.fromarray(b),(i*96,0));records.append({'frame':i,'support':'near' if i<4 else 'far','original_anchor':[hx,hy],'corrected_anchor':list(target),'shift':[dx,dy]})
sheet.save(OUT/'original.png');out.save(OUT/'calibrated.png')
(OUT/'manifest.json').write_text(json.dumps({'fps':12,'speed':24,'velocity':[-24/math.sqrt(2),-24/math.sqrt(2)],'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'frames':records,'status':'unapproved diagonal calibration','limits':['both feet move in adjusted bottom rows','nearest-pixel target rounding and held-frame residual','not biomechanical or visual acceptance']},indent=2))
print('NERIS_NW_TRAVEL_EXPORT_OK')
