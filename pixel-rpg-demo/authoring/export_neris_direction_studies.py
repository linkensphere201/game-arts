"""Export eight static direction studies, explicitly without animation clips."""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'
REG=json.loads(Path(__file__).with_name('roster-static-studies.json').read_text())
ORDER=[('S','neris'),('SW','neris-SW'),('W','neris-W'),('NW','neris-NW'),('N','neris-back'),('NE','neris-NE'),('E','neris-side'),('SE','neris-SE')]
atlas=Image.new('RGBA',(768,144));entries=[]
for index,(heading,asset) in enumerate(ORDER):
    path=ROOT/'pixel-rpg-demo/mosslight/model_review'/f'{asset}.png'
    im=Image.open(path).convert('RGBA')
    assert im.size==(96,144) and im.getbbox()[3]==122
    assert {i for i,count in enumerate(im.getchannel('A').histogram()) if count}=={0,255}
    atlas.paste(im,(index*96,0))
    entries.append({'heading':heading,'rect':[index*96,0,96,144],'sprite':str(path.relative_to(ROOT)),'sprite_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source':REG[asset]['source'],'source_sha256':hashlib.sha256((ROOT/REG[asset]['source']).read_bytes()).hexdigest(),'status':REG[asset]['status']})
assert len({e['sprite_sha256'] for e in entries})==8
atlas.save(OUT/'neris-direction-studies.png')
(OUT/'neris-direction-studies.json').write_text(json.dumps({'status':'unapproved static turnaround; not an animation sheet','cell':[96,144],'foot_anchor_y':122,'clips':[],'directions':entries,'atlas_sha256':hashlib.sha256((OUT/'neris-direction-studies.png').read_bytes()).hexdigest()},indent=2))
print('NERIS_STATIC_ATLAS_OK: 8 individually sourced headings, binary alpha, sole122; zero animation clips')
