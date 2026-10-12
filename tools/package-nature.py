"""Package three self-contained asset folders and a separate demo; all outputs local."""
from pathlib import Path
import re
import json
import hashlib
import zipfile

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT/'nature-demo'
VERSION='0.1.3'
ALLOWED={'.glb','.png','.gd','.gdshader','.tres','.tscn','.json','.md'}
results=[]
def archive(name,entries):
    entries=list(entries)
    assert len({n for _,n in entries})==len(entries)
    target=ROOT/'builds'/f'nature-{VERSION}-{name}.zip'
    manifest={n:hashlib.sha256(p.read_bytes()).hexdigest() for p,n in entries}
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
        for path,name in entries:z.write(path,name)
        z.writestr('SHA256.json',json.dumps(manifest,indent=2))
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        for name,digest in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==digest
    results.append({'name':target.name,'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'files':len(entries)})
    print(target.name,target.stat().st_size,flush=True)

all_assets=[]
sources=[]
for kind in ['ground','grass','tree']:
    pack=PROJECT/(kind+'_asset')
    files=sorted(p for p in pack.rglob('*') if p.is_file() and p.suffix in ALLOWED)
    for path in files:
        if path.suffix in {'.tres','.tscn','.gd','.gdshader'}:
            for ref in re.findall(r'res://[^"\s)]+',path.read_text(encoding='utf-8')):
                assert ref.startswith('res://'+kind+'_asset/'),(path,ref)
                assert (PROJECT/ref[6:]).is_file(),(path,ref)
    entries=[(p,p.relative_to(PROJECT).as_posix()) for p in files]
    archive(kind,entries)
    all_assets+=entries
    sources += [(p,p.relative_to(PROJECT).as_posix()) for p in files if p.suffix in {'.png','.md'}]
archive('demo',all_assets+[(PROJECT/p,p) for p in ['demo.gd','demo.tscn','project.godot','README.md']])
archive('sources',sources+[(ROOT/'art-source/nature'/p,p) for p in ['ground-grass.blend','coastal-tree.blend','grass-realistic-v2.blend','ground-realistic-v2.blend']]
    +[(PROJECT/'authoring'/p,'recipes/'+p) for p in ['build_nature.py','build_realistic_grass.py','build_tree.py','grass-presets.json','build_realistic_ground.py','ground-presets.json']])
archive('windows',[(ROOT/'builds/nature-study-0.1.3.exe','nature-study-0.1.3.exe'),(PROJECT/'README.md','README.md'),
    (ROOT/'scene-demo/sunward_coast/docs/GODOT_NOTICES.txt','GODOT_NOTICES.txt')])
(ROOT/'builds'/f'nature-{VERSION}-manifest.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
