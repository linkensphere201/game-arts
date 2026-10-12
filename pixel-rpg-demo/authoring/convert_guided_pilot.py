"""Convert the bounded guided pilot for an isolated engine review, not delivery approval."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy import ndimage
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'pixel-rpg-demo/mosslight/model_review';OUT.mkdir(exist_ok=True)
base=ROOT/'production/pixel-rpg/model-wave-01/guided'
entries=[('rowan',ROOT/'production/pixel-rpg/candidates/mosslight_chibi_731212_00001_.png',(64,96)),('guild',base/'guild-752005.png',(320,320)),('chest',base/'chest-752003.png',(56,56)),('book',base/'book-752004.png',(32,32))]
crops=[]
for ident,src,size in entries:
    im=Image.open(src).convert('RGB');rgb=np.asarray(im)
    white=(rgb.min(axis=2)>233)&((rgb.max(axis=2).astype(int)-rgb.min(axis=2))<28)
    labels,_=ndimage.label(white)
    border=np.unique(np.concatenate([labels[0],labels[-1],labels[:,0],labels[:,-1]]));border=border[border!=0]
    fg=~np.isin(labels,border);parts,_=ndimage.label(fg);counts=np.bincount(parts.ravel());counts[0]=0;fg=parts==counts.argmax()
    fg=ndimage.binary_erosion(fg,iterations=1)
    alpha=Image.fromarray((fg*255).astype('uint8'));im=im.convert('RGBA');im.putalpha(alpha)
    crop=im.crop(alpha.getbbox());crops.append(crop)
# Equal per-category palette sample weight, including the skin/hair family.
pool=Image.new('RGB',(128*len(crops),128))
for i,crop in enumerate(crops):pool.paste(crop.convert('RGB').resize((128,128)),(i*128,0))
palette=pool.quantize(colors=128,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
records=[]
for (ident,src,(w,h)),crop in zip(entries,crops):
    scale=min((w-6)/crop.width,(h-8)/crop.height);rw,rh=round(crop.width*scale),round(crop.height*scale)
    small=crop.resize((rw,rh),Image.Resampling.LANCZOS)
    mask=small.getchannel('A').point(lambda a:255 if a>=170 else 0)
    colored=small.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');colored.putalpha(mask)
    sprite=Image.new('RGBA',(w,h));sprite.alpha_composite(colored,((w-rw)//2,h-4-rh));sprite.save(OUT/f'{ident}.png')
    assert sprite.getbbox() and set(np.asarray(sprite.getchannel('A')).ravel())=={0,255}
    assert sprite.getbbox()[3]<=h-4
    records.append({'id':ident,'source':str(src.relative_to(ROOT)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'cell':[w,h],'anchor':[w//2,h-4],'status':'static review only'})
(base/'conversion.json').write_text(json.dumps({'shared_palette_limit':128,'method':'connected white background removal; largest component; resample, shared quantization, binary alpha','assets':records,'limitations':['automatic conversion, not final pixel cleanup','camera consistency unresolved','single static view, no new animation']},indent=2),encoding='utf-8')
(ROOT/'pixel-rpg-demo/model_review.tscn').write_text('[gd_scene load_steps=2 format=3]\n\n[ext_resource type="Script" path="res://model_review.gd" id="1"]\n\n[node name="ModelArtReview" type="Node2D"]\nscript = ExtResource("1")\n',encoding='utf-8')
print('GUIDED_CONVERSION_OK: four bounded RGBA sprites; 128-color shared palette; review only')
