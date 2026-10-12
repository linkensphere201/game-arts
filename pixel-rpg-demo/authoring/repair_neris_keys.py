"""Restore the original elven steward's brass key ring using local masked redraw."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();modes=parser.add_mutually_exclusive_group()
modes.add_argument('--coat',action='store_true');modes.add_argument('--placket',action='store_true');args=parser.parse_args()
seed=777006 if args.placket else (777003 if args.coat else 777002)
NAME=f'neris-keys-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/('neris-keys-777002.png' if args.coat else 'neris-777001.png');original=Image.open(source).convert('RGB')
if args.placket:
    source=OUT/'neris-keys-777003.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Keys hang from a leather belt tab, clear of the relaxed hand at screen right.
md.rounded_rectangle((278,408,308,482),5,fill=255)
d.rectangle((287,409,296,423),fill='#72523b',outline='#49382f',width=2)
d.ellipse((283,418,301,436),outline='#49382f',width=5)
d.ellipse((285,420,299,434),outline='#c0a66b',width=3)
for x,y,length in [(285,434,34),(298,435,41)]:
    d.ellipse((x-4,y-3,x+4,y+5),outline='#49382f',width=4)
    d.ellipse((x-3,y-2,x+3,y+4),outline='#c0a66b',width=2)
    d.line((x,y+4,x,y+length),fill='#49382f',width=6)
    d.line((x,y+4,x,y+length),fill='#c0a66b',width=3)
    d.line((x,y+length-5,x+7,y+length-5),fill='#49382f',width=5)
    d.line((x,y+length-5,x+7,y+length-5),fill='#c0a66b',width=3)
if args.coat:
    guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
    # Replace the oversized breast ornament and gold placket with tailored cloth.
    region=[(219,288),(239,290),(252,280),(266,283),(287,291),(287,336),(269,343),(269,400),(242,400),(240,343),(218,333)]
    md.polygon(region,fill=255)
    d.polygon(region,fill='#784650')
    d.polygon([(246,289),(264,289),(265,400),(247,400)],fill='#89545b')
    d.line([(246,290),(247,399)],fill='#52333c',width=2)
    d.line([(220,289),(239,300),(248,304)],fill='#a06f72',width=2)
    d.line([(284,291),(272,300),(264,304)],fill='#583a40',width=2)
    for y in (309,334,359,384):
        d.ellipse((252,y,259,y+7),fill='#b29a65',outline='#4d3e30',width=1)
if args.placket:
    guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
    # Continue the cloth placket below the belt and remove the unsupported tassel.
    md.polygon([(241,423),(268,423),(267,465),(271,518),(242,518),(244,466)],fill=255)
    d.polygon([(241,423),(268,423),(267,465),(271,518),(242,518),(244,466)],fill='#604a3c')
    d.polygon([(246,423),(265,423),(265,466),(248,473)],fill='#89545b',outline='#52333c',width=2)
    for y in (430,451):d.ellipse((252,y,259,y+7),fill='#b29a65',outline='#4d3e30',width=1)
    # Continue the existing clean coat-opening texture from below the old tassel.
    patch=original.crop((242,520,272,550)).resize((30,55),Image.Resampling.LANCZOS)
    guide.paste(patch,(242,464))
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'two simple antique brass door keys hanging from a small key ring attached to leather waist belt, burgundy coat behind keys, clean anime cel shading','hand holding keys, extra fingers, necklace, weapon, chainmail, text')
if args.coat:
    g=gen.graph(seed,'plain tailored burgundy steward coat chest, narrow matching cloth button placket with small antique brass buttons, restrained practical medieval clothing, clean anime cel shading','brooch, medallion, pendant, gold chest plate, embroidery, jewelry, necklace, text')
if args.placket:
    g=gen.graph(seed,'burgundy coat narrow cloth button placket below leather belt, plain dark trousers visible inside coat opening, small brass buttons, clean cel shading','tassel, gold strip, rope, pendant, embroidery, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.30,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending'}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'neris-keys'})['prompt_id']
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
        assert outside==0;print('NERIS_KEYS_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
