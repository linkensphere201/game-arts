"""Local Neris west down/up leg guides and masked model redraw."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--lead',choices=['near','far'],required=True);parser.add_argument('--phase',choices=['down','up'],required=True);args=parser.parse_args()
seed=(777113 if args.lead=='near' else 777114) if args.phase=='down' else (777117 if args.lead=='near' else 777118);NAME=f'neris-west-intermediate-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'neris-W-details-777031.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Construct from the actual west outfit and shoes, without mirroring east pixels.
md.rectangle((175,480,315,627),fill=255)
d.rectangle((175,480,315,627),fill='white')
d.polygon([(222,480),(282,480),(284,556),(221,556)],fill='#443e35')
near_forward=args.lead=='near'
for forward in (not near_forward,near_forward):
    near=forward==near_forward
    # Support heel advances under the body; swing foot clears the floor.
    if args.phase=='down':
        points=[(229,540),(251,542),(242,575),(242,606),(220,607),(222,574)] if forward else [(251,540),(273,540),(278,568),(286,598),(265,600),(258,577)]
        boot_xy=(200,597) if forward else (246,590)
    else:
        points=[(237,540),(259,540),(256,574),(265,605),(242,607),(237,579)] if forward else [(249,540),(272,542),(251,566),(228,589),(209,585),(230,559)]
        boot_xy=(225,597) if forward else (191,582)
    d.polygon(points,fill='#534b40' if near else '#39372f',outline='#302b28',width=2)
    boot=original.crop((201,596,251,620)).convert('RGBA')
    pixels=np.array(boot);white=(pixels[:,:,:3].min(2)>233)&(pixels[:,:,:3].max(2)-pixels[:,:,:3].min(2)<28);pixels[:,:,3][white]=0
    boot=Image.fromarray(pixels);guide.paste(boot,boot_xy,boot)
for x0,x1,sign in [(211,251,-1),(251,292,1)]:
    for y in range(480,557):
        offset=round(sign*3*(y-480)/77)
        pixels=np.array(original.crop((x0,y,x1,y+1)).convert('RGBA'));white=(pixels[:,:,:3].min(2)>233)&(pixels[:,:,:3].max(2)-pixels[:,:,:3].min(2)<28);pixels[:,:,3][white]=0
        strip=Image.fromarray(pixels);guide.paste(strip,(x0+offset,y),strip)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,f'walking {args.phase} phase, bent swinging knee, one raised foot, one grounded support foot, left facing side profile elf steward walking, two clearly separated trouser legs, plain brown closed shoes, continuous trouser cuffs covering ankles, wine burgundy coat ends at both knees, two charcoal gray trouser legs below horizontal coat hem, clean anime cel shading','long coat tails, brown trousers, boot laces, shoelaces, white gap at hip, front view, face change, extra leg, missing foot, detached shoe, bare leg, high heels, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.20,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending single key pose; not an animation clip','lead':args.lead,'phase':args.phase,'construction':'independent west outfit and shoe guide; no mirrored final pixels'}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'neris-west-stride'})['prompt_id']
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
        assert outside==0;print('NERIS_WEST_INTERMEDIATE_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
