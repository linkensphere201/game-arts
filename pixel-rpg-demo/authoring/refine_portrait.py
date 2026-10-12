"""Image-to-image refinement of an inspected, locally generated chibi crop."""
from pathlib import Path
import importlib.util,json,time,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('local_generation',ROOT/'tools/generate-character.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
OUT=ROOT/'production/pixel-rpg'
source=Image.open(OUT/'candidates/mosslight_portrait_731202_00001_.png').convert('RGB')
crop=source.crop((315,365,505,735))
crop=crop.resize((round(crop.width*1.6),round(crop.height*1.6)),Image.Resampling.LANCZOS)
reference=Image.new('RGB',(512,768),'white');reference.paste(crop,((512-crop.width)//2,(768-crop.height)//2))
reference.save(ROOT/'.local/comfy/ComfyUI_windows_portable/ComfyUI/input/mosslight_chibi_reference.png')

positive='(single character:1.5), (chibi:1.5), (full body:1.4), beautiful original JRPG female swordsman, auburn bob hair and side braid, amber eyes, teal shoulder cape, white tunic dress, brown leather belt and boots, cute expressive face, three heads tall, standing pose, front three quarter view, viewed slightly from above, clean colored outlines, cel shaded anime game art, isolated on plain white background, detailed coherent outfit, visible feet'
negative='multiple people, character sheet, panels, collage, text, signature, logo, scenery, background details, realistic, photograph, 3d render, extra arms, extra legs, missing feet, malformed hands, cropped, blurry'
for seed,denoise in [(731211,.28),(731212,.4)]:
 path=OUT/'runs'/f'portrait-refine-{seed}.json'
 if path.exists():raise FileExistsError(path)
 g=m.graph(seed,positive,negative)
 g['5']={'class_type':'LoadImage','inputs':{'image':'mosslight_chibi_reference.png'}}
 g['9']={'class_type':'VAEEncode','inputs':{'pixels':['5',0],'vae':['1',2]}}
 g['6']['inputs'].update(latent_image=['9',0],denoise=denoise,steps=30,cfg=6)
 g['8']['inputs']['filename_prefix']=f'mosslight_chibi_{seed}'
 queued=m.request('/prompt',{'prompt':g,'client_id':'mosslight-chibi-refine'});key=queued['prompt_id'];start=time.monotonic()
 record={'source':'mosslight_portrait_731202_00001_.png','source_crop':[315,365,505,735],'input':'mosslight_chibi_reference.png','graph':g,'prompt_id':key};path.write_text(json.dumps(record,indent=2));print('QUEUED',seed,flush=True)
 while time.monotonic()-start<600:
  hist=m.request('/history/'+key)
  if key in hist:
   result=hist[key];record.update(history=result,seconds=time.monotonic()-start);path.write_text(json.dumps(record,indent=2))
   if result['status']['status_str']!='success':raise RuntimeError(result['status'])
   for im in result['outputs']['8']['images']:
    src=ROOT/'.local/comfy/ComfyUI_windows_portable/ComfyUI/output'/im['subfolder']/im['filename'];shutil.copy2(src,OUT/'candidates'/im['filename'])
   print('COMPLETE',seed,round(record['seconds'],2),flush=True);break
  time.sleep(2)
 else:raise TimeoutError(key)
