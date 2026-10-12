"""Owned barrel layout guide for local model redrawing; not final game art."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
d.polygon([(158,150),(354,150),(374,244),(360,362),(339,396),(170,396),(150,356),(138,244)],fill='#98734e',outline='#4e4438',width=5)
d.ellipse((154,349,358,418),fill='#8b6746',outline='#4e4438',width=5)
for x in [175,205,235,266,297,327]:d.line([(x,174),(x-8 if x<250 else x+8,275),(x,391)],fill='#614b36',width=4)
for y in [201,325]:
 d.polygon([(145,y),(364,y),(368,y+23),(143,y+23)],fill='#657371',outline='#3d4c48',width=4)
 d.arc((143,y-20,368,y+25),0,180,fill='#91a29a',width=3)
d.ellipse((156,105,356,188),fill='#b3966b',outline='#4e4438',width=6)
d.ellipse((169,115,342,176),fill='#a88a60',outline='#736047',width=4)
for y in [132,151]:d.line((181,y,331,y),fill='#786247',width=3)
im.save(OUT/'barrel-layout.png')
