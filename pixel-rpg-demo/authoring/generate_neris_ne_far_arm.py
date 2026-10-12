"""Local opposing arm-swing poses on fixed Neris leg artwork."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--lead',choices=['near','far'],required=True);parser.add_argument('--half',action='store_true');args=parser.parse_args()
seed=(777197 if args.lead=='near' else 777198) if args.half else (777195 if args.lead=='near' else 777196);NAME=f'neris-NE-twoarm-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/(f"neris-NE-arm-{777189 if args.lead=='near' else 777190}.png" if args.half else f"neris-NE-arm-{777187 if args.lead=='near' else 777188}.png");original=Image.open(source).convert('RGB')
# Visible arm moves opposite the visible near leg. Guide uses original artwork.
arm_mask=Image.new('L',original.size)
ImageDraw.Draw(arm_mask).polygon([(214,298),(226,301),(225,331),(226,359),(227,388),(230,418),(226,436),(230,454),(222,464),(215,456),(212,442),(213,426),(209,403),(208,373),(207,342),(209,316)],fill=255)
arm_mask=arm_mask.filter(ImageFilter.MaxFilter(5))
arm=original.convert('RGBA');arm.putalpha(arm_mask)
pixels=np.array(arm);rgb=pixels[:,:,:3].astype(int)
white=(rgb.min(2)>190)&(rgb.max(2)-rgb.min(2)<35)
cuff=Image.new('L',original.size)
ImageDraw.Draw(cuff).polygon([(212,410),(227,412),(229,433),(213,432)],fill=255)
pixels[:,:,3][white & (np.asarray(cuff)==0)]=0;arm=Image.fromarray(pixels)
angle=(4 if args.lead=='near' else -4) if args.half else (8 if args.lead=='near' else -8)
moved=arm.rotate(angle,resample=Image.Resampling.BICUBIC,center=(220,311))
guide=original.copy();guide.paste('white',(0,0,512,768),arm_mask.filter(ImageFilter.MaxFilter(9)))
ImageDraw.Draw(guide).rectangle((198,316,222,472),fill='white')
ImageDraw.Draw(guide).polygon([(223,298),(242,305),(242,477),(223,477),(218,403),(218,353)],fill='#704453')
guide.paste(moved,(0,0),moved)
mask=Image.fromarray(np.maximum(np.array(arm_mask),np.array(moved.getchannel('A'))))
ImageDraw.Draw(mask).rectangle((198,316,222,472),fill=255)
mask=mask.filter(ImageFilter.MaxFilter(7))
# Head and equipment must not change when the sleeve moves.
md=ImageDraw.Draw(mask);md.rectangle((0,0,511,312),fill=0);md.rectangle((258,0,511,767),fill=0);md.rectangle((225,386,250,417),fill=0)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'northeast three quarter back view elf steward walking, far arm swings opposite near arm, same side coat, opposite arms swing naturally while walking, burgundy long coat sleeves, short cream wrist cuffs and relaxed bare hands, one arm forward other arm back, clean anime cel shading','extra arm, extra hand, white gloves, missing cuff, armor, weapon, text')
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
save();key=gen.request('/prompt',{'prompt':g,'client_id':'neris-NE-arm'})['prompt_id']
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
        assert outside==0;print('NERIS_NE_TWOARM_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
