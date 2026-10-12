"""Local conversion study from approved-quality model art; no procedural character redraw.
This produces single-view static candidates, not final animation or hand-cleaned pixel art.
"""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'production/pixel-rpg/candidates/mosslight_chibi_731212_00001_.png'
OUT=ROOT/'production/pixel-rpg/model-sprite-study';OUT.mkdir(parents=True,exist_ok=True)
image=Image.open(SOURCE).convert('RGB');rgb=np.asarray(image)
white=(rgb.min(axis=2)>235)&((rgb.max(axis=2).astype(int)-rgb.min(axis=2))<25)
labels,_=ndimage.label(white)
border=np.unique(np.concatenate([labels[0],labels[-1],labels[:,0],labels[:,-1]]));border=border[border!=0]
foreground=~np.isin(labels,border)
parts,_=ndimage.label(foreground);sizes=np.bincount(parts.ravel());sizes[0]=0
foreground=parts==sizes.argmax()  # Removes disconnected remnants from the extracted design sheet.
alpha=Image.fromarray((foreground*255).astype('uint8'))
cutout=image.convert('RGBA');cutout.putalpha(alpha);box=alpha.getbbox();crop=cutout.crop(box)
cutout.save(OUT/'segmented-source.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
small=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',12)
board=Image.new('RGBA',(1152,700),'#ded8c8');d=ImageDraw.Draw(board)
d.text((20,16),'MODEL ART -> TRANSPARENT CUTOUT -> SPRITE SIZE STUDY',font=font,fill='#292937')
d.text((20,42),'Same model-drawn face and costume. Single static view; animation is not produced yet.',font=small,fill='#51545b')
preview=crop.copy();preview.thumbnail((300,550),Image.Resampling.LANCZOS);board.alpha_composite(preview,((310-preview.width)//2+15,91))
d.text((25,651),'Model source / crop',font=font,fill='#292937')
records=[]
for index,(w,h,colors,scale) in enumerate([(48,64,48,5),(64,96,64,4),(96,128,96,3)]):
    fit=min((w-8)/crop.width,(h-12)/crop.height);size=(round(crop.width*fit),round(crop.height*fit))
    resized=crop.resize(size,Image.Resampling.LANCZOS)
    mask=resized.getchannel('A').point(lambda a:255 if a>=145 else 0)
    quantized=resized.convert('RGB').quantize(colors=colors,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGBA');quantized.putalpha(mask)
    sprite=Image.new('RGBA',(w,h));origin=((w-size[0])//2,h-6-size[1]);sprite.alpha_composite(quantized,origin)
    name=f'swordswoman-{w}x{h}.png';sprite.save(OUT/name)
    enlarged=sprite.resize((w*scale,h*scale),Image.Resampling.NEAREST)
    x=335+index*265;y=100+(520-h*scale)//2
    # Uniform scale within each candidate; nearest-neighbor enlargement makes lost clusters visible.
    board.alpha_composite(enlarged,(x,y))
    d.text((x,613),f'{w}x{h} / {colors} colors',font=font,fill='#292937')
    d.text((x,637),'1 view, static study',font=small,fill='#51545b')
    records.append({'file':name,'size':[w,h],'anchor':[w//2,h-6],'visible_size':size,'palette_limit':colors,'alpha':'binary','status':'conversion study; pixel cleanup and view/pose work pending'})
board.convert('RGB').save(OUT/'conversion-board.png')
# Retain the four local model outputs as a compact contact sheet for reproducible selection.
contact=Image.new('RGB',(1024,420),'#ded8c8');cd=ImageDraw.Draw(contact)
for i,seed in enumerate([731201,731202,731203,731204]):
    im=Image.open(ROOT/f'production/pixel-rpg/candidates/mosslight_portrait_{seed}_00001_.png').convert('RGB');im.thumbnail((250,375),Image.Resampling.LANCZOS);contact.paste(im,(i*256,20));cd.text((i*256+8,400),str(seed),font=small,fill='#292937')
contact.save(OUT/'portrait-candidates.png')
record={'source':str(SOURCE.relative_to(ROOT)),'sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'bbox':box,'method':'border-connected near-white segmentation, largest connected figure, premultiplied resize, palette quantization, alpha threshold; no geometric character reconstruction','candidates':records,'limitations':['single near-frontal view','not perspective-matched yet','not hand-cleaned final pixel art','no animation generated']}
(OUT/'conversion.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
for r in records:
    im=Image.open(OUT/r['file']);assert im.size==tuple(r['size']);assert set(np.asarray(im.getchannel('A')).ravel())=={0,255};assert im.getbbox()[3]<=r['anchor'][1]
print('MODEL_SPRITE_STUDY_OK',box,records)
