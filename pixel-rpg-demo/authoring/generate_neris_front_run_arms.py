"""Local Neris east stride guides and masked model redraw."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--lift',choices=['left','right'],required=True);args=parser.parse_args()
seed=777254 if args.lift=='left' else 777255;NAME=f'neris-front-run-arms-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/('neris-front-run-777250.png' if args.lift=='left' else 'neris-front-run-777251.png');original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Clear old hanging sleeves/hands, with bounded side masks.
for box in [(157,300,222,492),(290,300,349,492)]:md.rectangle(box,fill=255);d.rectangle(box,fill='white')
guide.paste(original.crop((204,301,309,493)),(204,301))
for side in ['left','right']:
    forward=side!=args.lift
    def pts(seq):return [(512-x,y) for x,y in seq] if side=='right' else seq
    if forward:
        sleeve=[(189,300),(207,303),(217,354),(207,388),(185,389),(168,367),(178,348)]
        forearm=[(175,363),(201,330),(216,340),(199,379),(185,391)]
        cuff=[(200,331),(204,318),(222,324),(217,342)]
        hand=[(205,317),(208,305),(222,307),(229,319),(223,329),(212,329)]
    else:
        sleeve=[(187,300),(207,306),(204,357),(185,391),(167,384),(168,363),(177,333)]
        forearm=[(169,377),(183,379),(193,405),(180,416),(167,398)]
        cuff=[(179,404),(193,400),(199,413),(185,420)]
        hand=[(185,418),(199,412),(205,423),(199,436),(188,433),(183,426)]
    d.polygon(pts(sleeve),fill='#67454f',outline='#30282b',width=3)
    d.polygon(pts(forearm),fill='#67454f',outline='#30282b',width=3)
    d.polygon(pts(cuff),fill='#ddd3bd',outline='#493b36',width=2)
    d.polygon(pts(hand),fill='#c4a183',outline='#493630',width=2)
mask=mask.filter(ImageFilter.GaussianBlur(1));ma=np.array(mask)
ma[:301]=0;ma[:,229:283]=0;ma[399:,204:309]=0;ma[486:]=0
mask=Image.fromarray(ma)
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'front facing elf steward running, bent elbows swinging opposite raised leg, one fist forward near chest and other fist down beside hip, wine burgundy coat cream cuffs, clean anime cel shading','extra arm, missing hand, face change, belt change, extra keys, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.30,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','lift':args.lift,'review':'front arm endpoint study; no finished cycle'}

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
        assert outside==0;print('NERIS_FRONT_RUN_ARMS_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
