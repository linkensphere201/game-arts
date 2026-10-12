"""Preserve model drawing details while comparing explicit cross-view landmarks."""
from pathlib import Path
import json, hashlib
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[2]
CONFIG=Path(__file__).with_name('rowan-proportion-study.json')
config=json.loads(CONFIG.read_text(encoding='utf-8'))
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided/proportions'
OUT.mkdir(exist_ok=True)

def foreground(im):
    rgba=np.asarray(im).astype(int)
    rgb=rgba[:,:,:3]
    white=(rgb.min(2)>233)&((rgb.max(2)-rgb.min(2))<28)
    background=white|(rgba[:,:,3]<128)
    labels,_=ndimage.label(background)
    edge=np.unique(np.concatenate([labels[0],labels[-1],labels[:,0],labels[:,-1]]))
    edge=edge[edge!=0]
    fg=(~np.isin(labels,edge))&(rgba[:,:,3]>=128)
    parts,_=ndimage.label(fg);counts=np.bincount(parts.ravel());counts[0]=0
    keep=np.flatnonzero(counts>=max(64,counts.max()*.005))
    fg=ndimage.binary_erosion(np.isin(parts,keep),iterations=1)
    result=im.copy();result.putalpha(Image.fromarray((fg*255).astype('uint8')))
    return result

assert len(config['target_y'])==len(config['landmarks'])
assert all(a<b for a,b in zip(config['target_y'],config['target_y'][1:]))
normalized=[];records=[]
for view in config['views']:
    assert len(view['source_y'])==len(config['target_y'])
    assert all(a<b for a,b in zip(view['source_y'],view['source_y'][1:]))
    src=ROOT/view['source'];im=foreground(Image.open(src).convert('RGBA'))
    # Oversample the continuous piecewise mapping, then resolve into native pixel cells.
    w,h=config['cell'];zoom=4
    xx=(np.arange(w*zoom)+.5)/zoom
    yy=(np.arange(h*zoom)+.5)/zoom
    sx=view['center_x']+(xx-config['anchor'][0])/config['horizontal_scale']
    sy=np.interp(yy,config['target_y'],view['source_y'],left=-20,right=im.height+20)
    gy,gx=np.meshgrid(sy,sx,indexing='ij')
    rgba=np.asarray(im,dtype=float)
    # Premultiply before sampling to avoid white fringes from the source background.
    rgba[:,:,:3]*=rgba[:,:,3:4]/255
    sampled=np.stack([ndimage.map_coordinates(rgba[:,:,c],[gy,gx],order=1,mode='constant',cval=0) for c in range(4)],axis=2)
    a=sampled[:,:,3:4]/255
    sampled[:,:,:3]=np.divide(sampled[:,:,:3],a,out=np.zeros_like(sampled[:,:,:3]),where=a>0)
    large=Image.fromarray(np.clip(sampled,0,255).astype('uint8'))
    cell=large.resize((w,h),Image.Resampling.LANCZOS)
    cell.putalpha(cell.getchannel('A').point(lambda v:255 if v>=150 else 0))
    normalized.append(cell)
    records.append({'direction':view['direction'],'source':view['source'],'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source_landmarks':view['source_y'],'target_landmarks':config['target_y']})

pool=Image.new('RGB',(96*len(normalized),128))
for i,cell in enumerate(normalized):pool.paste(cell.convert('RGB'),(i*96,0))
palette=pool.quantize(colors=96,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
board=Image.new('RGB',(len(normalized)*300,2*410+70),'#ded8ca')
draw=ImageDraw.Draw(board);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
draw.text((15,10),'BEFORE: FIT TO CELL / AFTER: EXPLICIT LANDMARK ALIGNMENT — STUDY ONLY',fill='#29333a',font=font)
switch_frames=[]
for i,(view,cell,record) in enumerate(zip(config['views'],normalized,records)):
    alpha=cell.getchannel('A')
    cell=cell.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');cell.putalpha(alpha)
    path=OUT/f"rowan-{view['direction']}-96x128.png";cell.save(path)
    box=cell.getbbox()
    assert box and 0<box[0]<box[2]<96 and 6<=box[1]<=10 and 121<=box[3]<=123, (view['direction'],box)
    assert set(np.unique(np.asarray(alpha)))=={0,255}
    record.update(output=str(path.relative_to(ROOT)),output_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bbox=box)
    before=Image.open(OUT.parent/f"rowan-{view['direction']}-96x128.png").convert('RGBA')
    for row,img in enumerate([before,cell]):
        preview=img.resize((288,384),Image.Resampling.NEAREST)
        x=i*300;y=40+row*410
        board.paste(preview,(x,y),preview)
        draw.text((x+8,y+383),view['direction']+(' / before' if row==0 else ' / aligned'),fill='#29333a',font=font)
        if row==1:
            for landmark in [42,82,122]:
                draw.line((x,y+landmark*3,x+288,y+landmark*3),fill='#aaa698',width=1)
    switch=Image.new('RGB',(600,450),'#ded8ca');sd=ImageDraw.Draw(switch)
    sd.text((12,8),'DIRECTION SWITCH / '+view['direction']+' / STATIC STUDY',fill='#29333a',font=font)
    for col,img in enumerate([before,cell]):
        preview=img.resize((288,384),Image.Resampling.NEAREST)
        switch.paste(preview,(col*300,30),preview)
        sd.text((col*300+12,420),'BEFORE' if col==0 else 'LANDMARK ALIGNED',fill='#29333a',font=font)
    switch_frames.append(switch)
board.save(OUT/'proportion-comparison.png')
switch_frames.extend(switch_frames[-2:0:-1])
switch_frames[0].save(OUT/'direction-switch-comparison.gif',save_all=True,append_images=switch_frames[1:],duration=700,loop=0)
(OUT/'manifest.json').write_text(json.dumps({'status':config['status'],'config_sha256':hashlib.sha256(CONFIG.read_bytes()).hexdigest(),'frames':records,'limitations':['vertical landmark alignment is not 3D camera reprojection','cloth and anatomy still need art review','no animation conversion in this study']},indent=2),encoding='utf-8')
print('PROPORTION_STUDY_OK:',len(normalized),'model views, bounded binary-alpha cells and aligned crown/sole')
