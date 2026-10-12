"""Local opposing arm-swing poses on fixed Neris leg artwork."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--leg',choices=['left','right'],required=True);parser.add_argument('--half',action='store_true');args=parser.parse_args()
seed=(777045 if args.leg=='left' else 777046) if args.half else (777043 if args.leg=='left' else 777044);NAME=f'neris-arm-pose-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
leg_seed=(777040 if args.leg=='left' else 777039) if args.half else (777036 if args.leg=='left' else 777037)
source=OUT/f'neris-walk-pose-{leg_seed}.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Original sleeve/hand pixels form the guide; the local model redraws joins.
polygons={
 'left':[(193,286),(203,304),(204,342),(214,375),(205,420),(202,448),(203,480),(191,489),(178,481),(178,445),(180,414),(170,370),(176,327)],
 'right':[(315,287),(325,300),(331,345),(331,395),(331,443),(334,472),(320,486),(305,476),(304,443),(299,416),(306,381),(301,346),(305,306)]}
for side,polygon in polygons.items():
    forward=side!=args.leg;factor=(1.04 if forward else .925) if args.half else (1.08 if forward else .85)
    arm_mask=Image.new('L',original.size);ImageDraw.Draw(arm_mask).polygon(polygon,fill=255)
    arm_mask=arm_mask.filter(ImageFilter.MaxFilter(9))
    arm=original.convert('RGBA');arm.putalpha(arm_mask)
    box=arm.getbbox();piece=arm.crop(box)
    piece=piece.resize((piece.width,round(piece.height*factor)),Image.Resampling.LANCZOS)
    moved=[(x,round(box[1]+(y-box[1])*factor)) for x,y in polygon]
    md.polygon(polygon,fill=255);md.polygon(moved,fill=255)
    erase=Image.new('L',original.size);ImageDraw.Draw(erase).polygon(polygon,fill=255);erase=erase.filter(ImageFilter.MaxFilter(9))
    guide.paste('white',(0,0,original.width,original.height),erase)
    # Continue coat behind shortened arm before compositing the moved sleeve.
    if side=='left':d.polygon([(193,285),(215,300),(215,486),(196,489)],fill='#744650')
    else:d.polygon([(299,287),(321,302),(321,488),(301,483)],fill='#744650')
    guide.paste(piece,(box[0],box[1]),piece)
mask=mask.filter(ImageFilter.MaxFilter(9))
# Preserve hanging keys and center tailoring rather than letting arm repair erase them.
ImageDraw.Draw(mask).rectangle((277,415,301,478),fill=0)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'front view walking elf steward, opposite arms swing naturally while walking, burgundy long coat sleeves, short cream wrist cuffs and relaxed bare hands, one arm forward other arm back, clean anime cel shading','extra arm, extra hand, white gloves, missing cuff, armor, weapon, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.28,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'opposing arm pose study, not completed walk','lifted_leg':args.leg,'half':args.half}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'neris-arm-pose'})['prompt_id']
rec.update(prompt_id=key,state='queued');save();print('QUEUED',key,flush=True)
start=time.monotonic()
while time.monotonic()-start<900:
    history=gen.request('/history/'+key)
    if key in history:
        h=history[key];rec.update(state=h['status']['status_str'],history=h);save()
        if rec['state']!='success':raise RuntimeError(record_path)
        f=h['outputs']['8']['images'][0];target=OUT/(NAME+'.png')
        shutil.copy2(BASE/'output'/f['subfolder']/f['filename'],target)
        diff=np.abs(np.asarray(Image.open(target).convert('RGB'),dtype=int)-np.asarray(original,dtype=int))
        outside=int(diff[np.asarray(mask)==0].max())
        rec.update(outside_mask_max_difference=outside,output_sha256=hashlib.sha256(target.read_bytes()).hexdigest());save()
        assert outside==0;print('NERIS_ARM_POSE_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
