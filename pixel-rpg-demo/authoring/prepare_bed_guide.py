"""Original single-bed composition guide for the local model."""
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[2]
im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
ink='#473b30';wood='#98754e'
d.rounded_rectangle((145,67,367,203),10,fill=wood,outline=ink,width=6)
d.rectangle((163,87,350,146),fill='#b39464',outline=ink,width=4)
for x in [144,350]:d.rectangle((x,83,x+20,440),fill=wood,outline=ink,width=5)
d.polygon([(160,168),(352,168),(389,391),(122,391)],fill='#ddd5b6',outline=ink,width=6)
d.rounded_rectangle((177,177,335,224),12,fill='#eee3c5',outline='#86795d',width=4)
d.polygon([(151,240),(361,240),(380,375),(129,375)],fill='#397a70',outline='#35483b',width=5)
d.line((154,251,359,251),fill='#9bb9a1',width=9)
d.polygon([(129,375),(380,375),(378,403),(132,403)],fill='#286057',outline=ink,width=4)
d.polygon([(120,385),(392,385),(389,421),(123,421)],fill=wood,outline=ink,width=6)
d.line((136,394,377,394),fill='#c3a775',width=4)
im.save(root/'production/pixel-rpg/model-wave-01/guided/bed-layout.png')
