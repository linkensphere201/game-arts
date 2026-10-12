"""Local Neris northeast intermediate guides and masked model redraw."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--lead',choices=['near','far'],required=True);parser.add_argument('--phase',choices=['down','up'],required=True);args=parser.parse_args()
seed=(777199 if args.lead=='near' else 777200) if args.phase=='down' else (777201 if args.lead=='near' else 777202);NAME=f'neris-NE-intermediate-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'neris-NE-777022.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Preserve the diagonal camera: near shoe is lower/larger than the far shoe.
md.rectangle((205,475,357,700),fill=255)
d.rectangle((205,475,357,700),fill='white')
d.polygon([(231,475),(309,475),(310,590),(232,590)],fill='#39372f')
for near in (False,True):
    support=near==(args.lead=='near')
    if args.phase=='down':
        dx=5 if support else -7;dy=-3 if support else (-17 if near else -9)
    else:
        dx=-5 if support else 7;dy=3 if support else (-20 if near else -11)
    x0,x1,top,bottom=(280,307,582,661) if near else (237,260,575,640)
    points=[(x0,top),(x1,top),(x1+dx,bottom+dy),(x0+dx,bottom+dy)] if support else [(x0,top),(x1,top),(x1+5,615),(x1+dx,bottom+dy),(x0+dx,bottom+dy),(x0+3,615)]
    d.polygon(points,fill='#43423a' if near else '#34352f',outline='#292a26',width=2)
    box=(278,652,340,684) if near else (229,633,277,665)
    shoe_mask=Image.new('L',original.size)
    outline=[(281,653),(304,653),(316,660),(338,663),(336,677),(324,682),(279,681)] if near else [(236,634),(259,635),(261,641),(274,644),(276,657),(265,663),(230,661)]
    ImageDraw.Draw(shoe_mask).polygon(outline,fill=255)
    boot=original.convert('RGBA');boot.putalpha(shoe_mask);boot=boot.crop(box);pixels=np.array(boot)
    white=(pixels[:,:,:3].min(2)>233)&(pixels[:,:,:3].max(2)-pixels[:,:,:3].min(2)<28);pixels[:,:,3][white]=0
    boot=Image.fromarray(pixels);guide.paste(boot,(box[0]+dx,box[1]+dy),boot)
for x0,x1,near in [(267,332,True),(217,267,False)]:
    sign=1 if near==(args.lead=='near') else -1
    for y in range(475,600 if near else 594):
        offset=round(sign*4*(y-475)/125)
        pixels=np.array(original.crop((x0,y,x1,y+1)).convert('RGBA'));white=(pixels[:,:,:3].min(2)>233)&(pixels[:,:,:3].max(2)-pixels[:,:,:3].min(2)<28);pixels[:,:,3][white]=0
        cloth=(pixels[:,:,0].astype(float)>pixels[:,:,1]*1.06)&(pixels[:,:,0].astype(float)>pixels[:,:,2]*.9)
        pixels[:,:,3][~cloth]=0
        strip=Image.fromarray(pixels);guide.paste(strip,(x0+offset,y),strip)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,f'walking {args.phase} phase, one bent knee with raised foot, northeast three quarter back view elf steward walking, two clearly separated trouser legs, one foot lifted beside grounded support foot, plain brown shoes, closed back of long wine burgundy coat, rear central vent splits naturally around thighs, clean anime cel shading','boot laces, shoelaces, white gap at hip, front view, front buttons, front lapels, face change, extra leg, missing foot, detached shoe, bare leg, high heels, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.20,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending single key pose; not an animation clip','support_leg':args.lead,'phase':args.phase,'construction':'independent northeast outfit; preserve near/far shoe perspective; no mirrored final pixels'}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'neris-NE-intermediate'})['prompt_id']
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
        assert outside==0;print('NERIS_NE_INTERMEDIATE_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
