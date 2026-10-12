"""M5 local concept generation; retains source prompt and server provenance."""
from pathlib import Path
import importlib.util,json,time,urllib.request,shutil
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('local_generation',ROOT/'tools/generate-character.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
positive="pixel art, 16 bit JRPG game character, one full body young adult adventurer, three quarter front view, chibi 3 heads tall, auburn tousled hair, teal short coat, ochre yellow scarf, cream trousers, brown leather boots, small brown satchel, friendly determined face, simple travel clothes, arms and legs clearly separated, compact readable silhouette, deliberate pixel clusters, dark colored outlines, restrained palette, centered, plain white background, entire body visible"
negative="photorealistic, painting, blurry, scenery, complex background, text, logo, watermark, cropped feet, multiple characters, extra arms, extra legs, sword, armor"
out=ROOT/'production/pixel-rpg'
for folder in ['runs','candidates']:(out/folder).mkdir(parents=True,exist_ok=True)
for seed in [710031,710032]:
    graph=mod.graph(seed,positive,negative)
    graph['8']['inputs']['filename_prefix']='mosslight_concept_'+str(seed)
    queued=mod.request('/prompt',{'prompt':graph,'client_id':'pixel-rpg-M5'})
    key=queued['prompt_id'];start=time.monotonic()
    record={'seed':seed,'graph':graph,'prompt_id':key,'purpose':'Concept only, not final animation'}
    path=out/'runs'/f'concept-{seed}.json'
    path.write_text(json.dumps(record,indent=2),encoding='utf-8')
    print('QUEUED',key,flush=True)
    while time.monotonic()-start<600:
        history=mod.request('/history/'+key)
        if key in history:
            result=history[key];record['history']=result;record['seconds']=time.monotonic()-start
            path.write_text(json.dumps(record,indent=2),encoding='utf-8')
            if result['status']['status_str']!='success':raise RuntimeError(result['status'])
            for im in result['outputs']['8']['images']:
                source=ROOT/'.local/comfy/ComfyUI_windows_portable/ComfyUI/output'/im['subfolder']/im['filename']
                shutil.copy2(source,out/'candidates'/im['filename'])
            print('COMPLETE',seed,record['seconds'],flush=True);break
        time.sleep(2)
    else:raise TimeoutError(key)
