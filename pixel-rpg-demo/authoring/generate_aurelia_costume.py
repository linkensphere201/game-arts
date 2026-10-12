"""Generate the additional adult blonde character concept locally, retaining provenance."""
from pathlib import Path
import hashlib, importlib.util, json, time, shutil, urllib.request, urllib.parse
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'production/pixel-rpg/model-wave-01/originals'
RECORD = ROOT / 'production/pixel-rpg/model-wave-01/runs/ch_aurelia-a10.json'
TARGET = OUT / 'ch_aurelia-a10.png'
if RECORD.exists() or TARGET.exists():
    raise RuntimeError('Existing trial: inspect before retrying; no overwrite.')
spec = importlib.util.spec_from_file_location('generation', ROOT / 'tools/generate-character.py')
gen = importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)
for port in (8188, 8189):
    gen.API = f'http://127.0.0.1:{port}'
    q = gen.request('/queue')
    if q.get('queue_running') or q.get('queue_pending'):
        raise RuntimeError(f'Occupied queue: {port}')
positive = '''(chibi:1.2), (hand drawn 2D anime illustration:1.4), single adult female fantasy sorceress, age 25, large head, (big expressive amber eyes:1.3), rounded facial contours, small nose, (long golden blonde hair:1.4), slender waist, full bust, (red bikini top:1.3), red bikini thong bottom, bare midriff, (flowing crimson red cape:1.4), brown boots, standing neutral pose, full body, three quarter view, clean dark colored outlines, simple matte cel shading, cohesive Japanese RPG character design, plain white background, complete silhouette'''

negative = 'child, underage, little girl, toddler, baby, loli, childish face, infant proportions, nude, naked, nipples, exposed genitals, transparent clothing, erotic pose, suggestive pose, photorealistic, photograph, 3d render, tiny eyes, corset, bodysuit, one piece swimsuit, covered belly, long dress, robe, skirt, trousers, sleeves, armor, cropped, missing feet, extra limbs, deformed hands, multiple people, text, watermark, hat, headgear, crown, short hair, green cape, blue cape, scenery, decorative lines, border, flat chest, long legs, tiny head, sharp angular face, realistic anatomy, harsh angular shading'

g = gen.graph(778010, positive, negative)
g['5']['inputs'].update(width=512, height=768)
g['6']['inputs'].update(steps=30, cfg=7)
source = ROOT / 'production/pixel-rpg/model-wave-01/originals/ch_rowan-a1.png'
shutil.copy2(source, ROOT / '.local/reference-comfy/input/aurelia-costume-reference.png')
g['9'] = {'class_type':'LoadImage','inputs':{'image':'aurelia-costume-reference.png'}}
g['10'] = {'class_type':'VAEEncode','inputs':{'pixels':['9',0],'vae':['1',2]}}
g['6']['inputs'].update(latent_image=['10',0], denoise=.68)
g['8']['inputs']['filename_prefix'] = 'mosslight_aurelia_778010'
record = {'id':'ch_aurelia', 'working_name':'Aurelia', 'task':'M5.2.6.2', 'state':'prepared', 'graph':g, 'api':gen.API, 'scope':'Additional adult blonde female concept only; no animation or replacement of existing roster', 'review':'pending', 'style_reference':str(source.relative_to(ROOT)), 'style_reference_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
def save(): RECORD.write_text(json.dumps(record, indent=2), encoding='utf-8')
save()
key = gen.request('/prompt', {'prompt':g, 'client_id':'mosslight-aurelia'})['prompt_id']
record.update(prompt_id=key, state='queued'); save(); print('QUEUED', key, flush=True)
start=time.monotonic()
while time.monotonic()-start < 900:
    h=gen.request('/history/'+key)
    if key in h:
        result=h[key]; record.update(state=result['status']['status_str'], history=result); save()
        if record['state'] != 'success': raise RuntimeError(RECORD)
        im=result['outputs']['8']['images'][0]
        url=gen.API+'/view?'+urllib.parse.urlencode({k:im[k] for k in ('filename','subfolder','type')})
        with urllib.request.urlopen(url, timeout=30) as response: data=response.read()
        TARGET.write_bytes(data)
        record.update(output=str(TARGET.relative_to(ROOT)), sha256=hashlib.sha256(data).hexdigest()); save()
        print('COMPLETE', TARGET, flush=True); break
    time.sleep(2)
else: raise TimeoutError(f'Inspect existing prompt {key}; do not resubmit.')
