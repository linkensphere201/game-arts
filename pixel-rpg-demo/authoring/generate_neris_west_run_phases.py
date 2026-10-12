"""Local Neris east stride guides and masked model redraw."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--phase',choices=['near-contact','far-down','far-support','far-flight','near-down','near-support','near-flight'],required=True);args=parser.parse_args()
seed={'near-contact':777239,'far-down':777240,'far-support':777241,'far-flight':777242,'near-down':777243,'near-support':777244,'near-flight':777245}[args.phase];NAME=f'neris-west-run-phase-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'neris-west-run-cuff-777238.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
md.rectangle((168,461,346,633),fill=255);d.rectangle((168,461,346,633),fill='white')
lead,phase=args.phase.split('-');near_leads=lead=='near'
d.polygon([(228,461),(277,461),(285,507),(238,514)],fill='#443e35')
for near in (False,True):
    support=near==near_leads
    if support:
        pts=[(241,482),(259,488),(218,542),(239,589),(222,599),(196,548),(199,533)]
        shoe=[(220,588),(239,588),(241,614),(198,617),(197,609),(217,600)]
        if phase=='down':
            pts=[(241,482),(260,488),(221,548),(244,584),(226,592),(200,551),(203,536)]
            shoe=[(225,582),(244,584),(246,605),(205,608),(204,600),(223,592)]
        elif phase=='support':
            pts=[(241,482),(261,488),(253,548),(267,592),(248,598),(231,549)]
            shoe=[(248,589),(268,591),(269,615),(227,618),(226,610),(245,600)]
        elif phase=='flight':
            pts=[(240,482),(260,488),(216,532),(234,570),(216,580),(195,539),(198,523)]
            shoe=[(214,571),(234,570),(236,590),(196,593),(195,585),(212,579)]
    else:
        pts=[(254,483),(277,486),(299,546),(313,524),(330,531),(307,564),(286,565),(254,519)]
        shoe=[(311,522),(322,510),(330,507),(338,520),(330,535),(314,537)]
        if phase=='support':
            pts=[(246,482),(267,488),(220,519),(219,536),(255,568),(267,552),(240,529),(270,504)]
            shoe=[(252,550),(270,552),(280,568),(265,579),(239,568),(240,559)]
        elif phase=='flight':
            pts=[(254,483),(277,486),(290,529),(307,510),(321,519),(301,548),(280,549),(251,518)]
            shoe=[(305,508),(316,496),(325,496),(331,509),(321,523),(306,522)]
    d.polygon(pts,fill='#534b40' if near else '#39372f',outline='#302b28',width=3)
    d.polygon(shoe,fill='#63462e' if near else '#49382a',outline='#302b28',width=3)
# Complete coat-tail footprint; model paint retained where classified as fabric.
tailmask=Image.new('L',original.size);ImageDraw.Draw(tailmask).polygon([(225,461),(281,461),(301,520),(280,539),(254,496),(238,540),(212,530)],fill=255)
for y in range(461,541):
    a=np.array(original.crop((205,y,306,y+1)).convert('RGBA'));r,g,b=a[:,:,:3].astype(int).transpose(2,0,1)
    cloth=(r>g*1.1)&(b>g*.92)&(r<190);a[:,:,:3][~cloth]=[103,69,79];a[:,:,3]=np.array(tailmask.crop((205,y,306,y+1)))
    dx=round((3 if near_leads else -3)*(y-461)/80);guide.paste(Image.fromarray(a),(205+dx,y),Image.fromarray(a))
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'left facing elf running '+phase+' phase, two trouser legs, bent knees, brown shoes, wine burgundy split coat tails, clean anime cel shading','extra leg, missing foot, detached shoe, bare leg, face change, text')
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
        assert outside==0;print('NERIS_WEST_RUN_PHASE_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
