"""Local Neris east stride guides and masked model redraw."""
from pathlib import Path
import hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
seed=777234;NAME=f'neris-east-run-arms-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'neris-east-run-details-777222.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Rebuild complementary bent sleeves below collar and above the unchanged belt.
md.rectangle((143,305,355,414),fill=255);d.rectangle((143,305,355,414),fill='white')
# Far arm swings forward behind torso.
d.polygon([(282,309),(297,314),(310,355),(324,339),(336,350),(314,379),(299,378),(275,337)],fill='#49333d',outline='#30282b',width=3)
d.polygon([(320,339),(329,330),(343,341),(334,353)],fill='#c6bea9',outline='#493b36',width=2)
d.ellipse((330,320,350,340),fill='#b39376',outline='#493630',width=2)
# Restore a continuous jacket torso and front seam.
d.polygon([(250,305),(302,305),(300,315),(291,373),(288,414),(226,414),(234,370)],fill='#67454f',outline='#30282b',width=3)
d.line([(295,319),(286,408)],fill='#36292d',width=3)
for cy in (338,365,392):d.ellipse((289-(cy-338)//18,cy,294-(cy-338)//18,cy+5),fill='#b6a375')
# Near elbow trails behind; bent forearm returns towards the ribs.
d.polygon([(242,311),(261,321),(236,363),(220,381),(198,372),(205,353),(227,326)],fill='#67454f',outline='#30282b',width=3)
d.polygon([(202,353),(223,339),(238,343),(241,359),(220,378),(201,371)],fill='#75525c',outline='#30282b',width=3)
d.polygon([(230,338),(241,334),(249,350),(239,359)],fill='#ddd3bd',outline='#493b36',width=2)
d.ellipse((239,325,259,344),fill='#c4a183',outline='#493630',width=2)
mask=mask.filter(ImageFilter.GaussianBlur(1))
# Keep neckline and belt exact even along the blurred mask boundary.
ma=np.array(mask);ma[:316]=0;ma[413:]=0;mask=Image.fromarray(ma)
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'right facing elf steward running, near elbow back with bent forearm at ribs, far arm swinging forward, two bent arms, wine burgundy fitted coat cream cuffs gold buttons, clean anime cel shading','extra arm, missing hand, straight arm, face change, belt change, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.38,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'opposite running arms study, not accepted animation','protected':'rows before316 and from413, including head collar belt keys and legs'}

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
        assert outside==0;print('NERIS_RUN_ARMS_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
