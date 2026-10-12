"""Resume one pinned model using bounded parallel HTTP ranges, then verify it.

Experimental fallback: sequential download proved faster on the tested network.
Completed range files stay in the ignored download cache (no automatic deletion).
Only one downloader may write a given model at a time.
"""
import concurrent.futures
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
model = json.loads((ROOT / "tools/photo-models.json").read_text(encoding="utf-8-sig"))[int(sys.argv[1])]
target = ROOT / model["destination"]
target.parent.mkdir(parents=True, exist_ok=True)
start = target.stat().st_size if target.exists() else 0
assert start <= model["bytes"], "Oversized file retained for inspection"
url = f'https://huggingface.co/{model["repository"]}/resolve/{model["revision"]}/{model["file"]}'
cache = ROOT / ".local/download-ranges" / target.name
cache.mkdir(parents=True, exist_ok=True)
chunk_size = 128 * 1024**2
ranges = [(offset, min(offset + chunk_size, model["bytes"]) - 1)
          for offset in range(start, model["bytes"], chunk_size)]


def download(interval):
    first, last = interval
    part = cache / f"{first}-{last}.part"
    expected = last - first + 1
    if not part.exists() or part.stat().st_size != expected:
        subprocess.run(["curl.exe", "-L", "--fail", "--silent", "--show-error",
                        "--retry", "3", "--connect-timeout", "30", "--max-time", "900",
                        "--max-filesize", str(expected), "--range", f"{first}-{last}",
                        "-o", str(part), url], check=True)
    assert part.stat().st_size == expected, f"Incorrect range size: {part}"
    print(f"RANGE_READY {first}-{last}", flush=True)
    return part


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    parts = list(pool.map(download, ranges))
assert (target.stat().st_size if target.exists() else 0) == start, "Another process changed the model"
with target.open("ab") as output:
    for part in parts:
        with part.open("rb") as source:
            while data := source.read(8 * 1024**2):
                output.write(data)
assert target.stat().st_size == model["bytes"]
with target.open("rb") as source:
    digest = hashlib.file_digest(source, "sha256").hexdigest()
assert digest == model["sha256"], "Hash mismatch; all files retained"
target.with_name(target.name + ".source.json").write_text(json.dumps(model, indent=2), encoding="utf-8")
print(f'VERIFIED {model["file"]}', flush=True)
