"""Native-size front/side/rear static sprite review from model drawings; no synthetic animation."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'
directions=['S','SE','E','NE','N']
paths=[ROOT/'production/pixel-rpg/model-sprite-study/segmented-source.png',OUT/'rowan-SE-cape-757005.png',OUT/'rowan-side-shoulder-755004.png',OUT/'rowan-NE-shoulder-758002.png',OUT/'rowan-N-shoulders-758001.png']
crops=[]
for src in paths:
 im=Image.open(src).convert('RGBA')
 if im.getchannel('A').getextrema()==(255,255):
  rgb=np.asarray(im)[:,:,:3];white=(rgb.min(axis=2)>233)&((rgb.max(axis=2).astype(int)-rgb.min(axis=2))<28)
  labels,_=ndimage.label(white);border=np.unique(np.concatenate([labels[0],labels[-1],labels[:,0],labels[:,-1]]));border=border[border!=0]
  fg=~np.isin(labels,border);parts,_=ndimage.label(fg);sizes=np.bincount(parts.ravel());sizes[0]=0
  # An occluded far leg can be a separate image component. Do not silently discard it.
  keep=np.flatnonzero(sizes>=max(64,sizes.max()*.005))
  fg=ndimage.binary_erosion(np.isin(parts,keep),iterations=1)
  im.putalpha(Image.fromarray((fg*255).astype('uint8')))
 crops.append(im.crop(im.getbbox()))
pool=Image.new('RGB',(128*len(crops),128))
for i,im in enumerate(crops):pool.paste(im.convert('RGB').resize((128,128)),(i*128,0))
palette=pool.quantize(colors=96,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
group_width=220*len(paths)
board=Image.new('RGB',(group_width*2,530),'#ded8ca');d=ImageDraw.Draw(board);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
d.text((20,14),'MODEL-DRAWN S / SE / E / NE / N — STATIC SPRITE STUDIES, NOT APPROVED GAMEPLAY DIRECTIONS',font=font,fill='#29333a')
records=[]
for j,(w,h,zoom) in enumerate([(64,96,4),(96,128,3)]):
 for i,(src,im) in enumerate(zip(paths,crops)):
  factor=min((w-8)/im.width,(h-12)/im.height);size=(round(im.width*factor),round(im.height*factor))
  resized=im.resize(size,Image.Resampling.LANCZOS);alpha=resized.getchannel('A').point(lambda a:255 if a>=170 else 0)
  pix=resized.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');pix.putalpha(alpha)
  sprite=Image.new('RGBA',(w,h));sprite.alpha_composite(pix,((w-size[0])//2,h-6-size[1]))
  direction=directions[i];name=f'rowan-{direction}-{w}x{h}.png';sprite.save(OUT/name)
  assert sprite.getbbox()[3]==h-6 and set(np.asarray(sprite.getchannel('A')).ravel())=={0,255}
  # Narrow display spacing crops transparent margins only; actual image remains full cell.
  enlarged=sprite.resize((w*zoom,h*zoom),Image.Resampling.NEAREST)
  x=j*group_width+i*220+20+(200-enlarged.width)//2;y=72
  board.paste(enlarged,(x,y),enlarged)
  d.text((j*group_width+i*220+22,478),f'{direction} / {w}x{h}',font=font,fill='#29333a')
  records.append({'direction':direction,'source':str(src.relative_to(ROOT)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'file':name,'cell':[w,h],'anchor':[w//2,h-6],'status':'static conversion study; not animation or final pixel cleanup'})
d.text((20,506),'Equal cell / foot line / shared palette. Identity, camera and diagonal views remain open.',font=font,fill='#29333a')
board.save(OUT/'direction-sprite-study.png')
(OUT/'direction-sprite-study.json').write_text(json.dumps({'shared_colors':96,'frames':records,'limitations':['head/body silhouette differs across generated views','not yet consistent overhead camera','no walk/run frames','automated pixel conversion still requires cleanup']},indent=2),encoding='utf-8')
print('DIRECTION_SPRITE_BOUNDS_ALPHA_OK:',len(paths),'views')
