"""Composition guides for local-model tree and rock studies."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
d.polygon([(226,250),(285,250),(284,409),(319,455),(269,449),(249,434),(212,450),(190,453),(221,409)],fill='#795c40',outline='#3c4333',width=7)
d.line((251,300,253,413),fill='#b29360',width=10)
d.line((248,328,192,274),fill='#795c40',width=20)
d.line((265,317,322,260),fill='#795c40',width=18)
for box,c in [((84,174,428,341),'#416650'),((56,115,264,288),'#648360'),((243,103,449,279),'#4d7356'),((128,48,353,266),'#779267'),((155,57,300,159),'#92a575')]:
    d.ellipse(box,fill=c,outline='#385340',width=6)
for x,y in [(124,192),(215,153),(299,210),(365,168),(186,265)]:
    d.arc((x-25,y-10,x+24,y+29),190,340,fill='#344e3b',width=5)
im.save(OUT/'tree-layout.png')
im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
d.polygon([(78,344),(91,236),(162,143),(288,104),(387,163),(440,288),(411,368),(306,411),(162,400)],fill='#899183',outline='#444e45',width=8)
d.polygon([(91,236),(162,143),(288,104),(307,238),(183,279)],fill='#b2b6a1',outline='#717a69',width=4)
d.polygon([(307,238),(387,163),(440,288),(411,368),(308,411)],fill='#68776b',outline='#535f54',width=4)
d.line((160,145,184,280,152,347),fill='#677362',width=6)
d.line((185,280,274,266,308,239),fill='#566451',width=5)
d.polygon([(87,337),(147,315),(179,353),(169,395),(113,382)],fill='#687e51')
d.polygon([(288,106),(322,126),(291,152),(245,151)],fill='#829459')
im.save(OUT/'rock-layout.png')
