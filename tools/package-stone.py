"""Local standalone stone archives; explicit contents and per-file hashes."""
from pathlib import Path
import hashlib
import json
import zipfile
import re

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT/'rock-demo'
PACK=PROJECT/'stone_asset'
allowed={'.glb','.png','.gd','.gdshader','.tres','.tscn','.md','.json'}
files=sorted(p for p in PACK.rglob('*') if p.is_file() and p.suffix in allowed)
for p in files:
    if p.suffix in {'.gd','.tres','.tscn','.gdshader'}:
        for resource in re.findall(r'res://[^"\s)]+',p.read_text(encoding='utf-8')):
            assert resource.startswith('res://stone_asset/'),resource
            assert (PROJECT/resource[6:]).is_file(),resource
assets=[(p,p.relative_to(PROJECT).as_posix()) for p in files]
def archive(name, entries):
    path=ROOT/'builds'/('limestone-0.1.0-'+name+'.zip')
    manifest={n:hashlib.sha256(p.read_bytes()).hexdigest() for p,n in entries}
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for p,n in entries:z.write(p,n)
        z.writestr('SHA256.json',json.dumps(manifest,indent=2))
    with zipfile.ZipFile(path) as z:assert z.testzip() is None
    print(path.name,path.stat().st_size)
archive('godot',assets)
archive('demo',assets+[(PROJECT/p,p) for p in ['project.godot','demo.tscn','demo.gd','README.md','reference/limestone_original.glb']])
archive('source',[(ROOT/'art-source/environment/limestone-study.blend','limestone-study.blend'),
                  (ROOT/'scene-demo/authoring/build_rock_study.py','build_rock_study.py'),(PACK/'README.md','README.md')])
archive('windows',[(ROOT/'builds/stone-study.exe','stone-study.exe'),(PACK/'README.md','README.md'),
                   (ROOT/'scene-demo/sunward_coast/docs/GODOT_NOTICES.txt','GODOT_NOTICES.txt')])
