"""Structural crate guide for local-model redraw, not final game art."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
d.polygon([(124,181),(325,181),(325,390),(124,390)],fill='#a78054',outline='#51432f',width=5)
d.polygon([(325,181),(389,126),(389,331),(325,390)],fill='#7a603f',outline='#51432f',width=5)
d.polygon([(124,181),(184,126),(389,126),(325,181)],fill='#c5a274',outline='#51432f',width=5)
for x in [171,219,267]:d.line((x,185,x,385),fill='#705535',width=4)
for x in [180,230,280]:d.line((x,180,x+61,129),fill='#95744e',width=3)
d.rectangle((130,186,319,204),fill='#bb9568',outline='#665136',width=3)
d.rectangle((130,363,319,384),fill='#bb9568',outline='#665136',width=3)
d.polygon([(137,344),(150,360),(309,228),(295,212)],fill='#b59061',outline='#665136',width=4)
for x,y in [(134,190),(309,190),(134,373),(309,373)]:d.rectangle((x-5,y-5,x+5,y+5),fill='#aa925b',outline='#5b523d',width=2)
im.save(OUT/'crate-layout.png')
