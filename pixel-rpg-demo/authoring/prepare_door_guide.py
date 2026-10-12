"""Owned plain timber door layout for the local illustration route."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
d.rectangle((131,54,381,460),fill='#574736',outline='#393c30',width=8)
d.rectangle((154,76,357,444),fill='#977449',outline='#c0a274',width=8)
for x in [198,240,282,324]:d.line((x,86,x,435),fill='#604b34',width=5)
for y in [138,362]:d.rectangle((158,y,354,y+24),fill='#725438',outline='#514430',width=4)
d.rectangle((130,47,382,76),fill='#a48153',outline='#4a4030',width=6)
d.ellipse((320,254,343,280),fill='#c4a262',outline='#635334',width=5)
d.rectangle((123,447,390,470),fill='#b59c71',outline='#514733',width=5)
im.save(OUT/'door-layout.png')
