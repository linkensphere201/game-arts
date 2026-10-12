"""Owned elderly swordsman layout; final illustration is generated locally."""
from pathlib import Path
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,768));d=ImageDraw.Draw(im)
ink='#473c35';skin='#caa68a';cloth='#725443';linen='#ded0aa';hair='#acae9e'
# Weathered open cloak and narrow stance distinguish him from the broad warden.
d.polygon([(198,279),(250,269),(292,287),(318,381),(330,564),(296,575),(278,558),(249,571),(218,557),(184,574),(168,552),(184,389)],fill=cloth,outline=ink,width=5)
d.polygon([(187,341),(204,326),(207,507),(194,554),(180,557)],fill='#503c34')
for x in (217,266):
 d.polygon([(x,481),(x+28,481),(x+29,606),(x+19,644),(x-3,644)],fill='#696657',outline=ink,width=4)
 d.polygon([(x-5,606),(x+28,608),(x+27,655),(x+37,676),(x+31,683),(x-12,683),(x-13,661)],fill='#68503c',outline=ink,width=4)
 d.line((x-8,673,x+29,675),fill='#3e342b',width=4)
# Cream shirt, narrow torso, practical belt and a fully sheathed sword.
d.polygon([(214,298),(278,298),(289,365),(278,432),(288,498),(250,511),(209,496),(221,429),(207,366)],fill=linen,outline=ink,width=4)
d.polygon([(217,343),(229,368),(228,440),(218,479),(214,492),(213,442)],fill='#b5a580')
d.rectangle((213,421,286,442),fill='#624934',outline=ink,width=3)
d.rectangle((244,422,263,441),fill='#b2945e',outline=ink,width=3)
d.polygon([(285,405),(302,410),(326,621),(315,646),(304,624)],fill='#604b39',outline=ink,width=4)
d.line((294,373,294,415),fill='#624933',width=12);d.line((278,407,310,411),fill='#af9665',width=7)
# Cloak shoulder folds, sleeves and older hands at rest.
for flip in (False,True):
 def pts(v):return [(512-x if flip else x,y) for x,y in v]
 d.polygon(pts([(210,296),(191,306),(180,368),(191,406),(208,392),(218,342)]),fill=cloth,outline=ink,width=4)
 d.polygon(pts([(184,398),(204,394),(207,444),(200,470),(185,466),(179,450)]),fill=skin,outline=ink,width=3)
 d.line(pts([(186,445),(188,459),(195,461)]),fill='#8d6e57',width=2)
# Long weathered face, swept grey hair, short beard and visibly aged brows.
d.polygon([(234,252),(274,252),(275,298),(254,317),(231,294)],fill=skin,outline=ink,width=3)
d.ellipse((191,132,310,277),fill=skin,outline=ink,width=4)
d.ellipse((181,191,201,224),fill=skin,outline=ink,width=3);d.ellipse((300,191,320,224),fill=skin,outline=ink,width=3)
d.polygon([(190,184),(185,155),(199,127),(229,111),(267,118),(301,133),(316,163),(309,192),(295,165),(278,146),(249,148),(220,160),(202,181)],fill=hair,outline=ink,width=4)
d.line((205,143,235,125,274,135),fill='#d8d7c4',width=8)
d.polygon([(197,223),(215,242),(239,243),(252,233),(267,244),(292,232),(299,220),(296,261),(275,285),(252,295),(225,282),(205,257)],fill=hair,outline=ink,width=4)
d.polygon([(217,248),(244,257),(264,256),(287,243),(279,267),(252,282),(227,268)],fill='#c9caba')
for x in (210,270):
 d.line((x,190,x+19,193),fill='#74786f',width=6)
 d.line((x+2,202,x+17,203),fill=ink,width=3)
 d.ellipse((x+7,200,x+11,207),fill='#514c3d')
 d.line((x,213,x+16,216),fill='#987861',width=2)
d.line((252,198,247,226,258,228),fill='#896a54',width=3)
d.line((234,244,269,244),fill='#665342',width=3)
im.save(BASE/'osric-layout.png')
print('OSRIC_GUIDE_OK: elderly lean male, grey beard, worn cloak and sheathed sword')
