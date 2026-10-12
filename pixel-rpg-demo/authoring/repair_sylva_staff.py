"""Bounded local-model staff repair; preserve all unmasked character pixels."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, shutil, time
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'production/pixel-rpg/model-wave-01/guided'
BASE = ROOT / '.local/reference-comfy'
parser=argparse.ArgumentParser()
parser.add_argument('--part',choices=['staff','back-hair','back-staff','back-details','back-heels','back-volume','side-details','side-costume'],default='staff')
parser.add_argument('--seed',type=int)
parser.add_argument('--denoise',type=float,default=.28)
parser.add_argument('--curved-locks',action='store_true',help='Experimental dense hair guide; rejected for striped appearance')
args=parser.parse_args()
seed=args.seed or {'staff':761002,'back-hair':761004,'back-staff':761007,'back-details':761011,'back-heels':761012,'back-volume':761013,'side-details':761017,'side-costume':761018}[args.part]
NAME = f'sylva-{args.part}-{seed}'
record_path = OUT / (NAME + '.json')
if record_path.exists():
    raise RuntimeError('Run exists; inspect recorded prompt before another trial.')
spec = importlib.util.spec_from_file_location('generation', ROOT/'tools/generate-character.py')
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)
for port in (8188, 8189):
    gen.API = f'http://127.0.0.1:{port}'
    queue = gen.request('/queue')
    if queue.get('queue_running') or queue.get('queue_pending'):
        raise RuntimeError(f'Generation queue {port} is occupied.')
source = OUT/{'staff':'sylva-front-761001.png','back-hair':'sylva-back-761003.png','back-staff':'sylva-back-hair-761006.png','back-details':'sylva-back-staff-761007.png','back-heels':'sylva-back-details-761011.png','back-volume':'sylva-back-heels-761012.png','side-details':'sylva-side-761016.png','side-costume':'sylva-side-details-761017.png'}[args.part]
original = Image.open(source).convert('RGB')
guide = original.copy()
draw = ImageDraw.Draw(guide)
mask = Image.new('L', original.size)
md = ImageDraw.Draw(mask)
# Remove the detached extra shaft on the white side, without erasing the robe.
draw.polygon([(119,542),(126,549),(157,488),(154,477)], fill=(250,250,250))
md.polygon([(116,542),(126,553),(159,488),(154,474)], fill=255)
# A short crystal staff above the existing grip, retaining its original lower shaft.
draw.line([(173,437),(187,383)], fill='#44322c', width=9)
draw.line([(174,436),(188,384)], fill='#92704a', width=5)
draw.polygon([(192,344),(204,365),(191,390),(178,371)], fill='#3aaca0', outline='#294e49', width=3)
draw.polygon([(192,349),(190,384),(182,371)], fill='#9ad7bd')
draw.line([(183,387),(195,390)], fill='#b18f52', width=5)
md.line([(173,436),(188,382)], fill=255, width=15)
md.polygon([(192,339),(210,364),(198,395),(173,392),(172,368)], fill=255)
positive='small teal faceted crystal mounted on a single brown wooden magic staff, brass socket, clean anime colored outlines, restrained cel shading, elf mage holding staff'
negative='spear, blade, double staff, extra fingers, text, photo, realistic'
if args.part=='back-hair':
    guide=original.copy();draw=ImageDraw.Draw(guide)
    mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
    # Continuous loose hair, covering nape/back; no tied tail roots or exposed scalp.
    draw.polygon([(179,224),(195,202),(221,194),(251,195),(277,202),(294,219),(302,274),(300,315),(319,379),(328,419),(307,440),(290,420),(279,379),(255,404),(234,412),(213,397),(192,439),(171,439),(158,416),(178,357),(179,302)],fill='#c7a66a',outline='#665136',width=2)
    draw.polygon([(200,208),(223,201),(212,242),(218,300),(210,361),(192,420),(179,432),(187,374),(191,303),(185,260)],fill='#e2c48b')
    draw.polygon([(261,204),(279,218),(286,270),(279,318),(297,393),(314,428),(297,418),(272,367),(268,300)],fill='#ab8853')
    draw.line([(235,202),(228,251),(239,309),(230,373),(216,398)],fill='#a88954',width=3)
    draw.line([(249,204),(254,258),(249,313),(264,385)],fill='#e3c791',width=4)
    # Curved, tapered locks give the model a hair surface rather than flat cloth bands.
    for index in range(23 if args.curved_locks else 0):
        t=index/22
        start=np.array([205+65*t,201+12*abs(t-.5)])
        end=np.array([169+146*t,430-31*np.sin(np.pi*t)])
        c1=np.array([174+123*t,250])
        c2=np.array([199+66*t,343])
        points=[]
        for u in np.linspace(0,1,65):
            point=(1-u)**3*start+3*(1-u)**2*u*c1+3*(1-u)*u*u*c2+u**3*end
            points.append(tuple(point))
        draw.line(points,fill=['#b3925c','#dec08a','#c6a46a','#e0c28e'][index%4],width=2 if index%3 else 3)
    md.polygon([(175,220),(193,197),(219,188),(255,190),(281,196),(300,215),(309,274),(307,315),(326,377),(335,421),(307,447),(288,429),(278,392),(255,412),(232,420),(215,409),(193,446),(168,446),(151,417),(171,354),(173,298)],fill=255)
    positive='(strict rear view:1.4), (back of head covered with golden hair:1.3), long loose golden blonde hair falling in one continuous curtain down her back, smooth rounded crown, natural flowing hair strands, clean colored outlines, simple anime cel shading'
    negative='ponytail, twin tails, pigtails, tied hair, bald patch, exposed scalp, face, eyes, front view, hair ornament, white band, headband, white collar, text, photo'
if args.part=='back-staff':
    guide=original.copy();draw=ImageDraw.Draw(guide)
    mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
    draw.line([(330,443),(322,401)],fill='#4c392b',width=7)
    draw.line([(330,442),(322,401)],fill='#967348',width=3)
    draw.polygon([(318,372),(333,389),(324,406),(311,391)],fill='#43a99b',outline='#2d5550',width=2)
    draw.polygon([(318,377),(320,401),(314,391)],fill='#a0d8bd')
    draw.line([(319,405),(327,404)],fill='#b79b60',width=3)
    md.line([(330,442),(322,402)],fill=255,width=12)
    md.polygon([(318,367),(338,389),(329,411),(306,395)],fill=255)
    positive='small faceted teal crystal on a single wooden magic staff, brass socket, clean dark colored outline, anime cel shading'
    negative='spear, blade, duplicate, text, photograph, extra fingers'
if args.part=='back-details':
    guide=original.copy();draw=ImageDraw.Draw(guide)
    mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
    # Remove the detached horn-shaped ornament; keep the lower pointed ear.
    draw.polygon([(306,195),(319,195),(321,242),(312,247),(306,236)],fill=(250,250,250))
    md.polygon([(304,194),(321,194),(323,244),(311,249),(304,237)],fill=255)
    # Rear cuff belongs to the teal bell sleeve, not a large white inner sleeve.
    draw.polygon([(311,408),(326,410),(334,434),(323,442),(313,433)],fill='#28675f',outline='#35463b',width=2)
    draw.polygon([(319,434),(332,429),(335,434),(323,442)],fill='#ded5b6',outline='#5c624d',width=1)
    md.polygon([(309,406),(329,408),(339,435),(324,445),(311,435)],fill=255)
    positive='rear view teal cloth bell sleeve with a narrow cream cuff, simple fabric folds, clean colored outlines, anime cel shading, plain white background'
    negative='white sleeve, horn, ornament, jewelry, extra arm, extra hand, text, photograph'
if args.part=='back-heels':
    guide=original.copy();draw=ImageDraw.Draw(guide)
    mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
    # Preserve the robe and ankles. Rear heel cups cover the front-facing toe straps.
    for polygon in [[(221,557),(240,554),(244,573),(241,581),(225,581),(221,575)],
                    [(277,555),(294,555),(304,574),(301,580),(278,580),(275,573)]]:
        draw.polygon(polygon,fill='#79553b',outline='#382f29',width=2)
        md.polygon(polygon,fill=255)
    draw.line([(230,558),(231,575)],fill='#ad8255',width=2)
    draw.line([(284,558),(289,574)],fill='#ad8255',width=2)
    draw.line([(224,577),(240,577)],fill='#3b3028',width=3)
    draw.line([(278,576),(301,576)],fill='#3b3028',width=3)
    positive='(rear view of brown leather shoes:1.4), closed brown leather heel cups, vertical back seam, dark flat soles, small chibi fantasy elf seen from behind, clean colored outlines, restrained anime cel shading'
    negative='toes, front view, sandal straps, laces, buckles, high heels, extra feet, text, photograph'
if args.part=='back-volume':
    guide=original.copy()
    mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
    # Repaint only the hair interior. Keep silhouette, ears, clothes and staff fixed.
    # No dense stripe guide: the earlier 761010 trial turned those into fabric bands.
    md.polygon([(189,226),(206,211),(245,203),(274,209),(292,229),
                (296,287),(295,327),(304,371),(311,424),(298,429),
                (282,387),(260,396),(239,401),(218,389),(198,409),
                (180,432),(169,422),(182,367),(187,311)],fill=255)
    positive='(rear view:1.4), back of the head of an elf girl, (long loose golden blonde hair:1.3), layered flowing locks of hair, tapered overlapping hair clumps, curved hair highlights, warm golden shadows between locks, detailed anime hair, clean colored line art, cel shaded fantasy JRPG character'
    negative='fabric, cloak, cape, hood, stripes, ribbon, band, hat, braid, ponytail, pigtails, eyes, face, front view, ornament, photorealistic, text'
if args.part=='side-details':
    guide=original.copy();draw=ImageDraw.Draw(guide)
    mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
    # Cover the invented bare shoulder with the robe's teal cloth and cream collar.
    draw.polygon([(245,285),(258,294),(277,306),(285,329),(276,347),(237,335),(237,313)],fill='#28675f',outline='#35463b',width=2)
    draw.line([(249,288),(257,300),(276,311)],fill='#ded5b6',width=4)
    md.polygon([(242,283),(262,292),(280,304),(288,330),(278,351),(234,338),(234,310)],fill=255)
    # Restore the single crystal head above the existing grip.
    draw.line([(310,461),(304,397)],fill='#604534',width=7)
    draw.line([(309,457),(303,397)],fill='#a27c4c',width=2)
    draw.polygon([(300,367),(314,384),(305,403),(292,386)],fill='#49a998',outline='#354e43',width=2)
    draw.polygon([(300,372),(302,397),(295,386)],fill='#a0d8bd')
    md.line([(310,462),(304,397)],fill=255,width=13)
    md.polygon([(300,364),(318,384),(309,407),(288,389)],fill=255)
    positive='side profile of elf mage wearing a closed teal cloth shoulder and narrow cream collar, small faceted teal crystal on a single wooden staff, clean colored outlines, restrained anime cel shading'
    negative='bare shoulder, bare chest, shoulder straps, horn, spear, blade, duplicate staff, jewelry, text, photo'
if args.part=='side-costume':
    guide=original.copy();draw=ImageDraw.Draw(guide)
    mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
    # Replace the invented white sock with skin, retaining the brown shoe straps.
    draw.polygon([(233,623),(252,626),(255,642),(251,651),(240,649),(239,637)],fill='#e8c6a2')
    draw.line([(235,625),(240,642),(241,648)],fill='#c79c7b',width=2)
    md.polygon([(232,621),(253,624),(257,642),(253,653),(238,651),(237,637)],fill=255)
    # Cream cloth cuff, not a metallic gold trim. Preserve the crossing staff.
    draw.polygon([(284,449),(317,434),(320,440),(289,457)],fill='#ded5b6',outline='#575746',width=1)
    md.polygon([(282,448),(318,432),(322,442),(289,460)],fill=255)
    guide.paste(original.crop((302,431,315,463)),(302,431))
    md.rectangle((302,431,314,462),fill=0)
    positive='side profile elf mage, bare ankle skin above brown leather strapped shoes, narrow cream fabric cuff on teal bell sleeve, clean anime colored outline, restrained cel shading'
    negative='white socks, stockings, gold cuff, metal bracelet, boots, new jewelry, extra toes, text, photo'
mask = mask.filter(ImageFilter.GaussianBlur(1))
for suffix, im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png')
    im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g = gen.graph(seed,positive,negative)
g['5'] = {'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9'] = {'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10'] = {'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11'] = {'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12'] = {'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13'] = {'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=args.denoise,steps=30,cfg=6)
g['14'] = {'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec = {'source':str(source.relative_to(ROOT)), 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending'}
def save():
    record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save()
key = gen.request('/prompt',{'prompt':g,'client_id':'sylva-staff-repair'})['prompt_id']
rec.update(prompt_id=key,state='queued'); save()
print('QUEUED',key,flush=True)
start = time.monotonic()
while time.monotonic()-start < 900:
    history = gen.request('/history/'+key)
    if key in history:
        h = history[key]; rec.update(state=h['status']['status_str'],history=h)
        save()
        if rec['state'] != 'success': raise RuntimeError(record_path)
        f = h['outputs']['8']['images'][0]
        target = OUT/(NAME+'.png')
        shutil.copy2(BASE/'output'/f['subfolder']/f['filename'],target)
        result = np.asarray(Image.open(target).convert('RGB'))
        outside = np.asarray(mask)==0
        difference = int(np.abs(result.astype(int)-np.asarray(original).astype(int))[outside].max())
        rec.update(outside_mask_max_difference=difference, output_sha256=hashlib.sha256(target.read_bytes()).hexdigest())
        save(); assert difference == 0
        print('MASKED_REPAIR_OK',flush=True)
        break
    time.sleep(2)
else:
    raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
