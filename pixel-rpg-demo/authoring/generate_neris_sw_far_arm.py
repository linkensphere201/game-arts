"""Local opposing arm-swing poses on fixed Neris leg artwork."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--lead',choices=['near','far'],required=True);parser.add_argument('--half',action='store_true');args=parser.parse_args()
seed=(777165 if args.lead=='near' else 777166) if args.half else (777163 if args.lead=='near' else 777164);NAME=f'neris-SW-twoarm-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/(f"neris-SW-arm-{777161 if args.lead=='near' else 777162}.png" if args.half else f"neris-SW-arm-{777159 if args.lead=='near' else 777160}.png");original=Image.open(source).convert('RGB')
# Visible arm moves opposite the visible near leg. Guide uses original artwork.
arm_mask=Image.new('L',original.size)
ImageDraw.Draw(arm_mask).polygon([(207,316),(220,319),(221,349),(218,379),(218,407),(215,431),(216,450),(203,455),(198,446),(203,420),(204,394),(197,369),(198,341)],fill=255)
arm_mask=arm_mask.filter(ImageFilter.MaxFilter(5))
arm=original.convert('RGBA');arm.putalpha(arm_mask)
pixels=np.array(arm);white=(pixels[:,:,:3].min(2)>233)&(pixels[:,:,:3].max(2)-pixels[:,:,:3].min(2)<28);white[:411]|=(pixels[:411,:,:3].min(2)>190)&(pixels[:411,:,:3].max(2)-pixels[:411,:,:3].min(2)<28)
pixels[:,:,3][white]=0;arm=Image.fromarray(pixels)
angle=(-4 if args.lead=='near' else 4) if args.half else (-8 if args.lead=='near' else 8)
moved=arm.rotate(angle,resample=Image.Resampling.BICUBIC,center=(213,328))
guide=original.copy();guide.paste('white',(0,0,512,768),arm_mask.filter(ImageFilter.MaxFilter(9)))
ImageDraw.Draw(guide).rectangle((190,325,216,462),fill='white')
ImageDraw.Draw(guide).polygon([(216,318),(234,318),(237,461),(214,461),(210,402),(211,357)],fill='#704453')
guide.paste(moved,(0,0),moved)
mask=Image.fromarray(np.maximum(np.array(arm_mask),np.array(moved.getchannel('A'))))
ImageDraw.Draw(mask).rectangle((190,325,216,462),fill=255)
mask=mask.filter(ImageFilter.MaxFilter(7))
# Head and equipment must not change when the sleeve moves.
md=ImageDraw.Draw(mask);md.rectangle((0,0,511,324),fill=0);md.rectangle((229,0,511,767),fill=0);md.rectangle((218,390,243,414),fill=0)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'southwest three quarter front view elf steward walking, far arm swings opposite near arm, same side coat, opposite arms swing naturally while walking, burgundy long coat sleeves, short cream wrist cuffs and relaxed bare hands, one arm forward other arm back, clean anime cel shading','extra arm, extra hand, white gloves, missing cuff, armor, weapon, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.22,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'opposing arm pose study, not completed walk','lead':args.lead,'arm_rotation_degrees':angle,'half':args.half}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'neris-SW-arm'})['prompt_id']
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
        assert outside==0;print('NERIS_SW_TWOARM_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
