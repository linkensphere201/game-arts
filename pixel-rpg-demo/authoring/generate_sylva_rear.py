"""Fresh rear-view local-model candidate, avoiding inherited flat guide geometry."""
from pathlib import Path
import hashlib, importlib.util, json, shutil, time
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'.local/reference-comfy'
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'
NAME='sylva-rear-fresh-761009'
record=OUT/(NAME+'.json')
if record.exists(): raise RuntimeError('Run exists; inspect recorded prompt before retrying.')
spec=importlib.util.spec_from_file_location('generation',ROOT/'tools/generate-character.py')
gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for port in [8188,8189]:
    gen.API=f'http://127.0.0.1:{port}'
    q=gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'): raise RuntimeError('Queue occupied')
g=gen.graph(761009,
    '(back view:1.4), full body chibi elf girl mage, viewed from behind, facing away, standing, long flowing loose golden blonde hair down her back, rounded back of head, long pointed elf ears, teal green long robe with wide bell sleeves, thin cream sleeve cuffs, brown waist belt, simple brass hem trim, brown sandals, petite slender body, four heads tall, beautiful anime JRPG character illustration, clean dark colored outlines, soft cel shading, plain white background, complete single figure centered with margin',
    'front view, looking at viewer, looking back, face, eyes, mouth, nose, portrait, close up, hat, headband, hairband, headdress, crown, horns, pigtails, twin tails, ponytail, short hair, cape, extra limbs, text, watermark, signature, photo, 3d render, cut off, cropped, adult proportions, long legs')
g['5']['inputs'].update(width=512,height=768)
g['6']['inputs'].update(steps=30,cfg=6)
g['8']['inputs']['filename_prefix']=NAME
r={'graph':g,'state':'prepared','review':'pending','purpose':'Independent rear concept; identity must be compared before selection'}
def save(): record.write_text(json.dumps(r,indent=2),encoding='utf-8')
save();key=gen.request('/prompt',{'prompt':g,'client_id':'sylva-rear-study'})['prompt_id']
r.update(prompt_id=key,state='queued');save();print('QUEUED',key,flush=True)
start=time.monotonic()
while time.monotonic()-start<900:
    history=gen.request('/history/'+key)
    if key in history:
        h=history[key];r.update(state=h['status']['status_str'],history=h);save()
        if r['state']!='success': raise RuntimeError(record)
        f=h['outputs']['8']['images'][0];target=OUT/(NAME+'.png')
        shutil.copy2(BASE/'output'/f['subfolder']/f['filename'],target)
        r['output_sha256']=hashlib.sha256(target.read_bytes()).hexdigest();save()
        print('SUCCESS',flush=True);break
    time.sleep(2)
else: raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit')
