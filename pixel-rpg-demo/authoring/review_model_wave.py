"""Contact sheets for human review of the local model batch. No acceptance is inferred."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
manifest=json.loads(Path(__file__).with_name('model-wave-01.json').read_text())
reviews={a['id']:a for a in json.loads(Path(__file__).with_name('model-wave-01-review.json').read_text(encoding='utf-8'))['assets']}
OUT=ROOT/'production/pixel-rpg/model-wave-01';(OUT/'review').mkdir(exist_ok=True)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14)
for category in ['character','building','prop','item']:
 assets=[a for a in manifest['assets'] if a['category']==category]
 height=432 if category=='character' else 312;cols=4;rows=(len(assets)+cols-1)//cols
 board=Image.new('RGB',(1024,rows*height+36),'#e3dcc9');d=ImageDraw.Draw(board);d.text((12,10),category.upper()+' / MODEL ORIGINALS / NOT FINAL SPRITES',font=font,fill='#252737')
 for i,a in enumerate(assets):
  x=i%cols*256;y=i//cols*height+36
  files=sorted((OUT/'originals').glob(a['id']+'-a*.png'),key=lambda f:int(f.stem.rsplit('-a',1)[1]))
  if files:
   im=Image.open(files[-1]).convert('RGB');im.thumbnail((250,height-52),Image.Resampling.LANCZOS);board.paste(im,(x+(256-im.width)//2,y))
  d.text((x+6,y+height-46),a['id']+(f' / a{files[-1].stem.rsplit(chr(97),1)[1]}' if files else ''),font=font,fill='#252737')
  d.text((x+6,y+height-24),reviews[a['id']]['status'].upper(),font=font,fill='#9b382e')
 board.save(OUT/'review'/f'{category}-originals.png')
print('Review boards refreshed')
