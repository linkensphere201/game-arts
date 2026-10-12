"""Match Neris rear sleeve/cuff length to her front design with local redraw."""
from pathlib import Path
import hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
seed=777008;NAME=f'neris-back-cuffs-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'neris-back-777007.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Left arm (screen left): burgundy sleeve continues to short linen cuff, then visible hand.
md.polygon([(192,397),(218,397),(219,429),(215,459),(198,461),(194,436)],fill=255)
d.polygon([(194,397),(216,397),(215,424),(198,426)],fill='#774651',outline='#49353d',width=2)
d.polygon([(198,424),(215,423),(216,440),(200,442)],fill='#dcd4b8',outline='#695747',width=2)
d.polygon([(200,442),(214,440),(214,453),(210,461),(202,457)],fill='#d9b79a',outline='#725343',width=2)
d.line([(208,445),(208,454),(205,455)],fill='#a17b60',width=1)
# Right arm: preserve hand placement, reduce the cream panel by extending sleeve above it.
md.polygon([(295,395),(319,395),(317,436),(316,450),(301,451),(298,429)],fill=255)
d.polygon([(297,395),(317,395),(316,424),(301,425)],fill='#74424e',outline='#49353d',width=2)
d.polygon([(301,424),(316,423),(316,442),(302,443)],fill='#dcd4b8',outline='#695747',width=2)
d.polygon([(302,443),(316,442),(315,451),(303,451)],fill='#d9b79a')
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'rear view of burgundy long coat sleeves ending in short cream linen cuffs at wrists, relaxed small natural hands visible below cuffs, clean anime cel shading','long white gloves, gauntlets, bandages, extra fingers, missing hand, text')
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
save();key=gen.request('/prompt',{'prompt':g,'client_id':'neris-back-cuffs'})['prompt_id']
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
        assert outside==0;print('NERIS_BACK_CUFFS_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
