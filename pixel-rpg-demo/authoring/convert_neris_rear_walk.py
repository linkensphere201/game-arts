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
source=ROOT/reg['neris-back']['source'];base=segment(source);bounds=base.getbbox();ref=base.crop(bounds);ref.thumbnail((84,114),Image.Resampling.LANCZOS)
rowan=np.asarray(Image.open(ROOT/'pixel-rpg-demo/mosslight/model_motion/idle_S.png').convert('RGBA').crop((0,0,96,144)))
colors=set(map(tuple,rowan[rowan[:,:,3]>0,:3].tolist()));colors.update(map(tuple,reg['neris']['palette_extension']));colors=sorted(colors)
palette=Image.new('P',(1,1));palette.putpalette([n for c in colors for n in c]+[0]*(768-3*len(colors)))
cells=[];records=[]
for name,path in [('rear-neutral',source),('rear-left',BASE/'neris-rear-walk-777053.png'),('rear-right',BASE/'neris-rear-walk-777054.png'),('rear-left-half',BASE/'neris-rear-walk-777055.png'),('rear-right-half',BASE/'neris-rear-walk-777056.png'),('rear-left-arm',BASE/'neris-rear-arm-777061.png'),('rear-right-arm',BASE/'neris-rear-arm-777062.png'),('rear-left-arm-half',BASE/'neris-rear-arm-777063.png'),('rear-right-arm-half',BASE/'neris-rear-arm-777064.png'),('rear-contact-left',BASE/'neris-rear-contact-777065.png'),('rear-contact-right',BASE/'neris-rear-contact-777066.png')]:
 im=segment(path).crop(bounds).resize(ref.size,Image.Resampling.LANCZOS)
 alpha=im.getchannel('A').point(lambda n:255 if n>=128 else 0)
 im=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha)
 cell=Image.new('RGBA',(96,144));cell.alpha_composite(im,((96-ref.width)//2,122-ref.height))
 assert {i for i,count in enumerate(cell.getchannel('A').histogram()) if count}=={0,255}
 # Restore protected support region after resampling to avoid filter bleed.
 if name!='rear-neutral' and 'contact' not in name:
  box=(50,90,96,144) if name.startswith('rear-left') else (0,90,48,144)
  cell.paste(Image.fromarray(cells[0]).crop(box),box[:2])
 cell.save(OUT/f'neris-walk-{name}.png');cells.append(np.asarray(cell))
 records.append({'pose':name,'source':str(path.relative_to(ROOT)),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sprite':f'pixel-rpg-demo/mosslight/model_review/neris-walk-{name}.png','bbox':cell.getbbox()})
assert np.array_equal(cells[0],np.asarray(Image.open(OUT/'neris-back.png').convert('RGBA'))),'Rear neutral parity'
assert all(np.array_equal(cells[0][:76],c[:76]) for c in cells[1:5]),'Protected back/head changed'
assert np.array_equal(cells[0][90:,50:],cells[1][90:,50:]),'Right support leg changed'
assert np.array_equal(cells[0][90:,:48],cells[2][90:,:48]),'Left support leg changed'
assert np.array_equal(cells[0][90:,50:],cells[3][90:,50:]),'Half-left support changed'
assert np.array_equal(cells[0][90:,:48],cells[4][90:,:48]),'Half-right support changed'
assert all(np.array_equal(cells[0][:43],c[:43]) for c in cells[5:]),'Arm redraw changed head'
for arm,leg in [(5,1),(6,2),(7,3),(8,4)]:
 assert np.array_equal(cells[arm][90:],cells[leg][90:]),'Arm redraw changed lower legs'
assert all(np.array_equal(cells[0][:103],c[:103]) for c in cells[9:]),'Contact upper body changed'
(BASE/'neris-rear-walk-keyposes.json').write_text(json.dumps({'status':'rear lift and arm studies; no walk clip','fixed_source_bounds':bounds,'fixed_resize':ref.size,'poses':records,'missing':['rear contact and passing','arm contour and shading polish','stance timing','cross-direction consistency','run']},indent=2))
print('NERIS_REAR_KEYPOSES_OK: rear neutral parity, protected head/back and support legs')
