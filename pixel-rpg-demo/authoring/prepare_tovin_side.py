"""Original right-facing goblin merchant layout for local image synthesis."""
from pathlib import Path
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,768));d=ImageDraw.Draw(im)
ink='#493c2e';skin='#89956a';hair='#664b36';ochre='#a68b57';cream='#dfd0ac'
# Short legs with heel at left and rounded toe toward the facing direction.
for x,y in [(195,538),(256,547)]:
    d.polygon([(x,y),(x+47,y),(x+43,618),(x+4,619)],fill='#68604b',outline=ink,width=4)
    d.polygon([(x,610),(x+44,610),(x+45,637),(x+68,651),(x+68,664),(x-3,664)],fill='#795638',outline=ink,width=4)
    d.line((x-1,657,x+67,657),fill='#40382c',width=5)
# Rounded profile torso: belly projects forward, back stays relatively straight.
d.polygon([(210,280),(270,281),(304,310),(326,356),(345,414),(340,466),(322,512),(292,547),(222,549),(182,519),(176,457),(182,359)],fill=ochre,outline=ink,width=4)
d.polygon([(287,299),(306,317),(324,359),(343,416),(338,465),(322,503),(311,511),(325,462),(329,416),(312,361)],fill=cream,outline=ink,width=3)
d.line([(192,330),(188,397),(191,481),(212,524)],fill='#c0a36f',width=5)
# Bag and shoulder strap are behind the hanging arm.
d.line((233,293,235,450),fill=ink,width=16);d.line((233,293,235,450),fill='#805b3c',width=10)
d.rounded_rectangle((222,440,293,514),8,fill='#805b3c',outline=ink,width=4)
d.polygon([(223,441),(291,441),(289,464),(262,474),(226,461)],fill='#a07850',outline=ink,width=3)
d.rectangle((258,460,270,477),fill='#b69c61',outline=ink,width=2)
# Cream rolled sleeve and near arm partly occlude the bag's rear edge.
d.polygon([(218,300),(245,302),(269,330),(267,380),(226,390),(205,357)],fill=cream,outline=ink,width=4)
d.polygon([(226,372),(267,369),(271,391),(231,403)],fill='#e9dbb8',outline=ink,width=3)
d.polygon([(232,402),(263,395),(265,434),(268,471),(257,490),(238,486),(229,468)],fill=skin,outline=ink,width=4)
d.line([(246,459),(245,478),(253,483)],fill='#647449',width=3)
# Neck and one true profile head, one eye and nose facing right.
d.polygon([(232,250),(279,253),(283,283),(270,303),(233,289)],fill=skin,outline=ink,width=4)
d.polygon([(192,144),(231,116),(283,119),(308,141),(321,176),(317,197),(337,209),(335,224),(320,231),(319,250),(302,270),(266,280),(224,264),(205,238),(188,197)],fill=skin,outline=ink,width=4)
d.polygon([(187,198),(179,158),(192,121),(219,99),(263,96),(297,116),(315,149),(313,175),(292,158),(279,128),(245,148),(217,142),(204,184)],fill=hair,outline=ink,width=4)
d.line([(192,149),(215,117),(247,108),(282,122)],fill='#896044',width=5)
d.polygon([(223,186),(155,156),(169,203),(206,226),(226,219)],fill=skin,outline=ink,width=4)
d.polygon([(211,193),(168,169),(180,198),(208,214)],fill='#a5ab79',outline='#68754c',width=2)
d.line((284,179,309,176),fill=ink,width=4)
d.ellipse((291,187,312,201),fill='#e0d2a1',outline=ink,width=2)
d.ellipse((304,188,310,200),fill='#51442c')
d.line((319,238,301,242),fill=ink,width=2)
d.line([(289,235),(285,245),(294,251)],fill='#69794e',width=2)
im.save(OUT/'tovin-side-layout.png')
print('TOVIN_SIDE_GUIDE_OK: single profile, projecting belly, arm over bag')
