"""Fixed-coordinate comparison of Neris running studies; never normalize each pose separately."""
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
source=BASE/'neris-profile-777018.png';base=segment(source);original_bounds=base.getbbox()
bounds=(140,original_bounds[1],385,original_bounds[3]);ref=base.crop(bounds);ref.thumbnail((84,114),Image.Resampling.LANCZOS)
rowan=np.asarray(Image.open(ROOT/'pixel-rpg-demo/mosslight/model_motion/idle_S.png').convert('RGBA').crop((0,0,96,144)))
colors=set(map(tuple,rowan[rowan[:,:,3]>0,:3].tolist()));colors.update(map(tuple,reg['neris']['palette_extension']));colors=sorted(colors)
palette=Image.new('P',(1,1));palette.putpalette([n for c in colors for n in c]+[0]*(768-3*len(colors)))
records=[];cells=[]
for name,path in [('idle',source),('walk',BASE/'neris-east-stride-777087.png'),('run-before',BASE/'neris-east-run-777220.png'),('run',BASE/'neris-east-run-details-777222.png')]:
    segmented=segment(path);box=segmented.getbbox()
    assert bounds[0]<=box[0] and bounds[1]<=box[1] and bounds[2]>=box[2] and bounds[3]>=box[3],(name,box,bounds)
    im=segmented.crop(bounds).resize(ref.size,Image.Resampling.LANCZOS)
    alpha=im.getchannel('A').point(lambda n:255 if n>=128 else 0)
    im=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha)
    cell=Image.new('RGBA',(96,144));cell.alpha_composite(im,(round(48-((original_bounds[0]+original_bounds[2])/2-bounds[0])*ref.width/(bounds[2]-bounds[0])),122-ref.height))
    assert set(np.unique(np.array(cell)[:,:,3]))=={0,255}
    cell.save(OUT/f'neris-east-run-study-{name}.png');cells.append(cell)
    records.append({'pose':name,'source':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bounds':box})
assert np.array_equal(np.array(cells[2])[:35],np.array(cells[3])[:35]),'Repair changed head'
assert np.array_equal(np.array(cells[2])[85:],np.array(cells[3])[85:]),'Repair changed legs'
# Run head is intentionally leaned: do not assert equality with the idle head.
from PIL import ImageDraw
review=Image.new('RGB',(768,330),'#30353b');d=ImageDraw.Draw(review)
for i,(name,cell) in enumerate(zip(['IDLE','WALK','RUN BEFORE','RUN REFINED'],cells)):
    review.paste(cell.resize((192,288),Image.Resampling.NEAREST),(192*i,28),cell.resize((192,288),Image.Resampling.NEAREST))
    d.text((192*i+25,8),name,fill='white');d.line((192*i+5,272,192*i+187,272),fill='#73777d')
review.save(BASE/'neris-east-run-comparison.png')
(BASE/'neris-east-run-study.json').write_text(json.dumps({'status':'unapproved single running key pose, not a loop','fixed_bounds':bounds,'fixed_resize':ref.size,'poses':records,'limitations':['collar edges remain rough','hand details rough','cross-view proportions unresolved','no complementary poses or flight phase yet']},indent=2))
print('NERIS_RUN_KEYPOSE_OK: fixed scale, silhouette containment and binary alpha')
