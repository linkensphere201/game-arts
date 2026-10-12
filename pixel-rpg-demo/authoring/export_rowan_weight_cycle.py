"""Add restrained weight transfer to model-authored poses, keeping boots fixed."""
from pathlib import Path
import hashlib
import json
import argparse
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
SOURCE=BASE/'support-cycle'
parser=argparse.ArgumentParser()
parser.add_argument('--phased-arms',action='store_true')
args=parser.parse_args()
OUT=BASE/('phased-cycle' if args.phased_arms else 'weight-cycle')
OUT.mkdir(exist_ok=True)
meta=json.loads((SOURCE/'manifest.json').read_text())
assert hashlib.sha256((SOURCE/'leg-poses.png').read_bytes()).hexdigest()==meta['sheet_sha256']
sheet=Image.open(SOURCE/'leg-poses.png').convert('RGBA')
result=Image.new('RGBA',sheet.size)
offsets=[(-1,1),(-1,2),(-1,0),(0,-1),(1,1),(1,2),(1,0),(0,-1)]
records=[]
previews=[]
for frame,(dx,dy) in enumerate(offsets):
    cell=sheet.crop((frame*96,0,(frame+1)*96,144))
    arm_source=None
    if args.phased_arms:
        # Contact extremes -> return -> neutral passing -> opposite advance.
        donors=[771015,771010,None,771009,771016,771009,None,771010]
        seed=donors[frame]
        name=f'rowan-front-knee-{seed}.png' if seed else 'rowan-keypose-neutral.png'
        path=ROOT/'pixel-rpg-demo/mosslight/model_review'/name
        donor=Image.open(path).convert('RGBA')
        assert donor.size==cell.size
        cell.paste(donor.crop((0,0,96,81)),(0,0))
        arm_source=dict(path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    source=np.array(cell)
    target=source.copy()
    target[:88]=0
    # Rigid face/torso through row 74; a short tunic/thigh band joins fixed legs.
    # Support boot begins at row 89 at its highest position, so it stays intact.
    for y in range(88):
        if y<75+dy:
            sy=y-dy
            shift=dx
        else:
            sy=round(75+(y-75-dy)*13/(13-dy))
            shift=round(dx*(88-y)/(13-dy))
        if not 0<=sy<88:continue
        if shift>0:target[y,shift:]=source[sy,:96-shift]
        elif shift<0:target[y,:96+shift]=source[sy,-shift:]
        else:target[y]=source[sy]
    assert np.array_equal(target[88:],source[88:])
    assert set(np.unique(target[:,:,3]))=={0,255}
    # Verify rigid upper-body pixels survive as a translated block.
    for sy in range(5,75):
        for sx in range(5,91):
            assert np.array_equal(target[sy+dy,sx+dx],source[sy,sx])
    output=Image.fromarray(target)
    result.paste(output,(frame*96,0))
    preview=Image.new('RGBA',(288,432),'#ded8ca')
    ImageDraw.Draw(preview).ellipse((117,361,171,373),fill='#a7a497')
    preview.alpha_composite(output.resize((288,432),Image.Resampling.NEAREST))
    previews.append(preview.convert('RGB'))
    records.append(dict(frame=frame,torso_offset=[dx,dy],lower_rows_unchanged_from=88,arm_source=arm_source))
result.save(OUT/'leg-poses.png')
result.resize((2304,432),Image.Resampling.NEAREST).save(OUT/'review-sheet.png')
previews[0].save(OUT/'leg-poses.gif',save_all=True,append_images=previews[1:],duration=[60,70,60,60]*2,loop=0)
(OUT/'manifest.json').write_text(json.dumps(dict(
    frames=records,fps=16,source_sheet_sha256=meta['sheet_sha256'],
    sheet_sha256=hashlib.sha256((OUT/'leg-poses.png').read_bytes()).hexdigest(),
    status='isolated weight-transfer candidate; art review pending',
    limitations=['compressed thigh band retained','arm transitions need silhouette review','no independent cloth motion',
                 'sampled stance inherited; held-frame sliding remains']
),indent=2),encoding='utf-8')
print('WEIGHT_CYCLE_OK: eight frames; rigid upper art preserved; all lower pixels unchanged')
