"""Reconstruct Neris side head and neck as one local model region."""
from pathlib import Path
import hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
seed=777018;NAME=f'neris-profile-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'neris-side-details-777015.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# A coherent broad chibi profile; retain the entire outfit below the collar.
md.rectangle((154,67,354,302),fill=255)
d.rectangle((154,67,354,281),fill='white')
d.polygon([(225,276),(276,276),(284,298),(232,297)],fill='#62434b')
ink='#46332d';skin='#d5b495';hair='#302d29'
d.polygon([(234,232),(274,239),(274,279),(262,289),(236,278)],fill=skin,outline=ink,width=2)
d.polygon([(232,276),(262,285),(278,276),(281,288),(264,296),(231,287)],fill='#ddd3b6',outline=ink,width=2)
d.polygon([(186,147),(213,114),(263,106),(306,125),(320,151),(319,181),(336,197),(322,207),(324,220),(315,235),(286,251),(250,248),(218,230),(192,201)],fill=skin,outline=ink,width=3)
d.polygon([(185,180),(175,148),(184,112),(210,86),(254,79),(291,89),(316,111),(326,143),(313,153),(294,131),(266,116),(235,130),(211,130),(203,178),(206,214),(185,206)],fill=hair,outline=ink,width=3)
d.line([(188,124),(212,102),(249,92),(277,96)],fill='#56534b',width=4)
d.ellipse((170,208,215,251),fill=hair,outline=ink,width=3)
d.arc((177,215,207,245),15,320,fill='#565047',width=3)
d.polygon([(224,179),(164,151),(179,189),(214,208),(232,201)],fill=skin,outline=ink,width=3)
d.line([(176,166),(200,189),(220,195)],fill='#ab8067',width=2)
d.line([(289,157),(308,157)],fill=ink,width=3)
d.polygon([(286,178),(295,169),(310,172),(313,182),(303,191),(292,187)],fill='#efe1c7',outline=ink,width=2)
d.ellipse((303,171,312,189),fill='#664630')
d.ellipse((308,174,312,184),fill='#302723')
d.line([(317,220),(307,221)],fill='#8e6753',width=2)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'strict right facing profile chibi adult female elf steward, broad rounded head, one open brown eye near nose, black swept back hair and low bun, long plain pointed ear, visible tan skin neck below jaw, narrow cream collar only at base of neck above burgundy coat, clean anime cel shading, broad simple shadows','frontal, two eyes, jewelry, earring, scarf, tall collar, white neck, white scarf, turtleneck, high collar, long neck, text, multiple heads')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.40,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending'}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'neris-profile'})['prompt_id']
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
        assert outside==0;print('NERIS_PROFILE_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')


