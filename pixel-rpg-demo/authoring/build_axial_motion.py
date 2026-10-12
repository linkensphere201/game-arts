"""Front/back model-pixel motion studies; projected articulation, not finished eight-way art."""
from pathlib import Path
import argparse,math,json,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--direction',choices=['S','SE','NE','N','NW','SW'])
parser.add_argument('--output-dir',type=Path)
parser.add_argument('--runtime-stride',action='store_true',help='Experimental final-pixel stride calibration; use isolated output')
parser.add_argument('--bounded-legs',action='store_true',help='Limit projected leg elongation with shared hip adjustment')
args=parser.parse_args()
OUT=(args.output_dir or ROOT/'production/pixel-rpg/model-wave-01/guided/axial-motion').resolve();OUT.mkdir(parents=True,exist_ok=True)
if args.direction in ['NW','SW'] and args.output_dir is None:
 raise ValueError('Left diagonal study requires an isolated --output-dir')
if args.runtime_stride and args.output_dir is None:raise ValueError('Calibrated study requires an isolated --output-dir')
if args.bounded_legs and not args.runtime_stride:raise ValueError('--bounded-legs requires --runtime-stride')
SIZE=(512,832) if args.runtime_stride else (512,768)
proportions=json.loads(Path(__file__).with_name('rowan-proportion-study.json').read_text())
views={v['direction']:v for v in proportions['views']}
views.update({'NW':{'source_y':[155,270,290,367,457,516,617],'horizontal_scale':.256},'SW':{'source_y':[155,266,290,356,443,499,617],'horizontal_scale':.256}})
def extrapolate(value,x,y):
 if value<x[0]:return y[0]+(value-x[0])*(y[1]-y[0])/(x[1]-x[0])
 if value>x[-1]:return y[-1]+(value-x[-1])*(y[-1]-y[-2])/(x[-1]-x[-2])
 return float(np.interp(value,x,y))

def segment(path):
 im=Image.open(path).convert('RGBA');a=np.asarray(im).astype(int);rgb=a[:,:,:3]
 bg=((rgb.min(2)>233)&(rgb.max(2)-rgb.min(2)<28))|(a[:,:,3]<128)
 labels,_=ndimage.label(bg);edge=np.unique(np.concatenate([labels[0],labels[-1],labels[:,0],labels[:,-1]]));edge=edge[edge!=0]
 parts,_=ndimage.label((~np.isin(labels,edge))&(a[:,:,3]>=128));counts=np.bincount(parts.ravel());counts[0]=0
 fg=ndimage.binary_erosion(np.isin(parts,np.flatnonzero(counts>=max(64,counts.max()*.005))),iterations=2)
 im.putalpha(Image.fromarray((fg*255).astype('uint8')))
 padded=Image.new('RGBA',SIZE);padded.alpha_composite(im);return padded

def polygon(points):
 mask=Image.new('L',SIZE);ImageDraw.Draw(mask).polygon(points,fill=255);return mask

def cut(im,points):
 p=im.copy();p.putalpha(Image.fromarray(np.minimum(np.asarray(im.getchannel('A')),np.asarray(polygon(points)))));return p

def bone(part,sa,sb,da,db):
 sa,sb,da,db=[np.array(p,float) for p in (sa,sb,da,db)]
 u=sb-sa;v=db-da;su=u/np.linalg.norm(u);dv=v/np.linalg.norm(v)
 # Preserve transverse width when shortening a projected limb; uniform scaling pinched ankles.
 sp=np.array([-su[1],su[0]]);dp=np.array([-dv[1],dv[0]])
 transform=np.outer(dp,sp)+np.outer(dv,su)*(np.linalg.norm(v)/np.linalg.norm(u))
 inv=np.linalg.inv(transform);off=sa-inv@da
 return part.transform(SIZE,Image.Transform.AFFINE,(*inv[0],off[0],*inv[1],off[1]),Image.Resampling.BICUBIC)

specs={
 'S':{'source':'production/pixel-rpg/model-sprite-study/segmented-source.png','forward':(0,1),'ground':665,'center':256,'hip':460,'knee':532,'ankle':632,'legs':[(224,198,251),(286,258,318)]},
 'SE':{'source':'production/pixel-rpg/model-wave-01/guided/rowan-SE-cape-757005.png','forward':(.707,.707),'ground':684,'center':268,'hip':461,'knee':540,'ankle':642,'legs':[(245,218,275),(301,277,332)]},
 'NE':{'source':'production/pixel-rpg/model-wave-01/guided/rowan-NE-shoulder-758002.png','forward':(.707,-.707),'ground':684,'center':277,'hip':503,'knee':554,'ankle':651,'legs':[(252,226,278),(307,280,340)]},
 'N':{'source':'production/pixel-rpg/model-wave-01/guided/rowan-N-shoulders-758001.png','forward':(0,-1),'ground':685,'center':257,'hip':510,'knee':551,'ankle':650,'legs':[(218,190,245),(287,262,310)]},
 'NW':{'source':'production/pixel-rpg/model-wave-01/guided/rowan-NW-cloth-769002.png','forward':(-.707,-.707),'ground':617,'center':237,'hip':457,'knee':516,'ankle':587,'legs':[(222,191,240),(258,240,278)]},
 'SW':{'source':'production/pixel-rpg/model-wave-01/guided/rowan-SW-770001.png','forward':(-.707,.707),'ground':617,'center':240,'hip':443,'knee':499,'ankle':583,'legs':[(217,195,240),(261,241,288)]}
}
specs={d:s for d,s in specs.items() if d==args.direction} if args.direction else {d:s for d,s in specs.items() if d not in ['NW','SW']}
all_frames={};records=[]
for direction,spec in specs.items():
 view=views[direction];ys=view['source_y'];yt=proportions['target_y'];xs=view.get('horizontal_scale',proportions['horizontal_scale'])
 forward=np.array(spec['forward'],float);forward/=np.linalg.norm(forward)
 src=ROOT/spec['source'];im=segment(src);rgb=np.asarray(im)[:,:,:3].astype(int)
 teal=(rgb[:,:,1]>rgb[:,:,0]*1.2)&(rgb[:,:,2]>rgb[:,:,0]*1.1)&(rgb[:,:,0]<140)
 body=im.copy();alpha=np.asarray(body.getchannel('A')).copy();leg_parts=[]
 for x,left,right in spec['legs']:
  hip,knee,ankle=spec['hip'],spec['knee'],spec['ankle']
  # Do not extract the tunic hem into the thigh: it otherwise becomes a moving white stripe.
  leg_start=hip+3
  pieces=[cut(im,[(left,leg_start),(right,leg_start),(right,knee+8),(left,knee+8)]),cut(im,[(left,knee-6),(right,knee-6),(right,ankle+8),(left,ankle+8)]),cut(im,[(left,ankle-8),(right,ankle-8),(right,spec['ground']+5),(left,spec['ground']+5)])]
  # Keep the actual cape as foreground occlusion, excluding its pixels from leg layers.
  for part in pieces:part.putalpha(Image.fromarray(np.where(teal,0,np.asarray(part.getchannel('A'))).astype('uint8')))
  region=alpha[leg_start:,left:right];region[~teal[leg_start:,left:right]]=0
  leg_parts.append((x,pieces))
 body.putalpha(Image.fromarray(alpha))
 arms=[]
 arm_specs={
  'S':[((211,299),(197,363),(186,425),[(201,296),(220,305),(212,348),(204,390),(201,447),(177,445),(177,388),(186,344)]),((325,300),(346,363),(355,426),[(314,302),(334,295),(347,334),(360,377),(374,446),(348,451),(335,401),(328,359)])],
  'SE':[((240,295),(233,367),(226,423),[(231,292),(251,296),(246,340),(243,375),(238,414),(236,443),(217,448),(209,433),(216,395),(222,346)]),((320,298),(328,367),(335,419),[(313,298),(326,298),(331,341),(339,389),(345,430),(331,442),(320,398),(314,346)])],
  'NE':[((318,290),(321,352),(335,428),[(310,286),(325,286),(331,330),(327,358),(341,403),(345,435),(330,447),(316,421),(307,362)])],
  'NW':[((210,327),(207,368),(198,415),[(199,323),(216,323),(222,346),(216,371),(207,402),(205,429),(193,435),(187,425),(193,400),(195,371)])],
  'SW':[((201,326),(198,364),(194,415),[(196,323),(205,326),(205,350),(201,377),(199,403),(201,425),(188,428),(184,416),(190,394),(191,368)]),((267,318),(273,367),(275,419),[(259,317),(274,316),(278,348),(281,373),(287,411),(283,433),(273,439),(266,425),(267,400),(263,374)])]
 }
 if direction in arm_specs:
  for shoulder,elbow,wrist,points in arm_specs[direction]:
   arm=cut(im,points)
   upper=arm.copy();lower=arm.copy()
   ua=np.asarray(upper.getchannel('A')).copy();la=ua.copy()
   ua[int(elbow[1])+7:]=0;la[:int(elbow[1])-7]=0
   upper.putalpha(Image.fromarray(ua));lower.putalpha(Image.fromarray(la))
   arms.append((upper,lower,shoulder,elbow,wrist))
   alpha=np.asarray(body.getchannel('A')).copy();remove=np.asarray(polygon(points))>0;alpha[remove&~teal]=0;body.putalpha(Image.fromarray(alpha))
 for action in ['walk','run']:
  frames=[];running=action=='run'
  for f in range(8):
   t=math.tau*f/8;bob=-abs(math.sin(2*t))*(9 if running else 3)
   body_dx=math.sin(t)* (3 if running else 1.5)
   def torso_point(point):
    x,y=point
    return np.array([x+body_dx+spec['forward'][0]*(.10 if running else .015)*(spec['hip']-y),y+bob])
   canvas=Image.new('RGBA',SIZE);joints=[];targets=[]
   for i,(x,pieces) in enumerate(leg_parts):
    phase=(t+i*math.pi)%math.tau;swing=phase>math.pi
    stride=32 if running else 18
    depth=stride*(1-2*phase/math.pi) if not swing else stride*math.cos(phase)
    lift=max(0,-math.sin(phase))*(35 if running else 16)
    flight=max(0,math.sin(2*t))*12 if running else 0
    # Front and rear project forward travel in opposite vertical screen directions.
    dx=spec['forward'][0]*depth;dy=spec['forward'][1]*depth-lift-flight
    source_sole=float(pieces[2].getbbox()[3])
    if args.runtime_stride:
     speed=115 if running else 65;dt=1/(20 if running else 16)
     half_stride=speed*dt*2
     depth=half_stride*(1-2*phase/math.pi) if not swing else half_stride*math.cos(phase)
     lift=max(0,-math.sin(phase))*(8 if running else 4)
     flight=max(0,math.sin(2*t))*3 if running else 0
     dx=forward[0]*depth/xs
     target_sole=extrapolate(source_sole,ys,yt)+forward[1]*depth-lift-flight
     dy=extrapolate(target_sole,yt,ys)-source_sole
    targets.append((i,x,pieces,phase,swing,depth,lift,flight,dx,dy,source_sole))
   hip_drop=0.
   if args.bounded_legs:
    length=spec['ankle']-spec['hip']
    for i,x,pieces,phase,swing,depth,lift,flight,dx,dy,source_sole in targets:
     # Shared pelvis shift preserves the planted sole instead of stretching its boot.
     horizontal=dx-body_dx
     reach=math.sqrt(max(1,(length*1.015)**2-horizontal**2))
     hip_drop=max(hip_drop,spec['ankle']+dy-reach-(spec['hip']+bob))
    bob+=hip_drop
   for i,x,pieces,phase,swing,depth,lift,flight,dx,dy,source_sole in targets:
    h=np.array([x+body_dx,spec['hip']+bob])
    k=np.array([x+body_dx+dx*.45+(1 if i else -1)*max(0,-math.sin(phase))*(8 if running else 3),spec['knee']+bob+dy*.30])
    a=np.array([x+dx,spec['ankle']+dy])
    if args.bounded_legs:
     fraction=(spec['knee']-spec['hip'])/(spec['ankle']-spec['hip'])
     delta=a-h;normal=np.array([-delta[1],delta[0]])/max(np.linalg.norm(delta),1)
     bend=max(0,-math.sin(phase))*(5 if running else 2)*(1 if i else -1)
     k=h+delta*fraction+normal*bend
    leg=bone(pieces[0],(x,spec['hip']),(x,spec['knee']),h,k)
    leg.alpha_composite(bone(pieces[1],(x,spec['knee']),(x,spec['ankle']),k,a))
    # Rigid foot patch; the projected leg shortens in recovery instead of shrinking the boot toe.
    leg.alpha_composite(bone(pieces[2],(x,spec['ankle']),(x+10,spec['ankle']),a,a+(10,0)))
    canvas.alpha_composite(leg)
    joints.append({'leg':i,'swing':swing,'depth':depth,'lift':lift,'flight':flight,'hip':h.tolist(),'knee':k.tolist(),'ankle':a.tolist(),'segment_ratios':[float(np.linalg.norm(k-h)/(spec['knee']-spec['hip'])),float(np.linalg.norm(a-k)/(spec['ankle']-spec['knee']))],'source_sole':source_sole,'sole':[x+dx,source_sole+dy]})
   canvas.alpha_composite(bone(body,(spec['center'],spec['hip']),(spec['center'],200),torso_point((spec['center'],spec['hip'])),torso_point((spec['center'],200))))
   arm_joints=[]
   for i,(upper,lower,shoulder,elbow,wrist) in enumerate(arms):
    phase=t+i*math.pi
    sh=torso_point(shoulder)
    # Upper and lower model-pixel pieces articulate independently at a shared elbow.
    # Screen projection preserves width; this is not a reconstructed 3D arm.
    sweep=math.cos(phase)*(24 if running else 10)
    side=spec['forward'][0]
    el=torso_point(elbow)+np.array([side*sweep,-abs(sweep)*.12])
    fore=np.array(wrist,float)-elbow
    bend=math.radians((48 if running else 15)+(12 if running else 8)*math.cos(phase))
    lateral=side if side else (1 if i else -1)*.28
    hand=el+np.array([fore[0]*math.cos(bend)+lateral*np.linalg.norm(fore)*math.sin(bend),fore[1]*math.cos(bend)])
    canvas.alpha_composite(bone(upper,shoulder,elbow,sh,el))
    canvas.alpha_composite(bone(lower,elbow,wrist,el,hand))
    arm_joints.append({'arm':i,'shoulder':sh.tolist(),'elbow':el.tolist(),'wrist':hand.tolist(),'bend_degrees':math.degrees(bend)})
   canvas.save(OUT/f'{direction}-{action}-{f}-source.png')
   # Fixed ground anchor with room for foreshortened forward steps below the anchor.
   preview_scale=.15 if args.runtime_stride else .17
   small=canvas.resize((round(SIZE[0]*preview_scale),round(SIZE[1]*preview_scale)),Image.Resampling.LANCZOS)
   cell=Image.new('RGBA',(96,128));cell.alpha_composite(small,(round(48-spec['center']*preview_scale),round(112-spec['ground']*preview_scale)))
   cell.putalpha(cell.getchannel('A').point(lambda v:255 if v>=150 else 0));frames.append(cell)
   records.append({'direction':direction,'action':action,'frame':f,'legs':joints,'arms':arm_joints,'hip_drop':hip_drop})
  all_frames[(direction,action)]=frames

pool=Image.new('RGB',(96*8*len(all_frames),128))
for i,frame in enumerate([f for seq in all_frames.values() for f in seq]):pool.paste(frame.convert('RGB'),(i*96,0))
palette=pool.quantize(colors=96,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
board=Image.new('RGB',(1152,len(all_frames)*218+40),'#ded8ca');draw=ImageDraw.Draw(board);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
draw.text((10,8),'MODEL PIXELS / '+' + '.join(specs)+' PROJECTED MOTION STUDIES / NOT FINAL ANIMATION',fill='#29333a',font=font)
sheet_hashes={}
for row,((direction,action),frames) in enumerate(all_frames.items()):
 sheet=Image.new('RGBA',(768,128));gif=[]
 for i,cell in enumerate(frames):
  alpha=cell.getchannel('A');cell=cell.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');cell.putalpha(alpha)
  sheet.alpha_composite(cell,(i*96,0));preview=cell.resize((144,192),Image.Resampling.NEAREST)
  board.paste(preview,(i*144,40+row*218),preview)
  bg=Image.new('RGBA',(384,512),'#ded8ca');gd=ImageDraw.Draw(bg);gd.ellipse((144,440,240,456),fill='#9b9d8f');bg.alpha_composite(cell.resize((384,512),Image.Resampling.NEAREST));gif.append(bg.convert('RGB'))
 name=f'rowan-{direction}-{action}';sheet.save(OUT/(name+'.png'))
 gif[0].save(OUT/(name+'.gif'),save_all=True,append_images=gif[1:],duration=(round(1000/(16 if action=='walk' else 20)) if args.runtime_stride else 100 if action=='walk' else 75),loop=0)
 sheet_hashes[name]=hashlib.sha256((OUT/(name+'.png')).read_bytes()).hexdigest()
 draw.text((8,40+row*218+191),direction+' / '+action,fill='#29333a',font=font)
board.save(OUT/'motion-contact.png')
(OUT/'manifest.json').write_text(json.dumps({'status':'projected axial/diagonal study; joint/arm/camera art review still required','method':'local model pixels with projected limb articulation; N arms remain occluded under cape','cell':[96,128],'anchor':[48,112],'runtime_stride':args.runtime_stride,'bounded_legs':args.bounded_legs,'calibrated_fps':{'walk':16,'run':20} if args.runtime_stride else None,'projection':{d:{'source_y':views[d]['source_y'],'target_y':proportions['target_y'],'horizontal_scale':views[d].get('horizontal_scale',proportions['horizontal_scale']),'forward':(np.array(s['forward'])/np.linalg.norm(s['forward'])).tolist()} for d,s in specs.items()},'directions':list(specs),'frames_per_action':8,'sources':{d:{'path':s['source'],'sha256':hashlib.sha256((ROOT/s['source']).read_bytes()).hexdigest()} for d,s in specs.items()},'sheet_sha256':sheet_hashes,'poses':records,'limitations':['use unified exporter for shared E anchor','segmented arms use projected elbow bends; joint seams and depth occlusion need visual review','rear cape currently follows torso; no independent cloth simulation','only listed directions generated; remaining headings require their own reviewed sources and rigs']},indent=2),encoding='utf-8')
print('PROJECTED_MOTION_STUDY_RENDERED:',len(specs),'directions, walk8 + run8')
