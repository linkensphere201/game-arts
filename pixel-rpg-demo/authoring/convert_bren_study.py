"""Preserve broad dragonborn silhouette while matching the existing sprite palette."""
from pathlib import Path
import hashlib,json
import argparse
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
OUT=ROOT/'pixel-rpg-demo/mosslight/model_review'
parser=argparse.ArgumentParser();group=parser.add_mutually_exclusive_group();group.add_argument('--back',action='store_true');group.add_argument('--side',action='store_true');args=parser.parse_args()
ident='bren-side' if args.side else 'bren-back' if args.back else 'bren'
source=BASE/('bren-side-clean-773015.png' if args.side else 'bren-back-773003.png' if args.back else 'bren-773001.png')
im=Image.open(source).convert('RGB');rgb=np.asarray(im).astype(int)
white=(rgb.min(2)>233)&(rgb.max(2)-rgb.min(2)<28)
labels,_=ndimage.label(white)
edge=np.unique(np.r_[labels[0],labels[-1],labels[:,0],labels[:,-1]])
parts,_=ndimage.label(~np.isin(labels,edge[edge!=0]));counts=np.bincount(parts.ravel());counts[0]=0
mask=parts==counts.argmax()
im=im.convert('RGBA');im.putalpha(Image.fromarray((mask*255).astype('uint8')))
im=im.crop(im.getbbox());im.thumbnail((84,114),Image.Resampling.LANCZOS)
reference=ROOT/'pixel-rpg-demo/mosslight/model_motion/idle_S.png'
rowan=Image.open(reference).convert('RGBA').crop((0,0,96,144))
a=np.array(rowan);colors=set(map(tuple,a[a[:,:,3]>0,:3].tolist()))
steel=[(48,62,65),(70,85,89),(94,112,116),(119,138,140),(149,165,164),(192,202,192)]
gold=[(86,65,40),(123,95,57),(157,125,75),(185,152,94),(211,178,120),(232,205,157)]
colors=sorted(colors.union(steel,gold));assert len(colors)<=256
palette=Image.new('P',(1,1));palette.putpalette([v for c in colors for v in c]+[0]*(768-len(colors)*3))
alpha=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
im=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha)
im=im.crop(im.getbbox())
sprite=Image.new('RGBA',(96,144));sprite.alpha_composite(im,((96-im.width)//2,122-im.height))
sprite.save(OUT/(ident+'.png'))
assert sprite.getbbox()[3]==122 and set(np.unique(np.asarray(sprite)[:,:,3]))=={0,255}
board=Image.new('RGB',(900,470),'#ded8c7');draw=ImageDraw.Draw(board)
comparison=[('Rowan',rowan),('Bren / front',Image.open(OUT/'bren.png')),('Bren / rear study',sprite)] if args.back else [('Rowan',rowan),('Sylva',Image.open(OUT/'sylva.png')),('Bren / front study',sprite)]
if args.side:comparison=[('Bren / front',Image.open(OUT/'bren.png')),('Bren / back',Image.open(OUT/'bren-back.png')),('Bren / side study',sprite)]
for index,(name,cell) in enumerate(comparison):
    draw.text((index*300+14,10),name,fill='#33352e')
    zoom=cell.resize((288,432),Image.Resampling.NEAREST);board.paste(zoom,(index*300+6,30),zoom)
board.save(BASE/(ident+'-roster-review.png'))
(BASE/(ident+'-conversion.json')).write_text(json.dumps(dict(
    source=str(source.relative_to(ROOT)),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    output_sha256=hashlib.sha256((OUT/(ident+'.png')).read_bytes()).hexdigest(),
    palette_reference_sha256=hashlib.sha256(reference.read_bytes()).hexdigest(),
    palette_extensions=dict(steel=steel,gold=gold),cell=[96,144],anchor=[48,122],
    status=ident+' static model-derived study; not animation or final acceptance',
    limitations=['camera remains an art review item','front/back/side are studies; diagonal views absent',
                 'central ornament and extra cheek frills removed; boot lacing removed; ear shape, armor and boot volume variation remain',
                 'no idle/walk/run frames','scale texture and gauntlet detail need pixel cleanup']
),indent=2),encoding='utf-8')
print('BREN_STATIC_OK: shared palette plus declared ramps, binary alpha, sole 122')
