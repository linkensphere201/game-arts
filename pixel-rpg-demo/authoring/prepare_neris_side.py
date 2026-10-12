"""Original profile guide for Neris; garments/equipment follow the same heading."""
from pathlib import Path
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,768));d=ImageDraw.Draw(im)
ink='#433536';coat='#75434f';hair='#353431';skin='#ddbb9b';cream='#ddd3b6'
for x in (222,263):
    d.polygon([(x,549),(x+28,549),(x+27,640),(x,640)],fill='#554c41',outline=ink,width=3)
    d.polygon([(x-2,633),(x+28,633),(x+29,647),(x+49,658),(x+46,666),(x-3,666)],fill='#654b36',outline=ink,width=3)
d.polygon([(223,281),(270,281),(288,319),(282,386),(288,439),(306,582),(283,593),(270,569),(258,596),(211,589),(219,432),(208,367),(208,307)],fill=coat,outline=ink,width=4)
d.line([(228,423),(223,561),(229,582)],fill='#a16671',width=4)
d.line([(275,422),(286,566)],fill='#50323a',width=4)
d.polygon([(218,389),(282,389),(284,405),(219,406)],fill='#654a37',outline=ink,width=3)
# Key ring hangs forward of the near hand, attached to the side belt.
d.ellipse((275,404,292,421),outline='#b39a62',width=4)
for x,y in [(280,420),(290,424)]:
    d.line((x,y,x,y+33),fill=ink,width=6);d.line((x,y,x,y+33),fill='#b39a62',width=3)
    d.line((x,y+28,x+7,y+28),fill='#b39a62',width=3)
d.polygon([(226,288),(249,294),(262,326),(258,399),(235,409),(218,356)],fill=coat,outline=ink,width=3)
d.polygon([(235,399),(258,395),(261,419),(238,424)],fill=cream,outline=ink,width=3)
d.polygon([(239,425),(258,420),(260,441),(256,455),(242,455),(237,444)],fill=skin,outline=ink,width=3)
d.line([(250,433),(249,447)],fill='#9e785e',width=2)
d.polygon([(237,252),(274,250),(277,281),(263,294),(236,280)],fill=skin,outline=ink,width=3)
d.polygon([(233,278),(272,278),(280,295),(264,302),(234,290)],fill=cream,outline=ink,width=3)
# One side eye/nose, swept black hair and a low bun behind the elf ear.
d.polygon([(205,140),(235,117),(277,117),(302,141),(310,178),(309,195),(324,210),(312,219),(311,240),(294,260),(259,270),(230,256),(211,230),(198,192)],fill=skin,outline=ink,width=3)
d.polygon([(200,187),(193,150),(204,118),(232,99),(274,97),(306,119),(317,150),(309,175),(296,157),(278,124),(253,146),(224,137),(211,185)],fill=hair,outline=ink,width=4)
d.line([(210,136),(234,112),(267,107)],fill='#615d53',width=4)
d.ellipse((179,215,219,255),fill=hair,outline=ink,width=3)
d.arc((187,222,211,247),10,310,fill='#605a50',width=3)
d.polygon([(232,190),(178,164),(190,201),(222,220),(235,211)],fill=skin,outline=ink,width=3)
d.line([(188,176),(212,198),(228,204)],fill='#ab8067',width=2)
d.line((284,181,303,179),fill=ink,width=3)
d.ellipse((289,189,306,201),fill='#e4d3b0',outline=ink,width=2)
d.ellipse((300,190,305,200),fill='#64513c')
d.line((307,234,296,234),fill='#996c58',width=2)
im.save(OUT/'neris-side-layout.png')
print('NERIS_SIDE_GUIDE_OK: profile face, low bun, long coat, cuffs and hip keys')
