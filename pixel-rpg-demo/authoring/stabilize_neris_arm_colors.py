"""Transfer reference sleeve shading along authored arm motion; preserve model silhouettes."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/pixel-rpg/model-wave-01/guided';OUT=ROOT/'pixel-rpg-demo/mosslight/model_review'
cfg=json.loads((BASE/'neris-walk-keyposes.json').read_text());bounds=cfg['fixed_source_bounds'];size=cfg['fixed_resize'];offset=((96-size[0])//2,122-size[1])
ref=np.asarray(Image.open(OUT/'neris-walk-neutral.png').convert('RGBA'))
shoulder=offset[1]+(286-bounds[1])*size[1]/(bounds[3]-bounds[1])
records=[]
for name,seed,leg,half in [('left-arm',777043,'left',False),('right-arm',777044,'right',False),('left-arm-half',777045,'left',True),('right-arm-half',777046,'right',True)]:
    source=OUT/f'neris-walk-{name}.png';a=np.array(Image.open(source).convert('RGBA'));candidate=a.copy()
    source_mask=Image.open(BASE/f'neris-arm-pose-{seed}-mask.png').convert('L').crop(bounds).resize(tuple(size),Image.Resampling.LANCZOS)
    mask=Image.new('L',(96,144));mask.paste(source_mask,offset);active=np.asarray(mask)>127
    changed=0
    for y,x in np.argwhere(active & (a[:,:,3]==255)):
        side='left' if x<48 else 'right';forward=side!=leg
        factor=(1.04 if forward else .925) if half else (1.08 if forward else .85)
        sy=round(shoulder+(y-shoulder)/factor)
        if not 0<=sy<144:continue
        # Keep original texels tied to the arm, rather than new model colors per frame.
        if ref[sy,x,3]==255:
            candidate[y,x,:3]=ref[sy,x,:3];changed+=1
    assert np.array_equal(a[:,:,3],candidate[:,:,3]),'Silhouette changed'
    assert np.array_equal(a[:43],candidate[:43]) and np.array_equal(a[92:],candidate[92:]),'Protected head/legs changed'
    assert np.array_equal(a[~active],candidate[~active]),'Unmasked colors changed'
    dest=OUT/f'neris-walk-{name}-stable.png';Image.fromarray(candidate).save(dest)
    records.append({'pose':name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'reference_sha256':hashlib.sha256((OUT/'neris-walk-neutral.png').read_bytes()).hexdigest(),'transferred_pixels':changed,'output_sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
(BASE/'neris-arm-color-study.json').write_text(json.dumps({'status':'unapproved model-derived color-transfer comparison; geometry unchanged','method':'nearest texel along inverse authored arm transform; keep target where reference is transparent','records':records},indent=2))
print('NERIS_ARM_COLOR_STUDY_OK: unchanged silhouettes/head/legs and colors outside arm mask')
