"""Run one neutral portrait per installed model; preserve history and images."""
import argparse
import hashlib
import importlib.util
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = "http://127.0.0.1:8189"


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def request(endpoint, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(URL + endpoint, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as response:
        body = response.read()
    return json.loads(body) if body else None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", choices=["realvisxl", "realistic-vision", "z-image-turbo"])
    args = parser.parse_args()
    manifest = json.loads((ROOT / "tools/photo-models.json").read_text(encoding="utf-8-sig"))
    indices = {"realvisxl": [0], "realistic-vision": [1, 2], "z-image-turbo": [3, 4, 5]}[args.model]
    for index in indices:
        entry = manifest[index]
        path = ROOT / entry["destination"]
        assert path.stat().st_size == entry["bytes"], f"Incomplete model: {path}"
        with path.open("rb") as source:
            assert hashlib.file_digest(source, "sha256").hexdigest() == entry["sha256"]
    queue = request("/queue")
    assert not queue["queue_running"] and not queue["queue_pending"], "ComfyUI is occupied"
    request("/free", {"unload_models": True, "free_memory": True})
    time.sleep(3)
    assert load_module("memory_gate", "run-comfy.py").check_memory(), "Insufficient initial commit headroom"
    builder = load_module("photo_workflows", "build-photo-workflows.py")
    graph = builder.make_graph(args.model)
    workflow = builder.ui_workflow(graph, request("/object_info"))
    started = time.monotonic()
    submitted = request("/prompt", {"prompt": graph, "extra_data": {"extra_pnginfo": {"workflow": workflow}}})
    prompt_id = submitted["prompt_id"]
    print(f"SUBMITTED {args.model} {prompt_id}", flush=True)
    while True:
        history = request(f"/history/{prompt_id}").get(prompt_id)
        if history:
            break
        time.sleep(3)
    report = {"model": args.model, "elapsed_seconds": time.monotonic() - started,
              "prompt_id": prompt_id, "history": history}
    output = ROOT / ".local/runs" / f"{args.model}-install-test.json"
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    assert history["status"]["status_str"] == "success", f"Generation failed; see {output}"
    print(f"SUCCESS {args.model} {report['elapsed_seconds']:.1f}s", flush=True)
    queue = request("/queue")
    if not queue["queue_running"] and not queue["queue_pending"]:
        request("/free", {"unload_models": True, "free_memory": True})
