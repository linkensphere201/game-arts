"""Neris contact/lift sequence with a rigid support-foot translation experiment."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];SRC=ROOT/'pixel-rpg-demo/mosslight/model_review'
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided/neris-stance';OUT.mkdir(exist_ok=True)
poses=['contact-left','right-arm-half-stable','right-arm-stable','right-arm-half-stable','contact-right','left-arm-half-stable','left-arm-stable','left-arm-half-stable']
fps,speed=12,24
naive=Image.new('RGBA',(768,144));locked=Image.new('RGBA',(768,144));records=[]
for i,pose in enumerate(poses):
    path=SRC/f'neris-walk-{pose}.png';im=Image.open(path).convert('RGBA');cell=im.copy()
    side='left' if i<4 else 'right';x0,x1=(28,48) if side=='left' else (49,68)
    box=im.crop((x0,103,x1,144)).getbbox();assert box;sole=103+box[3]
    phase=i%4
    if phase==0:initial=sole
    target=initial-round(speed*phase/fps);shift=target-sole
    hip,cuff=100,112
    assert hip<cuff+shift and shift<=1
    boot=im.crop((x0,cuff,x1,144))
    cell.paste((0,0,0,0),(x0,hip,x1,144))
    thigh=im.crop((x0,hip,x1,cuff)).resize((x1-x0,cuff+shift-hip),Image.Resampling.NEAREST)
    cell.paste(thigh,(x0,hip));cell.paste(boot,(x0,cuff+shift))
    assert cell.crop((x0,cuff+shift,x1,144+shift)).tobytes()==boot.tobytes()
    measured=100+cell.crop((x0,100,x1,144)).getbbox()[3];assert measured==target
    assert np.array_equal(np.asarray(im)[:100],np.asarray(cell)[:100])
    assert {j for j,c in enumerate(cell.getchannel('A').histogram()) if c}=={0,255}
    naive.paste(im,(96*i,0));locked.paste(cell,(96*i,0))
    records.append({'frame':i,'pose':pose,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'support':side,'naive_sole':sole,'locked_sole':measured,'boot_shift':shift})
for start in (0,4):
    assert len({speed*i/fps+records[i]['locked_sole'] for i in range(start,start+4)})==1
naive.save(OUT/'naive.png');locked.save(OUT/'locked.png')
(OUT/'manifest.json').write_text(json.dumps({'fps':fps,'speed':speed,'frames':records,'status':'unapproved forward gait/stance experiment','limitations':['contact arms are neutral','lower coat/thigh compression requires review','no torso weight transfer','discrete frames allow up to 2 pixels hold drift','single direction only']},indent=2))
print('NERIS_STANCE_EXPORT_OK: rigid support boot preserved, exact sampled stance lock; candidate only')
