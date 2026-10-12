"""Local opposing arm-swing poses on fixed Neris leg artwork."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--leg',choices=['left','right'],required=True);parser.add_argument('--half',action='store_true');args=parser.parse_args()
seed=(777063 if args.leg=='left' else 777064) if args.half else (777061 if args.leg=='left' else 777062);NAME=f'neris-rear-arm-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
leg_seed=(777055 if args.leg=='left' else 777056) if args.half else (777053 if args.leg=='left' else 777054)
source=OUT/f'neris-rear-walk-{leg_seed}.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Original sleeve/hand pixels form the guide; the local model redraws joins.
polygons={
 'left':[(200,310),(210,310),(217,341),(213,367),(220,387),(216,418),(214,459),(200,464),(194,438),(191,390),(187,367),(194,345)],
 'right':[(298,310),(308,309),(315,342),(317,360),(324,370),(317,388),(320,418),(316,463),(302,466),(295,445),(294,415),(291,387),(294,363)]}
for side,polygon in polygons.items():
    forward=side!=args.leg;factor=(.94 if forward else 1.03) if args.half else (.88 if forward else 1.06)
    arm_mask=Image.new('L',original.size);ImageDraw.Draw(arm_mask).polygon(polygon,fill=255)
    arm_mask=arm_mask.filter(ImageFilter.MaxFilter(9))
    arm=original.convert('RGBA');arm.putalpha(arm_mask)
    box=arm.getbbox();piece=arm.crop(box)
    piece=piece.resize((piece.width,round(piece.height*factor)),Image.Resampling.LANCZOS)
    moved=[(x,round(box[1]+(y-box[1])*factor)) for x,y in polygon]
    md.polygon(polygon,fill=255);md.polygon(moved,fill=255)
    erase=Image.new('L',original.size);ImageDraw.Draw(erase).polygon(polygon,fill=255);erase=erase.filter(ImageFilter.MaxFilter(9))
    guide.paste('white',(0,0,original.width,original.height),erase)
    # Continue coat behind shortened arm before compositing the moved sleeve.
    if side=='left':d.polygon([(206,312),(223,320),(223,462),(217,461)],fill='#744650')
    else:d.polygon([(288,312),(302,320),(295,464),(288,462)],fill='#744650')
    guide.paste(piece,(box[0],box[1]),piece)
mask=mask.filter(ImageFilter.MaxFilter(9))
# Preserve hanging keys and center tailoring rather than letting arm repair erase them.
ImageDraw.Draw(mask).rectangle((222,300,287,468),fill=0)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'back view walking elf steward moving away, closed coat back, no face or front buttons, opposite arms swing naturally while walking, burgundy long coat sleeves, short cream wrist cuffs and relaxed bare hands, one arm forward other arm back, clean anime cel shading','extra arm, extra hand, white gloves, missing cuff, armor, weapon, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.28,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'opposing arm pose study, not completed walk','lifted_leg':args.leg,'half':args.half}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'neris-rear-arm'})['prompt_id']
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
        assert outside==0;print('NERIS_REAR_ARM_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
