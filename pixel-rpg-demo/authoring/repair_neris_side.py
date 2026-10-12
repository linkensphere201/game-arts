"""Repair Neris profile face and belt keys with local model redraw."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--identity',action='store_true');args=parser.parse_args()
seed=777015 if args.identity else 777011;NAME=f'neris-side-details-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/('neris-side-details-777011.png' if args.identity else 'neris-side-777009.png');original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
if not args.identity:
    # Remove far-side facial features; keep nose contour and near eye.
    md.polygon([(290,148),(322,149),(320,169),(318,187),(310,195),(289,185)],fill=255)
    d.polygon([(291,149),(318,151),(315,163),(315,184),(309,192),(290,183)],fill=original.getpixel((280,190)))
    # Replace the decorative belt loop with two hanging key stems and teeth.
    md.rectangle((276,418,307,475),fill=255)
    d.polygon([(280,418),(290,418),(292,470),(280,470)],fill='#71504f')
    d.rectangle((293,418,307,475),fill='white')
    d.ellipse((281,422,296,437),fill='#78604a',outline='#c5aa6e',width=2)
    d.line([(285,435),(285,461),(291,461),(291,456)],fill='#b99d64',width=3)
    d.line([(292,435),(296,456),(302,455),(301,451)],fill='#c5aa6e',width=3)
else:
    # Open near eye; leave brow and nose intact.
    md.rectangle((246,160,280,195),fill=255)
    d.rectangle((247,161,279,194),fill=original.getpixel((280,190)))
    d.polygon([(249,175),(259,166),(273,170),(276,179),(266,190),(254,185)],fill='#eee1cc',outline='#634638',width=2)
    d.ellipse((264,169,274,187),fill='#694b35')
    d.ellipse((269,171,273,183),fill='#332c29')
    d.point((269,172),fill='#f8f0d9')
    d.line([(249,175),(259,166),(273,170)],fill='#47352c',width=2)
    # Plain ear/neck silhouette without generated jewelry.
    md.polygon([(206,201),(232,201),(246,224),(244,240),(220,223),(206,220)],fill=255)
    d.polygon([(206,202),(225,202),(237,218),(243,238),(227,221),(206,219)],fill='white')
    d.polygon([(226,204),(239,213),(244,236),(236,226)],fill='#c8a98d',outline='#765a48',width=1)
    # Reconnect the low bun to the hair behind the ear.
    md.polygon([(211,199),(230,203),(231,226),(209,235)],fill=255)
    d.polygon([(218,201),(228,205),(230,222),(217,231),(210,224)],fill='#332d2a',outline='#292422',width=2)
    d.line([(220,207),(220,220),(216,224)],fill='#57453a',width=2)
    # Neck redraw trials 777012-14 introduce seams; retain the source collar
    # until a coherent full head/neck profile is available.
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'strict right profile female elf face with only one visible eye, burgundy coat and two antique brass keys hanging from belt ring, clear key stems and teeth, clean anime cel shading','two eyes, frontal face, extra eye, buckle, ornament, text')
if args.identity:
    g=gen.graph(seed,'right profile adult female elf, one open brown eye, plain pointed ear without jewelry, burgundy tailored coat, clean anime cel shading','closed eyes, earrings, jewelry, scarf, tall collar, text, second eye')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.30 if args.identity else .20,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending'}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'neris-side-details'})['prompt_id']
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
        assert outside==0;print('NERIS_SIDE_DETAILS_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
