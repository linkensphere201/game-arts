"""Convert model plank texture into a bounded periodic pixel floor sample."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/pixel-rpg/model-wave-01/ground'
parser=argparse.ArgumentParser();parser.add_argument('--wall',action='store_true');args=parser.parse_args()
ident='wall' if args.wall else 'wood';size=(256,128) if args.wall else (128,128)
source=BASE/('timber-wall-765004.png' if args.wall else 'wood-floor-765003.png');output=ROOT/'pixel-rpg-demo/mosslight/model_ground'/(ident+'.png')
pixels=np.asarray(Image.open(source).convert('RGB').resize(size,Image.Resampling.LANCZOS),dtype=float).copy()
# Reconcile only a four-pixel edge band, preserving the model-painted center.
for axis in ([1] if args.wall else [0,1]):
    for distance in range(4):
        first=[slice(None),slice(None)];last=first.copy()
        first[axis]=distance;last[axis]=-1-distance
        first=tuple(first);last=tuple(last)
        average=(pixels[first]+pixels[last])/2
        weight=(4-distance)/4
        pixels[first]=(1-weight)*pixels[first]+weight*average
        pixels[last]=(1-weight)*pixels[last]+weight*average
im=Image.fromarray(np.rint(pixels).astype('uint8')).quantize(colors=24,dither=Image.Dither.NONE).convert('RGB')
im.save(output);a=np.asarray(im)
assert np.array_equal(a[:,0],a[:,-1])
if not args.wall:assert np.array_equal(a[0],a[-1])
assert len(im.getcolors())<=24
board=Image.new('RGB',(size[0]*4,size[1]*(1 if args.wall else 4)))
for y in range(1 if args.wall else 4):
    for x in range(4):board.paste(im,(x*size[0],y*size[1]))
board.save(BASE/(ident+'-repeat.png'))
(BASE/(ident+'-conversion.json')).write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'size':size,'colors':len(im.getcolors()),'edge_band':4,'repeat_axes':['x'] if args.wall else ['x','y'],'edge_rgb_equal':True,'status':'periodic full-pattern study; not arbitrary 32px terrain connectivity or final art approval'},indent=2))
print('MATERIAL_REPEAT_OK:',ident,size,'<=24 colors, declared opposite edges match')
