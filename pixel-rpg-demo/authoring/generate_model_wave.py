"""Resumable bounded local generation, with per-asset prompt/provenance and no implicit acceptance."""
from pathlib import Path
import argparse,importlib.util,json,time,shutil,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
p=argparse.ArgumentParser();p.add_argument('--ids');p.add_argument('--attempt',type=int,default=1);p.add_argument('--reference',action='store_true');args=p.parse_args()
manifest=json.loads(Path(__file__).with_name('model-wave-01.json').read_text())
OUT=ROOT/'production/pixel-rpg/model-wave-01';(OUT/'originals').mkdir(parents=True,exist_ok=True);(OUT/'runs').mkdir(exist_ok=True)
common='(hand drawn 2D anime illustration:1.3), (clean dark colored outlines:1.3), (simple cel shaded matte surfaces:1.3), clean confident colored lineart, beautiful anime cel shading, deliberate material highlights, cohesive Japanese fantasy RPG illustration, warm upper left lighting, centered, isolated on plain white background, complete silhouette inside the frame, no scenery, no text'
negative='photograph, photorealistic, 3d render, blurry, muddy, text, watermark, signature, cropped, cut off, out of frame, character sheet, collage, panels, multiple views, multiple objects, duplicate, background scenery, floor plane, landscape, modern technology, decorative background, circular background, border, picture frame, vignette, logo'
selected=set(args.ids.split(',')) if args.ids else None
for asset in manifest['assets']:
 if selected and asset['id'] not in selected:continue
 if (OUT/'pause.request').exists():print('PAUSED at asset boundary',flush=True);break
 ident=asset['id'];record_path=OUT/'runs'/f'{ident}-a{args.attempt}.json'
 if record_path.exists():
  old=json.loads(record_path.read_text())
  if old.get('state')=='success':print('SKIP completed',ident,flush=True);continue
  if old.get('prompt_id'):raise RuntimeError(f'Inspect existing incomplete prompt before retry: {record_path}')
 cat=asset['category']
 if cat=='character':
  positive='(single character:1.4), (full body:1.4), (chibi:1.35), one original '+asset['description']+', cute expressive anime face, approximately three and a half to four heads tall, standing relaxed, arms separated from torso, front three quarter view, visible feet, '+common
  neg=negative+', extra limbs, malformed hands, missing feet, nudity, underwear, cleavage, sexy, long legs, tiny head'
 else:
  positive='('+asset['description']+':1.35), fantasy illustration, anime art style, hand drawn dark linework, cel shading, (plain white background:1.3), isolated object, warm upper left light, complete object visible'
  if cat=='building':positive+=', three quarter elevated view, teal slate roof, warm cream plaster'
  neg='photograph, photorealistic, 3d render, logo, symbol, emblem design, vector logo, flat geometric shapes, abstract, diagram, infographic, border, circle frame, text, watermark, signature, cropped, person, people, hands, character, scenery'
  if ident=='prop_chest':positive='(closed wooden treasure chest with closed lid:1.5), '+positive;neg+=', open lid, open chest, jewels'
 seed=asset['seed']+(args.attempt-1)*10000;g=m.graph(seed,positive,neg)
 g['5']['inputs'].update(width=asset['size'][0],height=asset['size'][1]);g['6']['inputs'].update(steps=30,cfg=7)
 if args.reference and cat=='character':
  source=ROOT/'production/pixel-rpg/candidates/mosslight_chibi_731212_00001_.png'
  shutil.copy2(source,ROOT/'.local/comfy/ComfyUI_windows_portable/ComfyUI/input/mosslight_style_master.png')
  g['5']={'class_type':'LoadImage','inputs':{'image':'mosslight_style_master.png'}}
  g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
  g['6']['inputs'].update(latent_image=['9',0],denoise=.68,cfg=7.5)
 g['8']['inputs']['filename_prefix']=f"mosslight_wave01_{ident}_a{args.attempt}"
 record={'id':ident,'attempt':args.attempt,'state':'prepared','asset':asset,'graph':g,'review':'pending','style_reference':manifest['style_contract']['reference'] if args.reference and cat=='character' else None}
 record_path.write_text(json.dumps(record,indent=2),encoding='utf-8')
 queued=m.request('/prompt',{'prompt':g,'client_id':'mosslight-wave01'});key=queued['prompt_id'];record.update(prompt_id=key,state='queued');record_path.write_text(json.dumps(record,indent=2),encoding='utf-8')
 print('QUEUED',ident,key,flush=True);start=time.monotonic()
 while time.monotonic()-start<900:
  hist=m.request('/history/'+key)
  if key in hist:
   result=hist[key];record.update(history=result,state=result['status']['status_str'],seconds=time.monotonic()-start)
   if record['state']=='success':
    files=[]
    for im in result['outputs']['8']['images']:
     src=ROOT/'.local/comfy/ComfyUI_windows_portable/ComfyUI/output'/im['subfolder']/im['filename'];dst=OUT/'originals'/f'{ident}-a{args.attempt}.png';shutil.copy2(src,dst);files.append({'path':str(dst.relative_to(ROOT)),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
    record['outputs']=files
   record_path.write_text(json.dumps(record,indent=2),encoding='utf-8')
   if record['state']!='success':raise RuntimeError(record_path)
   print('COMPLETE',ident,round(record['seconds'],2),flush=True);break
  time.sleep(2)
 else:raise TimeoutError(key)
