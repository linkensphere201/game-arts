"""Local masked raised-knee key-pose study; preserve all unmasked reference pixels."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,math,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter,ImageOps
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=771001);p.add_argument('--denoise',type=float,default=.42);p.add_argument('--reference-boot',action='store_true');p.add_argument('--screen-leg',choices=['left','right'],default='right');p.add_argument('--lift',type=float,default=1.0);p.add_argument('--swing-arm',action='store_true');p.add_argument('--contact',action='store_true');p.add_argument('--contact-arm',action='store_true');args=p.parse_args()
if args.contact_arm:args.swing_arm=True
assert not(args.contact and args.swing_arm)
assert 0<args.lift<=1 and (args.lift==1 or args.reference_boot or args.swing_arm)
NAME=f'rowan-front-knee-{args.seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py');gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
 gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
 if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied generation queue')
source=ROOT/'production/pixel-rpg/model-sprite-study/segmented-source.png'
if args.swing_arm:
 leg_seed=(771003 if args.screen_leg=='right' else 771004) if args.lift==1 else (771005 if args.screen_leg=='right' else 771006)
 if args.contact_arm:leg_seed=771013 if args.screen_leg=='right' else 771014
 assert args.lift in (.5,1), 'Authored half/full leg sources only'
 source=OUT/f'rowan-front-knee-{leg_seed}.png'
original=Image.open(source).convert('RGBA');white=Image.new('RGBA',original.size,'white');white.alpha_composite(original);original=white.convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Screen-right leg only. Leave the supporting leg, face, costume and arms intact.
region=[(260,458),(321,458),(328,511),(327,573),(312,647),(309,675),(255,677),(254,616),(261,547)]
d.polygon(region,fill='white');md.polygon(region,fill=255)
# Foreshortened thigh and a bent lower leg; the model authors the final anatomy.
d.polygon([(274,457),(309,457),(320,485),(316,504),(288,509),(272,489)],fill='#e6ba9b',outline='#795246',width=2)
d.polygon([(276,456),(309,456),(310,471),(278,479)],fill='#302724',outline='#261f1d',width=2)
d.ellipse((287,483,317,506),fill='#edc4a2')
d.polygon([(286,506),(316,501),(307,534),(300,558),(306,576),(294,588),(274,582),(279,555),(280,532)],fill='#624235',outline='#322721',width=3)
d.polygon([(286,507),(315,502),(307,523),(296,516),(280,525)],fill='#3e2d28')
d.line([(290,527),(287,553),(283,575)],fill='#906348',width=4)
d.line([(276,581),(294,588),(306,576)],fill='#322821',width=3)
if args.reference_boot:
 # Keep the source boot's folded cuff and rounded toe in the projected guide.
 # This is only a guide; local inference redraws the masked knee/boot afterward.
 d.polygon(region,fill='white')
 def knee_point(x,y):return (x,round(457+(y-457)*(1+.30*(1-args.lift))))
 d.polygon([knee_point(x,y) for x,y in [(274,457),(309,457),(318,485),(314,506),(286,511),(272,489)]],fill='#e6ba9b',outline='#795246',width=2)
 d.polygon([(276,456),(309,456),(310,471),(278,479)],fill='#302724',outline='#261f1d',width=2)
 boot=original.crop((260,518,323,665)).convert('RGBA')
 rgb=np.asarray(boot)[:,:,:3].astype(int)
 white=(rgb.min(2)>230)&(rgb.max(2)-rgb.min(2)<30)
 boot.putalpha(Image.fromarray((~white*255).astype('uint8')))
 boot=boot.resize((round(63-13*args.lift),round(147-42*args.lift)),Image.Resampling.LANCZOS).rotate(-6*args.lift,Image.Resampling.BICUBIC,expand=True)
 guide.paste(boot,(round(260+9*args.lift),round(518-19*args.lift)),boot)
if args.screen_leg=='left':
 # Reflect only the editable pose scaffold; the original character is never mirrored.
 mask=ImageOps.mirror(mask)
 guide=Image.composite(ImageOps.mirror(guide),original,mask)
if args.swing_arm:
 guide=original.copy();mask=Image.new('L',original.size)
 # Art-directed foreground arm patch. The model resolves the elbow/hand contour.
 flip=args.screen_leg=='left'
 def pts(values):return [(542-x if flip else x,y) for x,y in values]
 def swingpts(values):
  angle=math.radians(45*(1-args.lift));c,s=math.cos(angle),math.sin(angle)
  return pts([(round(197+(x-197)*c-(y-365)*s),round(365+(x-197)*s+(y-365)*c)) for x,y in values])
 d=ImageDraw.Draw(guide);md=ImageDraw.Draw(mask)
 old_arm=pts([(184,355),(209,359),(205,393),(202,442),(192,452),(175,441),(177,395)])
 d.polygon(old_arm,fill='#276d65');md.polygon(old_arm,fill=255)
 d.polygon(pts([(178,392),(188,372),(191,408),(184,439),(176,439)]),fill='#205b57')
 d.line(pts([(200,379),(197,405),(195,438)]),fill='#3b8276',width=3)
 upper=pts([(188,348),(207,349),(208,370),(198,382),(184,374)])
 d.polygon(upper,fill='#e5bc9d',outline='#725047',width=2);md.polygon(upper,fill=255)
 forearm=swingpts([(193,373),(204,361),(230,378),(234,390),(224,398),(209,388)])
 d.polygon(forearm,fill='#694330',outline='#382821',width=2);md.polygon(forearm,fill=255)
 d.line(swingpts([(200,369),(223,386)]),fill='#a16b45',width=4)
 hand=swingpts([(226,383),(236,388),(240,400),(233,406),(223,397)])
 d.polygon(hand,fill='#e6b99a',outline='#775246',width=2);md.polygon(hand,fill=255)
 # Expand the blend boundary slightly while retaining an explicit local mask.
 mask=mask.filter(ImageFilter.MaxFilter(5))
if args.contact:
 guide=original.copy();mask=Image.new('L',original.size);d=ImageDraw.Draw(guide);md=ImageDraw.Draw(mask)
 # Separate original leg references preserve asymmetric boots; model redraws depth.
 for side,left,right in [('left',190,256),('right',255,328)]:
  front=side==args.screen_leg
  leg=original.crop((left,458,right,670)).convert('RGBA');rgb=np.asarray(leg)[:,:,:3].astype(int)
  white=(rgb.min(2)>230)&(rgb.max(2)-rgb.min(2)<30)
  teal=(rgb[:,:,1]>rgb[:,:,0]*1.2)&(rgb[:,:,2]>rgb[:,:,0]*1.1)&(rgb[:,:,0]<140)
  leg.putalpha(Image.fromarray((~(white|teal)*255).astype('uint8')))
  d.rectangle((left,458,right-1,710),fill='white');md.rectangle((left,458,right-1,710),fill=255)
  leg=leg.resize((right-left,235 if front else 184),Image.Resampling.LANCZOS)
  guide.paste(leg,(left,458),leg)
 # Preserve existing cape silhouette behind/between the legs.
 rgb=np.asarray(original).astype(int)
 teal=(rgb[:,:,1]>rgb[:,:,0]*1.2)&(rgb[:,:,2]>rgb[:,:,0]*1.1)&(rgb[:,:,0]<140)
 ma=np.asarray(mask).copy();ma[teal]=0;mask=Image.fromarray(ma)
 guide=Image.composite(guide,original,mask)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
 im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(args.seed,'front view chibi adventurer running passing pose, one knee raised toward viewer, bent leg, foreshortened bare thigh below dark shorts, brown knee high leather boot with folded angular top cuff, boot lifted above ground, natural knee and ankle anatomy, original white short tunic and teal cape, clean dark anime contour, cel shading, white background','standing straight legs, extra leg, extra foot, elongated leg, white stocking, high heel, metal armor, photo, text, detached boot')
if args.swing_arm:
 g=gen.graph(args.seed,'front view anime adventurer jogging, near forearm bent naturally forward at elbow, brown leather bracer, small relaxed hand, arm in front of teal cape and white tunic, original costume, clean dark colored outlines, restrained cel shading','extra arm, extra hand, clenched weapon, sword, staff, glove, sleeve, metal armor, text, photo, malformed fingers')
if args.contact:
 g=gen.graph(args.seed,'front view chibi adventurer walking contact pose, one leg steps toward viewer and bears weight, opposite leg behind in perspective, natural knees, dark shorts below short white tunic, brown knee high leather boots with angular folded cuffs and rounded toes, clean anime colored contour, restrained cel shading, plain white background','extra legs, extra feet, high heels, white socks, armor, crossed legs, giant boots, text, photo')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=args.denoise,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'arguments':vars(args),'graph':g,'state':'prepared','review':'pending'}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'rowan-keypose'})['prompt_id'];rec.update(prompt_id=key,state='queued');save();print('QUEUED',key,flush=True)
start=time.monotonic()
while time.monotonic()-start<900:
 history=gen.request('/history/'+key)
 if key in history:
  h=history[key];rec.update(state=h['status']['status_str'],history=h);save()
  if rec['state']!='success':raise RuntimeError(record_path)
  f=h['outputs']['8']['images'][0];target=OUT/(NAME+'.png');shutil.copy2(BASE/'output'/f['subfolder']/f['filename'],target)
  diff=np.abs(np.asarray(Image.open(target).convert('RGB'),dtype=int)-np.asarray(original,dtype=int));outside=int(diff[np.asarray(mask)==0].max())
  rec.update(outside_mask_max_difference=outside,output_sha256=hashlib.sha256(target.read_bytes()).hexdigest());save();assert outside==0
  print('LOCAL_KEYPOSE_OK: unmasked pixels preserved',flush=True);break
 time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
