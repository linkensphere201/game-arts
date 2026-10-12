"""Restore Tovin's ledger satchel in the local side-view study."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();modes=parser.add_mutually_exclusive_group()
modes.add_argument('--details',action='store_true');modes.add_argument('--ankles',action='store_true')
modes.add_argument('--collar',action='store_true');modes.add_argument('--clean-neck',action='store_true')
modes.add_argument('--face',action='store_true');args=parser.parse_args()
seed=776024 if args.face else (776021 if args.clean_neck else (776020 if args.collar else (776017 if args.ankles else (776016 if args.details else 776013))))
NAME=f'tovin-side-bag-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/('tovin-side-bag-776013.png' if args.details else 'tovin-side-776011.png');original=Image.open(source).convert('RGB')
if args.ankles:
    source=OUT/'tovin-side-bag-776016.png';original=Image.open(source).convert('RGB')
if args.collar:
    source=OUT/'tovin-side-bag-776017.png';original=Image.open(source).convert('RGB')
if args.clean_neck:
    source=OUT/'tovin-side-bag-776020.png';original=Image.open(source).convert('RGB')
if args.face:
    source=OUT/'tovin-side-bag-776021.png';original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
# Front flap remains visible beyond the hanging arm; preserve all existing hand pixels.
md.polygon([(277,438),(324,438),(328,506),(318,524),(276,519),(273,500)],fill=255)
d.rounded_rectangle((268,442,324,519),7,fill='#7f563b',outline='#49382c',width=3)
d.polygon([(274,443),(324,443),(321,466),(299,475),(277,465)],fill='#9d704b',outline='#49382c',width=3)
d.rectangle((296,464,306,480),fill='#b69a62',outline='#49382c',width=2)
# Visible leather strap segment runs behind the arm along the waistcoat.
md.polygon([(272,405),(283,406),(300,443),(288,446)],fill=255)
d.polygon([(273,405),(281,406),(298,444),(289,445)],fill='#79563c',outline='#49382c',width=2)
if args.details:
    guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
    # Remove the unsupported cheek marking without repainting the eye or silhouette.
    md.ellipse((270,192,296,209),fill=255)
    guide.paste(original.crop((245,192,272,210)),(270,192))
    # Plain linen replaces the green neck clasp, respecting the shirt's outside edge.
    md.polygon([(299,307),(316,308),(318,329),(306,332),(300,321)],fill=255)
    d.polygon([(299,307),(314,310),(316,328),(307,330),(301,320)],fill='#d4ccad')
    d.line([(313,311),(314,324),(316,330)],fill='#6e624c',width=2)
    # Extend trouser fabric over the tall turned-down boot cuffs; shoes remain below.
    for left,right,sample_left,sample_right in [(193,250,208,238),(259,314,274,299)]:
        for y in range(599,666):
            for x in range(left,right):
                if min(original.getpixel((x,y)))<220:
                    color=original.getpixel((min(max(x,sample_left),sample_right),598))
                    guide.putpixel((x,y),color);mask.putpixel((x,y),255)
    d.line([(215,605),(212,637),(217,660)],fill='#756957',width=2)
    d.line([(281,605),(286,639),(281,660)],fill='#756957',width=2)
if args.ankles:
    guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
    # Measured y610 boundaries: left199..245, right264..308. Join those actual edges.
    for box,points,sample in [((191,609,254,659),[(199,606),(245,606),(244,625),(243,643),(249,658),(198,658),(201,641),(202,624)],(220,606)),((255,609,319,659),[(264,606),(308,606),(306,625),(306,644),(313,658),(263,658),(266,641),(265,624)],(285,606))]:
        md.rectangle(box,fill=255);d.rectangle(box,fill='white')
        d.polygon(points,fill=original.getpixel(sample))
        d.line(points[1:5],fill='#443c30',width=2)
        d.line(points[5:]+[points[0]],fill='#443c30',width=2)
    d.line([(231,613),(225,637),(229,651)],fill='#695e4e',width=2)
    d.line([(290,613),(285,637),(291,650)],fill='#695e4e',width=2)
if args.collar:
    guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
    # Lower the stiff rear collar and expose a short green nape above folded linen.
    region=[(213,254),(284,264),(296,293),(298,310),(276,308),(245,293),(214,289)]
    md.polygon(region,fill=255)
    d.polygon(region,fill='#d6ceb0')
    d.polygon([(215,254),(280,265),(288,281),(270,288),(237,280),(216,280)],fill=original.getpixel((246,260)))
    d.polygon([(215,281),(247,286),(268,296),(257,306),(236,296),(216,289)],fill='#dcd3b6',outline='#61553d',width=2)
    d.polygon([(277,285),(291,292),(296,310),(275,299)],fill='#ded5b8',outline='#61553d',width=2)
    # Leather at the near shoulder meets the lower strap behind the occluding sleeve.
    md.polygon([(232,293),(243,292),(259,310),(254,326),(240,306)],fill=255)
    d.polygon([(233,295),(241,293),(257,312),(254,322),(240,305)],fill='#805b3c',outline='#49382c',width=2)
    # Remove only bright gold trim along the back edge, retaining the garment silhouette.
    for y in range(316,511):
        for x in range(182,205):
            r,gc,b=original.getpixel((x,y))
            if r>145 and gc>100 and b<140 and r-gc>12:
                guide.putpixel((x,y),(153,126,81));mask.putpixel((x,y),255)
if args.collar:
    guide.paste(original.crop((0,0,512,266)),(0,0))
    md.polygon([(207,237),(320,237),(318,277),(303,315),(268,319),(212,293)],fill=255)
if args.clean_neck:
    guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
    region=[(316,263),(329,265),(330,313),(303,313),(305,291)]
    md.polygon(region,fill=255);d.polygon(region,fill='white')
if args.face:
    guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
    # One narrow profile eye replaces the youthful oval; preserve nose, hair and ear.
    region=[(287,149),(302,145),(314,151),(325,166),(325,203),(313,208),(281,207)]
    md.polygon(region,fill=255);d.polygon(region,fill=original.getpixel((280,190)))
    d.line([(290,175),(301,172),(312,176)],fill='#4e4831',width=4)
    d.polygon([(294,185),(305,182),(311,187),(307,193),(296,193)],fill='#d1c59c',outline='#4c462f',width=2)
    d.ellipse((303,183,310,194),fill='#453b27')
    d.line((294,185,306,182,312,187),fill='#453b27',width=2)
    d.line([(291,199),(299,201),(307,199)],fill='#69724b',width=2)
    md.polygon([(279,216),(305,215),(315,234),(307,248),(281,245)],fill=255)
    d.line([(307,219),(300,226),(300,233)],fill='#667048',width=2)
    d.line([(287,234),(287,241),(295,243)],fill='#6b754c',width=2)
mask=mask.filter(ImageFilter.GaussianBlur(1))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'simple brown leather rectangular ledger satchel at goblin merchant hip behind hanging green hand, leather flap small brass clasp, shoulder strap, ochre waistcoat, clean anime cel shading','extra hand, weapon, pouch cluster, text, logo, ornate bag')
if args.details:
    g=gen.graph(seed,'goblin merchant with plain olive green cheek, simple cream linen shirt, loose dark olive trouser legs covering ankles above low brown shoes, clean anime cel shading','blush, orange cheek, neck jewel, green clasp, tall boots, boot cuffs, bare ankles, text')
if args.ankles:
    g=gen.graph(seed,'continuous dark olive trouser legs with natural tapered fabric folds, plain trouser hems resting on low brown leather shoes, clean anime cel shading','boot cuffs, rolled trousers, bare ankles, gap, detached legs, white stripe, text')
if args.collar:
    g=gen.graph(seed,'goblin merchant plain open cream linen folded shirt collar, green neck above collar, simple brown leather satchel shoulder strap, ochre waistcoat, clean anime cel shading','high collar, gold piping, necktie, jewelry, neck clasp, gold trim, extra buckle, text')
if args.clean_neck:
    g=gen.graph(seed,'plain white empty background below chin outside character silhouette','blue line, drool, beard, pendant, text, necklace')
if args.face:
    g=gen.graph(seed,'middle aged male goblin merchant in strict right profile, one small narrow amber eye with a dark brown pupil and dark upper eyelid, brown eyebrows, defined brow ridge, subtle cheek creases, mature friendly face, olive green skin, clean cel shading','child, baby, huge eye, blank white eye, cataract, blue eyebrows, two eyes, front view, beard, tattoo, blush, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.22 if args.face else (.20 if args.clean_neck else (.60 if args.collar else (.40 if args.ankles else .30))),steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending'}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'tovin-side-bag'})['prompt_id']
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
        assert outside==0;print('TOVIN_SIDE_BAG_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
