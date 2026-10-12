"""Articulated side-motion study from local model pixels; not eight-direction completion."""
from pathlib import Path
import argparse,json,math,hashlib,shutil
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont,ImageEnhance
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--source',type=Path,default=ROOT/'production/pixel-rpg/model-wave-01/guided/rowan-side-shoulder-755004.png')
parser.add_argument('--output-dir',type=Path)
args=parser.parse_args()
SRC=args.source.resolve()
OUT=(args.output_dir or SRC.parent/'motion').resolve();OUT.mkdir(parents=True,exist_ok=True)
# Preserve the first motion study for an honest before/after comparison.
previous=OUT/'motion.json'
if previous.exists() and json.loads(previous.read_text(encoding='utf-8')).get('revision',1)<4:
 old_revision=json.loads(previous.read_text(encoding='utf-8')).get('revision',1)
 archive=OUT/f'v{old_revision}';archive.mkdir(exist_ok=True)
 for old in OUT.glob('*'):
  if old.is_file() and not (archive/old.name).exists():shutil.copy2(old,archive/old.name)
SIZE=(512,768);im=Image.open(SRC).convert('RGBA');rgb=np.asarray(im)[:,:,:3].astype(int)
white=(rgb.min(2)>233)&((rgb.max(2)-rgb.min(2))<28)
labels,_=ndimage.label(white);border=np.unique(np.concatenate([labels[0],labels[-1],labels[:,0],labels[:,-1]]));border=border[border!=0]
fg=~np.isin(labels,border);parts,_=ndimage.label(fg);counts=np.bincount(parts.ravel());counts[0]=0
im.putalpha(Image.fromarray(((parts==counts.argmax())*255).astype('uint8')))
def mask(points):
 m=Image.new('L',SIZE);ImageDraw.Draw(m).polygon(points,fill=255);return m
def piece(points):
 m=mask(points);p=im.copy();p.putalpha(Image.fromarray(np.minimum(np.asarray(m),np.asarray(im.getchannel('A')))));return p
arm_mask=[(243,291),(278,286),(288,339),(313,405),(321,446),(313,453),(292,445),(278,416),(256,354),(246,327)]
upper=piece([(244,293),(277,288),(280,323),(290,352),(266,361),(252,331)])
lower=piece([(263,351),(285,343),(307,404),(309,418),(316,432),(313,445),(298,442),(287,428),(279,404)])
cape_mask=(rgb[:,:,1]>rgb[:,:,0]*1.2)&(rgb[:,:,2]>rgb[:,:,0]*1.1)&(rgb[:,:,0]<135)
cape_mask[:250]=False;cape_mask[:,260:]=False
cape=im.copy();cape.putalpha(Image.fromarray((cape_mask*255).astype('uint8')))
body=im.copy();a=np.asarray(body.getchannel('A')).copy();a[466:]=0;a[cape_mask]=0;a[np.asarray(mask(arm_mask))>0]=0;body.putalpha(Image.fromarray(a))
# Small occlusion fill only, behind the extracted near arm. Not a replacement geometric body.
fill=Image.new('RGBA',SIZE);d=ImageDraw.Draw(fill)
d.polygon([(254,300),(278,307),(291,339),(286,357),(291,383),(302,453),(242,453),(247,393)],fill='#e5e3d7')
d.polygon([(263,322),(278,326),(276,343),(279,378),(288,443),(273,451)],fill='#c4d0c6')
d.polygon([(247,350),(287,350),(289,371),(244,370)],fill='#604331')
fill.alpha_composite(body);body=fill
# Restore the narrow skirt panel hidden by the source hand, retaining the original hem elsewhere.
d=ImageDraw.Draw(body)
d.polygon([(283,401),(297,420),(306,454),(291,460),(278,460)],fill='#dcded6')
d.line([(297,420),(306,454),(291,460),(278,460)],fill='#5d6058',width=3)
d.line([(284,410),(289,451)],fill='#a7b2aa',width=3)
legs=[]
for name,hip,knee,ankle,polys in [
 ('far',(267,453),(267,536),(266,649),[[(248,449),(279,449),(282,546),(250,546)],[(250,534),(280,534),(282,655),(250,655)],[(249,640),(280,640),(287,680),(279,688),(246,688)]]),
 ('near',(286,453),(291,536),(290,649),[[(276,449),(304,449),(307,546),(276,546)],[(275,534),(307,534),(306,655),(272,655)],[(273,640),(301,640),(337,666),(339,688),(272,688)]])]:
 legs.append((name,np.array(hip,float),np.array(knee,float),np.array(ankle,float),[piece(poly) for poly in polys]))
# Rotate/scale each source limb segment between source and target joints.
def bone(part,src_a,src_b,dst_a,dst_b):
 sa,sb,da,db=map(lambda p:np.array(p,float),(src_a,src_b,dst_a,dst_b));u=sb-sa;v=db-da
 a=np.dot(u,v)/np.dot(u,u);b=(u[0]*v[1]-u[1]*v[0])/np.dot(u,u)
 mat=np.array([[a,-b],[b,a]]);inv=np.linalg.inv(mat);off=sa-inv@da
 return part.transform(SIZE,Image.Transform.AFFINE,(inv[0,0],inv[0,1],off[0],inv[1,0],inv[1,1],off[1]),Image.Resampling.BICUBIC)
def ik(hip,foot,l1,l2):
 delta=foot-hip;dist=np.linalg.norm(delta);stretch=max(1,dist/(l1+l2-.5));l1*=stretch;l2*=stretch
 direction=delta/max(dist,1);along=(l1*l1-l2*l2+dist*dist)/(2*dist);height=math.sqrt(max(0,l1*l1-along*along))
 # Knees bend toward the facing direction (+x).
 return hip+direction*along+np.array([direction[1],-direction[0]])*height,stretch
frames={};poses=[]
runtime_scale=json.loads(Path(__file__).with_name('rowan-proportion-study.json').read_text())['horizontal_scale']
runtime_speeds={'walk':65.0,'run':115.0}
frame_seconds={'walk':.1,'run':.075}
for action in ['walk','run']:
 seq=[]
 for f in range(8):
  t=2*math.pi*f/8;running=action=='run';bob=(-9*abs(math.sin(2*t)) if running else -4*math.sin(2*t)**2)
  lean=.12 if running else .025
  pivot=np.array([280.,453.]);destpivot=pivot+np.array([0,(16 if running else 12)+bob]);rot=np.array([[math.cos(lean),-math.sin(lean)],[math.sin(lean),math.cos(lean)]])
  def torso(p):return destpivot+rot@(np.array(p)-pivot)
  canvas=Image.new('RGBA',SIZE)
  shoulder=torso((274,292));arm_layers=[]
  for idx in range(2):
   phase=t+idx*math.pi;angle=math.cos(phase)*(.8 if running else .45)
   elbow=shoulder+np.array([math.sin(angle)*61,math.cos(angle)*61]);fore=angle+(1.15 if running else .12)
   wrist=elbow+np.array([math.sin(fore)*74,math.cos(fore)*74])
   arm=bone(upper,(274,292),(282,351),shoulder,elbow);arm.alpha_composite(bone(lower,(282,351),(301,419),elbow,wrist));arm_layers.append(arm)
  canvas.alpha_composite(ImageEnhance.Brightness(arm_layers[1]).enhance(.88))
  cape_end=torso((210,570))+np.array([-12*math.sin(t-.6)*(2 if running else 1),3*math.sin(t)])
  canvas.alpha_composite(bone(cape,(248,270),(210,570),torso((248,270)),cape_end))
  joint_record=[]
  for idx,(name,hip,knee,ankle,parts) in enumerate(legs):
   phase=(t+idx*math.pi)%(2*math.pi)
   # Four stance intervals must cancel the controller's travel in exported pixels.
   stride=runtime_speeds[action]*frame_seconds[action]*4/(2*runtime_scale)
   # Stance travels front -> back at constant speed; recovery travels back -> front in air.
   swing=phase>math.pi;lift=max(0,-math.sin(phase))*(82 if running else 28)
   foot_x=280+(stride*(1-2*phase/math.pi) if not swing else stride*math.cos(phase))
   pitch=(-.32*max(0,-math.sin(phase)) if not running else .65*math.sin(2*phase)) if swing else 0
   flight=max(0,math.sin(2*t))*16 if running else 0
   targethip=torso(hip)
   foot_direction=np.array([math.cos(pitch),math.sin(pitch)])*10
   rotated_foot=bone(parts[2],ankle,ankle+(10,0),ankle,ankle+foot_direction)
   bottom=rotated_foot.getbbox()[3]-ankle[1]
   targetfoot=np.array([foot_x,690-bottom-lift-flight])
   targetknee,stretch=ik(targethip,targetfoot,np.linalg.norm(knee-hip),np.linalg.norm(ankle-knee))
   layer=bone(parts[0],hip,knee,targethip,targetknee);layer.alpha_composite(bone(parts[1],knee,ankle,targetknee,targetfoot))
   layer.alpha_composite(bone(parts[2],ankle,ankle+(10,0),targetfoot,targetfoot+foot_direction))
   if idx==0:layer=ImageEnhance.Brightness(layer).enhance(.86)
   canvas.alpha_composite(layer)
   joint_record.append({'leg':name,'hip':targethip.tolist(),'knee':targetknee.tolist(),'ankle':targetfoot.tolist(),'stretch':stretch,'lift':lift+flight,'swing':swing,'foot_pitch':pitch})
  canvas.alpha_composite(bone(body,(280,453),(280,250),destpivot,torso((280,250))))
  canvas.alpha_composite(arm_layers[0])
  canvas.save(OUT/f'{action}-{f}-source.png');seq.append(canvas);poses.append({'action':action,'frame':f,'legs':joint_record})
 frames[action]=seq
pool=Image.new('RGB',(128*16,128))
for i,frame in enumerate(frames['walk']+frames['run']):pool.paste(frame.convert('RGB').resize((128,128)),(i*128,0))
palette=pool.quantize(colors=96,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
board=Image.new('RGB',(8*144,2*214+48),'#ded8ca');bd=ImageDraw.Draw(board)
bd.text((10,8),'MODEL PIXELS / ARTICULATED SIDE MOTION STUDY / WALK ABOVE, RUN BELOW',font=font,fill='#29333a')
for row,(action,seq) in enumerate(frames.items()):
 sheet=Image.new('RGBA',(96*8,128));gif=[]
 for f,frame in enumerate(seq):
  small=frame.resize((round(512*.18),round(768*.18)),Image.Resampling.LANCZOS)
  alpha=small.getchannel('A').point(lambda a:255 if a>=150 else 0)
  # Physically connected silhouette: remove detached source-arm / antialias fragments.
  labels,_=ndimage.label(np.asarray(alpha)>0,structure=np.ones((3,3)))
  counts=np.bincount(labels.ravel());counts[0]=0
  alpha=Image.fromarray(((labels==counts.argmax())*255).astype('uint8'))
  pix=small.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');pix.putalpha(alpha)
  cell=Image.new('RGBA',(96,128));cell.alpha_composite(pix,(-2,-2));sheet.alpha_composite(cell,(96*f,0))
  preview=cell.resize((144,192),Image.Resampling.NEAREST);board.paste(preview,(f*144,40+row*214),preview)
  bg=Image.new('RGBA',(384,512),'#ded8ca');gd=ImageDraw.Draw(bg);gd.ellipse((148,480,236,492),fill='#999b8d')
  enlarged=cell.resize((384,512),Image.Resampling.NEAREST);bg.alpha_composite(enlarged);gif.append(bg.convert('RGB'))
  assert cell.getbbox() and 0<cell.getbbox()[0] and cell.getbbox()[2]<96
 sheet.save(OUT/f'rowan-E-{action}.png')
 gif[0].save(OUT/f'rowan-E-{action}.gif',save_all=True,append_images=gif[1:],duration=100 if action=='walk' else 75,loop=0)
board.save(OUT/'motion-contact.png')
(OUT/'motion.json').write_text(json.dumps({'source':str(SRC.relative_to(ROOT)),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'revision':4,'method':'model-pixel cutout layers, small hand-painted occlusion fill, articulated limbs and two-link legs; no old procedural character sprites','cell':[96,128],'anchor':[48,122],'directions':['E'],'frames_per_action':8,'seconds_per_frame':{'walk':.1,'run':.075},'suggested_travel_pixels_per_second':{a:v*.18/runtime_scale for a,v in runtime_speeds.items()},'runtime_calibration':{'horizontal_scale':runtime_scale,'speed':runtime_speeds,'stance_intervals':4,'note':'runtime controller speeds; 0.18-scale legacy preview has different travel speed'},'sheet_sha256':{a:hashlib.sha256((OUT/f'rowan-E-{a}.png').read_bytes()).hexdigest() for a in frames},'poses':poses,'status':'motion study; visual review required; not full character delivery'},indent=2),encoding='utf-8')
print('SIDE_MOTION_STUDY_RENDERED: E only, walk8/run8')
