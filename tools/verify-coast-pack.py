"""M3.5.3: fresh-copy and actual GLB geometry-reimport regression checks.
Edits only a new isolated test directory. Never deletes files.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import struct
import subprocess
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
GODOT = ROOT / '.local/godot/Godot_v4.7.2-stable_win64_console.exe'
OUT = ROOT / 'validation/coast-release'
TEST = ROOT / '.local' / ('pack-fresh-' + datetime.now().strftime('%Y%m%d-%H%M%S'))
TEST.mkdir()
shutil.copytree(ROOT / 'scene-demo/sunward_coast', TEST / 'sunward_coast',
                ignore=shutil.ignore_patterns('.godot', '*.import'))
(TEST / 'project.godot').write_text('config_version=5\n[application]\nconfig/name="Pack buyer test"\n[rendering]\nrenderer/rendering_method="forward_plus"\n')
for name in ('validate_pack.gd', 'probe_reimport.gd'):
    shutil.copy2(ROOT / 'scene-demo/authoring' / name, TEST / name)

def run(name, *args):
    result = subprocess.run([str(GODOT), '--headless', '--path', str(TEST), *args],
                            capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60)
    text = result.stdout + result.stderr
    (OUT / name).write_text(text, encoding='utf-8')
    assert result.returncode == 0 and 'ERROR:' not in text and 'FAIL ' not in text, text[-3000:]
    return text

run('fresh-import.log', '--editor', '--import', '--quit')
run('fresh-controls.log', '--script', 'res://validate_pack.gd', '--quit-after', '500')
before = run('reimport-before.log', '--script', 'res://probe_reimport.gd')
wrapper = TEST / 'sunward_coast/props/coastal_tree.tscn'
wrapper_hash = hashlib.sha256(wrapper.read_bytes()).hexdigest()
model = TEST / 'sunward_coast/meshes/coastal_tree.glb'
data = model.read_bytes()
json_size = struct.unpack_from('<I', data, 12)[0]
doc = json.loads(data[20:20+json_size])
binary_start = 20 + json_size + 8
binary = bytearray(data[binary_start:])
accessors = {p['attributes']['POSITION'] for m in doc['meshes'] for p in m['primitives']}
for index in accessors:
    accessor = doc['accessors'][index]
    assert accessor['componentType'] == 5126 and accessor['type'] == 'VEC3'
    view = doc['bufferViews'][accessor['bufferView']]
    start = view.get('byteOffset', 0) + accessor.get('byteOffset', 0)
    stride = view.get('byteStride', 12)
    for vertex in range(accessor['count']):
        offset = start + vertex*stride
        x = struct.unpack_from('<f', binary, offset)[0]
        struct.pack_into('<f', binary, offset, x*1.2)
    accessor['min'][0] *= 1.2
    accessor['max'][0] *= 1.2
encoded = json.dumps(doc, separators=(',', ':')).encode()
encoded += b' ' * ((-len(encoded)) % 4)
total = 12+8+len(encoded)+8+len(binary)
model.write_bytes(struct.pack('<III',0x46546C67,2,total)+struct.pack('<II',len(encoded),0x4E4F534A)+encoded+
                  struct.pack('<II',len(binary),0x004E4942)+binary)
run('reimport-import.log', '--editor', '--import', '--quit')
after = run('reimport-after.log', '--script', 'res://probe_reimport.gd')
old = float(re.search(r'REIMPORT_WIDTH=([\d.]+)', before)[1])
new = float(re.search(r'REIMPORT_WIDTH=([\d.]+)', after)[1])
assert abs(new/old-1.2) < .002
assert hashlib.sha256(wrapper.read_bytes()).hexdigest() == wrapper_hash
report = {'fresh_project':str(TEST),'copied_folder_only':True,'source_width_before':old,
          'source_width_after':new,'width_ratio':new/old,'wrapper_unchanged':True,
          'collision_configuration_preserved':True,
          'note':'Model geometry updates; collider remains configured separately and must be reviewed after shape changes.'}
(OUT / 'fresh-reimport.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
