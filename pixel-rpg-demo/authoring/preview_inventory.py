"""Nearest-neighbor inventory review board; labels are not part of deliverable PNGs."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
names=['sword','shield','herb','coin','potion','crystal','book','key','scroll','bread','pouch','axe','ring','mushroom']
board=Image.new('RGB',(128*6,162*((len(names)+5)//6)),'#ded8c7');draw=ImageDraw.Draw(board)
for i,name in enumerate(names):
    im=Image.open(ROOT/'pixel-rpg-demo/mosslight/model_review'/f'{name}.png').convert('RGBA')
    assert im.size==(32,32)
    zoom=im.resize((128,128),Image.Resampling.NEAREST)
    x=(i%6)*128;y=(i//6)*162
    draw.text((x+8,y+4),name,fill='#33352e');board.paste(zoom,(x,y+28),zoom)
board.save(ROOT/'production/pixel-rpg/model-wave-01/guided/inventory-fourteen-review.png')
