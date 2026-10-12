"""Static elf scale study, preserving proportions and the current Rowan palette."""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
OUT=ROOT/'pixel-rpg-demo/mosslight/model_review'
parser=argparse.ArgumentParser();parser.add_argument('--direction',choices=['front','back','side'],default='front');args=parser.parse_args()
back=args.direction=='back'
source=BASE/{'front':'sylva-staff-761002.png','back':'sylva-back-volume-761013.png','side':'sylva-side-costume-761018.png'}[args.direction]
ident='sylva' if args.direction=='front' else 'sylva-'+args.direction
im=Image.open(source).convert('RGB');rgb=np.asarray(im).astype(int)
bg=(rgb.min(2)>233)&(rgb.max(2)-rgb.min(2)<28)
labels,_=ndimage.label(bg)
edge=np.unique(np.r_[labels[0],labels[-1],labels[:,0],labels[:,-1]])
parts,_=ndimage.label(~np.isin(labels,edge[edge!=0]))
counts=np.bincount(parts.ravel());counts[0]=0
mask=parts==counts.argmax()
im=im.convert('RGBA');im.putalpha(Image.fromarray((mask*255).astype('uint8')))
im=im.crop(im.getbbox());source_bounds=im.size
im.thumbnail((84,114),Image.Resampling.LANCZOS)
reference=ROOT/'pixel-rpg-demo/mosslight/model_motion/idle_S.png'
rowan=Image.open(reference).convert('RGBA').crop((0,0,96,144))
colors=sorted(set(map(tuple,np.asarray(rowan)[np.asarray(rowan)[:,:,3]>0,:3].tolist())))
# Shared base palette needs a restrained gold ramp: Rowan has no blonde hair.
gold_ramp=[(86,65,40),(123,95,57),(157,125,75),(185,152,94),(211,178,120),(232,205,157)]
colors=sorted(set(colors+gold_ramp))
assert len(colors)<=256
palette=Image.new('P',(1,1));palette.putpalette([v for c in colors for v in c]+[0]*(768-3*len(colors)))
alpha=im.getchannel('A').point(lambda x:255 if x>=128 else 0)
im=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha)
sprite=Image.new('RGBA',(96,144));sprite.alpha_composite(im,((96-im.width)//2,122-im.height))
sprite.save(OUT/(ident+'.png'))
assert sprite.getbbox()[3]==122
assert set(np.unique(np.asarray(sprite)[:,:,3]))=={0,255}
board=Image.new('RGB',(672,510),'#ded8c7');draw=ImageDraw.Draw(board)
comparison=Image.open(OUT/'sylva.png').convert('RGBA') if args.direction!='front' else rowan
for i,(name,cell) in enumerate([('Sylva / front' if args.direction!='front' else 'Rowan / existing',comparison),('Sylva / '+args.direction+' study',sprite)]):
    x=30+i*336;draw.text((x,12),name,fill='#33352e')
    zoom=cell.resize((288,432),Image.Resampling.NEAREST)
    draw.ellipse((x+99,386,x+189,402),fill='#b6b0a1')
    board.paste(zoom,(x,30),zoom)
draw.text((30,480),'3x nearest | 96x144 cells | Static studies; motion not authored',fill='#33352e')
board.save(BASE/(ident+'-scale-review.png'))
(BASE/(ident+'-conversion.json')).write_text(json.dumps({
    'source':str(source.relative_to(ROOT)), 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
    'palette_reference':str(reference.relative_to(ROOT)), 'palette_sha256':hashlib.sha256(reference.read_bytes()).hexdigest(),
    'source_bounds':source_bounds, 'scaled_size':im.size, 'cell':[96,144],'anchor':[48,122], 'gold_palette_extension':gold_ramp,
    'output_sha256':hashlib.sha256((OUT/(ident+'.png')).read_bytes()).hexdigest(),
    'status':'static proportion-preserving conversion study; not accepted production pixel art',
    'limitations':['Front/back/side static studies only; no animations','Staff overlaps robe at this resolution','Gameplay camera and head/body match require review','Rear hair needs highlight review; side shoulder/cuff/hem and shoe design still differ from front']
},indent=2),encoding='utf-8')
print('SYLVA_STATIC_OK: binary alpha, Rowan palette plus six gold shades, sole at 122; no directional animation claim')
