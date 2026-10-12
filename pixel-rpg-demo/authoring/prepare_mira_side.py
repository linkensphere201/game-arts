"""Owned right-profile guide for Mira; local model performs final illustration."""
from pathlib import Path
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,768));d=ImageDraw.Draw(im)
ink='#44382e';hair='#8e5935';sage='#87977a';dark='#354e36';linen='#ded5b4';skin='#e5c2a7'
# Tail behind the skirt, broad cream terminal patch.
d.polygon([(232,463),(207,475),(169,528),(148,584),(155,623),(183,647),(219,641),(192,618),(184,587),(209,549),(250,515)],fill=hair,outline=ink,width=4)
d.polygon([(150,581),(166,590),(177,582),(186,591),(187,614),(217,640),(185,646),(158,627),(149,607)],fill='#cfb391',outline=ink,width=3)
# Legs and profile boots.
for x,y in [(230,570),(263,578)]:
 d.rectangle((x,y,x+29,643),fill=skin,outline=ink,width=3)
 d.polygon([(x-3,632),(x+30,632),(x+31,663),(x+57,674),(x+58,688),(x-5,688),(x-7,674)],fill='#765138',outline=ink,width=4)
 d.line((x-2,682,x+54,682),fill='#45372c',width=4)
# Dress side volume and narrow forward apron, no broad frontal bib.
d.polygon([(229,292),(274,289),(302,322),(301,397),(291,436),(316,571),(290,592),(219,588),(203,571),(221,438),(214,347)],fill=dark,outline=ink,width=4)
d.polygon([(294,330),(304,346),(300,429),(319,571),(306,580),(289,445)],fill=linen,outline='#8a8468',width=3)
d.polygon([(216,405),(301,405),(299,418),(216,421)],fill='#805235',outline=ink,width=3)
# Profile head, one eye and projecting nose; ponytail falls behind skull.
d.polygon([(246,241),(278,242),(280,297),(260,309),(238,292)],fill=skin,outline=ink,width=3)
d.polygon([(214,148),(249,128),(281,141),(302,164),(301,202),(315,218),(305,226),(300,248),(279,264),(242,254),(217,224)],fill=skin,outline=ink,width=4)
d.polygon([(208,182),(197,216),(180,257),(184,304),(174,344),(204,328),(222,292),(224,244),(234,208)],fill=hair,outline=ink,width=4)
d.polygon([(208,191),(210,150),(235,125),(269,127),(292,146),(299,174),(286,198),(281,178),(268,159),(250,177),(231,205),(224,240),(209,230)],fill=hair,outline=ink,width=4)
d.polygon([(220,144),(216,100),(247,126)],fill=hair,outline=ink,width=4)
d.polygon([(247,132),(269,97),(271,149)],fill=hair,outline=ink,width=4)
d.polygon([(254,130),(265,109),(266,138)],fill='#cbb697')
d.ellipse((289,195,298,211),fill='#517343',outline=ink,width=2)
d.line((289,191,300,194),fill=ink,width=3)
d.line((299,237,307,234),fill=ink,width=2)
# Near blouse sleeve, wrist and hand; pouch hangs at near hip.
d.polygon([(225,301),(247,294),(272,310),(280,342),(269,357),(228,351),(216,333)],fill=sage,outline=ink,width=4)
d.polygon([(226,344),(273,350),(274,367),(226,361)],fill='#93a085',outline=ink,width=3)
d.polygon([(232,365),(269,369),(266,413),(258,447),(233,444),(236,401)],fill=skin,outline=ink,width=3)
d.rounded_rectangle((228,424,282,483),8,fill='#986441',outline=ink,width=4)
d.polygon([(228,428),(281,430),(279,445),(231,443)],fill='#ac7950',outline=ink,width=3)
d.ellipse((231,406,256,445),fill=skin,outline=ink,width=3)
for points in [[(266,430),(255,413),(257,399),(269,413)],[(269,427),(271,405),(284,400),(281,417)]]:d.polygon(points,fill='#718750',outline='#455239',width=2)
im.save(BASE/'mira-side-layout.png')
print('MIRA_SIDE_GUIDE_OK')
