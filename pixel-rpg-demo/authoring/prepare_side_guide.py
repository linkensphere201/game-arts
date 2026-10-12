"""Right-facing garment construction guide for local-model redrawing only."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
im=Image.new('RGBA',(512,768));d=ImageDraw.Draw(im)
ink='#342c2c';skin='#efd0b5';white='#ede9df';brown='#56392d';teal='#227b70'
def poly(points,color):d.polygon(points,fill=color,outline=ink,width=3)
# Far leg and boot; the side heel is behind the toe, which points right.
poly([(254,445),(277,448),(270,540),(249,540)],'#d7b39f')
poly([(249,533),(274,532),(266,610),(270,640),(292,650),(292,661),(247,661),(244,648)],'#402e2a')
# Cape is behind the torso and arm, on the left of a right-facing figure.
poly([(242,262),(279,267),(257,330),(244,423),(226,477),(214,532),(192,552),(201,481),(181,465),(197,356),(218,295)],'#17655f')
poly([(226,287),(247,291),(232,392),(211,467),(190,466)],'#248275')
# Body and skirt profile; front is right.
poly([(257,261),(289,270),(300,305),(289,352),(300,391),(305,455),(235,455),(242,399),(250,347),(244,304)],white)
d.polygon([(279,310),(288,315),(276,346),(283,376),(286,446),(260,447)],fill='#c7d2ca')
poly([(242,350),(291,349),(292,369),(239,369)],brown)
d.line([(267,371),(291,393)],fill='#694935',width=6)
# Near leg and boot, with a small lateral toe. No frontal flaps pasted onto the side.
poly([(278,456),(299,456),(299,538),(278,538)],skin)
poly([(276,532),(302,532),(297,592),(299,633),(328,647),(329,661),(276,661),(272,649)],brown)
d.line([(280,542),(284,602),(283,638)],fill='#835741',width=4)
d.line([(276,655),(327,655)],fill='#27242a',width=6)
# Near shoulder/arm covers the side of the dress, not the face or cape silhouette.
poly([(277,266),(296,278),(298,315),(290,356),(302,398),(291,412),(276,396),(270,355),(275,316)],skin)
poly([(280,363),(295,360),(306,399),(290,408)],brown)
poly([(291,407),(304,400),(311,425),(303,435),(293,427)],skin)
poly([(239,263),(272,259),(295,275),(298,288),(273,284),(238,278)],teal)
# Head profile. Face/nose/one eye on the right; bob covers the rear skull on the left.
poly([(269,224),(289,224),(286,267),(261,262)],skin)
poly([(234,115),(292,124),(310,157),(308,180),(325,198),(314,207),(315,222),(298,239),(267,233),(233,208)],skin)
d.ellipse((299,177,307,185),fill='#342c29');d.line([(299,172),(309,174)],fill=ink,width=4)
d.line([(311,215),(316,215)],fill='#a46454',width=2)
poly([(206,111),(248,96),(282,104),(301,123),(307,152),(290,144),(286,176),(270,192),(274,225),(259,243),(220,237),(204,217),(198,183),(187,194),(196,154)],'#964a2b')
d.polygon([(207,129),(241,112),(277,118),(293,139),(263,132),(240,142),(220,152),(203,166)],fill='#c77a3e')
d.line([(225,160),(221,201),(230,224)],fill='#613323',width=4)
d.line([(255,153),(247,188),(252,222)],fill='#613323',width=4)
im.save(ROOT/'production/pixel-rpg/model-wave-01/guided/rowan-side-layout.png')
print('SIDE_LAYOUT_GUIDE_ONLY')
