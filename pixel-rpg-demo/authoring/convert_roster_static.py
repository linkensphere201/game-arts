"""Convert a recorded model character without changing existing accepted/reference art."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'pixel-rpg-demo/mosslight/model_review'
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
registry=json.loads(Path(__file__).with_name('roster-static-studies.json').read_text())
parser=argparse.ArgumentParser();parser.add_argument('--id',choices=list(registry),required=True);args=parser.parse_args()
spec=registry[args.id];source=ROOT/spec['source']
image=Image.open(source).convert('RGB')
normalization=spec.get('body_scale')
if normalization:
    split=normalization['split_y'];factor=normalization['factor']
    assert 0<split<image.height and 0<factor<=1
    normalized=Image.new('RGB',image.size,'white');normalized.paste(image.crop((0,0,image.width,split)),(0,0))
    body=image.crop((0,split,image.width,image.height));body=body.resize((body.width,round(body.height*factor)),Image.Resampling.LANCZOS)
    normalized.paste(body,(0,split));image=normalized
rgb=np.asarray(image).astype(int)
white=(rgb.min(2)>233)&(rgb.max(2)-rgb.min(2)<28)
labels,_=ndimage.label(white);edge=np.unique(np.r_[labels[0],labels[-1],labels[:,0],labels[:,-1]])
parts,_=ndimage.label(~np.isin(labels,edge[edge!=0]));counts=np.bincount(parts.ravel());counts[0]=0
mask=parts==counts.argmax()
image=image.convert('RGBA');image.putalpha(Image.fromarray((mask*255).astype('uint8')))
figure_height=spec.get('figure_height',114)
assert isinstance(figure_height,int) and 32<=figure_height<=114
image=image.crop(image.getbbox());image.thumbnail((84,figure_height),Image.Resampling.LANCZOS)
reference=ROOT/'pixel-rpg-demo/mosslight/model_motion/idle_S.png'
rowan=Image.open(reference).convert('RGBA').crop((0,0,96,144));a=np.asarray(rowan)
colors=set(map(tuple,a[a[:,:,3]>0,:3].tolist()));colors.update(map(tuple,spec['palette_extension']))
colors=sorted(colors);assert len(colors)<=256
palette=Image.new('P',(1,1));palette.putpalette([v for c in colors for v in c]+[0]*(768-3*len(colors)))
alpha=image.getchannel('A').point(lambda v:255 if v>=128 else 0)
image=image.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');image.putalpha(alpha)
image=image.crop(image.getbbox())
sprite=Image.new('RGBA',(96,144));sprite.alpha_composite(image,((96-image.width)//2,122-image.height))
assert sprite.getbbox()[3]==122 and set(np.unique(np.asarray(sprite)[:,:,3]))=={0,255}
destination=OUT/(args.id+'.png');sprite.save(destination)
board=Image.new('RGB',(900,470),'#ded8c7');draw=ImageDraw.Draw(board)
comparison_id=spec.get('compare_to','bren')
for index,(name,cell) in enumerate([('Rowan',rowan),(comparison_id.title(),Image.open(OUT/(comparison_id+'.png'))),(args.id.title(),sprite)]):
    draw.text((index*300+14,10),name,fill='#33352e')
    zoom=cell.resize((288,432),Image.Resampling.NEAREST);board.paste(zoom,(index*300+6,30),zoom)
board.save(BASE/(args.id+'-roster-review.png'))
(BASE/(args.id+'-conversion.json')).write_text(json.dumps(dict(
    source=spec['source'],body_scale=normalization,figure_height=figure_height,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    output_sha256=hashlib.sha256(destination.read_bytes()).hexdigest(),
    palette_reference_sha256=hashlib.sha256(reference.read_bytes()).hexdigest(),
    palette_extension=spec['palette_extension'],cell=[96,144],anchor=[48,122],status=spec['status']
),indent=2),encoding='utf-8')
print('ROSTER_STATIC_OK:',args.id,'binary alpha, shared palette plus declared materials, sole 122')
