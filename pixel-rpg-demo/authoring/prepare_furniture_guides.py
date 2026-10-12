"""Owned furniture composition guides for local-model redraw."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
for x,y in [(110,263),(354,263),(134,306),(377,306)]:
    d.polygon([(x,y),(x+25,y),(x+20,427),(x+2,427)],fill='#795338',outline='#473b30',width=6)
d.polygon([(92,244),(418,244),(414,308),(96,308)],fill='#795338',outline='#473b30',width=6)
d.polygon([(126,121),(386,121),(434,253),(77,253)],fill='#b39464',outline='#493f31',width=8)
d.polygon([(77,253),(434,253),(434,276),(77,276)],fill='#85613e',outline='#493f31',width=5)
for y in [149,182,219]:d.line((120-(y-121)*.37,y,392+(y-121)*.33,y),fill='#806542',width=4)
d.line((133,131,380,131),fill='#d2b681',width=5)
im.save(OUT/'table-layout.png')
im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
d.polygon([(113,102),(380,102),(402,424),(94,424)],fill='#755438',outline='#443b2f',width=8)
d.rectangle((122,124,372,398),fill='#423b30')
for y in [207,302,401]:d.rectangle((110,y,385,y+17),fill='#a17d4f',outline='#5f4930',width=4)
for y in [138,230,323]:
    for i,x in enumerate(range(137,353,37)):
        color=['#397a70','#bda575','#97684d','#536958'][i%4]
        d.rectangle((x,y+(i%2)*9,x+25,y+67),fill=color,outline='#343e32',width=3)
        d.line((x+3,y+22+(i%2)*9,x+22,y+22+(i%2)*9),fill='#c4a66a',width=3)
d.rectangle((99,109,122,431),fill='#a17d4f',outline='#443b2f',width=5)
d.rectangle((373,109,396,431),fill='#85623e',outline='#443b2f',width=5)
d.polygon([(111,75),(377,75),(401,109),(91,109)],fill='#b79763',outline='#443b2f',width=7)
im.save(OUT/'bookshelf-layout.png')
