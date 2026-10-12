"""Local masked refinement of Tovin's adult face and heavy body build."""
from pathlib import Path
import hashlib,importlib.util,json,shutil,time,math
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
seed=776005;NAME=f'tovin-refined-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'tovin-776001.png';original=Image.open(source).convert('RGB')
guide=original.copy();mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Smoothly widen the full torso silhouette, including its sleeves and satchel.
# Head and boots remain at their original coordinates.
for y in range(290,582):
    factor=1+.19*math.sin(math.pi*(y-290)/292)**2
    width=round(original.width*factor)
    row=original.crop((0,y,512,y+1)).resize((width,1),Image.Resampling.BICUBIC)
    guide.paste(row.crop(((width-512)//2,0,(width-512)//2+512,1)),(0,y))
md.rounded_rectangle((87,296,425,576),18,fill=255)
# Strengthen eyebrows, eyelids and nose; retain original ears and hair.
d=ImageDraw.Draw(guide)
md.ellipse((185,163,323,266),fill=255)
# Clear the higher original brows before drawing the lowered mature brows.
for box in [(198,142,246,167),(267,142,312,167)]:
    md.rectangle(box,fill=255);d.rectangle(box,fill='#929870')
d.line([(203,178),(215,174),(228,179)],fill='#484630',width=4)
d.line([(277,178),(289,174),(300,179)],fill='#484630',width=4)
for x in (214,287):
    d.line((x-12,189,x+9,187),fill='#49442e',width=3)
    d.ellipse((x-3,189,x+3,197),fill='#4c452d')
    d.line((x-12,204,x+8,205),fill='#707b50',width=2)
d.arc((236,199,272,228),0,185,fill='#5b6844',width=3)
d.line([(230,226),(225,236),(229,240)],fill='#687548',width=2)
d.line([(281,226),(286,236),(282,240)],fill='#687548',width=2)
mask=mask.filter(ImageFilter.GaussianBlur(2))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'friendly middle aged male goblin merchant, mature broad face and nose, defined eyebrows and small amber eyes, olive green skin, fat round belly, ochre waistcoat cream shirt brown leather satchel, clean anime cel shading','child, baby, thin, human skin, missing bag, missing shoes, beard, extra limb, text')
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
save();key=gen.request('/prompt',{'prompt':g,'client_id':'tovin-refinement'})['prompt_id']
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
        assert outside==0;print('TOVIN_REFINEMENT_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
