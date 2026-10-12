"""Check saved motion exports, including foot contact/flight, not art acceptance."""
from pathlib import Path
import hashlib
import json
import numpy as np
from scipy import ndimage
from PIL import Image

root = Path(__file__).resolve().parents[2]
out = root / 'production/pixel-rpg/model-wave-01/guided/motion'
manifest = json.loads((out / 'motion.json').read_text(encoding='utf-8'))
assert hashlib.sha256((root / manifest['source']).read_bytes()).hexdigest() == manifest['source_sha256']
hashes = set()
for action in ('walk', 'run'):
    sheet = Image.open(out / f'rowan-E-{action}.png')
    assert hashlib.sha256((out / f'rowan-E-{action}.png').read_bytes()).hexdigest() == manifest['sheet_sha256'][action]
    assert sheet.mode == 'RGBA' and sheet.size == (768, 128)
    bottoms = []
    for frame in range(8):
        cell = sheet.crop((frame*96, 0, (frame+1)*96, 128))
        alpha = np.asarray(cell.getchannel('A'))
        assert set(np.unique(alpha)) == {0, 255}
        assert ndimage.label(alpha > 0, structure=np.ones((3, 3)))[1] == 1, 'Detached garment pixels'
        left, top, right, bottom = cell.getbbox()
        assert 0 < left < right < 96 and 0 < top < bottom < 128, 'Clipped frame'
        bottoms.append(bottom)
        digest = hashlib.sha256(cell.tobytes()).hexdigest()
        assert digest not in hashes, 'Duplicate animation pose'
        hashes.add(digest)
    if action == 'walk':
        assert bottoms == [122]*8, 'Walk must remain grounded'
    else:
        assert min(bottoms) < 122 and max(bottoms) == 122, 'Run needs flight and contact'
    poses = [p for p in manifest['poses'] if p['action'] == action]
    for leg_index in range(2):
        for a, b in zip(poses, poses[1:]):
            la, lb = a['legs'][leg_index], b['legs'][leg_index]
            if not la['swing'] and not lb['swing']:
                # In world space, advancing the body must cancel the planted foot's backward travel.
                dx = (lb['ankle'][0] - la['ankle'][0]) * .18
                advance = manifest['suggested_travel_pixels_per_second'][action] * manifest['seconds_per_frame'][action]
                assert abs(dx + advance) < .001, 'Sliding stance or reversed gait'
            elif la['swing'] and lb['swing']:
                assert lb['ankle'][0] > la['ankle'][0], 'Recovery must travel forward'
assert max(leg['stretch'] for pose in manifest['poses'] for leg in pose['legs']) < 1.08
print('SIDE_MOTION_EXPORT_QA_OK: 16 distinct connected bounded RGBA frames; grounded walk, run flight; forward recovery, planted stance; stretch <8%')
