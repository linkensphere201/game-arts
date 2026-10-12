"""Align the independent W illustration to the side rig, without using E pixels."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy import ndimage
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
OUT=BASE/'left-motion';OUT.mkdir(exist_ok=True)
source=BASE/'rowan-left-768001.png'
sy=[155,270,289,367,445,513,623]
ty=[89,238,266,357,466,550,688]
y=np.interp(np.arange(768),[0]+ty+[768],[86]+sy+[687])
x=242-(np.arange(512)-280)/1.28
gy,gx=np.meshgrid(y,x,indexing='ij')
a=np.asarray(Image.open(source).convert('RGB'),dtype=float)
sample=np.stack([ndimage.map_coordinates(a[:,:,c],[gy,gx],order=1,mode='constant',cval=255) for c in range(3)],axis=2)
target=OUT/'canonical-source.png'
Image.fromarray(np.clip(sample,0,255).astype('uint8')).save(target)
(OUT/'alignment.json').write_text(json.dumps({'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'canonical_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'source_y':sy,'canonical_y':ty,'source_center_x':242,'canonical_center_x':280,'horizontal_scale':1.28,'temporary_reflection':'W artwork faces right only inside the existing side rig; final frames must face left','status':'experimental alignment; masks require visual inspection'},indent=2),encoding='utf-8')
print('LEFT_CANONICAL_SOURCE_READY')
