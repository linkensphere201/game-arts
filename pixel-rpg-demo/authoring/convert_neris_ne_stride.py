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
source=ROOT/reg['neris-NE']['source'];base=segment(source);original_bounds=base.getbbox();bounds=(155,original_bounds[1],365,708);assert bounds[0]<=original_bounds[0] and bounds[2]>=original_bounds[2], 'Crop clips neutral silhouette'
ref=base.crop(bounds);ref.thumbnail((84,114),Image.Resampling.LANCZOS)
rowan=np.asarray(Image.open(ROOT/'pixel-rpg-demo/mosslight/model_motion/idle_S.png').convert('RGBA').crop((0,0,96,144)))
colors=set(map(tuple,rowan[rowan[:,:,3]>0,:3].tolist()));colors.update(map(tuple,reg['neris']['palette_extension']));colors=sorted(colors)
palette=Image.new('P',(1,1));palette.putpalette([n for c in colors for n in c]+[0]*(768-3*len(colors)))
cells=[];records=[]
for name,path in [('NE-neutral',source),('NE-near-contact',BASE/'neris-NE-stride-777171.png'),('NE-far-contact',BASE/'neris-NE-stride-777172.png'),('NE-near-passing',BASE/'neris-NE-passing-777173.png'),('NE-far-passing',BASE/'neris-NE-passing-777174.png'),('NE-near-arm',BASE/'neris-NE-arm-777187.png'),('NE-far-arm',BASE/'neris-NE-arm-777188.png'),('NE-near-arm-half',BASE/'neris-NE-arm-777189.png'),('NE-far-arm-half',BASE/'neris-NE-arm-777190.png'),('NE-near-twoarm',BASE/'neris-NE-twoarm-777195.png'),('NE-far-twoarm',BASE/'neris-NE-twoarm-777196.png'),('NE-near-twoarm-half',BASE/'neris-NE-twoarm-777197.png'),('NE-far-twoarm-half',BASE/'neris-NE-twoarm-777198.png'),('NE-near-down',BASE/'neris-NE-intermediate-777199.png'),('NE-far-down',BASE/'neris-NE-intermediate-777200.png'),('NE-near-up',BASE/'neris-NE-intermediate-777201.png'),('NE-far-up',BASE/'neris-NE-intermediate-777202.png')]:
 im=segment(path).crop(bounds).resize(ref.size,Image.Resampling.LANCZOS)
 alpha=im.getchannel('A').point(lambda n:255 if n>=128 else 0)
 im=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha)
 cell=Image.new('RGBA',(96,144));cell.alpha_composite(im,(round(48-((original_bounds[0]+original_bounds[2])/2-bounds[0])*ref.width/(bounds[2]-bounds[0])),122-round((original_bounds[3]-bounds[1])*ref.height/(bounds[3]-bounds[1]))))
 assert {i for i,count in enumerate(cell.getchannel('A').histogram()) if count}=={0,255}
 cell.save(OUT/f'neris-walk-{name}.png');cells.append(np.asarray(cell))
 records.append({'pose':name,'source':str(path.relative_to(ROOT)),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sprite':f'pixel-rpg-demo/mosslight/model_review/neris-walk-{name}.png','bbox':cell.getbbox()})
assert all(np.array_equal(cells[0][:78],c[:78]) for c in cells[1:5]),'Protected NE torso changed'
assert all(np.array_equal(cells[0][:49],c[:49]) for c in cells[5:]),'Head changed'
assert all(np.array_equal(cells[a][91:],cells[b][91:]) for a,b in [(1,5),(2,6),(3,7),(4,8)]),'Legs changed'
assert all(np.array_equal(cells[a][:,50:],cells[b][:,50:]) and np.array_equal(cells[a][91:],cells[b][91:]) for a,b in [(5,9),(6,10),(7,11),(8,12)]),'Far arm changed near side or legs'
assert all(np.array_equal(cells[0][:78],c[:78]) for c in cells[13:]),'Intermediate torso changed'
assert len({c.tobytes() for c in cells})==17
assert all(c[0,:,3].max()==0 and c[-1,:,3].max()==0 and c[:,0,3].max()==0 and c[:,-1,3].max()==0 for c in cells),'Clipped contact'
atlas=Image.new('RGBA',(1632,144))
for i,c in enumerate(cells):atlas.alpha_composite(Image.fromarray(c),(i*96,0))
atlas.save(BASE/'neris-NE-contact-study.png')
preview=Image.new('RGBA',(4896,432),'#bac4c5');preview.alpha_composite(atlas.resize((4896,432),Image.Resampling.NEAREST));preview.convert('RGB').save(BASE/'neris-NE-contact-review.png')
(BASE/'neris-NE-stride-keyposes.json').write_text(json.dumps({'status':'unapproved diagonal contacts and passing; not a complete walk','fixed_source_bounds':bounds,'fixed_resize':ref.size,'poses':records,'missing':['shoe and cuff polish','arm motion','diagonal ground contact','cross-direction consistency','run']},indent=2))
print('NERIS_NE_KEYPOSES_OK: fixed crop, protected torso, no clipping; art unapproved')
