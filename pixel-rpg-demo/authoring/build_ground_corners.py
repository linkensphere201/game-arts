"""Build 16 corner-connectivity paving overlays from the selected local-model texture."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'pixel-rpg-demo/mosslight/model_ground';BASE=ROOT/'production/pixel-rpg/model-wave-01/ground'
source=OUT/'paving.png';texture=np.asarray(Image.open(source).convert('RGB'))[:32,:32]
y,x=np.mgrid[0:32,0:32]/31.0
atlas=Image.new('RGBA',(128,128));masks=[]
for code in range(16):
 tl,tr,bl,br=[(code>>i)&1 for i in range(4)]
 coverage=tl*(1-x)*(1-y)+tr*x*(1-y)+bl*(1-x)*y+br*x*y
 mask=coverage>=.5;masks.append(mask)
 rgba=np.zeros((32,32,4),dtype='uint8');rgba[:,:,:3]=texture
 # A narrow colored rim reads as paving wear; preserve transparent grass outside.
 rim=mask&(coverage<.57);rgba[rim,:3]=(rgba[rim,:3].astype(float)*.86).astype('uint8')
 rgba[:,:,3]=mask*255
 atlas.paste(Image.fromarray(rgba),((code%4)*32,(code//4)*32))
# Exhaustively verify every valid shared-corner edge has matching alpha coverage.
checks=0
for a in range(16):
 for b in range(16):
  if ((a>>1)&1)==(b&1) and ((a>>3)&1)==((b>>2)&1):
   assert np.array_equal(masks[a][:,-1],masks[b][:,0]);checks+=1
  if ((a>>2)&1)==(b&1) and ((a>>3)&1)==((b>>1)&1):
   assert np.array_equal(masks[a][-1],masks[b][0]);checks+=1
assert not masks[0].any() and masks[15].all()
atlas.save(OUT/'paving-corners.png')
(BASE/'paving-corners.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'atlas_sha256':hashlib.sha256((OUT/'paving-corners.png').read_bytes()).hexdigest(),'cell':[32,32],'corner_bits':['TL','TR','BL','BR'],'tiles':16,'valid_edge_checks':checks,'method':'alpha overlays of model-derived paving; bilinear corner masks; no new model inference','limitations':['regular source slabs','no dirt transition or vegetation edge detail','run export_paving_tileset.gd after PNG import to create editor terrain resource']},indent=2))
print('CORNER_ATLAS_QA_OK:',checks,'compatible edge pairs, 16 masks')
