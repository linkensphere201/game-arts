"""Create small source-only delivery archives; never include local runtimes/caches."""
from pathlib import Path
import zipfile
import hashlib
import json
ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'builds'
BUILD.mkdir(exist_ok=True)
manifest = {}
for name, source in [('ember-imp-godot.zip', ROOT/'assets/ember-imp'), ('ember-imp-demo-source.zip', ROOT/'demo')]:
    destination = BUILD/name
    files = [p for p in source.rglob('*') if p.is_file() and '.godot' not in p.relative_to(source).parts]
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            archive.write(path, Path(source.name)/path.relative_to(source))
    with zipfile.ZipFile(destination) as archive:
        assert archive.testzip() is None
        assert all(not n.startswith('/') and '..' not in Path(n).parts for n in archive.namelist())
        manifest[name] = {'file_count':len(archive.namelist()), 'bytes':destination.stat().st_size, 'sha256':hashlib.sha256(destination.read_bytes()).hexdigest()}
exe = BUILD/'ember-imp-demo.exe'
if exe.exists():
    manifest[exe.name] = {'bytes':exe.stat().st_size, 'sha256':hashlib.sha256(exe.read_bytes()).hexdigest()}
(ROOT/'validation/delivery-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
