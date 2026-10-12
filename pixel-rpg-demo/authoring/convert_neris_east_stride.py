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
source=ROOT/reg['neris-side']['source'];base=segment(source);original_bounds=base.getbbox();bounds=(150,original_bounds[1],375,original_bounds[3]);ref=base.crop(bounds);ref.thumbnail((84,114),Image.Resampling.LANCZOS)
rowan=np.asarray(Image.open(ROOT/'pixel-rpg-demo/mosslight/model_motion/idle_S.png').convert('RGBA').crop((0,0,96,144)))
colors=set(map(tuple,rowan[rowan[:,:,3]>0,:3].tolist()));colors.update(map(tuple,reg['neris']['palette_extension']));colors=sorted(colors)
palette=Image.new('P',(1,1));palette.putpalette([n for c in colors for n in c]+[0]*(768-3*len(colors)))
cells=[];records=[]
for name,path in [('east-neutral',source),('east-near-contact',BASE/'neris-east-stride-777069.png'),('east-far-contact',BASE/'neris-east-stride-777070.png'),('east-near-passing',BASE/'neris-east-passing-777071.png'),('east-far-passing',BASE/'neris-east-passing-777072.png'),('east-near-arm',BASE/'neris-east-arm-777077.png'),('east-far-arm',BASE/'neris-east-arm-777078.png'),('east-near-arm-half',BASE/'neris-east-arm-777079.png'),('east-far-arm-half',BASE/'neris-east-arm-777080.png'),('east-near-down',BASE/'neris-east-intermediate-777081.png'),('east-far-down',BASE/'neris-east-intermediate-777082.png'),('east-near-up',BASE/'neris-east-intermediate-777083.png'),('east-far-up',BASE/'neris-east-intermediate-777084.png'),('east-near-compact',BASE/'neris-east-stride-777087.png'),('east-far-compact',BASE/'neris-east-stride-777088.png'),('east-near-compact-down',BASE/'neris-east-intermediate-777089.png'),('east-far-compact-down',BASE/'neris-east-intermediate-777090.png'),('east-near-compact-up',BASE/'neris-east-intermediate-777091.png'),('east-far-compact-up',BASE/'neris-east-intermediate-777092.png')]:
 im=segment(path).crop(bounds).resize(ref.size,Image.Resampling.LANCZOS)
 alpha=im.getchannel('A').point(lambda n:255 if n>=128 else 0)
 im=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha)
 cell=Image.new('RGBA',(96,144));cell.alpha_composite(im,(round(48-((original_bounds[0]+original_bounds[2])/2-bounds[0])*ref.width/(bounds[2]-bounds[0])),122-ref.height))
 assert {i for i,count in enumerate(cell.getchannel('A').histogram()) if count}=={0,255}
 cell.save(OUT/f'neris-walk-{name}.png');cells.append(np.asarray(cell))
 records.append({'pose':name,'source':str(path.relative_to(ROOT)),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sprite':f'pixel-rpg-demo/mosslight/model_review/neris-walk-{name}.png','bbox':cell.getbbox()})
assert all(np.array_equal(cells[0][:76],c[:76]) for c in cells[1:5]),'Protected profile head/torso changed'
assert len({c.tobytes() for c in cells})==19
assert all(np.where(c[:,:,3]>0)[1].max()<95 and np.where(c[:,:,3]>0)[1].min()>0 for c in cells),'Clipped stride'
assert all(np.array_equal(cells[0][:43],c[:43]) for c in cells[5:]),'Arm pose head drift'
assert np.array_equal(cells[1][85:],cells[5][85:]) and np.array_equal(cells[2][85:],cells[6][85:]),'Arm pose altered legs'
assert np.array_equal(cells[3][85:],cells[7][85:]) and np.array_equal(cells[4][85:],cells[8][85:]),'Half arm pose altered legs'
assert all(np.array_equal(cells[0][:76],c[:76]) for c in cells[9:]),'Intermediate torso changed'
(BASE/'neris-east-stride-keyposes.json').write_text(json.dumps({'status':'unapproved side contact and passing studies; no walk clip','fixed_source_bounds':bounds,'original_source_bounds':original_bounds,'fixed_resize':ref.size,'poses':records,'note':'expanded shared crop preserves stride toes; separately anchored neutral study does not replace static side sprite','missing':['foot and hem polish','passing and arm motion','stance timing','cross-direction consistency','run']},indent=2))
print('NERIS_EAST_KEYPOSES_OK: fixed expanded crop, protected head/torso, no horizontal clipping')
