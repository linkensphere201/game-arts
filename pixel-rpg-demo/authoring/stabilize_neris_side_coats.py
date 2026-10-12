"""Bounded side-coat palette study; preserve geometry and non-cloth colors."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy import ndimage
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/pixel-rpg/model-wave-01/guided';OUT=BASE/'neris-coat-palette';OUT.mkdir(exist_ok=True)
# Explicit brown fabric ramp -> existing burgundy ramp. Do not recolor all browns.
RAMP={(106,76,68):(123,65,79),(94,65,56):(91,52,63),(124,91,76):(154,90,104),(79,56,49):(65,43,49),(90,60,53):(91,52,63),(60,38,35):(65,43,49),(73,46,41):(65,43,49),(66,41,36):(65,43,49),(66,49,43):(65,43,49),(77,52,43):(91,52,63)}
records=[]
for heading,folder,name in [('E','neris-east-compact-travel','east'),('W','neris-west-travel','west')]:
 for kind,path in [('walk',BASE/folder/'calibrated.png'),('idle',ROOT/f'pixel-rpg-demo/mosslight/model_review/neris-walk-{name}-neutral.png')]:
  a=np.array(Image.open(path).convert('RGBA'));b=a.copy();mask=np.zeros(a.shape[:2],bool)
  # Protect visible hands per frame instead of excluding an entire horizontal band.
  rgb=a[:,:,:3].astype(float)
  skin=(rgb[:,:,0]>160)&(rgb[:,:,0]>rgb[:,:,1]*1.12)&(rgb[:,:,1]>rgb[:,:,2]*1.05)&(a[:,:,3]==255)
  skin[:65]=False;skin[88:]=False
  protected=ndimage.binary_dilation(skin,iterations=2)
  area=np.zeros(a.shape[:2],bool);area[49:103]=True;area[protected]=False
  for old,new in RAMP.items():
   selected=area & (a[:,:,3]==255) & np.all(a[:,:,:3]==old,axis=2);b[selected,:3]=new;mask|=selected
  assert mask.any() and np.array_equal(a[:,:,3],b[:,:,3]) and np.array_equal(a[~mask],b[~mask])
  assert np.array_equal(a[:49],b[:49]) and np.array_equal(a[protected],b[protected]) and np.array_equal(a[103:],b[103:])
  out=OUT/f'{heading}-{kind}.png';Image.fromarray(b).save(out)
  records.append({'heading':heading,'kind':kind,'source':str(path.relative_to(ROOT)),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'changed_pixels':int(mask.sum())})
(OUT/'manifest.json').write_text(json.dumps({'status':'unapproved side-coat palette study','limits':['hand protection inferred from warm highlights; material review still required','no geometry or proportion correction'],'records':records},indent=2))
print('NERIS_COAT_PALETTE_OK: unchanged alpha, protected head/hand regions/legs and nonselected colors')
