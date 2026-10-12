"""Bounded recolor and neckline study of the user-selected Aurelia a8."""
from pathlib import Path
import json, importlib.util, time, urllib.request, urllib.parse, hashlib
import numpy as np
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'; BASE=ROOT/'.local/reference-comfy/input'
NAME='aurelia-selected-778011'; recpath=OUT/(NAME+'.json')
if recpath.exists(): raise RuntimeError('Existing trial; inspect before retry.')
source=ROOT/'production/pixel-rpg/model-wave-01/originals/ch_aurelia-a8.png'
im=Image.open(source).convert('RGB'); a=np.array(im); hsv=np.array(im.convert('HSV')); yy,xx=np.indices(a.shape[:2])
r,g,b=a[:,:,0].astype(int),a[:,:,1].astype(int),a[:,:,2].astype(int)
hair=(yy<245)&(hsv[:,:,0]<24)&(hsv[:,:,1]>130)&(r>g*1.4)&(r>45)
cape=(yy>225)&(g>r*1.4)&(g>b*.7)&(b>r*1.3)
hsv[:,:,0][hair]=30; hsv[:,:,1][hair]=180; hsv[:,:,2][hair]=np.clip(hsv[:,:,2][hair].astype(float)*.62+100,0,255).astype('uint8')
hsv[:,:,0][cape]=250; hsv[:,:,1][cape]=205; hsv[:,:,2][cape]=np.clip(hsv[:,:,2][cape].astype(float)*1.1+28,0,255).astype('uint8')
converted=np.array(Image.fromarray(hsv,'HSV').convert('RGB')); changed=hair|cape; a[changed]=converted[changed]
base=Image.fromarray(a); guide=base.copy(); d=ImageDraw.Draw(guide)
# Restrict the neckline edit to existing blouse, below the unchanged cape clasp.
poly=[(280,279),(308,284),(327,289),(315,307),(299,315),(283,302),(271,295)]
d.polygon(poly,fill='#f4d5bb'); d.line([(271,295),(283,302),(299,315),(315,307),(327,289)],fill='#4d3431',width=2)
mask=Image.new('L',im.size); ImageDraw.Draw(mask).polygon([(269,277),(313,279),(333,288),(319,311),(300,320),(278,306),(266,296)],fill=255)
for suffix,img in [('source',base),('guide',guide),('mask',mask.convert('RGB'))]: img.save(BASE/f'{NAME}-{suffix}.png')
base.save(OUT/f'{NAME}-recolor.png')
spec=importlib.util.spec_from_file_location('gen',ROOT/'tools/generate-character.py'); gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in (8188,8189):
 gen.API=f'http://127.0.0.1:{port}';q=gen.request('/queue')
 if q.get('queue_running') or q.get('queue_pending'): raise RuntimeError('Occupied queue')
g=gen.graph(778011,'adult woman fantasy anime character, white blouse with a low V neckline, visible upper chest, opaque cloth covering bust, red cape, clean colored outlines, simple cel shading','nude, nipples, transparent cloth, extra accessories, text, jewelry, deformed anatomy')
g['5']={'class_type':'LoadImage','inputs':{'image':NAME+'-guide.png'}}
g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
g['10']={'class_type':'LoadImage','inputs':{'image':NAME+'-source.png'}}
g['11']={'class_type':'LoadImage','inputs':{'image':NAME+'-mask.png'}}
g['12']={'class_type':'ImageToMask','inputs':{'image':['11',0],'channel':'red'}}
g['13']={'class_type':'SetLatentNoiseMask','inputs':{'samples':['9',0],'mask':['12',0]}}
g['6']['inputs'].update(latent_image=['13',0],denoise=.35,steps=30,cfg=6)
g['14']={'class_type':'ImageCompositeMasked','inputs':{'destination':['10',0],'source':['7',0],'x':0,'y':0,'resize_source':False,'mask':['12',0]}}
g['8']['inputs'].update(images=['14',0],filename_prefix=NAME)
rec={'task':'M5.2.6.2','source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'graph':g,'state':'prepared'}
def save():recpath.write_text(json.dumps(rec,indent=2),encoding='utf-8')
save(); key=gen.request('/prompt',{'prompt':g,'client_id':'aurelia-selected'})['prompt_id'];rec.update(prompt_id=key,state='queued');save()
for _ in range(450):
 h=gen.request('/history/'+key)
 if key in h:
  result=h[key];rec.update(state=result['status']['status_str'],history=result);save()
  if rec['state']!='success':raise RuntimeError(recpath)
  f=result['outputs']['8']['images'][0];url=gen.API+'/view?'+urllib.parse.urlencode({k:f[k] for k in ('filename','subfolder','type')})
  target=OUT/(NAME+'.png')
  with urllib.request.urlopen(url) as response:target.write_bytes(response.read())
  final=np.array(Image.open(target).convert('RGB')); outside=np.array(mask)==0
  assert np.array_equal(final[outside],a[outside])
  rec.update(outside_mask_difference=0,output_sha256=hashlib.sha256(target.read_bytes()).hexdigest());save();print(target);break
 time.sleep(2)
else:raise TimeoutError(key)
