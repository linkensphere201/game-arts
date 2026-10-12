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
source=ROOT/reg['neris-SW']['source'];base=segment(source);original_bounds=base.getbbox();bounds=(175,original_bounds[1],330,636);ref=base.crop(bounds);ref.thumbnail((84,114),Image.Resampling.LANCZOS)
rowan=np.asarray(Image.open(ROOT/'pixel-rpg-demo/mosslight/model_motion/idle_S.png').convert('RGBA').crop((0,0,96,144)))
colors=set(map(tuple,rowan[rowan[:,:,3]>0,:3].tolist()));colors.update(map(tuple,reg['neris']['palette_extension']));colors=sorted(colors)
palette=Image.new('P',(1,1));palette.putpalette([n for c in colors for n in c]+[0]*(768-3*len(colors)))
cells=[];records=[]
for name,path in [('SW-neutral',source),('SW-near-contact',BASE/'neris-SW-stride-777151.png'),('SW-far-contact',BASE/'neris-SW-stride-777152.png'),('SW-near-passing',BASE/'neris-SW-passing-777153.png'),('SW-far-passing',BASE/'neris-SW-passing-777154.png'),('SW-near-arm',BASE/'neris-SW-arm-777159.png'),('SW-far-arm',BASE/'neris-SW-arm-777160.png'),('SW-near-arm-half',BASE/'neris-SW-arm-777161.png'),('SW-far-arm-half',BASE/'neris-SW-arm-777162.png'),('SW-near-twoarm',BASE/'neris-SW-twoarm-777163.png'),('SW-far-twoarm',BASE/'neris-SW-twoarm-777164.png'),('SW-near-twoarm-half',BASE/'neris-SW-twoarm-777165.png'),('SW-far-twoarm-half',BASE/'neris-SW-twoarm-777166.png'),('SW-near-down',BASE/'neris-SW-intermediate-777167.png'),('SW-far-down',BASE/'neris-SW-intermediate-777168.png'),('SW-near-up',BASE/'neris-SW-intermediate-777169.png'),('SW-far-up',BASE/'neris-SW-intermediate-777170.png')]:
 im=segment(path).crop(bounds).resize(ref.size,Image.Resampling.LANCZOS)
 alpha=im.getchannel('A').point(lambda n:255 if n>=128 else 0)
 im=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha)
 cell=Image.new('RGBA',(96,144));cell.alpha_composite(im,(round(48-((original_bounds[0]+original_bounds[2])/2-bounds[0])*ref.width/(bounds[2]-bounds[0])),122-round((original_bounds[3]-bounds[1])*ref.height/(bounds[3]-bounds[1]))))
 assert {i for i,count in enumerate(cell.getchannel('A').histogram()) if count}=={0,255}
 cell.save(OUT/f'neris-walk-{name}.png');cells.append(np.asarray(cell))
 records.append({'pose':name,'source':str(path.relative_to(ROOT)),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sprite':f'pixel-rpg-demo/mosslight/model_review/neris-walk-{name}.png','bbox':cell.getbbox()})
assert all(np.array_equal(cells[0][:84],c[:84]) for c in cells[1:5]),'Protected SW torso changed'
assert all(np.array_equal(cells[0][:49],c[:49]) for c in cells[5:]),'Arm head changed'
assert all(np.array_equal(cells[a][90:],cells[b][90:]) for a,b in [(1,5),(2,6),(3,7),(4,8)]),'Arm changed legs'
assert all(np.array_equal(cells[a][:,50:],cells[b][:,50:]) and np.array_equal(cells[a][90:],cells[b][90:]) for a,b in [(5,9),(6,10),(7,11),(8,12)]),'Far arm changed near side or legs'
assert all(np.array_equal(cells[0][:84],c[:84]) for c in cells[13:]),'Intermediate torso changed'
assert len({c.tobytes() for c in cells})==17
assert all(c[0,:,3].max()==0 and c[-1,:,3].max()==0 and c[:,0,3].max()==0 and c[:,-1,3].max()==0 for c in cells),'Clipped contact'
atlas=Image.new('RGBA',(1632,144))
for i,c in enumerate(cells):atlas.alpha_composite(Image.fromarray(c),(i*96,0))
atlas.save(BASE/'neris-SW-contact-study.png')
preview=Image.new('RGBA',(4896,432),'#bac4c5');preview.alpha_composite(atlas.resize((4896,432),Image.Resampling.NEAREST));preview.convert('RGB').save(BASE/'neris-SW-contact-review.png')
(BASE/'neris-SW-stride-keyposes.json').write_text(json.dumps({'status':'unapproved diagonal contacts; not a walk clip','fixed_source_bounds':bounds,'fixed_resize':ref.size,'poses':records,'missing':['shoe and cuff polish','arm motion','diagonal ground contact','cross-direction consistency','run']},indent=2))
print('NERIS_SW_KEYPOSES_OK: fixed crop, protected torso, no clipping; art unapproved')
