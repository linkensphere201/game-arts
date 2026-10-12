"""Local masked chest lid states; original lower box is pixel-exact across states."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, shutil, time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
p=argparse.ArgumentParser();p.add_argument('--state',choices=['half','open'],required=True);p.add_argument('--seed',type=int);a=p.parse_args()
seed=a.seed or (762001 if a.state=='half' else 762003);name=f'chest-{a.state}-{seed}'
record=OUT/(name+'.json')
if record.exists(): raise RuntimeError('Run exists; inspect original prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py');gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in [8188,8189]:
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Queue occupied')
source=OUT/'chest-752003.png';original=Image.open(source).convert('RGB');guide=original.copy();d=ImageDraw.Draw(guide)
d.rectangle((66,35,444,240),fill='white')
top=81 if a.state=='half' else 44
bottom=205 if a.state=='half' else 190
# Visible dark cavity with a gold upper rim; box below 242 is never regenerated.
d.polygon([(79,218),(112,189),(400,189),(433,218),(433,242),(79,242)],fill='#302922',outline='#4a3529',width=5)
d.line([(82,237),(430,237)],fill='#b79a56',width=5)
d.rounded_rectangle((82,top,430,bottom),radius=20,fill='#916c45',outline='#3a2e29',width=7)
d.rounded_rectangle((98,top+14,414,bottom-12),radius=12,fill='#60442e',outline='#bf9f59',width=6)
for x in [145,205,265,325,385]:d.line((x,top+18,x,bottom-16),fill='#4f392a',width=3)
d.line((92,bottom-3,420,bottom-3),fill='#c6ac68',width=5)
# Hinge arms connect the lifted lid to the unaltered box.
for x in [116,390]:d.line((x,bottom,x,237),fill='#b19653',width=7)
mask=Image.new('L',original.size);md=ImageDraw.Draw(mask);md.rectangle((65,30,445,237),fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(1));mask.paste(0,(0,242,512,512))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{name}-{suffix}.png');im.save(BASE/'input'/f'{name}-{suffix}.png')
g=gen.graph(seed,f'one wooden treasure chest with its lid {"partially" if a.state=="half" else "fully"} open, dark empty interior, brown wood planks and muted antique brass bands, straight front view, clean dark colored outlines, hand painted anime RPG game prop, restrained cel shading, plain white background','treasure, coins, gems, glow, extra chest, emblem, text, logo, photograph, photorealistic, perspective side view')
g['5']={'class_type':'LoadImage','inputs':{'image':name+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':name+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':name+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.38,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=name)
r={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending'}
def save():record.write_text(json.dumps(r,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'chest-lid-study'})['prompt_id'];r.update(state='queued',prompt_id=key);save();print('QUEUED',key,flush=True)
start=time.monotonic()
while time.monotonic()-start<900:
    history=gen.request('/history/'+key)
    if key in history:
        h=history[key];r.update(state=h['status']['status_str'],history=h);save()
        if r['state']!='success':raise RuntimeError(record)
        f=h['outputs']['8']['images'][0];target=OUT/(name+'.png');shutil.copy2(BASE/'output'/f['subfolder']/f['filename'],target)
        result=np.asarray(Image.open(target).convert('RGB'));outside=np.asarray(mask)==0
        r['outside_mask_max_difference']=int(np.abs(result.astype(int)-np.asarray(original).astype(int))[outside].max())
        assert r['outside_mask_max_difference']==0
        r['output_sha256']=hashlib.sha256(target.read_bytes()).hexdigest();save();print('CHEST_MASK_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(key)
