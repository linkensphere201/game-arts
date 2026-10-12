"""Original UI frame guide for local-model redraw; no baked text."""
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[2]
im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
d.rounded_rectangle((48,48,464,464),18,fill='#b39464',outline='#3e3c30',width=9)
d.rounded_rectangle((66,66,446,446),9,fill='#344e48',outline='#ddc58c',width=5)
d.rectangle((81,81,431,431),fill='#344e48',outline='#647b64',width=4)
for x,y in [(66,66),(446,66),(66,446),(446,446)]:
    d.polygon([(x,y-12),(x+12,y),(x,y+12),(x-12,y)],fill='#d3b674',outline='#695634',width=3)
im.save(root/'production/pixel-rpg/model-wave-01/guided/panel-layout.png')
