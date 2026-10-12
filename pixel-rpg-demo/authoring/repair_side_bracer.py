"""Local masked garment repair with pixel-exact preservation outside the blend mask."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,time,shutil
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'
BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--part',choices=['bracer','hair','cape','shoulder','ne-hair','ne-cape','ne-heading','ne-nape','se-belt','se-cape','n-shoulders','ne-shoulder'],default='bracer');args=parser.parse_args()
seed={'bracer':755001,'hair':755002,'cape':755003,'shoulder':755004,'ne-hair':756004,'ne-cape':756005,'ne-heading':756006,'ne-nape':756007,'se-belt':757004,'se-cape':757005,'n-shoulders':758001,'ne-shoulder':758002}[args.part]
NAME=f'rowan-side-{args.part}-{seed}' if not args.part.startswith('ne-') else f'rowan-NE-{args.part[3:]}-{seed}'
if args.part.startswith('se-'):NAME=f'rowan-SE-{args.part[3:]}-{seed}'
if args.part.startswith('n-'):NAME=f'rowan-N-{args.part[2:]}-{seed}'
record_path=OUT/f'{NAME}.json'
if record_path.exists():raise RuntimeError('Existing run: inspect prompt_id and result before retrying.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py');gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen);gen.API='http://127.0.0.1:8189'
src=OUT/{'bracer':'rowan-side-torso-control-754010.png','hair':'rowan-side-bracer-755001.png','cape':'rowan-side-hair-755002.png','shoulder':'rowan-side-cape-755003.png','ne-hair':'rowan-NE-756001.png','ne-cape':'rowan-NE-hair-756004.png','ne-heading':'rowan-NE-cape-756005.png','ne-nape':'rowan-NE-cape-756005.png','se-belt':'rowan-SE-757003.png','se-cape':'rowan-SE-belt-757004.png','n-shoulders':'rowan-back-masked-754012.png','ne-shoulder':'rowan-NE-nape-756007.png'}[args.part]
original=Image.open(src).convert('RGB');guide=original.copy();draw=ImageDraw.Draw(guide)
# Only a silhouette/material guide: remove the invented round metal ornament.
draw.polygon([(264,354),(286,347),(305,401),(288,409),(273,383)],fill='#704735',outline='#422f2c',width=2)
draw.line([(268,358),(285,398)],fill='#a1714d',width=3)
mask=Image.new('L',original.size,0);md=ImageDraw.Draw(mask)
md.polygon([(260,347),(290,340),(313,406),(291,418),(266,388)],fill=255)
if args.part=='hair':
 guide=original.copy();draw=ImageDraw.Draw(guide)
 draw.polygon([(184,215),(216,220),(244,223),(263,236),(271,247),(183,247)],fill='white')
 draw.polygon([(187,196),(208,207),(228,215),(250,218),(261,224),(240,229),(209,223),(195,216)],fill='#8e4d32')
 draw.line([(193,210),(210,218),(233,224),(254,224)],fill='#613a2c',width=2)
 mask=Image.new('L',original.size,0);md=ImageDraw.Draw(mask)
 md.polygon([(180,193),(224,202),(252,212),(267,229),(274,246),(186,247)],fill=255)
if args.part=='cape':
 guide=original.copy();draw=ImageDraw.Draw(guide)
 draw.polygon([(198,509),(220,504),(214,541),(200,579),(185,603),(191,575),(193,545)],fill='#287b73')
 draw.line([(218,510),(208,545),(196,577),(187,598)],fill='#205c5a',width=2)
 mask=Image.new('L',original.size,0);md=ImageDraw.Draw(mask)
 md.polygon([(190,502),(227,500),(225,548),(207,587),(190,611),(177,607),(184,566)],fill=255)
if args.part=='ne-hair':
 guide=original.copy();draw=ImageDraw.Draw(guide)
 draw.rectangle((155,75,336,246),fill='white')
 rear=Image.open(OUT/'rowan-back-masked-754012.png').convert('RGB')
 hair=rear.crop((158,81,344,239)).resize((155,158),Image.Resampling.LANCZOS)
 guide.paste(hair,(172,85))
 mask=Image.new('L',original.size,0);md=ImageDraw.Draw(mask)
 md.rectangle((153,73,338,246),fill=255)
if args.part=='ne-cape':
 # Widen only the actual teal cloth pixels about the near shoulder, keeping limbs intact.
 rgb=np.asarray(original).astype(int)
 cloth=(rgb[:,:,1]>rgb[:,:,0]*1.25)&(rgb[:,:,2]>rgb[:,:,0]*1.15)&(rgb[:,:,0]<140)
 cloth[:253]=False;cloth[610:]=False;cloth[:,311:]=False
 cloth_mask=Image.fromarray((cloth*255).astype('uint8')).filter(ImageFilter.MaxFilter(5))
 layer=original.convert('RGBA');layer.putalpha(cloth_mask)
 warped=layer.transform(original.size,Image.Transform.AFFINE,(1/1.45,0,311-311/1.45,0,1,0),Image.Resampling.BICUBIC)
 guide=original.copy();guide.paste('white',mask=cloth_mask);guide.paste(warped,mask=warped.getchannel('A'))
 mask=Image.fromarray(np.maximum(np.asarray(cloth_mask),np.asarray(warped.getchannel('A')))).filter(ImageFilter.MaxFilter(9))
if args.part=='ne-heading':
 guide=original.copy();draw=ImageDraw.Draw(guide)
 # Reconnect the neck and reveal the narrow far-facing cheek/ear on the right.
 draw.polygon([(267,226),(289,226),(289,249),(298,259),(276,265),(262,252)],fill='#ddb69c',outline='#614636')
 draw.polygon([(291,176),(311,181),(317,201),(322,208),(313,215),(313,228),(298,240),(285,230)],fill='#ebc4a7',outline='#694b38')
 draw.ellipse((288,200,302,221),fill='#d6a98b',outline='#7a4f38',width=2)
 draw.line([(292,207),(297,205),(297,215)],fill='#97694f',width=2)
 # Hair overlaps the rear edge of the ear; no front eye or frontal clasp is introduced.
 draw.polygon([(278,169),(297,179),(296,196),(290,210),(286,231),(272,239),(278,217)],fill='#975334',outline='#69402e')
 mask=Image.new('L',original.size,0);md=ImageDraw.Draw(mask)
 md.polygon([(272,162),(316,176),(330,205),(324,235),(304,248),(305,266),(270,271),(251,255),(258,230)],fill=255)
if args.part=='ne-nape':
 guide=original.copy();draw=ImageDraw.Draw(guide)
 draw.polygon([(252,238),(281,238),(286,249),(298,258),(275,261),(256,254)],fill='#dab399',outline='#74503d')
 draw.polygon([(306,197),(314,204),(316,215),(307,229),(301,229),(304,216)],fill='#e5ba9e',outline='#81553d')
 draw.line([(308,207),(311,211),(307,220)],fill='#ad785a',width=2)
 mask=Image.new('L',original.size,0);md=ImageDraw.Draw(mask)
 md.polygon([(249,235),(285,234),(291,248),(301,260),(275,265),(251,256)],fill=255)
 md.polygon([(303,193),(318,201),(320,216),(310,234),(298,233),(300,215)],fill=255)
if args.part=='shoulder':
 guide=original.copy();draw=ImageDraw.Draw(guide)
 # The front design shows bare shoulder above a teal upper-arm wrap, not a cap sleeve.
 draw.polygon([(252,257),(267,254),(281,261),(288,275),(288,290),(253,292),(244,280)],fill='#edcbb0',outline='#694c38')
 draw.polygon([(252,260),(264,260),(255,279),(253,287),(247,280)],fill='#d2aa90')
 draw.polygon([(241,282),(259,286),(289,278),(292,290),(268,300),(244,294)],fill='#27786b',outline='#284a40')
 draw.line([(247,286),(269,290),(286,285)],fill='#4a9480',width=2)
 mask=Image.new('L',original.size,0);md=ImageDraw.Draw(mask)
 md.polygon([(248,251),(270,249),(285,257),(295,277),(298,295),(267,306),(238,297),(237,278)],fill=255)
if args.part=='se-belt':
 guide=original.copy();draw=ImageDraw.Draw(guide)
 draw.polygon([(291,358),(306,358),(310,378),(292,384),(280,380)],fill='#e1e4da')
 draw.line([(288,380),(295,383),(307,381)],fill='#9ea99f',width=2)
 mask=Image.new('L',original.size,0);md=ImageDraw.Draw(mask)
 md.polygon([(290,356),(307,357),(314,378),(294,389),(279,383),(283,372)],fill=255)
if args.part=='se-cape':
 guide=original.copy();draw=ImageDraw.Draw(guide)
 draw.polygon([(174,404),(205,414),(210,442),(226,451),(220,480),(204,516),(190,550),(192,499),(174,463),(168,444)],fill='#21746b',outline='#25453f')
 draw.polygon([(194,423),(208,433),(209,459),(197,489),(194,522),(192,493),(182,463)],fill='#2b887a')
 draw.line([(214,459),(206,491),(195,529)],fill='#1b504c',width=3)
 mask=Image.new('L',original.size,0);md=ImageDraw.Draw(mask)
 md.polygon([(168,398),(190,405),(212,412),(211,442),(229,451),(231,473),(211,523),(194,558),(183,553),(185,500),(165,462),(160,446)],fill=255)
if args.part=='n-shoulders':
 # Preserve the central nape attachment; expose the rear shoulder caps above the wrap.
 guide=original.copy();draw=ImageDraw.Draw(guide)
 draw.polygon([(194,272),(201,259),(218,250),(231,249),(229,272),(220,289),(188,300)],fill='#e7c2a7',outline='#70513e')
 draw.polygon([(282,249),(300,251),(316,261),(324,278),(330,300),(296,291),(284,274)],fill='#e7c2a7',outline='#70513e')
 draw.polygon([(188,292),(221,281),(236,273),(243,280),(225,299),(189,312),(182,306)],fill='#287b73',outline='#235149')
 draw.polygon([(273,276),(291,284),(326,292),(333,306),(309,310),(284,297),(270,285)],fill='#287b73',outline='#235149')
 mask=Image.new('L',original.size,0);md=ImageDraw.Draw(mask)
 md.polygon([(190,267),(198,254),(219,245),(234,246),(239,267),(246,280),(229,305),(185,316),(177,306)],fill=255)
 md.polygon([(278,244),(303,246),(323,258),(330,279),(338,307),(311,316),(280,301),(266,284),(276,267)],fill=255)
if args.part=='ne-shoulder':
 guide=original.copy();draw=ImageDraw.Draw(guide)
 # Remove the white collar strip and lower the near-shoulder cloth band.
 draw.polygon([(244,253),(269,258),(280,261),(276,271),(246,264)],fill='#287b73')
 draw.polygon([(279,257),(297,258),(311,268),(320,284),(325,302),(309,304),(296,292),(283,280)],fill='#e5bea2',outline='#73503b')
 draw.polygon([(278,277),(296,288),(318,285),(323,296),(307,310),(284,301),(272,291)],fill='#287b73',outline='#244d47')
 draw.line([(282,286),(300,300),(317,293)],fill='#439487',width=2)
 mask=Image.new('L',original.size,0);md=ImageDraw.Draw(mask)
 md.polygon([(242,249),(273,254),(298,252),(315,264),(325,282),(330,305),(309,317),(280,307),(267,289),(242,267)],fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(2))
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
 im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
positive='side view of an anime female swordswoman, simple plain brown leather wrist bracer, smooth leather surface, subtle stitched seam, short leather wrist guard, no decoration, clean colored outlines, soft anime cel shading, natural arm anatomy'
negative='metal, gold, ornament, medallion, jewel, bracelet, tattoo, extra hand, extra fingers, text, watermark, logo, photograph, 3d render'
if args.part=='hair':
 positive='strict side view of an anime girl facing right, smooth short auburn bob haircut ending at jaw level, neatly rounded bob hair tips, visible back of neck, warm copper brown hair, clean colored outline, anime cel shading'
 negative='long hair, shoulder length hair, ponytail, hair ribbon, extra head, extra face, text, watermark, logo, photograph'
if args.part=='cape':
 positive='side view of a teal green cloth cape hanging behind an anime swordswoman, long tapered cape tail draping naturally to mid calf, smooth cloth folds, clean colored outlines, soft anime cel shading, white background'
 negative='new objects, limbs, shoes, weapons, staff, metal, gold, symbols, text, watermark, logo, photograph'
if args.part=='ne-hair':
 positive='rear three quarter view of one anime adventurer facing away to the right, short auburn rounded bob haircut, smooth rounded crown, loose copper brown bob hair ending at nape, fine dark outlines, soft anime cel shading'
 negative='hair bun, topknot, tied hair, ponytail, braid, hairpin, hair ornament, long hair, extra head, visible face, eyes, text, signature, photograph'
if args.part=='ne-cape':
 positive='rear three quarter view of a female adventurer, wide teal cloth cape draped across the back and rear shoulders, flowing cloth folds, pointed cape tails reaching mid calf, plain teal fabric, clean dark colored outlines, soft anime cel shading'
 negative='front view, clasp, embroidery, brown patches, torn fabric, symbols, armor, weapons, new limbs, text, watermark, photograph'
if args.part=='ne-heading':
 positive='back three quarter view of an anime girl facing away to the right, nape of neck, small right ear and narrow edge of cheek, rounded short auburn bob haircut, head aligned with shoulders, clean colored outlines, soft anime cel shading'
 negative='front view, looking at viewer, visible eyes, hair bun, ponytail, braid, jewelry, extra head, extra ear, text, watermark, photograph'
if args.part=='ne-nape':
 positive='back of neck and small right ear behind short auburn bob hair, rear three quarter view, face hidden facing away, natural skin shading, clean anime cel shading'
 negative='face, eyes, mouth, nose, front view, looking back, white collar, scarf, hair bun, ponytail, jewelry, extra ear, text'
if args.part=='shoulder':
 positive='strict right side view of an anime female adventurer, exposed rounded shoulder, bare shoulder above a narrow teal cloth band around upper arm, off shoulder white tunic and teal cape hanging behind, smooth natural skin, clean colored outlines, soft cel shading'
 negative='sleeve, shoulder armor, shoulder pad, pauldrons, metal, tattoo, jewelry, extra arm, text, watermark, photograph'
if args.part=='se-belt':
 positive='plain white tunic fabric immediately below a simple brown leather waist belt, subtle cloth folds, clean anime cel shading, smooth uninterrupted white fabric'
 negative='hook, key, keychain, pendant, ring, chain, buckle below waist, metal object, hanging accessory, text, watermark'
if args.part=='se-cape':
 positive='intact teal cloth cape behind a female adventurer, clean tapered cape edge and long pointed tail, smooth teal fabric with broad folds, dark colored outline, anime cel shading, white background'
 negative='torn cape, holes, ragged edge, brown strap, sword, scabbard, weapon, staff, metal, speckles, pattern, text, watermark'
if args.part=='n-shoulders':
 positive='strict rear view of an anime female adventurer, bare left and right shoulder caps, exposed skin above an off shoulder teal cloth wrap, teal cape covers the middle of the back, smooth natural skin, simple cloth folds, clean colored outline, soft anime cel shading'
 negative='front view, face, eyes, breast, clasp, buckle, shoulder armor, sleeves, tattoo, jewelry, extra limbs, text, watermark'
if args.part=='ne-shoulder':
 positive='rear three quarter view of an anime female adventurer facing away right, bare right shoulder cap, exposed skin above a low teal cloth band around upper arm, off shoulder cape covering back, plain teal cloth, natural skin, clean colored outlines, soft anime cel shading'
 negative='white collar, scarf, shoulder armor, sleeves, front view, eyes, clasp, jewelry, tattoo, extra arm, text, watermark'
g=gen.graph(seed,positive,negative)
g['5']={'class_type':'LoadImage','inputs':{'image':f'{NAME}-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':f'{NAME}-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':f'{NAME}-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise={'ne-nape':.24,'shoulder':.32,'se-belt':.32,'se-cape':.36,'n-shoulders':.30,'ne-shoulder':.30}.get(args.part,.42),steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
r={'source':str(src.relative_to(ROOT)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'mask_sha256':hashlib.sha256((OUT/f'{NAME}-mask.png').read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending'}
def save():record_path.write_text(json.dumps(r,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'mosslight-local-repair'})['prompt_id'];r.update(state='queued',prompt_id=key);save();print('QUEUED',key,flush=True)
start=time.monotonic()
while time.monotonic()-start<900:
 history=gen.request('/history/'+key)
 if key in history:
  h=history[key];r.update(state=h['status']['status_str'],history=h,seconds=time.monotonic()-start)
  if r['state']!='success':save();raise RuntimeError(record_path)
  f=h['outputs']['8']['images'][0];target=OUT/f'{NAME}.png';shutil.copy2(BASE/'output'/f['subfolder']/f['filename'],target)
  result=np.asarray(Image.open(target).convert('RGB'));outside=np.asarray(mask)==0
  r['outside_mask_max_difference']=int(np.abs(result.astype(int)-np.asarray(original).astype(int))[outside].max())
  r['changed_pixels']=int(np.any(result!=np.asarray(original),axis=2).sum())
  r['output_sha256']=hashlib.sha256(target.read_bytes()).hexdigest();save()
  assert r['outside_mask_max_difference']==0
  assert r['changed_pixels']>0
  print('MASKED_EDIT_OK',r['changed_pixels'],'changed pixels; outside mask unchanged',flush=True);break
 time.sleep(2)
else:raise TimeoutError(key)
