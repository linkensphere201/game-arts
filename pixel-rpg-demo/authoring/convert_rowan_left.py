"""Compare an independently redrawn left view against the old mirrored idle."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from PIL import Image
from scipy import ndimage
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
parser=argparse.ArgumentParser();parser.add_argument('--direction',choices=['W','NW','SW'],default='W');args=parser.parse_args()
spec={
 'W':('rowan-left-768001.png','rowan-left',242,[155,270,289,367,445,513,623]),
 'NW':('rowan-NW-cloth-769002.png','rowan-NW',237,[155,270,290,367,457,516,617]),
 'SW':('rowan-SW-770001.png','rowan-SW',240,[155,266,290,356,443,499,617])
}[args.direction]
filename,ident,center,sy=spec;source=BASE/filename
im=Image.open(source).convert('RGBA');a=np.asarray(im);rgb=a[:,:,:3].astype(int)
white=(rgb.min(2)>233)&(rgb.max(2)-rgb.min(2)<28)
background,_=ndimage.label(white)
edge=np.unique(np.r_[background[0],background[-1],background[:,0],background[:,-1]])
labels,_=ndimage.label(~np.isin(background,edge[edge!=0]));counts=np.bincount(labels.ravel());counts[0]=0
im.putalpha(Image.fromarray((ndimage.binary_erosion(labels==counts.argmax())*255).astype('uint8')))
ty=[8,38,42,61,82,96,122]
y=np.interp((np.arange(144*3)+.5)/3,ty,sy,left=-20,right=800)
x=center+((np.arange(96*3)+.5)/3-48)/.256
gy,gx=np.meshgrid(y,x,indexing='ij');a=np.asarray(im,dtype=float);a[:,:,:3]*=a[:,:,3:4]/255
sample=np.stack([ndimage.map_coordinates(a[:,:,c],[gy,gx],order=1,mode='constant') for c in range(4)],axis=2)
alpha=sample[:,:,3:4]/255
sample[:,:,:3]=np.divide(sample[:,:,:3],alpha,out=np.zeros_like(sample[:,:,:3]),where=alpha>0)
cell=Image.fromarray(np.clip(sample,0,255).astype('uint8')).resize((96,144),Image.Resampling.LANCZOS)
alpha=cell.getchannel('A').point(lambda v:255 if v>=150 else 0)
reference=ROOT/f'pixel-rpg-demo/mosslight/model_motion/idle_{args.direction}.png'
r=np.asarray(Image.open(reference).convert('RGBA'))
colors=sorted(set(map(tuple,r[r[:,:,3]>0,:3].tolist())))
palette=Image.new('P',(1,1));palette.putpalette([v for color in colors for v in color]+[0]*(768-len(colors)*3))
cell=cell.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');cell.putalpha(alpha)
shift=122-cell.getbbox()[3]
anchored=Image.new('RGBA',(96,144));anchored.alpha_composite(cell,(0,shift));cell=anchored
assert cell.getbbox()[3]==122 and set(np.unique(np.asarray(cell)[:,:,3]))=={0,255}
output=ROOT/f'pixel-rpg-demo/mosslight/model_review/{ident}.png';cell.save(output)
(BASE/(ident+'-conversion.json')).write_text(json.dumps({'direction':args.direction,'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'source_landmarks':sy,'target_landmarks':ty,'cell':[96,144],'anchor':[48,122],'status':'independent static source comparison; this converter does not update gameplay','limitations':['landmark warp is not camera reprojection','hair part and hip accessory need art review','SW walk/run remain mirrored in gameplay; W/NW have separate motion exporters']},indent=2))
print('LEFT_STATIC_OK: independent model source, shared palette, binary alpha and sole y122')
