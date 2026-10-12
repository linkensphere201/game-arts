"""Repair duplicate head in a retained local Osric profile trial."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();modes=parser.add_mutually_exclusive_group()
modes.add_argument('--sleeve',action='store_true');modes.add_argument('--details',action='store_true')
modes.add_argument('--sword',action='store_true');modes.add_argument('--hip',action='store_true');args=parser.parse_args()
seed=775017 if args.hip else (775016 if args.sword else (775013 if args.details else (775012 if args.sleeve else 775011)))
NAME=f'osric-side-clean-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/('osric-side-clean-775012.png' if args.details else ('osric-side-clean-775011.png' if args.sleeve else 'osric-side-775007.png'));original=Image.open(source).convert('RGB')
if args.sword:
    source=OUT/'osric-side-clean-775013.png';original=Image.open(source).convert('RGB')
if args.hip:
    source=OUT/'osric-side-clean-775016.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
if args.hip:
    # Rebuild continuous cloak edge and trouser folds behind the existing arm.
    region=[(233,430),(250,432),(264,449),(272,463),(274,487),(251,502),(235,484)]
    md.polygon(region,fill=255)
    cloth=original.copy();cd=ImageDraw.Draw(cloth)
    cd.polygon(region,fill='#8b817a')
    cd.polygon([(233,430),(240,430),(247,462),(249,502),(232,502)],fill='#665044')
    cd.line([(240,433),(242,452),(246,475),(247,501)],fill='#42382f',width=2)
    cd.polygon([(255,445),(260,460),(257,488),(252,499),(254,474)],fill='#746d68')
    cd.line([(268,475),(263,489),(262,500)],fill='#aca199',width=2)
    guide.paste(cloth,(0,0),mask);d=ImageDraw.Draw(guide)
    # A short suspension strap is visible between belt and guard; the hand stays in front.
    md.polygon([(298,414),(305,415),(307,443),(299,445)],fill=255)
    d.polygon([(298,414),(303,415),(306,442),(300,443)],fill='#77583b',outline='#49392c',width=1)
elif args.sword:
    # Remove the transverse black hilt from the cloak; carry a vertical wrapped grip.
    md.polygon([(234,443),(251,445),(275,457),(275,487),(243,468),(234,454)],fill=255)
    # Borrow nearby cloak/trouser texture rather than leaving a solid-color patch.
    patch=original.crop((232,491,276,535)).resize((44,44),Image.Resampling.LANCZOS)
    cloth=original.copy();cloth.paste(patch,(232,443))
    guide.paste(cloth,(0,0),mask);d=ImageDraw.Draw(guide)
    md.polygon([(283,390),(304,390),(308,444),(298,446),(285,438)],fill=255)
    d.polygon([(289,399),(300,399),(302,432),(290,432)],fill='#795639',outline='#44352b',width=2)
    d.ellipse((287,390,301,403),fill='#af925e',outline='#4e3d2b',width=2)
    for y in range(405,430,6):d.line((291,y,299,y+1),fill='#b2976b',width=2)
    d.polygon([(283,431),(305,428),(307,435),(286,439)],fill='#aa8c56',outline='#493a2c',width=2)
    md.polygon([(285,486),(298,486),(298,630),(291,650),(282,632)],fill=255)
    d.polygon([(287,486),(296,486),(295,627),(290,642),(284,628)],fill='#65513b',outline='#403329',width=2)
    d.line((290,489,289,625),fill='#a17d50',width=2)
    d.polygon([(284,628),(295,628),(290,644)],fill='#ab905c',outline='#493a2c',width=2)
elif args.details:
    # Interior-only patches keep the sleeve edge, hand, boot contours and sword intact.
    md.polygon([(248,377),(257,377),(265,390),(261,398),(250,395),(245,385)],fill=255)
    d.polygon([(248,377),(257,377),(265,390),(261,398),(250,395),(245,385)],fill='#c9ae90')
    for box,color in [((230,618,239,644),'#77654e'),((268,626,278,649),'#806a4e')]:
        md.rectangle(box,fill=255);d.rectangle(box,fill=color)
elif not args.sleeve:
    # Keep the valid lower profile face; remove only the duplicate above it.
    md.polygon([(182,75),(330,75),(330,181),(305,185),(280,193),(242,210),(190,210)],fill=255)
    d.rectangle((180,73,332,182),fill='white')
    d.polygon([(198,185),(216,164),(239,150),(263,148),(285,153),(300,165),(307,184),(282,186),(252,187),(223,187)],fill='#aeb0a8',outline='#655f55',width=2)
    d.line((216,174,239,157,264,154,282,158),fill='#d8d6c9',width=4)
else:
    md.polygon([(238,371),(267,367),(286,410),(298,444),(273,455),(254,420),(238,394)],fill=255)
    d.polygon([(245,380),(265,377),(277,402),(286,421),(294,438),(293,451),(278,451),(269,427),(254,408),(244,392)],fill='#cba68a',outline='#775c47',width=2)
    d.polygon([(245,387),(252,389),(261,411),(275,430),(279,447),(273,431),(256,414),(248,401)],fill='#ae8b6e')
    d.polygon([(238,375),(263,370),(271,384),(246,395)],fill='#cec09c',outline='#766952',width=2)
    d.line((244,378,264,376),fill='#e2d5b2',width=3)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'short swept silver grey hair on a single elderly man in right profile, smooth connected hair crown, plain white empty background above head, clean anime cel shading','extra head, second face, floating head, ponytail, hat, text, photo')
if args.sleeve:
    g=gen.graph(seed,'elderly man bare forearm below cream linen rolled elbow sleeve, natural aged skin, sleeve ends at elbow, relaxed hand, clean cel shading','long sleeve, gauntlet, bracelet, armor, extra hand, text')
if args.details:
    g=gen.graph(seed,'elderly swordsman plain bare forearm, natural skin, simple worn brown leather boots with smooth leather shafts, clean anime cel shading','tattoo, symbol, bracelet, laces, straps, buckles, ornament, text')
if args.sword:
    g=gen.graph(seed,'simple medieval sword sheathed vertically at hip behind relaxed hand, brown wrapped grip, small brass crossguard and pommel, narrow brown leather scabbard with plain brass tip, clean cel shading','black sword, horizontal grip, ornate sword, jewels, bare blade, extra hand, text')
if args.hip:
    g=gen.graph(seed,'elderly swordsman hip, continuous brown cloak edge over grey trousers with soft natural fabric folds, small leather sword suspension strap, clean cel shaded anime game character','patchwork, horizontal seam, belt crossing arm, extra hand, tattoo, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.38 if args.hip else (.25 if (args.details or args.sword) else (.30 if args.sleeve else .42)),steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending'}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'osric-side-repair'})['prompt_id']
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
        assert outside==0;print('OSRIC_SIDE_REPAIR_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
