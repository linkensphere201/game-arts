"""Coordinate existing model-derived arm poses with contact and passing legs."""
from pathlib import Path
import hashlib,json,sys
rear="--rear" in sys.argv
join=90 if rear else 92
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided/neris-stance'
if rear:BASE=BASE.parent/'neris-rear-stance'
SRC=ROOT/'pixel-rpg-demo/mosslight/model_review'
source=Image.open(BASE/'locked.png').convert('RGBA');out=source.copy();records=[]
# Contact: opposite arm forward. First passing pose returns toward neutral;
# the following half-step progresses toward the next contact arm extreme.
for frame,pose in [(0,'left-arm-stable'),(1,'left-arm-half-stable'),(4,'right-arm-stable'),(5,'right-arm-half-stable')]:
    if rear:pose='rear-'+pose.removesuffix('-stable')
    arm_path=SRC/f'neris-walk-{pose}.png'
    arms=Image.open(arm_path).convert('RGBA')
    original=source.crop((frame*96,0,(frame+1)*96,144))
    cell=original.copy();cell.paste(arms.crop((0,0,96,join)),(0,0))
    assert np.array_equal(np.array(cell)[join:],np.array(original)[join:])
    assert np.array_equal(np.array(cell)[:43],np.array(original)[:43])
    assert set(np.unique(np.array(cell)[:,:,3]))=={0,255}
    out.paste(cell,(frame*96,0))
    records.append({'frame':frame,'upper_pose':pose,'source_sha256':hashlib.sha256(arm_path.read_bytes()).hexdigest(),'join_row':join})
# Art-directed outer sleeve corridor at sprite resolution. This region contains
# upper sleeves only; preserve cuffs/hands, torso, keys, head and every leg pixel.
contours=[]
for frame in range(0 if rear else 8):
    cell=np.array(out.crop((96*frame,0,96*(frame+1),144)))
    original=cell.copy()
    for y in range(57,68):
        cell[y,:33]=0
        cell[y,63:]=0
        for x in (33,62):
            if cell[y,x,3]:
                # Reuse the established coat outline color, never add palette colors.
                cell[y,x,:3]=(65,43,49)
    changed=np.any(cell!=original,axis=2)
    assert not changed[:57].any() and not changed[68:].any()
    assert not changed[:,34:62].any()
    contours.append({'frame':frame,'changed_pixels':int(changed.sum())})
    out.paste(Image.fromarray(cell),(96*frame,0))
out.save(BASE/'coordinated.png')
(BASE/'contact-arm-study.json').write_text(json.dumps({'status':'unapproved coordinated contact/arm candidate','source_sha256':hashlib.sha256((BASE/'locked.png').read_bytes()).hexdigest(),'frames_changed':records,'sleeve_contour_cleanup':contours,'output_sha256':hashlib.sha256((BASE/'coordinated.png').read_bytes()).hexdigest(),'limitations':['join and sleeve contour need art review','no new model artwork; reuses recorded local-model poses','single direction walk experiment; run absent']},indent=2))
print('NERIS_CONTACT_ARMS_OK: contact opposition, head and lower legs preserved')
