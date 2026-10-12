from pathlib import Path
import json
from PIL import Image
root=Path(__file__).resolve().parents[1]
spec=json.loads((root/'authoring/art-spec.json').read_text(encoding='utf-8-sig'))
for action,count in [('idle',4),('walk',6)]:
    im=Image.open(root/'mosslight'/f'{action}.png').convert('RGBA')
    assert im.size==(48*count,512)
    headings=[]
    for row in range(8):
        cells=[im.crop((i*48,row*64,(i+1)*48,(row+1)*64)) for i in range(count)]
        unique=len({c.tobytes() for c in cells})
        assert unique>= (4 if action=='walk' else 2),(action,row,unique)
        for c in cells:
            bbox=c.getbbox();assert bbox and bbox[0]>0 and bbox[2]<48 and bbox[3]<64
        headings.append(cells[0].tobytes())
    assert len(set(headings))==8
for name in spec['props']:
    im=Image.open(root/'mosslight'/f'{name}.png')
    assert im.size==(96,96) and im.mode=='RGBA'
    assert im.getbbox()
assert len(spec['props'])==12
print('M5_ASSET_QA_PASS: 8 distinct headings, animated poses, dimensions, alpha margins, 12 props')
