"""Compare the existing 16 character briefs using local Animagine XL 4.0 Opt."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, time, urllib.request, urllib.parse, threading
from PIL import Image, ImageOps, ImageDraw
ROOT=Path(__file__).resolve().parents[2]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
m=module('gen',ROOT/'tools/generate-character.py')
mem=module('mem',ROOT/'tools/run-comfy.py')
p=argparse.ArgumentParser();p.add_argument('--limit',type=int,default=16);args=p.parse_args()
OUT=ROOT/'production/pixel-rpg/animagine-comparison';OUT.mkdir(parents=True,exist_ok=True)
model=ROOT/'.local/models/animagine-xl-4.0-opt.safetensors'
meta=json.loads(Path(str(model)+'.source.json').read_text(encoding='utf-8-sig'))
if not model.exists() or model.stat().st_size!=meta['bytes']:raise RuntimeError('Model download incomplete')
print('CHECKSUM',flush=True)
with model.open('rb') as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
if actual!=meta['sha256']:raise RuntimeError('Model checksum mismatch')
for port in (8189,):
 m.API=f'http://127.0.0.1:{port}';q=m.request('/queue')
 if q.get('queue_running') or q.get('queue_pending'):raise RuntimeError('Queue occupied')
 req=urllib.request.Request(m.API+'/free',data=json.dumps({'unload_models':True,'free_memory':True}).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=30) as r:r.read()
time.sleep(3)
if not mem.check_memory():raise RuntimeError('Insufficient commit headroom; do not queue generation')
m.API='http://127.0.0.1:8189'
info=m.request('/object_info/CheckpointLoaderSimple')
assert model.name in info['CheckpointLoaderSimple']['input']['required']['ckpt_name'][0]
manifest=json.loads((ROOT/'pixel-rpg-demo/authoring/model-wave-01.json').read_text())
assets=[a for a in manifest['assets'] if a['category']=='character'][:args.limit]
for asset in assets:
 ident=asset['id'];rp=OUT/(ident+'.json');target=OUT/(ident+'.png')
 if rp.exists():
  old=json.loads(rp.read_text())
  if old.get('state')=='success' and target.exists():continue
  raise RuntimeError(f'Inspect prior trial: {rp}')
 prompt='solo, adult character, full body, chibi, '+asset['description']+', standing, front three-quarter view, simple background, white background, clean colored outlines, anime cel shading, matte surfaces, teal cream brass brown palette, complete silhouette, visible feet, masterpiece, high score, great score, absurdres'
 negative='lowres, bad anatomy, bad hands, text, error, missing fingers, extra digits, fewer digits, cropped, worst quality, low quality, low score, bad score, signature, watermark, blurry, photorealistic, 3d render, nude, underwear, child, multiple people, collage, scenery, decorative background'
 g=m.graph(asset['seed'],prompt,negative);g['1']['inputs']['ckpt_name']=model.name
 g['5']['inputs'].update(width=832,height=1216)
 g['6']['inputs'].update(steps=28,cfg=5,sampler_name='euler_ancestral',scheduler='normal')
 g['8']['inputs']['filename_prefix']='animagine_compare_'+ident
 rec={'task':'M5.2.6.2','asset':asset,'model':meta,'graph':g,'state':'prepared','comparison':'Same 16 briefs and seeds; model-specific prompt tags, sampler and native resolution. Not a controlled checkpoint-only benchmark. No reference image or adapters.'}
 def save():rp.write_text(json.dumps(rec,indent=2),encoding='utf-8')
 save();key=m.request('/prompt',{'prompt':g,'client_id':'animagine-comparison'})['prompt_id'];rec.update(prompt_id=key,state='queued');save()
 print('QUEUED',ident,key,flush=True);start=time.monotonic();stop=threading.Event();samples=[]
 monitor=threading.Thread(target=m.sample_gpu,args=(stop,samples),daemon=True);monitor.start()
 try:
  while time.monotonic()-start<1800:
   history=m.request('/history/'+key)
   if key in history:
    result=history[key];rec.update(state=result['status']['status_str'],history=result,elapsed_seconds=time.monotonic()-start,peak_device_vram_mib=max(samples) if samples else None);save()
    if rec['state']!='success':raise RuntimeError(rp)
    im=result['outputs']['8']['images'][0];url=m.API+'/view?'+urllib.parse.urlencode({k:im[k] for k in ('filename','subfolder','type')})
    with urllib.request.urlopen(url,timeout=60) as r:target.write_bytes(r.read())
    with Image.open(target) as check:assert check.size==(832,1216);check.verify()
    rec.update(output_sha256=hashlib.sha256(target.read_bytes()).hexdigest());save();print('COMPLETE',ident,round(rec['elapsed_seconds'],1),rec['peak_device_vram_mib'],flush=True);break
   time.sleep(2)
  else:raise TimeoutError(f'Inspect existing prompt {key}; no resubmission')
 finally:stop.set();monitor.join(timeout=6)
 images=[(a,OUT/(a['id']+'.png')) for a in assets if (OUT/(a['id']+'.png')).exists()]
 sheet=Image.new('RGB',(1024,416*((len(images)+3)//4)), '#e7e2d6');d=ImageDraw.Draw(sheet)
 for i,(a,path) in enumerate(images):
  x=(i%4)*256;y=(i//4)*416
  tile=ImageOps.contain(Image.open(path).convert('RGB'),(248,378))
  sheet.paste(tile,(x+(256-tile.width)//2,y));d.text((x+8,y+383),a['id']+' / Animagine Opt',fill='#222222')
 sheet.save(OUT/'character-overview.png')
print('ANIMAGINE_BATCH_OK',len(assets),flush=True)
