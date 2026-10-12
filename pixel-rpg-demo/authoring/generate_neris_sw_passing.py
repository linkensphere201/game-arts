"""Local Neris southwest passing guides and masked model redraw."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--lead',choices=['near','far'],required=True);args=parser.parse_args()
seed=777153 if args.lead=='near' else 777154;NAME=f'neris-SW-passing-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'neris-SW-777032.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Preserve the diagonal camera: near shoe is lower/larger than the far shoe.
md.rectangle((175,460,320,635),fill=255)
d.rectangle((175,460,320,635),fill='white')
d.polygon([(214,460),(286,460),(284,535),(214,535)],fill='#39372f')
for near in (False,True):
    support=near==(args.lead=='near')
    dx=0 if support else (-5 if near else 5);dy=0 if support else (-28 if near else -15)
    x0,x1,top,bottom=(255,275,527,597) if near else (219,240,516,588)
    points=[(x0,top),(x1,top),(x1+dx,bottom+dy),(x0+dx,bottom+dy)] if support else [(x0,top),(x1,top),(x1-4,563),(x1+dx,bottom+dy),(x0+dx,bottom+dy),(x0-6,563)]
    d.polygon(points,fill='#43423a' if near else '#34352f',outline='#292a26',width=2)
    box=(228,588,280,618) if near else (194,579,241,606)
    shoe_mask=Image.new('L',original.size)
    outline=[(254,588),(274,588),(280,612),(267,617),(229,617),(229,607),(247,598)] if near else [(220,580),(238,580),(241,603),(195,605),(195,596),(211,589)]
    ImageDraw.Draw(shoe_mask).polygon(outline,fill=255)
    boot=original.convert('RGBA');boot.putalpha(shoe_mask);boot=boot.crop(box);pixels=np.array(boot)
    white=(pixels[:,:,:3].min(2)>233)&(pixels[:,:,:3].max(2)-pixels[:,:,:3].min(2)<28);pixels[:,:,3][white]=0
    boot=Image.fromarray(pixels);guide.paste(boot,(box[0]+dx,box[1]+dy),boot)
for x0,x1,near in [(244,296,True),(207,244,False)]:
    sign=-1 if near==(args.lead=='near') else 1
    for y in range(460,560 if near else 542):
        offset=round(sign*3*(y-460)/100)
        pixels=np.array(original.crop((x0,y,x1,y+1)).convert('RGBA'));white=(pixels[:,:,:3].min(2)>233)&(pixels[:,:,:3].max(2)-pixels[:,:,:3].min(2)<28);pixels[:,:,3][white]=0
        cloth=(pixels[:,:,0].astype(float)>pixels[:,:,1]*1.06)&(pixels[:,:,0].astype(float)>pixels[:,:,2]*.9)
        pixels[:,:,3][~cloth]=0
        strip=Image.fromarray(pixels);guide.paste(strip,(x0+offset,y),strip)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'walking passing pose, one bent knee with raised foot, southwest three quarter front view elf steward walking, two clearly separated trouser legs, one foot lifted beside grounded support foot, plain brown shoes, long wine burgundy coat splits naturally around thighs, clean anime cel shading','boot laces, shoelaces, white gap at hip, front view, face change, extra leg, missing foot, detached shoe, bare leg, high heels, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.20,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending single key pose; not an animation clip','lead':args.lead,'construction':'independent southwest outfit; preserve near/far shoe perspective; no mirrored final pixels'}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'neris-SW-passing'})['prompt_id']
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
        assert outside==0;print('NERIS_SW_PASSING_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
