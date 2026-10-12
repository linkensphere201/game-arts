"""Local Neris east stride guides and masked model redraw."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
seed=777220;NAME=f'neris-east-run-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'neris-profile-777018.png';reference=Image.open(source).convert('RGB')
# Pivot upper silhouette forward at the waist, preserving its painted identity.
original=Image.new('RGB',reference.size,'white')
for y in range(reference.height):
    dx=round(.10*max(0,480-y))
    original.paste(reference.crop((0,y,reference.width-dx,y+1)),(dx,y))
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Reconstruct clothing and limbs together below the neck; the tilted head is protected.
md.rectangle((150,292,390,703),fill=255)
d.rectangle((150,292,390,703),fill='white')
# Far sleeve bends backward; near sleeve bends forward. Cream cuffs belong to sleeves.
d.polygon([(246,308),(223,323),(201,371),(171,363),(164,383),(205,400),(225,385),(265,335)],fill='#48333b',outline='#30282b',width=3)
d.polygon([(166,362),(180,365),(174,383),(161,380)],fill='#ddd3bd')
d.ellipse((150,361,169,380),fill='#c4a183',outline='#493630',width=2)
# Rear leg folds at knee: thigh down/back, calf lifted behind, distinct from walking.
d.polygon([(239,527),(265,543),(230,606),(207,608),(171,563),(190,550),(221,579)],fill='#39372f',outline='#302b28',width=3)
d.polygon([(170,548),(192,549),(191,562),(176,569),(158,557),(153,548)],fill='#63462e',outline='#302b28',width=3)
# Forward thigh raised, shin extends to a contacting toe.
d.polygon([(255,525),(276,526),(329,561),(333,580),(307,650),(284,648),(303,582),(256,558)],fill='#534b40',outline='#302b28',width=3)
d.polygon([(283,641),(307,644),(312,662),(337,670),(339,679),(282,676)],fill='#63462e',outline='#302b28',width=3)
# Leaning waist, split coat tails follow hips rather than retaining a standing hem.
d.polygon([(252,291),(306,294),(293,402),(282,469),(280,510),(308,571),(285,590),(250,543),(229,584),(195,574),(226,477),(231,405)],fill='#67454f',outline='#30282b',width=3)
d.polygon([(234,423),(265,427),(254,536),(229,584),(215,577)],fill='#533942')
d.line([(229,418),(289,424)],fill='#352d24',width=13)
d.rectangle((278,417,289,430),fill='#ac8c43',outline='#322b20',width=2)
# Neckline follows the leaned reference, with a closed collar and front fastening.
d.polygon([(252,292),(276,304),(306,294),(297,319),(278,314),(254,309)],fill='#473139',outline='#30282b',width=2)
d.line([(297,317),(286,411)],fill='#36292d',width=3)
for cy in (338,365,392):d.ellipse((289-(cy-338)//18,cy,294-(cy-338)//18,cy+5),fill='#b6a375')
d.line([(243,451),(225,552)],fill='#88636b',width=3)
d.line([(263,463),(270,536),(292,575)],fill='#36292d',width=3)
# Near arm has an actual bent elbow, cuff and forward hand.
d.polygon([(247,311),(267,316),(279,356),(294,358),(319,335),(331,350),(301,383),(275,382),(254,363),(241,337)],fill='#67454f',outline='#30282b',width=3)
d.polygon([(314,336),(323,329),(338,343),(329,354)],fill='#ddd3bd',outline='#493b36',width=2)
d.ellipse((325,319,348,340),fill='#c4a183',outline='#493630',width=2)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'right facing side profile elf steward running, forward leaning body, bent elbows swinging opposite legs, front knee raised and shin reaching down, rear knee bent with heel kicked up behind, long wine burgundy coat split tails follow motion, cream cuffs, brown trousers and shoes, clean anime cel shading, white background','standing straight, walking, straight hanging arms, extra arms, extra legs, detached shoe, front view, face change, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.48,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending single key pose; not an animation clip','pose':'near-leg forward running key pose','head_guide':'waist-pivot shear 0.10; not model-redrawn','status_note':'unapproved single pose, no run cycle'}
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
        assert outside==0;print('NERIS_EAST_RUN_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
