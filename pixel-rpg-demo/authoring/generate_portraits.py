"""Bounded local model-first art study. Retains exact workflow and source images."""
from pathlib import Path
import importlib.util,json,time,shutil
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('local_generation',ROOT/'tools/generate-character.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
OUT=ROOT/'production/pixel-rpg'
for name in ['runs','candidates']:(OUT/name).mkdir(parents=True,exist_ok=True)
positive='(full body:1.4), (chibi:1.35), solo, one original fantasy female swordsman, young adult, cute expressive anime face, large amber eyes, auburn shoulder length hair, side braid, small brass hair clasp, teal short fitted tunic, cream undershirt, brown belt with small pouches, short asymmetrical teal cape, brown leather knee boots, simple sheathed sword at left hip, practical layered fantasy adventurer clothes, JRPG character concept art, clean confident lineart, beautiful cel shading, detailed fabric folds, charming compact proportions, three heads tall, standing relaxed with arms separated from torso, front three quarter view, visible boots, centered, isolated on plain white background, high quality character illustration'
negative='photograph, realistic, 3d render, elderly, man, masculine, long legs, tiny head, modern clothing, trenchcoat, coat tails, jeans, cleavage, underwear, nude, sexy, high heels, intricate armor, multiple characters, character sheet, collage, cropped, out of frame, missing feet, extra limbs, extra fingers, bad hands, malformed face, text, signature, watermark, scenery, floor, background objects, blurry'
for seed in [731201,731202,731203,731204]:
 record_path=OUT/'runs'/f'portrait-{seed}.json'
 if record_path.exists():raise FileExistsError(f'Existing run: inspect before repeating {record_path}')
 graph=m.graph(seed,positive,negative);graph['5']['inputs']['height']=768
 graph['6']['inputs'].update(steps=30,cfg=7.0)
 graph['8']['inputs']['filename_prefix']=f'mosslight_portrait_{seed}'
 record={'purpose':'Original model-first art quality study; not animation','seed':seed,'graph':graph,'system':m.request('/system_stats')}
 queued=m.request('/prompt',{'prompt':graph,'client_id':'mosslight-art-redesign'});key=queued['prompt_id'];record['prompt_id']=key
 record_path.write_text(json.dumps(record,indent=2),encoding='utf-8');start=time.monotonic();print('QUEUED',seed,key,flush=True)
 while time.monotonic()-start<600:
  hist=m.request('/history/'+key)
  if key in hist:
   result=hist[key];record.update(history=result,seconds=time.monotonic()-start);record_path.write_text(json.dumps(record,indent=2),encoding='utf-8')
   if result['status']['status_str']!='success':raise RuntimeError(result['status'])
   for im in result['outputs']['8']['images']:
    src=ROOT/'.local/comfy/ComfyUI_windows_portable/ComfyUI/output'/im['subfolder']/im['filename'];shutil.copy2(src,OUT/'candidates'/im['filename'])
   print('COMPLETE',seed,round(record['seconds'],2),flush=True);break
  time.sleep(2)
 else:raise TimeoutError(key)
