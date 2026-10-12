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
source=ROOT/reg['neris']['source'];base=segment(source);bounds=base.getbbox();ref=base.crop(bounds);ref.thumbnail((84,114),Image.Resampling.LANCZOS)
rowan=np.asarray(Image.open(ROOT/'pixel-rpg-demo/mosslight/model_motion/idle_S.png').convert('RGBA').crop((0,0,96,144)))
colors=set(map(tuple,rowan[rowan[:,:,3]>0,:3].tolist()));colors.update(map(tuple,reg['neris']['palette_extension']));colors=sorted(colors)
palette=Image.new('P',(1,1));palette.putpalette([n for c in colors for n in c]+[0]*(768-3*len(colors)))
cells=[];records=[]
for name,path in [('neutral',source),('left',BASE/'neris-walk-pose-777036.png'),('right',BASE/'neris-walk-pose-777037.png'),('left-half',BASE/'neris-walk-pose-777040.png'),('right-half',BASE/'neris-walk-pose-777039.png'),('left-arm',BASE/'neris-arm-pose-777043.png'),('right-arm',BASE/'neris-arm-pose-777044.png'),('left-arm-half',BASE/'neris-arm-pose-777045.png'),('right-arm-half',BASE/'neris-arm-pose-777046.png'),('contact-left',BASE/'neris-contact-777047.png'),('contact-right',BASE/'neris-contact-777048.png')]:
 im=segment(path).crop(bounds).resize(ref.size,Image.Resampling.LANCZOS)
 alpha=im.getchannel('A').point(lambda n:255 if n>=128 else 0)
 im=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha)
 cell=Image.new('RGBA',(96,144));cell.alpha_composite(im,((96-ref.width)//2,122-ref.height))
 assert {i for i,count in enumerate(cell.getchannel('A').histogram()) if count}=={0,255}
 cell.save(OUT/f'neris-walk-{name}.png');cells.append(np.asarray(cell))
 records.append({'pose':name,'source':str(path.relative_to(ROOT)),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sprite':f'pixel-rpg-demo/mosslight/model_review/neris-walk-{name}.png','bbox':cell.getbbox()})
assert np.array_equal(cells[0],np.asarray(Image.open(OUT/'neris.png').convert('RGBA'))),'Neutral conversion differs from current front'
assert all(np.array_equal(cells[0][:78],c[:78]) for c in cells[1:5]),'Protected upper body changed'
assert np.array_equal(cells[0][103:,49:],cells[1][103:,49:]),'Right support foot changed'
assert np.array_equal(cells[0][103:,:48],cells[2][103:,:48]),'Left support foot changed'
assert np.array_equal(cells[0][103:,49:],cells[3][103:,49:]),'Half-left support foot changed'
assert np.array_equal(cells[0][103:,:48],cells[4][103:,:48]),'Half-right support foot changed'
assert all(np.array_equal(cells[0][:43],c[:43]) for c in cells[5:]),'Head changed in arm poses'
assert np.array_equal(cells[1][92:],cells[5][92:]),'Left leg pose changed during arm conversion'
assert np.array_equal(cells[2][92:],cells[6][92:]),'Right leg pose changed during arm conversion'
assert np.array_equal(cells[3][92:],cells[7][92:]),'Half-left leg changed during arm conversion'
assert np.array_equal(cells[4][92:],cells[8][92:]),'Half-right leg changed during arm conversion'
assert all(np.array_equal(cells[0][:103],c[:103]) for c in cells[9:]),'Contact upper body changed'
contact_feet=[]
for c in cells[9:]:
    bottoms=[]
    for lo,hi in [(28,48),(49,68)]:
        rows=np.where(np.any(c[103:,lo:hi,3]>0,axis=1))[0];assert len(rows)>0;bottoms.append(int(rows[-1]+103))
    contact_feet.append(bottoms)
assert contact_feet[0][0]>contact_feet[0][1] and contact_feet[1][1]>contact_feet[1][0],'Contact depth ordering is wrong'
(BASE/'neris-walk-keyposes.json').write_text(json.dumps({'status':'lift and arm studies plus two projected contact poses; not a completed walk cycle','fixed_source_bounds':bounds,'fixed_resize':ref.size,'protected_upper_rows':{'leg_only':78,'arm':43},'lift_support_foot_pixels_unchanged':True,'contact_feet_y':contact_feet,'poses':records,'missing':['contact/passing timing and ground-lock validation','arm/coat contour polish','weight transfer','all-direction walk/run']},indent=2))
print('NERIS_WALK_KEYPOSES_OK: fixed mapping; leg poses preserve upper78/support feet, arm poses preserve head43/legs; not a cycle')


