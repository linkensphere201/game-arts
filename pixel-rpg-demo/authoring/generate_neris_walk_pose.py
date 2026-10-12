"""Local Neris front walk key poses; preserve face, torso and support leg."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--swing',choices=['left','right'],required=True);parser.add_argument('--half',action='store_true');args=parser.parse_args()
seed=(777040 if args.swing=='left' else 777039) if args.half else (777036 if args.swing=='left' else 777037);NAME=f'neris-walk-pose-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/'neris-keys-777006.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Change only the swinging leg and its coat tail. Support foot stays planted.
left=args.swing=='left'
x0,x1=(182,252) if left else (262,332)
region=[(204,470),(252,470),(252,698),(182,698),(182,500),(203,500)] if left else [(263,480),(314,480),(332,502),(332,698),(262,698)]
md.polygon(region,fill=255);d.polygon(region,fill='white')
ink='#42352f';cloth='#744650'
if left:
    leg=[(211,533),(237,534),(242,572),(232,619),(213,627),(204,612),(218,572)]
    tail=[(207,500),(245,500),(246,537),(231,572),(195,563),(197,540)]
    boot=original.crop((198,641,254,684)).resize((48,37),Image.Resampling.LANCZOS)
    boot_xy=(202,616)
else:
    leg=[(276,533),(302,532),(309,572),(296,620),(278,627),(269,612),(283,574)]
    tail=[(266,500),(307,500),(322,549),(313,569),(276,577),(267,542)]
    boot=original.crop((266,641,319,685)).resize((48,37),Image.Resampling.LANCZOS)
    boot_xy=(271,616)
if args.half:
    leg=[(x,round(533+(y-533)*1.18)) for x,y in leg]
    boot_xy=(boot_xy[0],633)
d.polygon(leg,fill='#534b3e',outline=ink,width=3)
if args.half and left:
    d.polygon([(212,622),(238,623),(236,653),(210,653)],fill='#534b3e',outline=ink,width=2)
# Keep boot background transparent so it cannot cut through the lower leg.
def paste_foreground(piece,xy):
    piece=piece.convert('RGBA');pixels=np.asarray(piece).copy()
    white=(pixels[:,:,:3].min(2)>233)&(pixels[:,:,:3].max(2)-pixels[:,:,:3].min(2)<28)
    pixels[:,:,3][white]=0;piece=Image.fromarray(pixels)
    guide.paste(piece,xy,piece)
paste_foreground(boot,boot_xy)
# Compress the original coat-tail painting rather than attaching a flat patch.
if left:
    piece=original.crop((189,470,252,606)).resize((63,121 if args.half else 106),Image.Resampling.LANCZOS)
    paste_foreground(piece,(189,470))
else:
    piece=original.crop((262,480,322,606)).resize((60,115 if args.half else 102),Image.Resampling.LANCZOS)
    paste_foreground(piece,(262,480))
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'front view walking elf steward, one knee bends and foot lifts during a step, dark trouser leg and plain brown shoe, burgundy long coat tail drapes over raised thigh with curved folds, opposite leg supports body, clean anime cel shading','bare leg, extra leg, extra foot, missing foot, high heel, boot laces, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.38,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending single key pose; not an animation clip','swing':args.swing,'half':args.half}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'neris-walk-pose'})['prompt_id']
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
        assert outside==0;print('NERIS_WALK_POSE_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
