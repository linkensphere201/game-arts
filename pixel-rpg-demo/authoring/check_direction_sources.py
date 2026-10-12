"""Verify runtime W actually uses independent art; audit declared mirror sources."""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
manifest=json.loads((ROOT/'production/pixel-rpg/model-wave-01/guided/unified-motion/manifest.json').read_text())
records={a['name']:a for a in manifest['animations']}
assert 'W' not in manifest['mirror_sources']
assert 'NW' not in manifest['mirror_sources']
assert not manifest['mirror_sources']
for name,record in records.items():
    path=ROOT/record['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256'],name
    for source in manifest['source_poses'][name]:
        assert 'derived_from_animation' not in source
        assert hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()==source['sha256']
for action in ('idle','walk','run'):
    name=action+'_W'
    for record in manifest['source_poses'][name]:
        assert 'derived_from_animation' not in record
        assert 'left-motion' in Path(record['path']).parts
        assert hashlib.sha256((ROOT/record['path']).read_bytes()).hexdigest()==record['sha256']
        alignment=record['alignment']
        assert hashlib.sha256((ROOT/alignment['source']).read_bytes()).hexdigest()==alignment['source_sha256']
    west=Image.open(ROOT/records[name]['path']).convert('RGBA')
    east=Image.open(ROOT/records[action+'_E']['path']).convert('RGBA')
    for i in range(records[name]['frames']):
        box=(96*i,0,96*(i+1),144)
        assert west.crop(box).tobytes()!=east.crop(box).transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes()
for action in ('idle','walk','run'):
    name=action+'_NW'
    for record in manifest['source_poses'][name]:
        assert 'derived_from_animation' not in record
        assert hashlib.sha256((ROOT/record['path']).read_bytes()).hexdigest()==record['sha256']
        assert ('rowan-NW-cloth-769002.png' in record['path']) if action=='idle' else ('nw-motion' in Path(record['path']).parts)
    west=Image.open(ROOT/records[name]['path']).convert('RGBA')
    east=Image.open(ROOT/records[action+'_NE']['path']).convert('RGBA')
    for i in range(records[name]['frames']):
        box=(96*i,0,96*(i+1),144)
        assert west.crop(box).tobytes()!=east.crop(box).transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes()
for action in ('idle','walk','run'):
    name=action+'_SW'
    for record in manifest['source_poses'][name]:
        assert ('rowan-SW-770001.png' in record['path']) if action=='idle' else ('sw-motion' in Path(record['path']).parts)
    west=Image.open(ROOT/records[name]['path']).convert('RGBA')
    east=Image.open(ROOT/records[action+'_SE']['path']).convert('RGBA')
    for i in range(records[name]['frames']):
        box=(96*i,0,96*(i+1),144)
        assert west.crop(box).tobytes()!=east.crop(box).transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes()
assert len({manifest['source_poses']['idle_'+d][0]['sha256'] for d in manifest['directions']})==8
for direction,source in manifest['mirror_sources'].items():
    for action in ('idle','walk','run'):
        record=records[action+'_'+direction]
        target=Image.open(ROOT/record['path']).convert('RGBA')
        original=Image.open(ROOT/records[action+'_'+source]['path']).convert('RGBA')
        for i in range(record['frames']):
            box=(96*i,0,96*(i+1),144)
            assert target.crop(box).tobytes()==original.crop(box).transpose(Image.Transpose.FLIP_LEFT_RIGHT).tobytes()
print('DIRECTION_SOURCE_QA_OK: eight distinct view sources; all source/sheet hashes verified; no mirrored heading')
