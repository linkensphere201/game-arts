"""Local Neris east stride guides and masked model redraw."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--lift',choices=['left','right'],required=True);args=parser.parse_args()
seed=777250 if args.lift=='left' else 777251;NAME=f'neris-front-run-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'neris-keys-777006.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
md.rectangle((188,479,326,698),fill=255);d.rectangle((188,479,326,698),fill='white')
d.polygon([(213,479),(298,479),(296,553),(216,553)],fill='#443e35')
for side,x in [('left',211),('right',273)]:
    if side==args.lift:
        d.polygon([(x,521),(x+30,521),(x+39,556),(x+30,581),(x+8,591),(x-4,567)],fill='#534b40',outline='#302b28',width=3)
        d.polygon([(x+6,577),(x+28,575),(x+33,590),(x+27,604),(x-6,604),(x-10,596),(x-4,585)],fill='#63462e',outline='#302b28',width=3)
    else:
        d.polygon([(x,526),(x+31,526),(x+31,649),(x+4,654)],fill='#39372f',outline='#302b28',width=3)
        patch=original.crop((x-14,642,x+42,688)).convert('RGBA');a=np.array(patch);white=(a[:,:,:3].min(2)>233)&(a[:,:,:3].max(2)-a[:,:,:3].min(2)<28);a[:,:,3][white]=0;patch=Image.fromarray(a);guide.paste(patch,(x-14,642),patch)
# Keep the original front fastening and ivory trim; shorten only raised-side tail.
for side,x0,x1 in [('left',190,254),('right',261,321)]:
    patch=original.crop((x0,479,x1,604)).convert('RGBA');a=np.array(patch);r,g,b=a[:,:,:3].astype(int).transpose(2,0,1)
    white=(a[:,:,:3].min(2)>233)&(a[:,:,:3].max(2)-a[:,:,:3].min(2)<28);a[:,:,3][white]=0;patch=Image.fromarray(a)
    if side==args.lift:patch=patch.resize((patch.width,79),Image.Resampling.LANCZOS)
    guide.paste(patch,(x0,479),patch)
mask=mask.filter(ImageFilter.GaussianBlur(1));ma=np.array(mask);ma[:479]=0;mask=Image.fromarray(ma)
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'front facing elf steward running, one knee raised high towards camera and foot lifted, opposite foot planted, long wine burgundy coat opens over raised knee, retain ivory vertical trim and buttons, brown trousers and shoes, clean anime cel shading','extra leg, missing foot, detached shoe, bare leg, face change, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.30,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','lift':args.lift,'review':'leg-only running phases, upper body fixed; no finished cycle'}

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
        assert outside==0;print('NERIS_FRONT_RUN_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
