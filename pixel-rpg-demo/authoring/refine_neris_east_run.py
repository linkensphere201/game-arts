"""Local Neris east stride guides and masked model redraw."""
from pathlib import Path
import hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
seed=777222;NAME=f'neris-east-run-details-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'neris-east-run-777220.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Local neckline cleanup; no regeneration of the face, hands or running pose.
md.polygon([(234,281),(255,280),(274,289),(309,289),(308,316),(252,313),(234,299)],fill=255)
d.polygon([(234,281),(254,281),(255,291),(240,296),(234,296)],fill='white')
d.polygon([(252,277),(294,284),(301,294),(278,299),(253,290)],fill='#c4aa88')
d.polygon([(252,290),(278,298),(302,291),(303,302),(279,308),(250,300)],fill='#5e3f49',outline='#362a2f',width=2)
# Restore the actual reference gold key silhouette, retaining current cloth behind it.
reference=OUT/'neris-profile-777018.png'
patch=Image.open(reference).convert('RGBA').crop((279,417,306,462))
a=np.array(patch);r,g,b=a[:,:,:3].astype(int).transpose(2,0,1)
keep=(r>b+20)&(g>b+12)&(r>95)&(g>75)&(r>g*.95)&(r<g*1.7)
a[:,:,3]=keep.astype('uint8')*255;patch=Image.fromarray(a)
guide.paste(patch,(276,424),patch);md.rectangle((274,420,305,473),fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'same elf steward in wine burgundy coat, simple fitted round collar, small gold keys hanging from right waist belt, clean anime cel shading, preserve running pose','necktie, white shirt triangle, extra jewelry, extra arms, extra legs, face change, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.20,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending single key pose; not an animation clip','pose':'near-leg forward running key pose','reference':str(reference.relative_to(ROOT)),'reference_sha256':hashlib.sha256(reference.read_bytes()).hexdigest(),'repair':'collar and reference keys only','status_note':'unapproved single pose, no run cycle'}
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
        assert outside==0;print('NERIS_RUN_DETAILS_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
