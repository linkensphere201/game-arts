"""Run the bounded local ComfyUI character trial and retain provenance."""
import argparse
import json
import pathlib
import time
import subprocess
import threading
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
API = 'http://127.0.0.1:8188'

def request(path, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(API + path, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)

def graph(seed, positive, negative):
    return {
        '1': {'class_type': 'CheckpointLoaderSimple', 'inputs': {'ckpt_name': 'DreamShaper_8_pruned.safetensors'}},
        '3': {'class_type': 'CLIPTextEncode', 'inputs': {'text': positive, 'clip': ['1', 1]}},
        '4': {'class_type': 'CLIPTextEncode', 'inputs': {'text': negative, 'clip': ['1', 1]}},
        '5': {'class_type': 'EmptyLatentImage', 'inputs': {'width': 512, 'height': 512, 'batch_size': 1}},
        '6': {'class_type': 'KSampler', 'inputs': {'model': ['1', 0], 'positive': ['3', 0], 'negative': ['4', 0], 'latent_image': ['5', 0], 'seed': seed, 'steps': 28, 'cfg': 7.0, 'sampler_name': 'dpmpp_2m', 'scheduler': 'karras', 'denoise': 1.0}},
        '7': {'class_type': 'VAEDecode', 'inputs': {'samples': ['6', 0], 'vae': ['1', 2]}},
        '8': {'class_type': 'SaveImage', 'inputs': {'images': ['7', 0], 'filename_prefix': f'ember_imp_{seed}'}},
    }

def sample_gpu(stop, samples):
    while not stop.is_set():
        try:
            value = subprocess.check_output(['nvidia-smi', '--query-gpu=memory.used', '--format=csv,noheader,nounits'], creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0), timeout=5, text=True)
            samples.append(int(value.strip().splitlines()[0]))
        except (OSError, ValueError, subprocess.SubprocessError):
            pass
        stop.wait(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=420052)
    parser.add_argument('--count', type=int, default=1)
    parser.add_argument('--brief', type=pathlib.Path, default=ROOT / 'production/brief.json')
    parser.add_argument('--prompt', help='Override the text description/prompt')
    parser.add_argument('--negative', help='Override the negative prompt')
    args = parser.parse_args()
    brief = json.loads(args.brief.read_text(encoding='utf-8-sig'))
    positive = args.prompt or brief['generation']['positive_prompt']
    negative = args.negative or brief['generation']['negative_prompt']
    if not 1 <= args.count <= 8:
        parser.error('Use 1-8 candidates per bounded trial')
    out = ROOT / 'production' / 'runs'
    out.mkdir(parents=True, exist_ok=True)
    for seed in range(args.seed, args.seed + args.count):
        prompt = graph(seed, positive, negative)
        record_path = out / f'{seed}.json'
        if record_path.exists():
            record_path = out / f'{seed}-{time.time_ns()}.json'
        start = time.monotonic()
        samples = []
        stop = threading.Event()
        monitor = threading.Thread(target=sample_gpu, args=(stop, samples), daemon=True)
        monitor.start()
        record = {'seed': seed, 'prompt': prompt, 'system': request('/system_stats')}
        queued = request('/prompt', {'prompt': prompt, 'client_id': 'game-arts-local-mvp'})
        prompt_id = queued['prompt_id']
        record['prompt_id'] = prompt_id
        record['state'] = 'queued'
        record_path.write_text(json.dumps(record, indent=2), encoding='utf-8')
        print(f'QUEUED {seed} {prompt_id}', flush=True)
        deadline = time.monotonic() + 1800
        while time.monotonic() < deadline:
            history = request('/history/' + prompt_id)
            if prompt_id in history:
                result = history[prompt_id]
                stop.set()
                monitor.join(timeout=6)
                record['state'] = result.get('status', {}).get('status_str', 'unknown')
                record.update({'elapsed_seconds': time.monotonic() - start, 'history': result, 'gpu_total_memory_used_mib_samples': samples, 'peak_gpu_total_memory_used_mib': max(samples) if samples else None, 'memory_note': 'Device-wide nvidia-smi samples, includes desktop/other GPU apps; not an isolated allocation measurement.'})
                record_path.write_text(json.dumps(record, indent=2), encoding='utf-8')
                if result.get('status', {}).get('status_str') != 'success':
                    raise RuntimeError(f'Generation failed: see {out / f"{seed}.json"}')
                print(f'COMPLETE {seed} {record["elapsed_seconds"]:.1f}s {result["outputs"]}', flush=True)
                break
            time.sleep(2)
        else:
            raise TimeoutError(f'Generation still incomplete: {prompt_id}; inspect server before retrying')

if __name__ == '__main__':
    main()
