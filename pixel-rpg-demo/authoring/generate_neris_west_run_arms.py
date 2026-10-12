"""Local Neris east stride guides and masked model redraw."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--pose',choices=['back','middle'],required=True);args=parser.parse_args()
seed=777248 if args.pose=='back' else 777249;NAME=f'neris-west-run-arms-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'neris-west-run-cuff-777238.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
md.rectangle((175,311,323,399),fill=255);d.rectangle((175,311,323,399),fill='white')
# Smaller far sleeve in front, behind the near arm and torso.
d.polygon([(229,322),(214,326),(209,364),(191,344),(181,352),(201,380),(218,377),(239,341)],fill='#49333d',outline='#30282b',width=2)
d.polygon([(185,341),(196,344),(189,356),(178,349)],fill='#c6bea9',outline='#493b36',width=2)
d.ellipse((176,329,190,344),fill='#b39376',outline='#493630',width=2)
# Stable left fastening and jacket volume.
d.polygon([(221,318),(270,320),(275,337),(272,399),(221,399),(217,354)],fill='#67454f',outline='#30282b',width=2)
d.line([(223,325),(224,396)],fill='#36292d',width=2)
for cy in (340,365,390):d.ellipse((220,cy,224,cy+4),fill='#b6a375')
if args.pose=='back':
    d.polygon([(257,322),(274,326),(294,356),(309,368),(299,382),(280,373),(253,343)],fill='#67454f',outline='#30282b',width=2)
    d.polygon([(301,363),(282,342),(269,350),(280,370),(299,381)],fill='#75525c',outline='#30282b',width=2)
    d.polygon([(280,342),(272,333),(261,344),(268,355)],fill='#ddd3bd',outline='#493b36',width=2)
    d.ellipse((255,325,273,342),fill='#c4a183',outline='#493630',width=2)
else:
    d.polygon([(255,322),(272,326),(279,369),(272,389),(256,389),(250,361)],fill='#67454f',outline='#30282b',width=2)
    d.polygon([(269,375),(249,352),(237,359),(253,384),(268,390)],fill='#75525c',outline='#30282b',width=2)
    d.polygon([(249,354),(243,343),(231,348),(236,362)],fill='#ddd3bd',outline='#493b36',width=2)
    d.ellipse((229,333,246,350),fill='#c4a183',outline='#493630',width=2)
mask=mask.filter(ImageFilter.GaussianBlur(1));ma=np.array(mask);ma[:311]=0;ma[:325,218:276]=0;ma[399:]=0;mask=Image.fromarray(ma)
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'left facing running elf steward, bent near elbow '+('behind torso' if args.pose=='back' else 'beneath shoulder')+', opposite far arm forward, wine burgundy coat cream cuffs gold buttons, clean anime cel shading','extra arm, missing hand, white glove, face change, belt change, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.28,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','pose':args.pose,'review':'left running arms study, not accepted animation','protected':'rows before311 and from399, collar rectangle to325, including head collar belt keys and legs'}

def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'neris-east-run'})['prompt_id']
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
        assert outside==0;print('NERIS_WEST_RUN_ARMS_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
