"""Separate the veteran swordsman scabbard from his cloak using local redraw."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--attach',action='store_true');args=parser.parse_args()
seed=775003 if args.attach else 775002
NAME=f'osric-sword-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/('osric-sword-775002.png' if args.attach else 'osric-775001.png');original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
if not args.attach:
    # Clear only the unsupported hanging cloak strip below the proper cloak hem.
    md.polygon([(308,557),(339,553),(341,656),(304,656)],fill=255)
    d.polygon([(312,558),(340,552),(342,657),(305,657)],fill='white')
    # Sheathed sword hangs outside the hand, not merged into the cloak edge.
    region=[(338,370),(363,370),(377,413),(376,637),(351,650),(337,621)]
    md.polygon(region,fill=255)
    d.polygon([(344,420),(361,418),(370,617),(361,640),(350,620)],fill='#5c4938',outline='#392e27',width=3)
    d.line((349,435,359,616),fill='#9b7750',width=3)
    d.polygon([(350,616),(370,614),(366,631),(361,641),(353,628)],fill='#a68c58',outline='#493b29',width=2)
    d.polygon([(344,377),(355,376),(359,418),(346,419)],fill='#77523a',outline='#3e3028',width=3)
    for y in range(384,413,7):d.line((346,y,355,y+1),fill='#b09162',width=2)
    d.ellipse((341,371,356,384),fill='#ac925e',outline='#493b29',width=2)
    d.polygon([(337,416),(367,412),(372,420),(339,425)],fill='#b09661',outline='#493b29',width=3)
else:
    # Visible leather suspension emerges from behind the relaxed hand.
    region=[(330,450),(350,443),(358,455),(354,473),(330,477)]
    md.polygon(region,fill=255)
    d.polygon([(331,458),(350,449),(353,456),(334,470)],fill='#80603f',outline='#493929',width=2)
    d.polygon([(350,449),(356,451),(357,467),(349,469)],fill='#ac8d58',outline='#493929',width=2)
    md.rectangle((304,567,311,598),fill=255);d.rectangle((304,567,311,598),fill='white')
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'simple medieval sword fully sheathed in a narrow brown leather scabbard hanging vertically at the hip, visible wrapped grip and brass crossguard, brass scabbard tip, clean cel shaded game equipment','bare blade, staff, cane, cloak strip, hand holding sword, extra hand, text, photo')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.25,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending'}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'osric-sword-repair'})['prompt_id']
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
        assert outside==0;print('OSRIC_SWORD_REPAIR_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
