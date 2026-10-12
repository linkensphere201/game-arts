"""Convert the replacement barrel against the existing pilot palette without recoloring it."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from scipy import ndimage
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/pixel-rpg/model-wave-01/guided';OUT=ROOT/'pixel-rpg-demo/mosslight/model_review'
sources={'barrel':'barrel-760001.png','crate':'crate-760002.png','potion':'potion-760003.png','crystal':'crystal-760004.png','sword':'sword-763001.png','shield':'shield-763002.png','herb':'herb-763003.png','coin':'coin-763004.png','tree':'tree-764001.png','rock':'rock-764002.png'}
sources.update(table='table-765001.png',bookshelf='bookshelf-765002.png')
sources.update(door='door-765005.png')
sources.update(chair='chair-765006.png',bed='bed-765007.png')
sources.update(key='key-766001.png',scroll='scroll-766002.png',bread='bread-766003.png',pouch='pouch-766004.png')
sources.update(axe='axe-772004.png',ring='ring-772002.png',mushroom='mushroom-772003.png')
parser=argparse.ArgumentParser();parser.add_argument('--prop',choices=list(sources),default='barrel');args=parser.parse_args()
ident=args.prop;source=BASE/sources[ident];im=Image.open(source).convert('RGB');a=np.asarray(im).astype(int)
white=(a.min(2)>233)&(a.max(2)-a.min(2)<28);labels,_=ndimage.label(white);edge=np.unique(np.r_[labels[0],labels[-1],labels[:,0],labels[:,-1]]);edge=edge[edge!=0]
parts,_=ndimage.label(~np.isin(labels,edge));counts=np.bincount(parts.ravel());counts[0]=0
mask=parts==counts.argmax()
if ident in ['herb','chair','key','ring']:
 mask &= ~white # Enclosed leaf / backrest gaps are transparent too.
 if ident=='chair':
  parts,_=ndimage.label(mask);counts=np.bincount(parts.ravel());counts[0]=0
  mask=parts==counts.argmax() # Reject model speckles floating inside chair gaps.
if ident!='herb':mask=ndimage.binary_erosion(mask,iterations=1)
im=im.convert('RGBA');im.putalpha(Image.fromarray((mask*255).astype('uint8')));im=im.crop(im.getbbox())
colors=set();references={}
for name in ['guild','chest','book','rowan']:
 path=OUT/(name+'.png');references[name]=hashlib.sha256(path.read_bytes()).hexdigest();rgb=np.asarray(Image.open(path).convert('RGBA'));colors.update(map(tuple,rgb[rgb[:,:,3]>0,:3].tolist()))
palette_extension=[(48,73,56),(66,94,68),(86,111,77),(111,133,94),(137,153,111)] if ident in ['tree','rock'] else []
if ident=='rock':palette_extension += [(72,87,80),(96,112,102),(124,139,125),(155,167,148),(181,190,169)]
if ident in ['bed','scroll']:palette_extension += [(161,152,126),(194,185,157),(219,213,187),(237,232,212)]
colors=sorted(colors.union(map(tuple,palette_extension)));assert len(colors)<=256
palette=Image.new('P',(1,1));palette.putpalette([v for c in colors for v in c]+[0]*(768-len(colors)*3))
size={'barrel':(48,64),'crate':(56,56),'tree':(160,192),'rock':(64,64),'table':(128,112),'bookshelf':(144,176),'door':(96,144),'chair':(64,96),'bed':(128,176)}.get(ident,(32,32));w,h=size;im.thumbnail((w-6,h-8),Image.Resampling.LANCZOS);threshold=100 if ident=='herb' else 170;alpha=im.getchannel('A').point(lambda v:255 if v>=threshold else 0)
im=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha)
im=im.crop(im.getbbox()) # Anchor actual surviving pixels after small stems disappear on reduction.
sprite=Image.new('RGBA',size);sprite.alpha_composite(im,((w-im.width)//2,h-4-im.height));sprite.save(OUT/(ident+'.png'))
assert sprite.getbbox()[3]==h-4 and set(np.unique(np.asarray(sprite)[:,:,3]))=={0,255}
for name,digest in references.items():assert hashlib.sha256((OUT/(name+'.png')).read_bytes()).hexdigest()==digest
(BASE/(ident+'-conversion.json')).write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256((OUT/(ident+'.png')).read_bytes()).hexdigest(),'palette_references':references,'palette_extension':palette_extension,'cell':size,'anchor':[w//2,h-4],'status':'static model-derived prop study; camera and pixel art approval pending'},indent=2))
print('PROP_CONVERSION_OK:',ident,size,'binary alpha, shared palette +',len(palette_extension),'declared material shades; references unchanged')
