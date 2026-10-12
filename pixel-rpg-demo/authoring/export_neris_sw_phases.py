"""Compose separate local-model arm/leg poses with an explicit phase map."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'pixel-rpg-demo/mosslight/model_review';OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'
legs=['near-contact','near-down','near-passing','near-up','far-contact','far-down','far-passing','far-up']
arms=['near-twoarm','near-twoarm-half','far-passing','far-twoarm-half','far-twoarm','far-twoarm-half','near-passing','near-twoarm-half']
sheet=Image.new('RGBA',(768,144));records=[]
for i,(leg,arm) in enumerate(zip(legs,arms)):
    lp=SRC/f'neris-walk-SW-{leg}.png';ap=SRC/f'neris-walk-SW-{arm}.png'
    lower=Image.open(lp).convert('RGBA');upper=Image.open(ap).convert('RGBA');cell=lower.copy()
    cell.paste(upper.crop((0,0,96,90)),(0,0))
    assert np.array_equal(np.array(cell)[90:],np.array(lower)[90:])
    assert np.array_equal(np.array(cell)[:49],np.array(lower)[:49])
    assert set(np.unique(np.array(cell)[:,:,3]))=={0,255}
    sheet.paste(cell,(96*i,0))
    records.append({'frame':i,'leg':leg,'arm':arm,'leg_sha256':hashlib.sha256(lp.read_bytes()).hexdigest(),'arm_sha256':hashlib.sha256(ap.read_bytes()).hexdigest()})
sheet.save(OUT/'neris-SW-complete-phase-study.png')
(OUT/'neris-SW-complete-phase-study.json').write_text(json.dumps({'status':'unapproved in-place phase study','join_row':90,'fps':8,'frames':records,'missing':['shading and join polish','travel and stance lock','run']},indent=2))
print('NERIS_SW_PHASE_OK: independent arm/leg phase map, protected head and legs')
