"""Normalize Mira profile proportions and locally restore blouse and herb pouch."""
from pathlib import Path
import hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
NAME='mira-profile-774008';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
upstream=OUT/'mira-side-774007.png'
raw=Image.open(upstream).convert('RGB')
# Bring head/body ratio toward the front study, without changing the profile face.
def compact(im,background):
    result=Image.new(im.mode,im.size,background)
    result.paste(im.crop((0,0,512,235)),(0,0))
    result.paste(im.crop((0,235,512,768)).resize((512,384),Image.Resampling.LANCZOS),(0,235))
    return result
original=compact(raw,'white');source=OUT/(NAME+'-normalized.png');original.save(source)
guide=raw.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',raw.size);md=ImageDraw.Draw(mask)
# Recolor the existing modeled sleeve while retaining its shaded fold values.
region=[(252,258),(270,256),(287,275),(291,309),(294,339),(250,340),(242,330),(243,291)]
local=Image.new('L',raw.size);ImageDraw.Draw(local).polygon(region,fill=255)
a=np.asarray(guide).copy();sel=np.asarray(local)>0
shade=np.asarray(raw).mean(2)/220
for channel,value in enumerate((135,151,122)):
    a[:,:,channel][sel]=np.clip(shade[sel]*value,0,255).astype('uint8')
guide=Image.fromarray(a);d=ImageDraw.Draw(guide);md.polygon(region,fill=255)
d.polygon([(247,323),(291,329),(293,342),(249,338)],fill='#87977a',outline='#4d5b43',width=2)
# Replace pale tie with leather side belt and a herb pouch behind the forearm.
md.polygon([(233,387),(331,387),(331,417),(234,416)],fill=255)
d.polygon([(238,390),(328,393),(329,407),(237,404)],fill='#80563a',outline='#493a2b',width=2)
md.polygon([(217,411),(254,407),(263,429),(263,479),(218,479)],fill=255)
d.rounded_rectangle((222,430,260,474),5,fill='#96633f',outline='#463627',width=3)
d.polygon([(222,430),(258,430),(258,442),(224,441)],fill='#aa7852',outline='#463627',width=2)
for polygon in [[(242,432),(225,422),(226,410),(240,419)],[(243,431),(246,411),(257,408),(254,423)]]:
    d.polygon(polygon,fill='#738952',outline='#43523a',width=2)
guide=compact(guide,'white');mask=compact(mask,0)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(774008,'right profile apothecary woman wearing sage green linen puff sleeve with rolled cuff, muted sage fabric folds, brown leather belt and small leather herb pouch, broad medicinal leaves, simple clean anime cel shading','white sleeve, white belt, ribbons, extra hand, jewelry, text, photo')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.25,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending','upstream':str(upstream.relative_to(ROOT)),'upstream_sha256':hashlib.sha256(upstream.read_bytes()).hexdigest(),'normalization':{'split_y':235,'body_height_from':533,'body_height_to':384}}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'mira-profile-repair'})['prompt_id']
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
        assert outside==0;print('MIRA_PROFILE_REPAIR_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
