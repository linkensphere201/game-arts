"""Compare local-model knee artwork at the same coordinates/palette as its source."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
parser=argparse.ArgumentParser();parser.add_argument('--seed',type=int,default=771001);args=parser.parse_args()
suffix='' if args.seed==771001 else '-'+str(args.seed)
generation=json.loads((BASE/f'rowan-front-knee-{args.seed}.json').read_text())
fixed_rows=54 if generation['arguments'].get('swing_arm') else 75
cfg=json.loads(Path(__file__).with_name('rowan-proportion-study.json').read_text());v=next(v for v in cfg['views'] if v['direction']=='S')
sy=np.array(v['source_y']);ty=np.array(cfg['target_y'])
yy=np.interp((np.arange(144*3)+.5)/3,np.r_[0,ty,144],np.r_[sy[0]-ty[0]*(sy[1]-sy[0])/(ty[1]-ty[0]),sy,sy[-1]+(144-ty[-1])*(sy[-1]-sy[-2])/(ty[-1]-ty[-2])])
xx=v['center_x']+((np.arange(96*3)+.5)/3-48)/cfg['horizontal_scale'];gy,gx=np.meshgrid(yy,xx,indexing='ij')
ref=ROOT/'pixel-rpg-demo/mosslight/model_motion/idle_S.png';r=np.asarray(Image.open(ref).convert('RGBA'));colors=sorted(set(map(tuple,r[r[:,:,3]>0,:3].tolist())))
palette=Image.new('P',(1,1));palette.putpalette([n for c in colors for n in c]+[0]*(768-len(colors)*3))
cells=[];records=[]
for path in (ROOT/v['source'],BASE/f'rowan-front-knee-{args.seed}.png'):
    im=Image.open(path).convert('RGBA');a=np.asarray(im);rgb=a[:,:,:3].astype(int)
    white=((rgb.min(2)>233)&(rgb.max(2)-rgb.min(2)<28))|(a[:,:,3]<128)
    labels,_=ndimage.label(white);edge=np.unique(np.r_[labels[0],labels[-1],labels[:,0],labels[:,-1]])
    parts,_=ndimage.label(~np.isin(labels,edge[edge!=0]));counts=np.bincount(parts.ravel());counts[0]=0
    im.putalpha(Image.fromarray((ndimage.binary_erosion(parts==counts.argmax(),iterations=2)*255).astype('uint8')))
    a=np.asarray(im,dtype=float);a[:,:,:3]*=a[:,:,3:4]/255
    sampled=np.stack([ndimage.map_coordinates(a[:,:,c],[gy,gx],order=1,mode='constant') for c in range(4)],axis=2)
    alpha=sampled[:,:,3:4]/255;sampled[:,:,:3]=np.divide(sampled[:,:,:3],alpha,out=np.zeros_like(sampled[:,:,:3]),where=alpha>0)
    cell=Image.fromarray(np.clip(sampled,0,255).astype('uint8')).resize((96,144),Image.Resampling.LANCZOS)
    alpha=cell.getchannel('A').point(lambda n:255 if n>=150 else 0)
    cell=cell.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');cell.putalpha(alpha)
    assert set(np.unique(np.asarray(alpha)))=={0,255}
    cells.append(cell);records.append({'source':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bbox':cell.getbbox()})
assert np.array_equal(np.asarray(cells[0])[:fixed_rows],np.asarray(cells[1])[:fixed_rows]),'Protected upper region changed during conversion'
cells[0].save(ROOT/'pixel-rpg-demo/mosslight/model_review/rowan-keypose-neutral.png')
out=ROOT/f'pixel-rpg-demo/mosslight/model_review/rowan-front-knee{suffix}.png';cells[1].save(out)
board=Image.new('RGB',(640,480),'#ded8ca');d=ImageDraw.Draw(board)
for i,cell in enumerate(cells):
    d.text((16+i*320,12),'Standing source' if i==0 else 'Local-model raised knee / study',fill='#29333a')
    enlarged=cell.resize((288,432),Image.Resampling.NEAREST);board.paste(enlarged,(16+i*320,35),enlarged)
board.save(BASE/f'rowan-keypose-comparison{suffix}.png')
(BASE/f'rowan-keypose-conversion{suffix}.json').write_text(json.dumps({'sources':records,'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'cell':[96,144],'identical_upper_rows':fixed_rows,'status':'key-pose study; costume and pose review required; no animation integration'},indent=2),encoding='utf-8')
print(f'KEYPOSE_CONVERSION_OK: same transform/palette, identical upper {fixed_rows} rows; single study only')
