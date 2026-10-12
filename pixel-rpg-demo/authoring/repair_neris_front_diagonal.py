"""Restore Neris southeast low bun and belt keys."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--coat',action='store_true');args=parser.parse_args()
seed=777026 if args.coat else 777024;NAME=f'neris-SE-details-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/('neris-SE-details-777024.png' if args.coat else 'neris-SE-777023.png');original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
if not args.coat:
    # Clear the loose rear tuft and attach a compact low bun behind the ear.
    md.polygon([(176,224),(216,220),(238,235),(236,266),(178,266)],fill=255)
    d.polygon([(177,225),(216,221),(237,235),(235,266),(178,266)],fill='white')
    d.polygon([(204,224),(218,224),(227,240),(219,251),(203,244)],fill='#342e2a',outline='#292622',width=2)
    d.ellipse((181,230,219,262),fill='#342e2a',outline='#292622',width=2)
    d.arc((187,235,214,257),20,310,fill='#655447',width=2)
    # Keys hang from a small leather tab on the visible hip, clear of both hands.
    md.rectangle((291,408,308,477),fill=255)
    d.polygon([(295,410),(301,410),(301,425),(295,425)],fill='#654833',outline='#44352c',width=1)
    d.ellipse((294,422,305,435),outline='#bda16c',width=3)
    d.line([(297,434),(297,466),(302,466),(302,462)],fill='#bda16c',width=3)
    d.line([(304,434),(304,459),(307,459)],fill='#bda16c',width=2)
else:
    # Preserve luminance folds; shift only brown cloth, excluding belt/skin/cuffs.
    pixels=np.array(original);region=np.zeros(pixels.shape[:2],dtype=bool)
    region[285:601,203:332]=True;region[393:419,249:309]=False
    red=pixels[:,:,0].astype(int);green=pixels[:,:,1].astype(int);blue=pixels[:,:,2].astype(int)
    cloth=region & (red>green+6) & (red<150) & (green>=45) & (blue<110)
    shifted=pixels.copy();shifted[:,:,1][cloth]=np.maximum(0,green[cloth]-18)
    shifted[:,:,2][cloth]=np.minimum(255,blue[cloth]+4)
    guide=Image.fromarray(shifted);mask=Image.fromarray((cloth*255).astype('uint8'))
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'female elf steward in burgundy long coat, black hair tightly gathered into compact low bun behind ear, two small antique brass keys hanging from leather tab at belt, clean anime cel shading','loose hair, ponytail, hair ribbon, earrings, jewelry, weapon, missing key, text')
if args.coat:
    g=gen.graph(seed,'burgundy wine red tailored long coat with plain small brass buttons, restrained anime cel shading, consistent dark wine cloth','brown coat, orange coat, red armor, ornate decoration, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.18 if args.coat else .28,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending'}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'neris-SE-details'})['prompt_id']
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
        assert outside==0;print('NERIS_SE_DETAILS_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')

