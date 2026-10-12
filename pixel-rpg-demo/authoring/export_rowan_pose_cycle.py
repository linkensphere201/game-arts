"""Sequence model-authored leg poses for visual review, not a locomotion animation."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];ASSETS=ROOT/'pixel-rpg-demo/mosslight/model_review'
parser=argparse.ArgumentParser();parser.add_argument('--arms',action='store_true');parser.add_argument('--contact',action='store_true');args=parser.parse_args()
if args.contact:args.arms=True
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'/('contact-cycle' if args.contact else 'coordinated-cycle' if args.arms else 'keypose-cycle');OUT.mkdir(exist_ok=True)
names=['rowan-keypose-neutral','rowan-front-knee-771005','rowan-front-knee-771003','rowan-front-knee-771005','rowan-keypose-neutral','rowan-front-knee-771006','rowan-front-knee-771004','rowan-front-knee-771006']
if args.arms:names=['rowan-keypose-neutral','rowan-front-knee-771009','rowan-front-knee-771011','rowan-front-knee-771009','rowan-keypose-neutral','rowan-front-knee-771010','rowan-front-knee-771012','rowan-front-knee-771010']
if args.contact:names[0]='rowan-front-knee-771014';names[4]='rowan-front-knee-771013'
fixed_rows=54 if args.arms else 75
sheet=Image.new('RGBA',(768,144));gif=[];records=[];upper=None;unique=set()
for i,name in enumerate(names):
    path=ASSETS/(name+'.png');cell=Image.open(path).convert('RGBA');a=np.asarray(cell)
    assert cell.size==(96,144) and set(np.unique(a[:,:,3]))=={0,255}
    assert 0<cell.getbbox()[0]<cell.getbbox()[2]<96 and 0<cell.getbbox()[1]<cell.getbbox()[3]<144
    if upper is None:upper=a[:fixed_rows].copy()
    else:assert np.array_equal(upper,a[:fixed_rows])
    unique.add(hashlib.sha256(cell.tobytes()).hexdigest());sheet.alpha_composite(cell,(96*i,0))
    preview=Image.new('RGBA',(288,432),'#ded8ca');d=ImageDraw.Draw(preview)
    d.ellipse((117,361,171,373),fill='#a7a497');preview.alpha_composite(cell.resize((288,432),Image.Resampling.NEAREST));gif.append(preview.convert('RGB'))
    soles={side:94+cell.crop((left,94,right,144)).getbbox()[3] for side,left,right in [('left',33,48),('right',49,64)]}
    records.append({'frame':i,'source':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sole_y':soles})
assert len(unique)==(6 if args.contact else 5)
sheet.save(OUT/'leg-poses.png')
gif[0].save(OUT/'leg-poses.gif',save_all=True,append_images=gif[1:],duration=120,loop=0)
contact_drift=[]
if args.contact:
    for start,side in [(0,'left'),(4,'right')]:
        for i in range(start,start+3):
            contact_drift.append({'from_frame':i,'leg':side,'world_y_drift_at_65px_s':65*.12+records[i+1]['sole_y'][side]-records[i]['sole_y'][side]})
(OUT/'manifest.json').write_text(json.dumps({'frames':records,'fps':1000/120,'unique_poses':len(unique),'cell':[96,144],'arm_coordination':args.arms,'contact_poses':args.contact,'contact_drift':contact_drift,'protected_rows':fixed_rows,'sheet_sha256':hashlib.sha256((OUT/'leg-poses.png').read_bytes()).hexdigest(),'status':'isolated pose loop; not walking/running animation','limitations':['torso fixed; arm poses supplied only in coordinated variant','stance does not cancel world movement','contact pose does not prove weight transfer; cloth animation absent']},indent=2),encoding='utf-8')
print(f'KEYPOSE_CYCLE_OK: 8 timeline frames, {len(unique)} unique poses, identical upper rows; no locomotion claim')
if contact_drift:print('RASTER_CONTACT_DRIFT:',json.dumps(contact_drift))
