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
for name,path in [('near-contact',BASE/'neris-east-run-details-777222.png'),('near-down',BASE/'neris-east-run-down-777231.png'),('near-support',BASE/'neris-east-run-crossing-777229.png'),('near-flight',BASE/'neris-east-run-phase-777227.png'),('far-contact',BASE/'neris-east-run-phase-777226.png'),('far-down',BASE/'neris-east-run-down-777232.png'),('far-support',BASE/'neris-east-run-crossing-777230.png'),('far-flight',BASE/'neris-east-run-phase-777228.png')]:
    segmented=segment(path);box=segmented.getbbox()
    assert bounds[0]<=box[0] and bounds[1]<=box[1] and bounds[2]>=box[2] and bounds[3]>=box[3],(name,box,bounds)
    im=segmented.crop(bounds).resize(ref.size,Image.Resampling.LANCZOS)
    alpha=im.getchannel('A').point(lambda n:255 if n>=128 else 0)
    im=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha)
    cell=Image.new('RGBA',(96,144));cell.alpha_composite(im,(round(48-((original_bounds[0]+original_bounds[2])/2-bounds[0])*ref.width/(bounds[2]-bounds[0])),122-ref.height))
    assert set(np.unique(np.array(cell)[:,:,3]))=={0,255}
    cell.save(OUT/f'neris-east-run-leg-{name}.png');cells.append(cell)
    records.append({'pose':name,'source':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bounds':box})
assert all(np.array_equal(np.array(cells[0])[:81],np.array(c)[:81]) for c in cells[1:]),'Protected upper body changed'
assert len({c.tobytes() for c in cells})==8
contact_floor=max(cells[0].getbbox()[3],cells[4].getbbox()[3])
assert all(contact_floor-cells[i].getbbox()[3]>=4 for i in (3,7)),'Flight feet did not clear contact floor'
sheet=Image.new('RGBA',(768,144))
for i,c in enumerate(cells):sheet.alpha_composite(c,(i*96,0))
sheet.save(BASE/'neris-east-run-leg-phases.png')
weighted=Image.new('RGBA',(768,144))
for i,c in enumerate(cells):
    dy=2 if i in (1,5) else 0
    weighted.alpha_composite(c,(i*96,dy))
    if dy:assert abs(c.getbbox()[3]+dy-contact_floor)<=1,'Compression sole leaves ground'
weighted.save(BASE/'neris-east-run-leg-weighted.png')
(BASE/'neris-east-run-leg-phases.json').write_text(json.dumps({'status':'eight leg-phase studies, fixed arms; incomplete run cycle','fixed_bounds':bounds,'fixed_resize':ref.size,'poses':records,'contact_floor':contact_floor,'compression_dy':2,'flight_clearance':[contact_floor-cells[i].getbbox()[3] for i in (3,7)],'limitations':['near/far legs have weak visual differentiation','opposite arm phases absent','arms remain fixed','shoe and coat contours rough','no travel calibration']},indent=2))
print('NERIS_RUN_LEGS_OK: eight unique poses, fixed upper81, airborne silhouettes, common scale')
