"""Fixed-coordinate comparison of Neris running studies; never normalize each pose separately."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from scipy import ndimage
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/pixel-rpg/model-wave-01/guided';OUT=ROOT/'pixel-rpg-demo/mosslight/model_review'
reg=json.loads(Path(__file__).with_name('roster-static-studies.json').read_text())
def segment(path):
 im=Image.open(path).convert('RGBA');a=np.asarray(im)[:,:,:3].astype(int)
 white=(a.min(2)>233)&(a.max(2)-a.min(2)<28)
 labels,_=ndimage.label(white);edge=np.unique(np.r_[labels[0],labels[-1],labels[:,0],labels[:,-1]])
 parts,_=ndimage.label(~np.isin(labels,edge[edge!=0]));counts=np.bincount(parts.ravel());counts[0]=0
 im.putalpha(Image.fromarray(((parts==counts.argmax())*255).astype('uint8')));return im
source=BASE/'neris-profile-777018.png';base=segment(source);original_bounds=base.getbbox()
bounds=(140,original_bounds[1],385,original_bounds[3]);ref=base.crop(bounds);ref.thumbnail((84,114),Image.Resampling.LANCZOS)
rowan=np.asarray(Image.open(ROOT/'pixel-rpg-demo/mosslight/model_motion/idle_S.png').convert('RGBA').crop((0,0,96,144)))
colors=set(map(tuple,rowan[rowan[:,:,3]>0,:3].tolist()));colors.update(map(tuple,reg['neris']['palette_extension']));colors=sorted(colors)
palette=Image.new('P',(1,1));palette.putpalette([n for c in colors for n in c]+[0]*(768-3*len(colors)))
parser=argparse.ArgumentParser();parser.add_argument('--middle',action='store_true');args=parser.parse_args()
path=BASE/('neris-east-run-arms-777235.png' if args.middle else 'neris-east-run-arms-777234.png');im=segment(path)
box=im.getbbox();assert bounds[0]<=box[0] and bounds[2]>=box[2]
im=im.crop(bounds).resize(ref.size,Image.Resampling.LANCZOS);alpha=im.getchannel('A').point(lambda n:255 if n>=128 else 0)
im=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha)
cell=Image.new('RGBA',(96,144));cell.alpha_composite(im,(round(48-((original_bounds[0]+original_bounds[2])/2-bounds[0])*ref.width/(bounds[2]-bounds[0])),122-ref.height))
neutral=Image.open(OUT/'neris-east-run-leg-near-contact.png').convert('RGBA')
a=np.array(cell);n=np.array(neutral)
assert np.array_equal(a[:49],n[:49]),'Head changed'
assert np.array_equal(a[74:],n[74:]),'Belt or legs changed'
cell.save(OUT/('neris-east-run-arm-middle.png' if args.middle else 'neris-east-run-arm-back.png'))
back=np.array(Image.open(OUT/'neris-east-run-arm-back.png').convert('RGBA'))
arm_map=['back','back','middle','front','front','front','middle','back'] if args.middle else ['back']*4+['front']*4
raw=Image.open(BASE/'neris-east-run-leg-phases.png').convert('RGBA');atlas=Image.new('RGBA',raw.size)
for i in range(8):
    phase=raw.crop((i*96,0,(i+1)*96,144));pixels=np.array(phase)
    if arm_map[i]=='back':pixels[:74]=back[:74]
    elif arm_map[i]=='middle':pixels[:74]=a[:74]
    assert np.array_equal(pixels[74:],np.array(phase)[74:])
    atlas.alpha_composite(Image.fromarray(pixels),(i*96,2 if i in (1,5) else 0))
prefix='neris-east-run-arm-middle' if args.middle else 'neris-east-run-arm-phases'
atlas.save(BASE/(prefix+'.png'))
(BASE/(prefix+'.json')).write_text(json.dumps({'status':'three arm poses, unapproved transitions' if args.middle else 'two endpoint arms over eight leg phases, abrupt transition unapproved','arm_source':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'splice_row':74,'arm_mapping':arm_map,'limitations':['single midpoint reused for both swing directions','shoulder seams and flat torso shading','rough hands','travel uncalibrated']},indent=2))
print('NERIS_RUN_ARM_ASSEMBLY_OK: head49 and lower74 preserved, opposite near-arm/leg endpoints')
