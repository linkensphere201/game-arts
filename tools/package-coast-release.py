"""Build local review archives with an allowlist, dependency audit and hashes."""
from pathlib import Path
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'scene-demo'
PACK = PROJECT / 'sunward_coast'
VERSION = '0.2.0-rc1'
OUT = ROOT / 'builds'
OUT.mkdir(exist_ok=True)

def package(name, entries):
    entries = list(entries)
    names = [name for _, name in entries]
    assert len(names) == len(set(names)), 'Duplicate archive paths'
    manifest = {name: hashlib.sha256(path.read_bytes()).hexdigest() for path, name in entries}
    target = OUT / f'sunward-coast-{VERSION}-{name}.zip'
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path, arcname in entries:
            archive.write(path, arcname)
        archive.writestr('SHA256.json', json.dumps(manifest, indent=2))
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
    return {'file': target.name, 'bytes': target.stat().st_size,
            'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'files': len(entries)}

allowed = {'.tscn', '.tres', '.res', '.glb', '.gd', '.gdshader', '.md', '.txt', '.json'}
files = sorted(p for p in PACK.rglob('*') if p.is_file() and p.suffix in allowed)
assert len(list((PACK / 'meshes').glob('*.glb'))) == 17
assert (PACK / 'docs/GODOT_NOTICES.txt').stat().st_size > 1000
for path in files:
    if path.suffix in {'.tscn', '.tres', '.gd', '.gdshader'}:
        for resource in re.findall(r'res://[^"\s)]+', path.read_text(encoding='utf-8')):
            assert resource.startswith('res://sunward_coast/'), (path, resource)
            assert (PROJECT / resource.removeprefix('res://')).is_file(), (path, resource)
assets = [(p, p.relative_to(PROJECT).as_posix()) for p in files]
docs = [(p, p.name) for p in files if p.parent == PACK / 'docs']
results = [package('godot', assets)]
demo = assets + [(PROJECT / p, p) for p in
                 ('project.godot', 'levels/coast.tscn', 'scripts/coast_demo.gd')]
results.append(package('demo', demo))
results.append(package('windows', [(OUT / 'sunward-coast.exe', 'sunward-coast.exe')] + docs))
results.append(package('blender', [(ROOT / 'art-source/environment' / p, p) for p in
                                 ('coastal-kit.blend', 'coastal-terrain.blend')] + docs))
(OUT / f'sunward-coast-{VERSION}-manifest.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
print(json.dumps(results, indent=2))
