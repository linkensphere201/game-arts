"""Bounded palette candidate for model-derived running upper garments."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from scipy import ndimage
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
source=BASE/'neris-east-run-arm-middle.png';im=Image.open(source).convert('RGBA');before=np.array(im);after=before.copy()
mapping={(79,56,49):(65,43,49),(60,38,35):(65,43,49),(88,56,49):(91,52,63),(77,52,43):(65,43,49),(73,46,41):(65,43,49),(94,65,56):(91,52,63),(106,76,68):(91,52,63),(90,60,53):(91,52,63),(111,65,52):(91,52,63),(93,62,48):(91,52,63)}
records=[];allowed=np.zeros(before.shape[:2],bool)
for i in range(8):
    a=before[:,i*96:(i+1)*96];out=after[:,i*96:(i+1)*96];dy=2 if i in (1,5) else 0
    rgb=a[:,:,:3].astype(int);skin=(rgb[:,:,0]>145)&(rgb[:,:,0]>rgb[:,:,1]*1.10)&(rgb[:,:,1]>rgb[:,:,2]*1.03)&(a[:,:,3]>0)
    protected=ndimage.binary_dilation(skin,iterations=1)
    region=np.zeros((144,96),bool);region[51+dy:73+dy]=True;region&=~protected;region&=a[:,:,3]>0
    selected=np.zeros((144,96),bool)
    for old,new in mapping.items():
        hit=region&np.all(a[:,:,:3]==old,axis=2);out[hit,:3]=new;selected|=hit
    allowed[:,i*96:(i+1)*96]=selected
    records.append({'frame':i,'changed_pixels':int(np.any(out!=a,axis=2).sum()),'selected_pixels':int(selected.sum())})
assert np.array_equal(before[:,:,3],after[:,:,3]),'Alpha changed'
assert np.array_equal(before[~allowed],after[~allowed]),'Unselected pixel changed'
target=BASE/'neris-east-run-material.png';Image.fromarray(after).save(target)
(BASE/'neris-east-run-material.json').write_text(json.dumps({'status':'optional unapproved material candidate; geometry unchanged','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'material_rows':[51,73],'down_offset':2,'mapping':[[list(k),list(v)] for k,v in mapping.items()],'frames':records,'limitations':['hand mask heuristic','shoulder geometry and folds not repaired','art not approved']},indent=2))
print('NERIS_RUN_MATERIAL_OK: alpha and every unselected pixel unchanged',sum(r['changed_pixels'] for r in records))
