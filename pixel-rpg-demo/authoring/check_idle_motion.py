"""Verify exported breathing cycles preserve contact and return through a repeated pose."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided/unified-motion'
m=json.loads((OUT/'manifest.json').read_text())
board=Image.new('RGB',(768,576),'#ded8ca');draw=ImageDraw.Draw(board)
for index,direction in enumerate(m['directions']):
 record=next(r for r in m['animations'] if r['name']=='idle_'+direction)
 path=ROOT/record['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256']
 assert record['frames']==4 and record['fps']==2
 sheet=Image.open(path).convert('RGBA');assert sheet.size==(384,144)
 cells=[sheet.crop((96*i,0,96*(i+1),144)) for i in range(4)]
 assert cells[1].tobytes()==cells[3].tobytes()
 assert len({c.tobytes() for c in cells})==3
 for c in cells[1:]:
  assert np.array_equal(np.asarray(c)[82:],np.asarray(cells[0])[82:]),direction
 for f,c in enumerate(cells[:3]):
  board.paste(c,(index*96,f*184+24),c)
 draw.text((index*96+8,4),direction,fill='#29333a')
board.save(OUT/'idle-review.png')
print('IDLE_QA_OK: 8 loops, 2 seconds, 3 distinct poses each, exact lower-body preservation')
