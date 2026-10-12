"""Bounded local DreamShaper ground-material study with retained workflow/history."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,shutil,time,random
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/ground';OUT.mkdir(parents=True,exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('--guided',action='store_true');parser.add_argument('--grass',action='store_true');parser.add_argument('--wood',action='store_true');parser.add_argument('--wall',action='store_true');args=parser.parse_args()
seed=(759004 if args.guided else 759003) if args.grass else (759002 if args.guided else 759001)
if args.wood:seed=765003
if args.wall:seed=765004
name=f'{"timber-wall" if args.wall else "wood-floor" if args.wood else "meadow-grass" if args.grass else "warm-paving"}-{seed}';record=OUT/(name+'.json')
if record.exists():raise RuntimeError('Existing run; inspect recorded prompt/history before retrying')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py');gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
gen.API='http://127.0.0.1:8189'
q=gen.request('/queue');assert not q['queue_running'] and not q['queue_pending']
g=gen.graph(seed,'seamless repeating texture of worn sandstone paving slabs, directly overhead orthographic view, entire image filled with irregular rectangular warm beige stone tiles and thin muted brown joints, small subtle cool teal moss in a few cracks, Japanese RPG hand painted background art, restrained cel shading, broad flat stone faces, fine colored outlines, uniform diffuse light, consistent tile scale','perspective, horizon, building, person, object, grass field, deep shadow, glossy, photorealistic, 3d render, text, watermark, border, vignette, white background')
if args.guided and not args.grass:
 guide=Image.new('RGB',(512,512),'#847e69');draw=ImageDraw.Draw(guide)
 colors=['#bab096','#b2aa91','#c3b79b','#ada78f']
 for row in range(8):
  for col in range(-1,5):
   x=col*128+(64 if row%2 else 0);y=row*64
   draw.rounded_rectangle((x+3,y+3,x+125,y+61),radius=5,fill=colors[(row+col)%4],outline='#8d8774',width=2)
   draw.line((x+10,y+8,x+116,y+8),fill='#cec3a6',width=2)
 guide.save(OUT/(name+'-guide.png'));guide.save(ROOT/'.local/reference-comfy/input'/(name+'-guide.png'))
 g['5']={'class_type':'LoadImage','inputs':{'image':name+'-guide.png'}}
 g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
 g['6']['inputs'].update(latent_image=['9',0],denoise=.48,cfg=6)
 g['4']['inputs']['text']+=', diagonal lines, triangular tiles, polished ceramic, bevel, realistic stone grain'
if args.grass:
 g['3']['inputs']['text']='seamless tileable game ground texture, direct overhead orthographic view, flat short meadow grass, muted sage green and olive green, tiny sparse blade clusters, broad calm green ground areas, hand painted Japanese RPG environment, simplified cel shading, low contrast, evenly lit, entire image covered in grass, no focal object'
 g['4']['inputs']['text']='perspective, horizon, landscape, sky, tree, bush, flowers, tall grass, large leaves, photo, photorealistic, glossy, 3d render, high contrast, text, watermark, border, vignette, dirt path'
if args.grass and args.guided:
 guide=Image.new('RGB',(512,512),'#7c926c');draw=ImageDraw.Draw(guide);rng=random.Random(seed)
 for i in range(190):
  x=rng.randrange(512);y=rng.randrange(512)
  color=rng.choice(['#879a73','#738a63','#80956c','#6e865f'])
  draw.polygon([(x-6,y),(x-8,y-10),(x-2,y-5),(x+1,y-13),(x+3,y-4),(x+7,y-9),(x+5,y)],fill=color)
 guide.save(OUT/(name+'-guide.png'));guide.save(ROOT/'.local/reference-comfy/input'/(name+'-guide.png'))
 g['5']={'class_type':'LoadImage','inputs':{'image':name+'-guide.png'}}
 g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
 g['6']['inputs'].update(latent_image=['9',0],denoise=.48,cfg=6)
 g['4']['inputs']['text']+=', circle, ring, symbol, medallion, logo, stone, architecture, geometric pattern'
if args.wood:
 if args.grass:raise ValueError('Choose wood or grass, not both')
 guide=Image.new('RGB',(512,512),'#76593d');draw=ImageDraw.Draw(guide)
 for row in range(8):
  for col in range(-1,3):
   x=col*256+(128 if row%2 else 0);y=row*64
   draw.rectangle((x+2,y+2,x+254,y+62),fill=['#a18a62','#ab9169','#99835f','#a68c65'][row%4],outline='#806644',width=2)
   draw.line((x+18,y+19,x+205,y+19),fill='#b19a72',width=2)
   draw.line((x+50,y+43,x+229,y+43),fill='#8f7650',width=2)
 guide.save(OUT/(name+'-guide.png'));guide.save(ROOT/'.local/reference-comfy/input'/(name+'-guide.png'))
 g['3']['inputs']['text']='seamless repeating wooden floor texture, direct overhead orthographic view, entire image filled with long horizontal staggered wooden planks, muted warm honey brown, subtle wood grain, thin dark joints, matte hand painted Japanese RPG game environment, broad calm color areas, even diffuse light'
 g['4']['inputs']['text']='perspective, horizon, room, furniture, frame, border, object, emblem, circle, parquet, herringbone, diagonal, glossy, photo, photorealistic, text, watermark, vignette'
 g['5']={'class_type':'LoadImage','inputs':{'image':name+'-guide.png'}}
 g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
 g['6']['inputs'].update(latent_image=['9',0],denoise=.48,cfg=6)
if args.wall:
 if args.grass or args.wood:raise ValueError('Wall is a separate material choice')
 guide=Image.new('RGB',(512,256),'#d3c5a2');draw=ImageDraw.Draw(guide)
 draw.rectangle((0,0,511,27),fill='#927147',outline='#5d4d35',width=4)
 draw.rectangle((0,228,511,255),fill='#886942',outline='#58482f',width=4)
 for x in [0,256,512]:
  draw.rectangle((x-12,28,x+12,227),fill='#9c7950',outline='#655036',width=4)
 draw.line((0,222,511,222),fill='#b0a17f',width=4)
 guide.save(OUT/(name+'-guide.png'));guide.save(ROOT/'.local/reference-comfy/input'/(name+'-guide.png'))
 g['3']['inputs']['text']='straight interior wall panel, flat front elevation, cream plaster infill between warm brown timber posts, horizontal wooden top beam and wooden skirting board, restrained hand painted Japanese RPG environment texture, broad clean color areas, matte cel shading, evenly lit, entire image filled by wall, horizontally repeating module'
 g['4']['inputs']['text']='perspective, room, furniture, door, window, floor, ceiling, picture frame, ornament, emblem, text, watermark, photo, photorealistic, bricks, stone blocks, weathered ruins'
 g['5']={'class_type':'LoadImage','inputs':{'image':name+'-guide.png'}}
 g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
 g['6']['inputs'].update(latent_image=['9',0],denoise=.45,cfg=6)
g['8']['inputs']['filename_prefix']=name
r={'graph':g,'state':'prepared','review':'pending','model':'DreamShaper_8_pruned.safetensors'}
def save():record.write_text(json.dumps(r,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'mosslight-ground-study'})['prompt_id'];r.update(state='queued',prompt_id=key);save();print('QUEUED',key,flush=True)
start=time.monotonic()
while time.monotonic()-start<900:
 h=gen.request('/history/'+key)
 if key in h:
  result=h[key];r.update(state=result['status']['status_str'],history=result);save();assert r['state']=='success'
  f=result['outputs']['8']['images'][0];target=OUT/(name+'.png');shutil.copy2(ROOT/'.local/reference-comfy/output'/f['subfolder']/f['filename'],target)
  r['sha256']=hashlib.sha256(target.read_bytes()).hexdigest();save();print('GROUND_SOURCE_GENERATED',target,flush=True);break
 time.sleep(2)
else:raise TimeoutError(key)
