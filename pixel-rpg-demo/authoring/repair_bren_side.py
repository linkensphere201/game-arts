"""Local masked cleanup of invented dragonborn head details; preserve other pixels."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--seed',type=int,default=773011);parser.add_argument('--cheeks',action='store_true');parser.add_argument('--trim-spikes',action='store_true');parser.add_argument('--boots',action='store_true');args=parser.parse_args()
assert sum([args.cheeks,args.trim_spikes,args.boots])<=1
NAME=f'bren-side-clean-{args.seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/('bren-side-clean-773013.png' if args.boots else 'bren-side-clean-773011.png' if args.trim_spikes else 'bren-side-773006.png');original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Remove the invented ornament between the two original horns.
ornament=[(289,86),(313,86),(313,115),(306,130),(291,141),(278,140),(281,128),(289,116)]
d.polygon(ornament,fill='white');md.polygon(ornament,fill=255)
# Remove only the extra rear cheek spikes and reconnect the bare skull contour.
if args.cheeks:
    region=[(231,140),(310,140),(311,190),(308,219),(298,243),(296,269),(278,272),(251,260),(233,232),(228,198)]
    d.polygon(region,fill='white');md.polygon(region,fill=255)
    skull=[(253,148),(254,177),(253,195),(256,218),(263,241),(277,258),(293,269),(317,270),(319,137),(270,137)]
    d.polygon(skull,fill='#719594')
    d.line(skull[:7],fill='#34494a',width=2)
if args.trim_spikes:
    # Preserve the actual ear and center head shading; trim only the extra frills.
    for region in [
        [(245,166),(267,165),(271,181),(263,194),(251,194),(245,184)],
        [(235,218),(260,221),(277,236),(274,252),(264,259),(250,254),(250,239),(233,234)],
    ]:
        d.polygon(region,fill='white');md.polygon(region,fill=255)
    d.polygon([(263,169),(258,183),(258,194),(301,200),(302,165)],fill='#709898')
    d.line([(263,169),(258,183),(258,194)],fill='#34494a',width=2)
    d.polygon([(254,221),(251,232),(259,235),(264,247),(274,254),(306,261),(308,216)],fill='#709898')
    d.line([(254,221),(251,232),(259,235),(264,247),(274,254)],fill='#34494a',width=2)
if args.boots:
    guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
    region=[(332,571),(354,571),(353,619),(350,641),(328,645),(326,618)]
    d.polygon(region,fill='#554337');md.polygon(region,fill=255)
    outside=[(346,576),(356,576),(356,637),(344,637),(344,617),(345,589)]
    d.polygon(outside,fill='white')
    d.line([(346,576),(345,589),(344,617),(344,637)],fill='#332e28',width=3)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(args.seed,'right profile bare blue grey reptilian skull, clean smooth rear head contour, two original ivory horns only, no head ornament, consistent flat anime shading, white background','third horn, jewelry, crown, ornament, cheek spikes, frills, ears, hair, hood, photo, text')
if args.boots:
    g=gen.graph(args.seed,'right side brown leather boot, plain closed boot shaft, uninterrupted smooth leather panel, simple dark side seam, same original heavy rounded boot, clean dark anime contours and restrained shading','laces, lacing, eyelets, straps, buckles, ornate armor, spikes, text, extra foot')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.25,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'arguments':vars(args),'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending'}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'bren-side-repair'})['prompt_id']
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
        assert outside==0;print('BREN_MASKED_REPAIR_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
