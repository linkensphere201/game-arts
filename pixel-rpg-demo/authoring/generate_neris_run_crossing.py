"""Local Neris east stride guides and masked model redraw."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--phase',choices=['near-support','far-support'],required=True);args=parser.parse_args()
seed={'near-support':777229,'far-support':777230}[args.phase];NAME=f'neris-east-run-crossing-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'neris-east-run-details-777222.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
md.rectangle((143,479,361,698),fill=255);d.rectangle((143,479,361,698),fill='white')
near_support=args.phase=='near-support'
d.polygon([(224,479),(282,479),(283,546),(254,566),(220,543)],fill='#443e35')
for near in (False,True):
    support=near==near_support
    if support:
        pts=[(237,526),(260,528),(277,589),(265,650),(243,650),(251,593),(229,550)]
        shoe=[(242,643),(264,646),(266,660),(291,669),(292,679),(237,677)]
    else:
        pts=[(251,525),(274,526),(310,552),(312,573),(270,614),(249,602),(286,566),(253,552)]
        shoe=[(249,594),(272,606),(269,620),(287,629),(284,638),(245,621),(237,607)]
    d.polygon(pts,fill='#534b40' if near else '#39372f',outline='#302b28',width=3)
    d.polygon(shoe,fill='#63462e' if near else '#49382a',outline='#302b28',width=3)
# Solid tail mask prevents color-threshold holes in shaded fabric.
tailmask=Image.new('L',original.size);td=ImageDraw.Draw(tailmask)
td.polygon([(225,479),(280,479),(277,512),(294,556),(306,575),(288,589),(264,563),(251,541),(228,576),(202,566)],fill=255)
for y in range(479,590):
    strip=original.crop((192,y,312,y+1)).convert('RGBA');a=np.array(strip);r,g,b=a[:,:,:3].astype(int).transpose(2,0,1)
    cloth=(r>g*1.10)&(b>g*.92)&(r<190)
    a[:,:,:3][~cloth]=[103,69,79]
    a[:,:,3]=np.array(tailmask.crop((192,y,312,y+1)));strip=Image.fromarray(a)
    dx=round((-3 if near_support else 3)*(y-479)/115)
    guide.paste(strip,(192+dx,y),strip)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'right facing elf running passing phase, one supporting leg beneath hips slightly bent, other knee lifted forward and foot folded back across supporting shin, wine burgundy split coat tails, brown trousers and shoes, clean anime cel shading','extra leg, missing foot, detached shoe, bare leg, face change, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.30,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','phase':args.phase,'review':'leg-only running phases, upper body fixed; no finished cycle'}

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
        assert outside==0;print('NERIS_RUN_CROSSING_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
