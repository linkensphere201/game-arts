"""Technical checks for the isolated W study, not artistic acceptance."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from scipy import ndimage
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided/left-motion'
manifest=json.loads((OUT/'export.json').read_text())
alignment=manifest['alignment']
assert hashlib.sha256((ROOT/alignment['source']).read_bytes()).hexdigest()==alignment['source_sha256']
assert hashlib.sha256((OUT/'canonical-source.png').read_bytes()).hexdigest()==alignment['canonical_sha256']
seen=set()
for action in ('walk','run'):
    sheet=Image.open(OUT/f'{action}_W.png')
    assert sheet.size==(768,144) and sheet.mode=='RGBA'
    bottoms=[]
    for i in range(8):
        cell=sheet.crop((96*i,0,96*(i+1),144));a=np.asarray(cell)[:,:,3]
        assert set(np.unique(a))=={0,255}
        assert ndimage.label(a>0,structure=np.ones((3,3)))[1]==1,'Detached body/cloth component'
        left,top,right,bottom=cell.getbbox()
        assert 0<left<right<96 and 0<top<bottom<144
        digest=hashlib.sha256(cell.tobytes()).hexdigest()
        assert digest not in seen;seen.add(digest);bottoms.append(bottom)
        path=OUT/'rig'/f'{action}-{i}-source.png'
        assert hashlib.sha256(path.read_bytes()).hexdigest()==manifest['frames'][action][i]['source_sha256']
    assert bottoms==[122]*8 if action=='walk' else min(bottoms)<122 and max(bottoms)==122
print('LEFT_MOTION_QA_OK: 16 distinct bounded connected frames; walk contact and run flight')
