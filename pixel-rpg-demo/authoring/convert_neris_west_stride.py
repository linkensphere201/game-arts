"""Fixed-coordinate conversion of Neris lift poses; never normalize each pose separately."""
from pathlib import Path
import hashlib,json
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
source=ROOT/reg['neris-W']['source'];base=segment(source);original_bounds=base.getbbox();bounds=(175,original_bounds[1],340,original_bounds[3]);ref=base.crop(bounds);ref.thumbnail((84,114),Image.Resampling.LANCZOS)
rowan=np.asarray(Image.open(ROOT/'pixel-rpg-demo/mosslight/model_motion/idle_S.png').convert('RGBA').crop((0,0,96,144)))
colors=set(map(tuple,rowan[rowan[:,:,3]>0,:3].tolist()));colors.update(map(tuple,reg['neris']['palette_extension']));colors=sorted(colors)
palette=Image.new('P',(1,1));palette.putpalette([n for c in colors for n in c]+[0]*(768-3*len(colors)))
cells=[];records=[]
for name,path in [('west-neutral',source),('west-near-contact',BASE/'neris-west-ankle-777095.png'),('west-far-contact',BASE/'neris-west-ankle-777096.png'),('west-near-passing',BASE/'neris-west-passing-777099.png'),('west-far-passing',BASE/'neris-west-passing-777100.png'),('west-near-arm',BASE/'neris-west-arm-777109.png'),('west-far-arm',BASE/'neris-west-arm-777110.png'),('west-near-arm-half',BASE/'neris-west-arm-777111.png'),('west-far-arm-half',BASE/'neris-west-arm-777112.png'),('west-near-down',BASE/'neris-west-intermediate-777113.png'),('west-far-down',BASE/'neris-west-intermediate-777114.png'),('west-near-up',BASE/'neris-west-intermediate-777117.png'),('west-far-up',BASE/'neris-west-intermediate-777118.png')]:
 im=segment(path).crop(bounds).resize(ref.size,Image.Resampling.LANCZOS)
 alpha=im.getchannel('A').point(lambda n:255 if n>=128 else 0)
 im=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha)
 cell=Image.new('RGBA',(96,144));cell.alpha_composite(im,(round(48-((original_bounds[0]+original_bounds[2])/2-bounds[0])*ref.width/(bounds[2]-bounds[0])),122-ref.height))
 assert {i for i,count in enumerate(cell.getchannel('A').histogram()) if count}=={0,255}
 cell.save(OUT/f'neris-walk-{name}.png');cells.append(np.asarray(cell))
 records.append({'pose':name,'source':str(path.relative_to(ROOT)),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sprite':f'pixel-rpg-demo/mosslight/model_review/neris-walk-{name}.png','bbox':cell.getbbox()})
assert all(np.array_equal(cells[0][:85],c[:85]) for c in cells[1:5]),'Protected west head/torso changed'
assert all(np.array_equal(cells[0][:45],c[:45]) for c in cells[5:]),'Arm head changed'
assert all(np.array_equal(cells[a][90:],cells[b][90:]) for a,b in [(1,5),(2,6),(3,7),(4,8)]),'Arm altered lower body'
assert all(np.array_equal(cells[0][:85],c[:85]) for c in cells[9:]),'Intermediate torso changed'
assert len({c.tobytes() for c in cells})==13
assert all(np.where(c[:,:,3]>0)[1].max()<95 and np.where(c[:,:,3]>0)[1].min()>0 for c in cells),'Clipped stride'
atlas=Image.new('RGBA',(1248,144))
for i,c in enumerate(cells):atlas.alpha_composite(Image.fromarray(c),(i*96,0))
atlas.save(BASE/'neris-west-contact-study.png')
preview=Image.new('RGBA',(3744,432),'#bac4c5');preview.alpha_composite(atlas.resize((3744,432),Image.Resampling.NEAREST));preview.convert('RGB').save(BASE/'neris-west-contact-review.png')
(BASE/'neris-west-stride-keyposes.json').write_text(json.dumps({'status':'unapproved contact studies; ankle continuity improved; shoe and cuff polish remains; no animation clip','fixed_source_bounds':bounds,'fixed_resize':ref.size,'poses':records,'missing':['shoe and cuff polish','arm shading consistency','stance timing','cross-direction consistency','run']},indent=2))
print('NERIS_WEST_KEYPOSES_OK: fixed crop, protected torso, no clipping; art unapproved')
