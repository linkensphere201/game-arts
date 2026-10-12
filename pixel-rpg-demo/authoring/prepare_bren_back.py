"""Rear clothing/dragon anatomy guide; local inference authors the final study."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
im=Image.open(BASE/'bren-773001.png').convert('RGB');d=ImageDraw.Draw(im)
ink='#303d3e';skin='#728b8b';teal='#286f67'
# Remove the old side tail before drawing its visible rear root.
d.polygon([(319,494),(353,494),(396,568),(437,600),(431,657),(324,657)],fill='white')
# Back of head: no muzzle/eyes; retain ivory horn geometry from the same source.
d.polygon([(222,249),(284,249),(289,292),(222,292)],fill=skin,outline=ink,width=4)
d.polygon([(181,167),(199,142),(222,134),(275,134),(300,151),(311,183),(310,222),(289,256),(260,270),(225,267),(192,246),(169,221),(150,211),(165,202),(171,182)],fill=skin,outline=ink,width=4)
d.polygon([(240,139),(256,130),(271,139),(264,166),(267,191),(255,223),(243,191),(247,165)],fill='#536e70',outline=ink,width=3)
for y in [237,252,267,280]:d.arc((221,y-10,286,y+16),5,175,fill='#4e696b',width=3)
# Closed back tabard and shoulder attachment, no chest fasteners or front lapels.
d.polygon([(183,289),(223,280),(285,280),(324,293),(316,372),(320,435),(186,435),(190,374)],fill=teal,outline=ink,width=4)
d.line((254,291,254,428),fill='#225c58',width=4)
d.polygon([(194,306),(204,320),(204,412),(195,428)],fill='#43857a')
d.polygon([(294,303),(302,341),(294,425),(282,427)],fill='#205650')
# Reverse armor shell plates; back seams replace front bright bevels.
for points in [[(185,282),(151,287),(119,316),(107,333),(155,343),(190,324)],[(321,282),(352,292),(377,318),(387,336),(340,343),(317,324)]]:
    d.polygon(points,fill='#91a5a2',outline=ink,width=5)
d.line((121,327,155,334,184,320),fill='#5d767a',width=5)
d.line((326,320,342,334,372,331),fill='#5d767a',width=5)
d.rectangle((186,430,320,455),fill='#604c39',outline=ink,width=4)
d.line((195,438,310,438),fill='#94714c',width=3)
d.polygon([(191,458),(314,458),(325,520),(296,554),(262,510),(226,554),(185,526)],fill=teal,outline=ink,width=4)
# Tail emerges from the rear belt opening, then curves beside the right boot.
d.polygon([(244,460),(275,460),(295,490),(320,523),(337,565),(364,608),(404,615),(383,638),(349,638),(317,607),(297,561),(272,528),(242,496)],fill=skin,outline=ink,width=4)
for x,y in [(276,496),(299,532),(316,568),(336,602),(366,623)]:
    d.line((x-10,y-2,x+17,y-7),fill='#4f686b',width=4)
# Rear boot shafts/seams and heel caps; no frontal kneecap ornaments.
for left,right in [(184,244),(274,326)]:
    d.polygon([(left,570),(right,570),(right+1,670),(right-8,680),(left-6,678),(left-8,652)],fill='#65503e',outline=ink,width=4)
    d.line(((left+right)//2,580,(left+right)//2,656),fill='#423a32',width=3)
    d.rectangle((left-4,658,right-2,676),fill='#443b32',outline=ink,width=3)
im.save(BASE/'bren-back-layout.png')
print('BREN_BACK_GUIDE_OK: rear skull, tabard, armor, heels and tail root')
