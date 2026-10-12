"""Compose separate local-model arm/leg poses with an explicit phase map."""
from pathlib import Path
import json,hashlib,sys
compact="--compact" in sys.argv
complete="--leg-transitions" in sys.argv or compact
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'pixel-rpg-demo/mosslight/model_review';OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'
legs=['near-contact','far-passing','far-passing','far-passing','far-contact','near-passing','near-passing','near-passing']
if complete:legs=['near-contact','near-down','far-passing','near-up','far-contact','far-down','near-passing','far-up']
if compact:legs=['near-compact','near-compact-down','far-passing','near-compact-up','far-compact','far-compact-down','near-passing','far-compact-up']
arms=['near-arm','near-arm-half','far-passing','far-arm-half','far-arm','far-arm-half','near-passing','near-arm-half']
sheet=Image.new('RGBA',(768,144));records=[]
for i,(leg,arm) in enumerate(zip(legs,arms)):
    lp=SRC/f'neris-walk-east-{leg}.png';ap=SRC/f'neris-walk-east-{arm}.png'
    lower=Image.open(lp).convert('RGBA');upper=Image.open(ap).convert('RGBA');cell=lower.copy()
    cell.paste(upper.crop((0,0,96,85)),(0,0))
    assert np.array_equal(np.array(cell)[85:],np.array(lower)[85:])
    assert np.array_equal(np.array(cell)[:43],np.array(lower)[:43])
    assert set(np.unique(np.array(cell)[:,:,3]))=={0,255}
    sheet.paste(cell,(96*i,0))
    records.append({'frame':i,'leg':leg,'arm':arm,'leg_sha256':hashlib.sha256(lp.read_bytes()).hexdigest(),'arm_sha256':hashlib.sha256(ap.read_bytes()).hexdigest()})
sheet.save(OUT/('neris-east-compact-phase-study.png' if compact else 'neris-east-complete-phase-study.png' if complete else 'neris-east-phase-study.png'))
(OUT/('neris-east-compact-phase-study.json' if compact else 'neris-east-complete-phase-study.json' if complete else 'neris-east-phase-study.json')).write_text(json.dumps({'status':'unapproved in-place phase study','join_row':85,'fps':8,'frames':records,'missing':['down/up leg transitions','shading and join polish','travel and stance lock','run']},indent=2))
print('NERIS_EAST_PHASE_OK: independent arm/leg phase map, protected head and legs')
