"""Fresh-import each extracted asset archive alone, never delete existing projects."""
from pathlib import Path
from datetime import datetime
import shutil
import zipfile
import subprocess
import json
import argparse

ROOT=Path(__file__).resolve().parents[1]
GODOT=ROOT/'.local/godot/Godot_v4.7.2-stable_win64_console.exe'
BASE=ROOT/'.local'/('nature-fresh-'+datetime.now().strftime('%Y%m%d-%H%M%S'))
BASE.mkdir()
reports=[]
parser=argparse.ArgumentParser()
parser.add_argument('--only',choices=['ground','grass','tree','demo'])
only=parser.parse_args().only
for kind in ([only] if only else ['ground','grass','tree','demo']):
    target=BASE/kind
    target.mkdir()
    with zipfile.ZipFile(ROOT/'builds'/f'nature-0.1.3-{kind}.zip') as z:z.extractall(target)
    if kind!='demo':
        (target/'project.godot').write_text('config_version=5\n',encoding='utf-8')
        script='validate_tree.gd' if kind=='tree' else 'validate_samples.gd'
        shutil.copy2(ROOT/'nature-demo/authoring'/script,target/'verify.gd')
    for stage,args in [('import',['--editor','--import','--quit']),('load',
            ['--quit-after','120'] if kind=='demo' else ['--script','res://verify.gd','--quit-after','120'])]:
        p=subprocess.run([str(GODOT),'--headless','--path',str(target)]+args,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=60)
        log=p.stdout+p.stderr
        (ROOT/'validation/nature'/f'fresh-{kind}-{stage}.log').write_text(log,encoding='utf-8')
        assert p.returncode==0 and 'ERROR' not in log and 'Assertion failed' not in log,log[-2500:]
        if stage=='load' and kind!='demo':assert '_OK' in log
    reports.append({'asset':kind,'project':str(target),'pass':True})
    print('PASS independent',kind,flush=True)
(ROOT/'validation/nature'/('fresh-'+only+'-results.json' if only else 'fresh-results.json')).write_text(json.dumps(reports,indent=2),encoding='utf-8')
