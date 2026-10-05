"""Package the M3.4 scene without local runtimes, caches or Blender backups."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
archive = ROOT / "builds/sunward-coast-source.zip"
archive.parent.mkdir(exist_ok=True)
files = []
for folder in ("scene-demo", "art-source/environment", "validation/coast"):
    for path in sorted((ROOT / folder).rglob("*")):
        if not path.is_file():
            continue
        if any(part in {".godot", "__pycache__"} for part in path.parts):
            continue
        if path.suffix in {".blend1", ".blend2", ".pyc"}:
            continue
        files.append(path)
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
    for path in files:
        z.write(path, path.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert "scene-demo/project.godot" in z.namelist()
    assert not any("/.godot/" in name for name in z.namelist())
outputs = [archive, ROOT / "builds/sunward-coast.exe"]
record = []
for path in outputs:
    with path.open("rb") as f:
        digest = hashlib.file_digest(f, "sha256").hexdigest()
    record.append({"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": digest})
(ROOT / "builds/sunward-coast-manifest.json").write_text(json.dumps({"files_in_source_zip":len(files),"outputs":record}, indent=2))
print(json.dumps(record, indent=2))
