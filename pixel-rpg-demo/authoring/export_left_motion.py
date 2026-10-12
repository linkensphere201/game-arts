"""Export an isolated W motion study; do not replace gameplay resources."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided/left-motion'
cfg=json.loads(Path(__file__).with_name('rowan-proportion-study.json').read_text())
view=next(v for v in cfg['views'] if v['direction']=='E')
tx=np.array(cfg['target_y'],float);sy=np.array(view['source_y'],float)
extra_y=np.r_[sy[0]-tx[0]*(sy[1]-sy[0])/(tx[1]-tx[0]),sy,sy[-1]+(144-tx[-1])*(sy[-1]-sy[-2])/(tx[-1]-tx[-2])]
y=np.interp((np.arange(144*3)+.5)/3,np.r_[0,tx,144],extra_y)
x=view['center_x']+((np.arange(96*3)+.5)/3-48)/cfg['horizontal_scale']
gy,gx=np.meshgrid(y,x,indexing='ij')
reference=ROOT/'pixel-rpg-demo/mosslight/model_motion/idle_W.png'
r=np.asarray(Image.open(reference).convert('RGBA'))
colors=sorted(set(map(tuple,r[r[:,:,3]>0,:3].tolist())))
palette=Image.new('P',(1,1));palette.putpalette([v for color in colors for v in color]+[0]*(768-len(colors)*3))
board=Image.new('RGB',(8*192,2*320+32),'#ded8ca');d=ImageDraw.Draw(board)
d.text((12,8),'INDEPENDENT W SOURCE / WALK (TOP) / RUN (BOTTOM) / STUDY',fill='#29333a')
records={}
for row,action in enumerate(('walk','run')):
    sheet=Image.new('RGBA',(96*8,144));gif=[];records[action]=[]
    for i in range(8):
        path=OUT/'rig'/f'{action}-{i}-source.png'
        a=np.asarray(Image.open(path).convert('RGBA'),dtype=float);a[:,:,:3]*=a[:,:,3:4]/255
        sample=np.stack([ndimage.map_coordinates(a[:,:,c],[gy,gx],order=1,mode='constant') for c in range(4)],axis=2)
        alpha=sample[:,:,3:4]/255
        sample[:,:,:3]=np.divide(sample[:,:,:3],alpha,out=np.zeros_like(sample[:,:,:3]),where=alpha>0)
        cell=Image.fromarray(np.clip(sample,0,255).astype('uint8')).resize((96,144),Image.Resampling.LANCZOS)
        alpha=cell.getchannel('A').point(lambda v:255 if v>=150 else 0)
        labels,_=ndimage.label(np.asarray(alpha)>0,structure=np.ones((3,3)))
        counts=np.bincount(labels.ravel());counts[0]=0
        # Remove only isolated 1-2 pixel resampling residue, never substantial limbs.
        alpha=Image.fromarray((np.isin(labels,np.flatnonzero(counts>=3))*255).astype('uint8'))
        cell=cell.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');cell.putalpha(alpha)
        cell=cell.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        assert cell.getbbox() and 0<cell.getbbox()[0]<cell.getbbox()[2]<96
        sheet.alpha_composite(cell,(96*i,0))
        enlarged=cell.resize((192,288),Image.Resampling.NEAREST)
        board.paste(enlarged,(192*i,32+320*row),enlarged)
        frame=Image.new('RGBA',(288,432),'#ded8ca')
        ImageDraw.Draw(frame).ellipse((117,363,171,375),fill='#999b8d')
        frame.alpha_composite(cell.resize((288,432),Image.Resampling.NEAREST));gif.append(frame.convert('RGB'))
        records[action].append({'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bbox':cell.getbbox(),'components':ndimage.label(np.asarray(alpha)>0,structure=np.ones((3,3)))[1]})
    sheet.save(OUT/f'{action}_W.png')
    gif[0].save(OUT/f'{action}_W.gif',save_all=True,append_images=gif[1:],duration=100 if action=='walk' else 75,loop=0)
board.save(OUT/'left-motion-contact.png')
(OUT/'export.json').write_text(json.dumps({'cell':[96,144],'anchor':[48,122],'alignment':json.loads((OUT/'alignment.json').read_text()),'frames':records,'palette_sha256':hashlib.sha256(reference.read_bytes()).hexdigest(),'status':'isolated cutout motion study; gameplay unchanged; joint/cloth review required'},indent=2),encoding='utf-8')
print('LEFT_MOTION_EXPORTED: isolated W walk8/run8; gameplay unchanged')
