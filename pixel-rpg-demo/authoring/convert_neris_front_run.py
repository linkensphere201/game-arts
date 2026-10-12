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
source=BASE/'neris-keys-777006.png';base=segment(source);original_bounds=base.getbbox()
bounds=(140,original_bounds[1],385,original_bounds[3]);ref=base.crop(bounds);ref.thumbnail((84,114),Image.Resampling.LANCZOS)
rowan=np.asarray(Image.open(ROOT/'pixel-rpg-demo/mosslight/model_motion/idle_S.png').convert('RGBA').crop((0,0,96,144)))
colors=set(map(tuple,rowan[rowan[:,:,3]>0,:3].tolist()));colors.update(map(tuple,reg['neris']['palette_extension']));colors=sorted(colors)
palette=Image.new('P',(1,1));palette.putpalette([n for c in colors for n in c]+[0]*(768-3*len(colors)))
records=[];cells=[]
for name,path in [('idle',source),('left-lift',BASE/'neris-front-run-777250.png'),('right-lift',BASE/'neris-front-run-777251.png'),('left-arms',BASE/'neris-front-run-clean-777256.png'),('right-arms',BASE/'neris-front-run-clean-777257.png')]:
    segmented=segment(path);box=segmented.getbbox()
    assert bounds[0]<=box[0] and bounds[1]<=box[1] and bounds[2]>=box[2] and bounds[3]>=box[3],(name,box,bounds)
    im=segmented.crop(bounds).resize(ref.size,Image.Resampling.LANCZOS)
    alpha=im.getchannel('A').point(lambda n:255 if n>=128 else 0)
    im=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha)
    cell=Image.new('RGBA',(96,144));cell.alpha_composite(im,(round(48-((original_bounds[0]+original_bounds[2])/2-bounds[0])*ref.width/(bounds[2]-bounds[0])),122-ref.height))
    assert set(np.unique(np.array(cell)[:,:,3]))=={0,255}
    cell.save(OUT/f'neris-front-run-study-{name}.png');cells.append(cell)
    records.append({'pose':name,'source':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bounds':box})
assert all(np.array_equal(np.array(cells[0])[:81],np.array(c)[:81]) for c in cells[1:3]),'Protected upper body changed'
assert len({c.tobytes() for c in cells})==5
assert all(np.array_equal(np.array(cells[0])[:47],np.array(c)[:47]) for c in cells[3:]),'Arm head drift'
assert np.array_equal(np.array(cells[1])[87:],np.array(cells[3])[87:]) and np.array_equal(np.array(cells[2])[87:],np.array(cells[4])[87:]),'Arm edit changed legs'
from PIL import ImageDraw
review=Image.new('RGB',(960,330),'#30353b');d=ImageDraw.Draw(review)
for i,(name,cell) in enumerate(zip(['FRONT IDLE','LEFT KNEE','RIGHT KNEE','LEFT + ARMS','RIGHT + ARMS'],cells)):
    enlarged=cell.resize((192,288),Image.Resampling.NEAREST);review.paste(enlarged,(192*i,28),enlarged);d.text((192*i+15,8),name,fill='white')
review.save(BASE/'neris-front-run-comparison.png')
(BASE/'neris-front-run-study.json').write_text(json.dumps({'status':'two high-knee and opposite arm studies; not a run cycle','fixed_bounds':bounds,'fixed_resize':ref.size,'poses':records,'limitations':['upright torso, shoulder shading and small side remnants remain','shoe contour rough','no compression/flight phases or travel calibration']},indent=2))
print('NERIS_FRONT_RUN_KEYPOSE_OK: common scale, full silhouette, binary alpha, protected upper81')
