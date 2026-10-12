"""Owned upright wooden chair guide; local model redraw is the artwork source."""
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[2]
im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
dark='#473b30';wood='#96724b';light='#b39464'
# Rear posts continue into legs, with two horizontal backrest rails.
for x in [162,327]:
    d.polygon([(x,72),(x+22,72),(x+23,419),(x+4,419)],fill=wood,outline=dark,width=5)
for y in [85,150]:
    d.rectangle((178,y,333,y+31),fill=light,outline=dark,width=5)
# Raised camera reveals the seat top while preserving a square-grid front view.
d.polygon([(170,255),(341,255),(375,329),(132,329)],fill=light,outline=dark,width=6)
for y in [277,302]:d.line((162-(y-255)*.3,y,348+(y-255)*.3,y),fill='#806542',width=3)
d.polygon([(132,329),(375,329),(375,347),(132,347)],fill='#795338',outline=dark,width=4)
for x in [140,344]:
    d.polygon([(x,346),(x+22,346),(x+18,437),(x,437)],fill=wood,outline=dark,width=5)
im.save(root/'production/pixel-rpg/model-wave-01/guided/chair-layout.png')
