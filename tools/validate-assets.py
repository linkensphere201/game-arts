"""Validate the actual deliverable strips and their imported demo copies."""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
folder = ROOT / 'assets' / 'ember-imp'
report = {'checks': [], 'files': {}, 'limitations': 'Structural checks do not judge anatomy or animation quality.'}
colors = set()
for name, count in [('idle', 4), ('walk', 6)]:
    path = folder / f'{name}.png'
    image = Image.open(path)
    assert image.mode == 'RGBA', (name, image.mode)
    assert image.size == (64 * count, 64), (name, image.size)
    assert set(image.getchannel('A').get_flattened_data()) <= {0, 255}, name
    frames = []
    for i in range(count):
        frame = image.crop((64*i, 0, 64*(i+1), 64))
        bbox = frame.getchannel('A').getbbox()
        assert bbox and bbox[0] > 0 and bbox[1] > 0 and bbox[2] < 64 and bbox[3] < 64, (name, i, bbox)
        frames.append(hashlib.sha256(frame.tobytes()).hexdigest())
        colors.update(pixel[:3] for pixel in frame.get_flattened_data() if pixel[3])
    assert len(set(frames)) > 1, f'{name}: static duplicate frames'
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == hashlib.sha256((ROOT / 'demo' / 'ember_imp' / path.name).read_bytes()).hexdigest(), 'Demo/source drift'
    report['files'][path.name] = {'sha256': digest, 'frames': count, 'distinct_frames': len(set(frames)), 'size': list(image.size)}
assert len(colors) <= 32, len(colors)
for name in ['ember_imp.tscn', 'ember_imp_frames.tres', 'character.json']:
    assert (folder / name).read_bytes() == (ROOT / 'demo' / 'ember_imp' / name).read_bytes(), name
report['opaque_palette_size'] = len(colors)
report['checks'] = ['RGBA dimensions', 'binary alpha', 'nonempty unclipped frames', 'animated variation', 'shared palette <=32 colors', 'demo assets byte-identical to reusable package']
(ROOT / 'validation' / 'asset-checks.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
