"""Reconstruct Tovin's rear hair, waistcoat, satchel back and shoe heels."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
BASE=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
# Mirroring places the asymmetric bag; all directional surfaces below are redrawn.
im=ImageOps.mirror(Image.open(BASE/'tovin-refined-776005.png').convert('RGB'))
d=ImageDraw.Draw(im);ink='#493c2e';hair='#654b38';ochre='#a58d58';skin='#859163'
# Rear ears have outer green surfaces, not front-facing inner ear bowls.
d.polygon([(180,178),(116,138),(132,179),(160,205),(189,213)],fill=skin,outline=ink,width=3)
d.polygon([(328,178),(393,138),(377,181),(350,205),(322,213)],fill=skin,outline=ink,width=3)
d.line([(126,150),(146,178),(176,195)],fill='#6e7a50',width=3)
d.line([(383,150),(363,178),(334,195)],fill='#6e7a50',width=3)
# Nape is the only exposed skin beneath the fully closed back of the hair.
d.polygon([(222,230),(291,230),(285,283),(277,297),(235,296),(221,277)],fill=skin,outline=ink,width=3)
d.polygon([(174,146),(190,111),(225,88),(273,85),(310,103),(332,139),(334,184),(320,231),(298,256),(277,252),(263,266),(249,256),(230,260),(205,245),(187,218),(179,185)],fill=hair,outline=ink,width=4)
d.polygon([(188,147),(209,118),(240,104),(283,104),(308,125),(271,120),(228,136),(206,166),(191,198)],fill='#826044')
for points in [[(204,178),(207,211),(225,242)],[(248,139),(240,183),(248,242)],[(298,155),(306,193),(290,242)]]:
    d.line(points,fill='#513f31',width=3)
# Back waistcoat: no shirt placket, pockets, buttons, lapels or front buckle.
d.polygon([(181,288),(226,276),(253,292),(284,276),(332,289),(348,342),(361,417),(355,484),(337,521),(288,534),(223,535),(170,520),(151,486),(148,419),(162,341)],fill=ochre,outline=ink,width=4)
d.line([(183,299),(169,366),(166,445),(177,504)],fill='#c1a976',width=5)
d.line([(331,312),(344,396),(345,471),(330,514)],fill='#7f6b45',width=5)
d.line([(253,297),(254,404),(258,491),(255,529)],fill='#897344',width=2)
d.line([(191,446),(247,458),(318,447)],fill='#705637',width=8)
d.rectangle((244,450,262,463),fill='#a58b56',outline=ink,width=2)
# Back-view bag on screen left; reverse panel has seams but no frontal flap.
d.rounded_rectangle((133,442,201,522),8,fill='#795437',outline=ink,width=3)
d.rounded_rectangle((140,450,194,514),5,outline='#a1774e',width=2)
d.line([(302,282),(269,335),(225,393),(174,447)],fill=ink,width=15)
d.line([(302,282),(269,335),(225,393),(174,447)],fill='#825b3b',width=10)
# Heels replace toe caps and front laces.
for left,right in [(166,246),(268,348)]:
    d.rounded_rectangle((left,628,right,682),9,fill='#785738',outline=ink,width=4)
    d.line(((left+right)//2,633,(left+right)//2,668),fill='#574330',width=2)
    d.rectangle((left+3,670,right-3,680),fill='#493d2d',outline=ink,width=2)
im.save(BASE/'tovin-back-layout.png')
print('TOVIN_BACK_GUIDE_OK: no front face, waistcoat placket or satchel flap')
