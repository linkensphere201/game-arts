"""Bounded local Klein FP8 generation/edit test, with replayable ComfyUI graphs."""
import argparse
import ctypes
import hashlib
import importlib.util
import json
import shutil
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / '.local/reference-comfy'
URL = 'http://127.0.0.1:8189'
PROMPT = ('A polished minimalist summer beverage advertising poster background, vertical composition. '
          'One tall clear glass of sparkling orange lemonade with ice cubes and orange slices, '
          'on a pale sandstone pedestal in the lower right quadrant. Turquoise coastal sea and '
          'sunlit soft beige sky. The upper left half is clean empty pale sky reserved for a headline. '
          'Elegant commercial product photography, realistic glass reflections, warm sunlight, '
          'restrained composition. No text, no letters, no logo, no watermark.')
EDIT = ('Change only the orange lemonade in the glass into pink strawberry lemonade and replace '
        'the orange slices with strawberries. Keep the same glass shape, pedestal, camera viewpoint, '
        'coastal background, lighting and empty upper-left headline space. No text or logo.')


def request(endpoint, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(URL + endpoint, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as response:
        body = response.read()
    return json.loads(body) if body else None


def graph(edit_image=None, width=576, height=768):
    g = {}
    def node(i, kind, **kw):
        g[str(i)] = {'class_type': kind, 'inputs': kw}
    node(1, 'UNETLoader', unet_name='flux-2-klein-4b-fp8.safetensors', weight_dtype='default')
    node(2, 'CLIPLoader', clip_name='qwen_3_4b_fp4_flux2.safetensors', type='flux2', device='default')
    node(3, 'VAELoader', vae_name='flux2-vae.safetensors')
    node(4, 'CLIPTextEncode', clip=['2', 0], text=EDIT if edit_image else PROMPT)
    node(5, 'EmptyFlux2LatentImage', width=width, height=height, batch_size=1)
    node(6, 'Flux2Scheduler', steps=4, width=width, height=height)
    node(7, 'KSamplerSelect', sampler_name='euler')
    node(8, 'RandomNoise', noise_seed=20261008)
    conditioning = ['4', 0]
    if edit_image:
        node(13, 'LoadImage', image=edit_image)
        node(16, 'ImageScale', image=['13', 0], upscale_method='area', width=width, height=height, crop='disabled')
        node(14, 'VAEEncode', pixels=['16', 0], vae=['3', 0])
        node(15, 'ReferenceLatent', conditioning=conditioning, latent=['14', 0])
        conditioning = ['15', 0]
    node(9, 'BasicGuider', model=['1', 0], conditioning=conditioning)
    node(10, 'SamplerCustomAdvanced', noise=['8', 0], guider=['9', 0], sampler=['7', 0],
         sigmas=['6', 0], latent_image=['5', 0])
    node(11, 'VAEDecodeTiled', samples=['10', 0], vae=['3', 0], tile_size=512,
         overlap=64, temporal_size=64, temporal_overlap=8)
    node(12, 'SaveImage', images=['11', 0], filename_prefix='poster_klein/' + ('edit' if edit_image else 'base'))
    return g


def ui_workflow(g, schema):
    nodes, links, lookup = [], [], {}
    for index, (key, item) in enumerate(g.items()):
        definition = schema[item['class_type']]
        specs = dict(definition['input'].get('required', {}))
        specs.update(definition['input'].get('optional', {}))
        widgets, inputs = [], []
        for name, spec in specs.items():
            if name not in item['inputs']:
                continue
            value = item['inputs'][name]
            if isinstance(value, list):
                inputs.append({'name': name, 'type': spec[0], 'link': None})
            else:
                widgets.append(value)
                if len(spec) > 1 and isinstance(spec[1], dict) and spec[1].get('control_after_generate'):
                    widgets.append('fixed')
        if item['class_type'] == 'LoadImage':
            widgets.append('image')
        n = {'id': int(key), 'type': item['class_type'], 'pos': [(index // 4) * 390, (index % 4) * 320],
             'size': [360, 290], 'flags': {}, 'order': index, 'mode': 0, 'inputs': inputs,
             'outputs': [{'name': t, 'type': t, 'links': []} for t in definition['output']],
             'properties': {'Node name for S&R': item['class_type']}, 'widgets_values': widgets}
        nodes.append(n)
        lookup[key] = n
    for key in g:
        for slot, socket in enumerate(lookup[key]['inputs']):
            source, out_slot = g[key]['inputs'][socket['name']]
            output = lookup[source]['outputs'][out_slot]
            assert output['type'] == socket['type']
            number = len(links) + 1
            socket['link'] = number
            output['links'].append(number)
            links.append([number, int(source), out_slot, int(key), slot, socket['type']])
    return {'last_node_id': max(map(int, g)), 'last_link_id': len(links), 'nodes': nodes,
            'links': links, 'groups': [], 'config': {}, 'extra': {}, 'version': 0.4}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['generate', 'edit'])
    parser.add_argument('--input', type=Path)
    parser.add_argument('--width', type=int, default=576)
    parser.add_argument('--height', type=int, default=768)
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'tools/klein-models.json').read_text(encoding='utf-8-sig'))
    for item in manifest:
        path = ROOT / item['destination']
        assert path.stat().st_size == item['bytes'], f'Incomplete file: {path}'
        with path.open('rb') as f:
            assert hashlib.file_digest(f, 'sha256').hexdigest() == item['sha256'], f'Hash mismatch: {path}'
    queue = request('/queue')
    assert not queue['queue_running'] and not queue['queue_pending'], 'ComfyUI is occupied'
    request('/free', {'unload_models': True, 'free_memory': True})
    time.sleep(3)
    spec = importlib.util.spec_from_file_location('memory_gate', ROOT / 'tools/run-comfy.py')
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    assert gate.check_memory(), 'Insufficient memory headroom'
    edit_image = None
    if args.mode == 'edit':
        assert args.input and args.input.is_file(), 'Editing needs --input PNG'
        edit_image = 'klein-reference-' + hashlib.sha256(args.input.read_bytes()).hexdigest()[:12] + '.png'
        (BASE / 'input').mkdir(parents=True, exist_ok=True)
        shutil.copyfile(args.input, BASE / 'input' / edit_image)
    assert args.width > 0 and args.height > 0 and args.width % 16 == 0 and args.height % 16 == 0
    g = graph(edit_image, args.width, args.height)
    workflow = ui_workflow(g, request('/object_info'))
    workflows = ROOT / 'production/workflows'
    workflows.mkdir(parents=True, exist_ok=True)
    name = f'klein-poster-{args.mode}'
    workflow_path = workflows / (name + '.json')
    workflow_path.write_text(json.dumps(workflow, indent=2) + '\n', encoding='utf-8')
    ui_dir = BASE / 'user/default/workflows'
    ui_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(workflow_path, ui_dir / workflow_path.name)
    runs = ROOT / '.local/runs'
    (runs / (name + '-api.json')).write_text(json.dumps(g, indent=2), encoding='utf-8')
    started = time.monotonic()
    result = request('/prompt', {'prompt': g, 'extra_data': {'extra_pnginfo': {'workflow': workflow}}})
    prompt_id = result['prompt_id']
    print(f'SUBMITTED {prompt_id}', flush=True)
    samples = []
    report_path = runs / (name + '-' + time.strftime('%Y%m%d-%H%M%S') + '.json')
    interrupted_for_memory = False
    while True:
        history = request('/history/' + prompt_id).get(prompt_id)
        memory = gate.MemoryStatus()
        memory.length = ctypes.sizeof(memory)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory))
        gpu = subprocess.run(['nvidia-smi', '--query-gpu=memory.used', '--format=csv,noheader,nounits'],
                             capture_output=True, text=True, creationflags=0x08000000)
        samples.append({'seconds': round(time.monotonic() - started, 2),
                        'gpu_mib': int(gpu.stdout.strip()) if gpu.returncode == 0 else None,
                        'available_commit_gib': memory.available_commit / 1024**3,
                        'available_physical_gib': memory.available_physical / 1024**3})
        report = {'mode': args.mode, 'prompt_id': prompt_id, 'samples': samples, 'history': history,
                  'elapsed_seconds': time.monotonic() - started, 'workflow': str(workflow_path),
                  'interrupted_for_memory': interrupted_for_memory}
        report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
        if history:
            break
        if memory.available_commit / 1024**3 < 0.75 and not interrupted_for_memory:
            queue = request('/queue')
            if len(queue['queue_running']) == 1 and queue['queue_running'][0][1] == prompt_id:
                request('/interrupt', {})
                interrupted_for_memory = True
                print('Interrupt requested: less than 0.75 GiB available commit', flush=True)
        if time.monotonic() - started > 900:
            raise TimeoutError(f'Polling timed out; inspect job {prompt_id} before resubmitting')
        time.sleep(2)
    print(f'REPORT {report_path}', flush=True)
    queue = request('/queue')
    if not queue['queue_running'] and not queue['queue_pending']:
        request('/free', {'unload_models': True, 'free_memory': True})
    assert history['status']['status_str'] == 'success', history['status']
    for output in history.get('outputs', {}).values():
        for image in output.get('images', []):
            print('IMAGE', BASE / 'output' / image['subfolder'] / image['filename'], flush=True)
    print(f'SUCCESS {args.mode} {report["elapsed_seconds"]:.1f}s', flush=True)
    queue = request('/queue')
    if not queue['queue_running'] and not queue['queue_pending']:
        request('/free', {'unload_models': True, 'free_memory': True})


if __name__ == '__main__':
    main()
