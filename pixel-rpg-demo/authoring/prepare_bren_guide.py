"""Owned broad dragonborn silhouette for local-model character redraw."""
from pathlib import Path
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,768));d=ImageDraw.Draw(im)
ink='#333c3b';skin='#718b8b';steel='#91a4a1';teal='#306f67';brass='#b29356'
# Tail behind the legs, clearly distinct from the front tabard.
d.polygon([(300,458),(361,480),(395,543),(407,606),(449,603),(422,638),(383,640),(365,602),(348,548),(288,520)],fill=skin,outline=ink,width=5)
for x,y in [(372,509),(389,547),(399,582)]:d.polygon([(x,y),(x+18,y-6),(x+6,y+17)],fill='#536e72',outline=ink)
# Wide torso, short practical split tabard and heavy separate boots.
d.polygon([(177,299),(332,299),(350,373),(325,465),(188,465),(163,373)],fill=teal,outline=ink,width=5)
d.polygon([(204,463),(309,463),(331,571),(274,568),(258,507),(244,567),(183,571)],fill=teal,outline=ink,width=5)
d.line([(213,468),(199,560)],fill=brass,width=7);d.line([(301,468),(316,560)],fill=brass,width=7)
for x in [184,274]:
    d.polygon([(x,545),(x+56,545),(x+61,647),(x+71,676),(x+6,682),(x-4,666)],fill='#604a39',outline=ink,width=5)
    d.rectangle((x-2,548,x+58,570),fill='#384440',outline=ink,width=4)
for flip in [False,True]:
    def points(v):return [(512-x if flip else x,y) for x,y in v]
    d.polygon(points([(174,313),(142,323),(127,394),(142,448),(180,444),(193,371)]),fill=skin,outline=ink,width=5)
    d.polygon(points([(141,403),(178,402),(183,453),(143,461)]),fill='#594838',outline=ink,width=4)
    d.ellipse((135 if not flip else 330,446,182 if not flip else 377,493),fill=skin,outline=ink,width=4)
    d.polygon(points([(184,285),(144,295),(119,338),(162,356),(203,330)]),fill=steel,outline=ink,width=5)
    d.line(points([(139,336),(162,343),(192,323)]),fill=brass,width=6)
d.rectangle((183,432,329,462),fill='#614b38',outline=ink,width=5)
d.rectangle((239,435,273,460),fill=brass,outline=ink,width=4)
d.polygon([(231,264),(282,264),(288,310),(256,324),(222,310)],fill=skin,outline=ink,width=4)
# Broad angular reptilian head with short muzzle, paired ivory horns and brow ridges.
d.polygon([(194,156),(230,136),(280,136),(316,161),(316,227),(294,270),(259,284),(221,268),(193,231)],fill=skin,outline=ink,width=5)
d.polygon([(204,165),(178,138),(165,91),(194,115),(224,149)],fill='#d4c7a4',outline=ink,width=5)
d.polygon([(302,165),(332,136),(344,91),(315,116),(283,149)],fill='#d4c7a4',outline=ink,width=5)
d.polygon([(193,178),(218,148),(278,140),(313,178),(290,166),(274,184),(248,166),(224,182)],fill='#364b4a',outline=ink,width=4)
d.polygon([(219,229),(237,216),(277,216),(294,232),(282,250),(233,250)],fill='#91a5a0',outline=ink,width=3)
for x in [218,278]:
    d.line((x-7,202,x+15,198),fill=ink,width=6)
    d.ellipse((x,202,x+11,213),fill='#c3a361',outline=ink,width=2)
d.line((238,244,277,244),fill=ink,width=3)
im.save(OUT/'bren-layout.png')
print('BREN_GUIDE_OK: broad build, horns, grey scaled head, tabard, boots, tail')
