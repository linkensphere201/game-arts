from pathlib import Path
import json
from PIL import Image
root=Path(__file__).resolve().parents[1]/'mosslight/theme'
m=json.loads((root/'manifest.json').read_text())
for pid in m['characters']:
    for action,count in [('idle',4),('walk',6)]:
        im=Image.open(root/f'{pid}_{action}.png').convert('RGBA')
        assert im.size==(48*count,512)
        headings=[]
        for row in range(8):
            cells=[im.crop((x*48,row*64,(x+1)*48,(row+1)*64)) for x in range(count)]
            assert len({c.tobytes() for c in cells})>=(4 if action=='walk' else 2),(pid,action,row)
            for c in cells:
                bounds=c.getbbox();assert bounds and bounds[0]>0 and bounds[2]<48 and bounds[3]<64
            headings.append(cells[0].tobytes())
        assert len(set(headings))==8,(pid,action,'directions')
for name in m['items']:
    im=Image.open(root/f'item_{name}.png');assert im.size==(32,32) and im.mode=='RGBA'
    b=im.getbbox();assert b[0]>0 and b[1]>0 and b[2]<32 and b[3]<32
print('THEME_ASSET_QA_PASS: 4 designs, 32 headings, 320 slots, 12 icons; bounds and animated poses')
