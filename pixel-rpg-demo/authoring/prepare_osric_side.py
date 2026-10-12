"""Owned right-profile layout for the elderly swordsman, for local redraw."""
from pathlib import Path
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,768));d=ImageDraw.Draw(im)
ink='#493c32';cloak='#765642';skin='#cba68a';grey='#b9bbae'
# Narrow stance and side-facing footwear.
for x in (226,262):
 d.polygon([(x,482),(x+27,484),(x+27,615),(x+20,643),(x-4,643)],fill='#6b6759',outline=ink,width=3)
 d.polygon([(x-5,607),(x+26,608),(x+29,655),(x+54,671),(x+52,681),(x-6,681),(x-10,660)],fill='#6d523b',outline=ink,width=4)
 d.line((x-4,675,x+48,675),fill='#45372c',width=3)
# Cloak is behind torso; cream shirt is visible only along the forward edge.
d.polygon([(219,278),(262,275),(284,318),(289,422),(301,545),(282,564),(238,560),(208,571),(196,554),(208,444),(203,352)],fill=cloak,outline=ink,width=4)
d.polygon([(211,327),(224,348),(218,446),(214,551),(203,554)],fill='#997657')
d.polygon([(264,302),(285,326),(299,371),(291,423),(302,490),(283,500),(267,435)],fill='#d9cba5',outline=ink,width=3)
d.polygon([(268,416),(295,416),(295,433),(268,434)],fill='#614630',outline=ink,width=3)
# A simple sword at the near hip; cloak falls behind the scabbard.
d.polygon([(239,418),(257,418),(257,612),(248,637),(237,614)],fill='#594936',outline=ink,width=3)
d.polygon([(237,607),(257,607),(253,625),(248,637),(241,624)],fill='#aa905b',outline=ink,width=2)
d.rectangle((240,374,252,414),fill='#76503a',outline=ink,width=3)
d.ellipse((238,365,254,379),fill='#b19866',outline=ink,width=2)
d.polygon([(228,412),(263,412),(264,421),(228,421)],fill='#b29860',outline=ink,width=3)
# Relaxed near arm in front of the cloak, beside the sword.
d.polygon([(223,296),(251,299),(269,325),(274,356),(261,380),(234,372),(219,344)],fill=cloak,outline=ink,width=3)
d.polygon([(235,373),(258,378),(270,409),(269,436),(262,450),(251,449),(245,433),(247,411)],fill=skin,outline=ink,width=3)
# Profile face with one eye, pronounced nose, swept grey hair and short beard.
d.polygon([(241,247),(275,242),(277,280),(261,301),(237,283)],fill=skin,outline=ink,width=3)
d.polygon([(211,144),(241,126),(275,138),(295,160),(296,191),(312,211),(306,218),(294,219),(295,239),(278,263),(245,262),(215,239),(204,197)],fill=skin,outline=ink,width=4)
d.polygon([(207,195),(198,168),(203,139),(229,116),(265,117),(289,133),(298,153),(296,170),(279,149),(254,142),(230,163),(217,204)],fill=grey,outline=ink,width=4)
d.line((212,147,235,127,264,128,285,140),fill='#dedcca',width=6)
d.ellipse((217,195,235,220),fill=skin,outline=ink,width=2)
d.polygon([(222,219),(238,233),(262,231),(276,234),(294,223),(298,244),(286,268),(264,282),(239,271),(224,252)],fill=grey,outline=ink,width=3)
d.polygon([(239,243),(260,251),(283,245),(274,263),(257,271),(242,260)],fill='#d4d4c3')
d.line((277,188,295,191),fill='#777c70',width=6)
d.line((282,202,294,201),fill=ink,width=3)
d.line((282,213,291,215),fill='#927057',width=2)
d.line((280,240,294,238),fill='#6d5948',width=2)
# Beard strands make the lower grey mass unambiguously facial hair.
for line in [(233,239,243,261),(242,244,252,271),(252,244,259,275),(264,246,266,272),(275,244,274,262)]:
 d.line(line,fill='#8d9387',width=3)
d.line((267,233,288,229),fill='#e0dfcb',width=4)
im.save(BASE/'osric-side-layout.png')
print('OSRIC_SIDE_GUIDE_OK: elderly profile, beard, cloak depth and sheathed sword')
