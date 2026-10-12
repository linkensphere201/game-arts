"""Local Neris east stride guides and masked model redraw."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
seed=777236;NAME=f'neris-west-run-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'neris-W-details-777031.png';reference=Image.open(source).convert('RGB')
original=Image.new('RGB',reference.size,'white')
for y in range(reference.height):
    dx=round(.10*max(0,430-y))
    original.paste(reference.crop((dx,y,reference.width,y+1)),(0,y))
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
md.rectangle((168,316,345,630),fill=255);d.rectangle((168,316,345,630),fill='white')
# Independent left-facing source; far leg reaches forward, near leg recovers behind.
d.polygon([(241,482),(259,488),(218,542),(239,589),(222,599),(196,548),(199,533)],fill='#39372f',outline='#302b28',width=3)
d.polygon([(220,588),(239,588),(241,614),(198,617),(197,609),(217,600)],fill='#49382a',outline='#302b28',width=3)
d.polygon([(254,483),(277,486),(299,546),(313,524),(330,531),(307,564),(286,565),(254,519)],fill='#534b40',outline='#302b28',width=3)
d.polygon([(311,522),(322,510),(330,507),(338,520),(330,535),(314,537)],fill='#63462e',outline='#302b28',width=3)
# Far sleeve recedes behind torso.
d.polygon([(261,320),(279,324),(299,367),(278,373),(259,343)],fill='#49333d',outline='#30282b',width=3)
d.polygon([(277,356),(283,341),(296,347),(295,365)],fill='#c6bea9')
d.ellipse((277,331,294,347),fill='#b39376',outline='#493630',width=2)
# Matching closed wine jacket, left front buttons, plain belt; no right-side keys.
d.polygon([(222,311),(268,313),(275,328),(272,399),(281,442),(301,519),(280,537),(252,493),(238,540),(210,530),(225,436),(217,391)],fill='#67454f',outline='#30282b',width=3)
d.line([(224,325),(224,394)],fill='#36292d',width=3)
for cy in (340,365,390):d.ellipse((220,cy,225,cy+4),fill='#b6a375')
d.line([(220,408),(272,407)],fill='#352d24',width=12);d.rectangle((224,402,235,413),fill='#8e7045',outline='#322b20',width=2)
d.line([(261,437),(281,521)],fill='#392b31',width=3)
# Near bent arm moves forward, opposite the recovering near leg.
d.polygon([(257,320),(272,327),(265,374),(247,386),(228,373),(213,347),(225,337),(245,359),(247,338)],fill='#67454f',outline='#30282b',width=3)
d.polygon([(212,343),(224,334),(216,322),(205,330)],fill='#ddd3bd',outline='#493b36',width=2)
d.ellipse((195,315,215,333),fill='#c4a183',outline='#493630',width=2)
mask=mask.filter(ImageFilter.GaussianBlur(1));ma=np.array(mask);ma[:320]=0;mask=Image.fromarray(ma)
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'left facing side profile elf steward running, leaned torso, near bent arm forward, far leg extended to ground ahead, near leg bent heel kicked behind, long wine burgundy coat split tails, cream cuffs, plain belt, brown trousers and shoes, clean anime cel shading','standing, front view, face change, gold hanging keys, extra arm, extra leg, detached shoe, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.44,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending single key pose; not an animation clip','pose':'far-leg forward left-running key pose','head_guide':'leftward waist-pivot shear 0.10; not model-redrawn','status_note':'unapproved single pose, no run cycle'}
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
        assert outside==0;print('NERIS_WEST_RUN_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
