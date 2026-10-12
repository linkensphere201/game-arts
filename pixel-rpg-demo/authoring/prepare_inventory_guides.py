"""Owned shape guides for local-model inventory illustration redraws."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
d.ellipse((139,191,373,430),fill='#85b8aa',outline='#355b56',width=7)
d.polygon([(139,296),(373,296),(355,374),(313,421),(199,421),(157,374)],fill='#358a7e')
d.ellipse((142,273,370,319),fill='#54a89a',outline='#366d66',width=4)
d.rounded_rectangle((210,132,300,229),radius=12,fill='#a9c9b6',outline='#355b56',width=6)
d.rounded_rectangle((216,99,294,161),radius=8,fill='#b48c57',outline='#655038',width=6)
d.line((181,245,166,288,171,326),fill='#cee0ca',width=10)
d.polygon([(257,315),(276,338),(257,362),(238,338)],fill='#c7a463',outline='#76623c',width=4)
im.save(OUT/'potion-layout.png')
im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
d.polygon([(254,88),(355,221),(326,365),(255,430),(160,365),(139,225)],fill='#318d89',outline='#284e50',width=7)
d.polygon([(254,88),(254,220),(139,225)],fill='#9ed8bc',outline='#406f69',width=4)
d.polygon([(254,88),(355,221),(254,220)],fill='#69b7ac',outline='#406f69',width=4)
d.polygon([(254,220),(326,365),(255,430)],fill='#236d75',outline='#365758',width=4)
d.polygon([(139,225),(254,220),(255,430),(160,365)],fill='#4da99a',outline='#365758',width=4)
im.save(OUT/'crystal-layout.png')
