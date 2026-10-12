"""Original wolf-beastfolk apothecary layout; the local model supplies final artwork."""
from pathlib import Path
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,768));d=ImageDraw.Draw(im)
ink='#453a32';hair='#a5683c';teal='#33766a';cream='#dfd2af';skin='#e4b998'
# Fluffy wolf tail and copper ponytail behind the figure.
d.polygon([(304,468),(356,491),(382,535),(386,581),(367,617),(334,639),(294,635),(324,613),(338,579),(333,550),(295,520)],fill=hair,outline=ink,width=5)
d.polygon([(367,585),(379,576),(371,613),(337,634),(306,634),(329,612)],fill=cream,outline=ink,width=3)
d.polygon([(184,171),(163,190),(154,237),(163,302),(152,348),(185,332),(207,271),(204,209)],fill=hair,outline=ink,width=4)
# Separated legs and practical ankle boots.
for x in [204,270]:
    d.polygon([(x,551),(x+36,551),(x+33,631),(x+2,631)],fill=skin,outline=ink,width=4)
    d.polygon([(x-2,618),(x+36,618),(x+36,657),(x+48,673),(x+44,681),(x-8,681),(x-8,662)],fill='#715039',outline=ink,width=4)
    d.line((x,630,x+32,630),fill='#ad8856',width=5)
# Dress with separate light linen apron, no weapon.
d.polygon([(206,278),(293,278),(315,338),(300,415),(326,565),(294,588),(203,584),(178,559),(203,414),(183,339)],fill=teal,outline=ink,width=4)
d.polygon([(222,296),(276,296),(286,397),(304,557),(274,571),(210,560),(217,411)],fill=cream,outline=ink,width=4)
d.line((228,303,224,397),fill='#f0e3c6',width=6)
d.line((282,416,291,548),fill='#b4a482',width=4)
d.rectangle((200,397,304,418),fill='#765239',outline=ink,width=4)
d.rectangle((238,399,260,416),fill='#b59b60',outline=ink,width=3)
# Rolled sleeves and bare forearms.
for flip in [False,True]:
    def pts(v):return [(512-x if flip else x,y) for x,y in v]
    d.polygon(pts([(206,290),(185,294),(171,334),(173,363),(205,365),(216,327)]),fill=teal,outline=ink,width=4)
    d.polygon(pts([(171,346),(205,347),(205,367),(173,369)]),fill=cream,outline=ink,width=4)
    d.polygon(pts([(177,368),(200,368),(196,412),(201,440),(187,452),(173,441),(174,410)]),fill=skin,outline=ink,width=4)
# Herb pouch: leaves, cork vial and simple leather flap.
d.rounded_rectangle((296,418,339,472),8,fill='#8d6846',outline=ink,width=4)
d.polygon([(307,427),(300,393),(313,406),(317,382),(327,399),(335,387),(331,421)],fill='#658754',outline=ink,width=3)
d.rectangle((310,425,324,451),fill='#66a390',outline=ink,width=2)
d.rectangle((311,420,323,427),fill='#ad8e5c',outline=ink,width=2)
# Face, copper fringe and clearly paired furry ears.
d.ellipse((195,143,309,265),fill=skin,outline=ink,width=4)
d.polygon([(190,181),(190,140),(209,120),(272,119),(310,143),(315,192),(290,180),(276,148),(253,175),(228,157),(207,192)],fill=hair,outline=ink,width=4)
for points,inside in [([(195,147),(175,91),(216,115),(226,136)],[(197,132),(188,108),(213,125)]), ([(280,131),(314,94),(312,154),(293,150)],[(291,132),(306,110),(305,145)])]:
    d.polygon(points,fill=hair,outline=ink,width=4);d.polygon(inside,fill=cream)
for x in [218,274]:
    d.ellipse((x,191,x+16,211),fill='#6e7844',outline=ink,width=3)
    d.ellipse((x+3,193,x+7,197),fill='#f1e6ce')
d.line((247,238,260,238),fill=ink,width=2)
d.polygon([(234,261),(274,261),(278,281),(253,300),(231,281)],fill=skin,outline=ink,width=3)
im.save(BASE/'mira-layout.png')
print('MIRA_GUIDE_OK: copper ponytail, wolf ears/tail, apron, herb pouch, ankle boots')
