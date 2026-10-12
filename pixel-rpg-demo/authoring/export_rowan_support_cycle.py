"""Isolated raster stance experiment; preserve boot pixels by rigid translation."""
from pathlib import Path
import hashlib
import json

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'production/pixel-rpg/model-wave-01/guided'
OUT = BASE / 'support-cycle'
OUT.mkdir(exist_ok=True)
manifest = json.loads((BASE / 'contact-cycle/manifest.json').read_text())
fps, speed = 16, 65
cells, records = [], []
for i, record in enumerate(manifest['frames']):
    source = ROOT / record['source']
    assert hashlib.sha256(source.read_bytes()).hexdigest() == record['sha256']
    original = Image.open(source).convert('RGBA')
    cell = original.copy()
    side = 'left' if i < 4 else 'right'
    left, right = (33, 48) if side == 'left' else (49, 64)
    phase = i % 4
    initial = manifest['frames'][i - phase]['sole_y'][side]
    target = round(initial - speed * phase / fps)
    shift = target - record['sole_y'][side]
    # Below the tunic: shorten only exposed thigh, retaining every boot pixel.
    hip, cuff = 85, 96
    assert hip < cuff + shift and shift <= 1
    bottom = original.getbbox()[3]
    boot = original.crop((left, cuff, right, bottom))
    if shift:
        cell.paste((0, 0, 0, 0), (left, hip, right, 144))
        thigh = original.crop((left, hip, right, cuff))
        thigh = thigh.resize((right-left, cuff+shift-hip), Image.Resampling.NEAREST)
        cell.paste(thigh, (left, hip))
        cell.paste(boot, (left, cuff+shift))
    assert cell.crop((left, cuff+shift, right, bottom+shift)).tobytes() == boot.tobytes()
    assert np.array_equal(np.asarray(cell)[:hip], np.asarray(original)[:hip])
    assert set(np.unique(np.asarray(cell)[:, :, 3])) == {0, 255}
    sole = 94 + cell.crop((left, 94, right, 144)).getbbox()[3]
    assert sole == target
    cells.append(cell)
    records.append(dict(frame=i, source=record['source'], source_sha256=record['sha256'],
                        support=side, sole_y=sole, boot_shift_y=shift,
                        rigid_boot_preserved=True))
drift = []
for start in (0, 4):
    for i in range(start, start+3):
        error = speed/fps + records[i+1]['sole_y'] - records[i]['sole_y']
        assert abs(error) <= 1
        drift.append(dict(from_frame=i, world_y_drift=error))
sheet = Image.new('RGBA', (768,144))
previews = []
for i, cell in enumerate(cells):
    sheet.paste(cell, (96*i, 0))
    preview = Image.new('RGBA', (288,432), '#ded8ca')
    ImageDraw.Draw(preview).ellipse((117,361,171,373), fill='#a7a497')
    preview.alpha_composite(cell.resize((288,432), Image.Resampling.NEAREST))
    previews.append(preview.convert('RGB'))
sheet.save(OUT/'leg-poses.png')
sheet.resize((2304,432), Image.Resampling.NEAREST).save(OUT/'review-sheet.png')
previews[0].save(OUT/'leg-poses.gif', save_all=True, append_images=previews[1:], duration=60, loop=0)
(OUT/'manifest.json').write_text(json.dumps(dict(
    frames=records, fps=fps, movement_speed=speed, contact_drift=drift,
    sheet_sha256=hashlib.sha256((OUT/'leg-poses.png').read_bytes()).hexdigest(),
    status='isolated support-foot experiment; not integrated or art accepted',
    limitations=['stance checked only at sampled frames, not between frames',
                 'thigh compression and cuff seams require visual review',
                 'fixed torso, neutral contact arms, no cloth simulation',
                 'GIF uses 60 ms timing; Godot uses exact 16 fps']
), indent=2), encoding='utf-8')
print('SUPPORT_CYCLE_OK: rigid boots unchanged; six sampled stance intervals within 1 px')
