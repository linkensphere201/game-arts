"""Separate model-derived torso weight experiment; preserve stance pixels exactly."""
from pathlib import Path
import hashlib,json,sys
contact="--contact" in sys.argv
source_name="coordinated.png" if contact else "locked.png"
output_name="coordinated-weighted.png" if contact else "weighted.png"
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided/neris-stance'
if '--rear' in sys.argv:BASE=BASE.parent/'neris-rear-stance'
sheet=Image.open(BASE/source_name).convert('RGBA')
out=Image.new('RGBA',sheet.size)
records=[]
for i,(dx,dy) in enumerate(zip([-1,-1,-1,0,1,1,1,0],[0,1,0,-1,0,1,0,-1])):
    source=np.array(sheet.crop((i*96,0,(i+1)*96,144)))
    yy,xx=np.indices((144,96))
    weight=np.clip((100-yy)/15,0,1)
    sx=np.rint(xx-dx*weight).astype(int)
    sy=np.rint(yy-dy*weight).astype(int)
    valid=(sx>=0)&(sx<96)&(sy>=0)&(sy<144)
    target=np.zeros_like(source)
    target[valid]=source[sy[valid],sx[valid]]
    assert np.array_equal(source[100:],target[100:])
    assert set(np.unique(target[:,:,3]))=={0,255}
    assert np.array_equal(source[10:40,30:60],target[10+dy:40+dy,30+dx:60+dx])
    out.paste(Image.fromarray(target),(i*96,0))
    records.append({'frame':i,'upper_dx':dx,'upper_dy':dy,'fixed_from_row':100})
out.save(BASE/output_name)
(BASE/('contact-weight-study.json' if contact else 'weight-study.json')).write_text(json.dumps({'source_sha256':hashlib.sha256((BASE/source_name).read_bytes()).hexdigest(),'output_sha256':hashlib.sha256((BASE/output_name).read_bytes()).hexdigest(),'frames':records,'status':'unapproved torso sway/bob experiment','limitations':['nearest-neighbor waist transition may step','contact/arm correspondence remains subject to visual review','single direction only; not biomechanical validation']},indent=2))
print('NERIS_WEIGHT_EXPORT_OK: rigid head shift, binary alpha, all stance pixels unchanged')
