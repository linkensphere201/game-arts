"""Local Neris east stride guides and masked model redraw."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--lead',choices=['near','far'],required=True);parser.add_argument('--compact',action='store_true');args=parser.parse_args()
seed=(777087 if args.lead=='near' else 777088) if args.compact else (777069 if args.lead=='near' else 777070);NAME=f'neris-east-stride-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'neris-profile-777018.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Separate legs in profile; retain actual coat painting as a split-tail guide.
md.rectangle((170,475,365,693),fill=255)
d.rectangle((170,475,365,693),fill='white')
d.polygon([(232,475),(282,475),(294,579),(226,579)],fill='#443e35')
near_forward=args.lead=='near'
for forward in (not near_forward,near_forward):
    near=forward==near_forward
    points=[(252,546),(279,548),(310,600),(335,655),(311,662),(283,616),(257,585)] if forward else [(232,546),(257,554),(244,606),(219,659),(195,654),(216,598)]
    if args.compact:
        points=[(round(x+.55*(258-((265+.44*(y-546)) if forward else (245-.32*(y-546))))),y) for x,y in points]
    d.polygon(points,fill='#534b40' if near else '#39372f',outline='#302b28',width=3)
    boot=original.crop((265,649,326,685)).resize((58,34),Image.Resampling.LANCZOS)
    boot_x=307 if forward else 188
    if args.compact:boot_x=round(258+(boot_x-258)*.45)
    boot=boot.convert('RGBA');pixels=np.array(boot);white=(pixels[:,:,:3].min(2)>233)&(pixels[:,:,:3].max(2)-pixels[:,:,:3].min(2)<28);pixels[:,:,3][white]=0;boot=Image.fromarray(pixels)
    guide.paste(boot,(boot_x,650),boot)
# Move lower tail edges apart without changing the waist or head.
for x0,x1,sign in [(213,261,-1),(261,312,1)]:
    for y in range(475,604):
        offset=round(sign*(10 if args.compact else 22)*(y-475)/129)
        strip=original.crop((x0,y,x1,y+1))
        pixels=np.array(strip.convert('RGBA'));white=(pixels[:,:,:3].min(2)>233)&(pixels[:,:,:3].max(2)-pixels[:,:,:3].min(2)<28);pixels[:,:,3][white]=0
        strip=Image.fromarray(pixels);guide.paste(strip,(x0+offset,y),strip)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,('short natural walking step, modest leg separation, ' if args.compact else '')+'right facing side profile elf steward walking long stride, two clearly separated trouser legs, one foot forward and other behind, plain brown shoes touching ground, long wine burgundy coat splits naturally around thighs, clean anime cel shading','boot laces, shoelaces, white gap at hip, front view, face change, extra leg, missing foot, detached shoe, bare leg, high heels, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.38,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending single key pose; not an animation clip','lead':args.lead,'compact':args.compact}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'neris-east-stride'})['prompt_id']
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
        assert outside==0;print('NERIS_EAST_STRIDE_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
