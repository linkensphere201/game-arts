"""Remove unsupported profile costume details using a bounded local redraw."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided';BASE=ROOT/'.local/reference-comfy'
parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=['cuffs','collar','hair','trim','proportion','ponytail','pouch','finish','hair-style','hair-locks'],default='cuffs');args=parser.parse_args()
seed={'cuffs':774010,'collar':774011,'hair':774012,'trim':774014,'proportion':774015,'ponytail':774016,'pouch':774020,'finish':774021,'hair-style':774023,'hair-locks':774025}[args.mode]
NAME=f'mira-details-{seed}';record_path=OUT/(NAME+'.json')
if record_path.exists():raise RuntimeError('Existing trial: inspect prompt before retry.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
    gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Occupied queue')
source=OUT/{'cuffs':'mira-profile-774008.png','collar':'mira-details-774010.png','hair':'mira-details-774011.png','trim':'mira-details-774012.png','proportion':'mira-details-774014.png','ponytail':'mira-details-774015.png','pouch':'mira-details-774016.png','finish':'mira-details-774020.png','hair-style':'mira-details-774021.png','hair-locks':'mira-details-774021.png'}[args.mode];original=Image.open(source).convert('RGB')
guide=original.copy();d=ImageDraw.Draw(guide);mask=Image.new('L',original.size);md=ImageDraw.Draw(mask)
if args.mode=='cuffs':
    # Identify neutral light sock pixels only; never paint the white backdrop.
    rgb=np.asarray(original).astype(int)
    region=np.zeros(rgb.shape[:2],dtype=bool);region[501:522,239:317]=True
    neutral=(rgb.max(2)-rgb.min(2)<23)&(rgb.min(2)>160)&(rgb.max(2)<245)
    selected=region&neutral
    assert 50<int(selected.sum())<1000
    paint=np.asarray(guide).copy();paint[selected]=[210,177,151]
    guide=Image.fromarray(paint);mask=Image.fromarray((selected*255).astype('uint8'))
    mask=mask.filter(ImageFilter.GaussianBlur(0))
elif args.mode=='collar':
    # Recolor only the blouse collar; leave skin, sleeve shading and apron intact.
    region=[(251,228),(266,230),(282,235),(290,244),(281,255),(256,253),(243,250)]
    md.polygon(region,fill=255)
    rgb=np.asarray(original).astype(float);paint=np.asarray(guide).copy()
    selected=np.asarray(mask)>0;light=rgb.mean(2)/220
    for channel,value in enumerate((132,148,117)):
        paint[:,:,channel][selected]=np.clip(light[selected]*value,0,255).astype('uint8')
    guide=Image.fromarray(paint)
elif args.mode=='hair':
    # Borrow shaded hair texture rather than a flat polygon over the ear.
    patch=original.crop((239,148,265,184)).resize((25,43),Image.Resampling.LANCZOS)
    guide.paste(patch,(258,167))
    md.polygon([(260,168),(275,166),(283,177),(281,193),(273,210),(261,206),(255,190)],fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(1))
elif args.mode=='trim':
    # Remove the invented neck bow outside the blouse silhouette.
    region=[(284,237),(298,234),(310,243),(310,273),(297,271),(283,250)]
    md.polygon(region,fill=255);d.polygon(region,fill='white')
    d.polygon([(283,240),(291,248),(298,266),(307,278),(296,282),(284,262),(280,248)],fill='#829173',outline='#48513c',width=2)
    # Plain leather boot opening: replace bright cuff bands and ornamental buckle.
    for region in [[(241,506),(276,507),(278,522),(247,523)],[(280,505),(314,507),(314,520),(281,520)]]:
        md.polygon(region,fill=255);d.polygon(region,fill='#755740')
    md.rectangle((296,518,311,531),fill=255)
    guide.paste(original.crop((284,526,297,540)).resize((16,14)),(296,518))
    mask=mask.filter(ImageFilter.GaussianBlur(.5))
elif args.mode=='proportion':
    # Broaden the head toward the front design, fixing the nose x coordinate.
    # Smoothly return to the existing neck/ponytail below the jaw.
    from scipy.ndimage import map_coordinates
    yy,xx=np.indices((original.height,original.width),dtype=float)
    blend=np.clip((255-yy)/35,0,1)
    scale=1+.22*blend
    sample_x=330+(xx-330)/scale
    arr=np.asarray(original)
    warped=np.stack([map_coordinates(arr[:,:,c],[yy,sample_x],order=1,mode='constant',cval=255) for c in range(3)],axis=2)
    guide=Image.fromarray(warped.astype('uint8'))
    md.rectangle((150,70,342,253),fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(1))
elif args.mode=='ponytail':
    # Taper the mid-ponytail continuously, retaining the existing shaded strands.
    from scipy.ndimage import map_coordinates
    yy,xx=np.indices((original.height,original.width),dtype=float)
    scale=1-.20*np.exp(-((yy-224)/30)**2)
    sample_x=np.where(xx<240,240+(xx-240)/scale,xx)
    arr=np.asarray(original)
    warped=np.stack([map_coordinates(arr[:,:,c],[yy,sample_x],order=1,mode='constant',cval=255) for c in range(3)],axis=2)
    guide=Image.fromarray(warped.astype('uint8'))
    md.polygon([(177,177),(231,177),(241,209),(241,262),(226,284),(181,280),(170,224)],fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(2))
elif args.mode=='pouch':
    # Rebuild the layering: dress, belt/pouch, then a hanging forearm and hand.
    # The old image has a hand in a pocket and a belt across the arm.
    md.polygon([(248,322),(286,322),(287,341),(315,357),(317,418),(218,418),(218,357),(248,357)],fill=255)
    d.polygon([(218,357),(237,357),(237,418),(218,418)],fill='white')
    cloth=original.crop((289,421,310,466)).resize((70,62),Image.Resampling.LANCZOS)
    guide.paste(cloth,(235,357));d=ImageDraw.Draw(guide)
    d.rounded_rectangle((271,378,310,414),4,fill='#93613f',outline='#433627',width=2)
    d.polygon([(272,378),(309,378),(309,389),(272,388)],fill='#ab7951',outline='#433627',width=2)
    for points in [[(294,379),(284,365),(288,357),(297,369)],[(297,378),(301,360),(311,357),(309,371)]]:
        d.polygon(points,fill='#788d56',outline='#435338',width=2)
    # A relaxed fist points down, in front of the pouch rather than through it.
    d.polygon([(254,321),(279,321),(282,358),(277,376),(283,386),(282,398),(275,405),(268,403),(262,393),(261,382),(264,368),(255,353)],fill='#dcb79c',outline='#735647',width=2)
    d.polygon([(254,321),(259,321),(267,357),(271,377),(267,391),(274,402),(268,399),(263,389),(265,372),(257,351)],fill='#bd977e')
    d.line((277,385,275,396),fill='#a88069',width=1)
    mask=mask.filter(ImageFilter.GaussianBlur(1))
elif args.mode=='finish':
    # Blend the internal arm seam with the surrounding skin shading, not contours.
    arr=np.asarray(original).astype(float);paint=arr.copy()
    for y in range(315,333):
        t=(y-315)/17
        paint[y,256:278]=(1-t)*arr[314,256:278]+t*arr[333,256:278]
    md.rectangle((256,315,277,332),fill=255)
    pouch_mask=Image.new('L',original.size)
    ImageDraw.Draw(pouch_mask).polygon([(282,378),(308,378),(309,412),(277,412),(277,402),(285,397)],fill=255)
    selected=np.asarray(pouch_mask)>0
    paint[selected]=np.clip(arr[selected]*np.array([1.10,.83,.70]),0,255)
    md.bitmap((0,0),pouch_mask,fill=255)
    guide=Image.fromarray(paint.astype('uint8'));mask=mask.filter(ImageFilter.GaussianBlur(.5))
elif args.mode=='hair-style':
    # Simplify only hair masses, retaining facial pixels and the outer silhouette.
    for region in [[(223,133),(243,126),(279,128),(307,139),(324,154),(324,174),(316,187),(309,170),(292,159),(279,188),(273,207),(251,205),(237,185),(223,166)],[(213,160),(233,163),(231,195),(238,230),(238,264),(229,284),(210,297),(199,300),(207,281),(213,265),(201,244),(197,216),(202,183)]]:
        md.polygon(region,fill=255)
    softened=np.asarray(original.filter(ImageFilter.MedianFilter(5)))
    light=softened.mean(2)
    ramp=np.array([[77,51,35],[119,76,48],[154,99,61],[186,132,85]],dtype='uint8')
    bands=np.digitize(light,[65,100,137])
    painted=np.asarray(original).copy();selected=np.asarray(mask)>0
    painted[selected]=(.65*ramp[bands[selected]]+.35*softened[selected]).astype('uint8')
    guide=Image.fromarray(painted);mask=mask.filter(ImageFilter.GaussianBlur(.7))
else:
    # Continuous shadow shapes follow lock direction rather than brightness bins.
    regions=[[(223,133),(243,126),(279,128),(307,139),(324,154),(324,174),(316,187),(309,170),(292,159),(279,188),(273,207),(251,205),(237,185),(223,166)],[(213,160),(233,163),(231,195),(238,230),(238,264),(229,284),(210,297),(199,300),(207,281),(213,265),(201,244),(197,216),(202,183)]]
    layer=Image.new('RGB',original.size,'#8d5c3c');ld=ImageDraw.Draw(layer)
    def curve(p0,p1,p2,p3):
        return [tuple((1-t)**3*np.array(p0)+3*(1-t)**2*t*np.array(p1)+3*(1-t)*t*t*np.array(p2)+t**3*np.array(p3)) for t in np.linspace(0,1,24)]
    shadow=curve((234,150),(236,166),(251,186),(267,201))+curve((267,201),(248,207),(234,178),(230,162))
    ld.polygon(shadow,fill='#694731')
    highlight=curve((246,135),(270,130),(302,140),(316,153))+curve((316,153),(287,143),(267,146),(246,135))
    ld.polygon(highlight,fill='#a8734c')
    ld.polygon([(226,166),(221,196),(226,222),(234,243),(231,267),(218,288),(205,297),(216,271),(214,247),(208,223),(212,190)],fill='#63432f')
    ld.polygon([(213,173),(209,200),(208,221),(216,245),(220,259),(220,275),(225,263),(223,241),(215,216),(216,190)],fill='#ab7751')
    for region in regions:md.polygon(region,fill=255)
    # Retain edge shading to avoid a visible join at the selected region boundary.
    blend=mask.filter(ImageFilter.GaussianBlur(2))
    guide=Image.composite(layer,original,blend)
    mask=blend
for suffix,im in [('source',original),('guide',guide),('mask',mask.convert('RGB'))]:
    im.save(OUT/f'{NAME}-{suffix}.png');im.save(BASE/'input'/f'{NAME}-{suffix}.png')
g=gen.graph(seed,'right facing anime wolf beastfolk apothecary, copper brown hair side lock covering human ear, sage green standing blouse collar, bare ankle skin above brown leather boots, consistent clean cel shading','human ear, white collar, neck bow, socks, jewelry, text, photo')
if args.mode=='pouch':
    g=gen.graph(seed,'relaxed female forearm and small closed hand hanging naturally in front of a brown leather belt pouch, green herb leaves above pouch behind hand, dark green skirt, correct hand anatomy, clean anime cel shading','hand in pocket, belt over arm, handbag, lock, metal buckle, extra fingers, extra hand, white patch, text')
if args.mode=='finish':
    g=gen.graph(seed,'smooth continuous bare forearm skin, warm brown leather herb pouch, clean anime cel shading','arm band, bracelet, seam across skin, green bag, extra fingers, text')
if args.mode in ('hair-style','hair-locks'):
    g=gen.graph(seed,'copper brown ponytail hair, broad simple cel shaded locks, clean anime game character illustration, large warm brown shadow shapes, limited hair detail','fine hair strands, realistic hair, glossy highlights, grey hair, text')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.42 if args.mode in ('hair-style','hair-locks') else .36 if args.mode=='pouch' else (.18 if args.mode=='proportion' else (.30 if args.mode=='hair' else .25)),steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared','review':'pending','mode':args.mode}
def save():record_path.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'mira-details-repair'})['prompt_id']
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
        assert outside==0;print('MIRA_DETAILS_REPAIR_OK',flush=True);break
    time.sleep(2)
else:raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
