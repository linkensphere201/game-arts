"""Bounded local cleanup of Tovin rear hair and unsupported hip strap."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--strap-only',action='store_true');args=parser.parse_args()
seed=776010 if args.strap_only else 776009
NAME=f'tovin-back-clean-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'tovin-back-776006.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Short, irregular hairline reveals the green nape rather than a long bob.
region=[(196,230),(317,230),(317,284),(282,292),(254,304),(230,292),(196,284)]
md.polygon(region,fill=255);d.polygon(region,fill='white')
d.polygon([(205,250),(307,250),(298,273),(280,282),(279,299),(254,307),(232,299),(232,281),(214,274)],fill='#8c9769',outline='#514c34',width=2)
d.polygon([(195,225),(317,225),(311,249),(302,259),(290,261),(283,270),(271,264),(260,272),(249,266),(236,270),(225,261),(214,265),(205,258)],fill='#68513a')
d.line([(213,263),(225,259),(237,268),(249,264),(260,270),(271,262),(282,267),(291,260)],fill='#493d2d',width=2)
# Restore sleeve-side hand and continuous waistcoat edge instead of a second bag strap.
region=[(326,431),(343,431),(349,456),(344,478),(325,486),(320,476)]
md.polygon(region,fill=255)
d.polygon(region,fill='#879265')
d.polygon([(325,431),(333,433),(333,453),(327,475),(324,484),(318,484)],fill='#a78f57')
d.line([(333,433),(333,451),(329,468),(324,483)],fill='#514530',width=2)
d.line([(343,457),(340,469),(335,473)],fill='#63734a',width=2)
md.polygon([(190,175),(202,147),(241,137),(291,147),(319,166),(324,225),(317,282),(280,301),(230,302),(193,275)],fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(2))
if args.strap_only:
    guide.paste(original.crop((0,0,512,320)),(0,0))
    mask.paste(0,(0,0,512,320))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'rear view of goblin merchant, short brown hair trimmed above exposed green nape, plain ochre waistcoat beside relaxed green hand, clean simple anime cel shading','long hair, bob haircut, extra strap, second satchel, wrist bracelet, face, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.30 if args.strap_only else .55,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending'}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'tovin-back-cleanup'})['prompt_id']
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
        assert outside==0;print('TOVIN_BACK_CLEANUP_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
