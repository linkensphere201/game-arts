"""Original right-facing dragonborn profile guide for local model redraw."""
from pathlib import Path
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,768));d=ImageDraw.Draw(im)
ink='#303d3e';skin='#728b8b';steel='#91a5a2';teal='#286f67'
# Far tail starts at pelvis and falls behind the near leg toward screen-left.
d.polygon([(237,463),(199,482),(183,534),(172,592),(139,631),(94,624),(116,655),(160,658),(199,629),(218,570),(261,509)],fill=skin,outline=ink,width=5)
for x,y in [(207,509),(195,548),(180,586),(151,626)]:d.line((x-14,y-7,x+12,y+8),fill='#4f686b',width=4)
# Far leg and near leg keep the broad heavy leather boots, toes face right.
d.polygon([(241,496),(285,496),(289,579),(278,637),(310,652),(310,677),(226,679),(224,655),(232,575)],fill='#4f4437',outline=ink,width=5)
d.polygon([(269,494),(315,502),(312,579),(306,640),(344,656),(344,681),(260,681),(254,653),(262,573)],fill='#65503e',outline=ink,width=5)
d.polygon([(260,568),(314,568),(313,588),(258,587)],fill='#384440',outline=ink,width=4)
d.line((267,674,338,674),fill='#332e29',width=5)
# Barrel chest and tabard side split, no duplicated frontal belt buckle.
d.polygon([(224,280),(282,277),(317,318),(321,379),(304,438),(310,469),(332,540),(284,551),(265,482),(248,543),(209,532),(220,456),(208,363)],fill=teal,outline=ink,width=5)
d.line((258,335,254,432),fill='#1f5753',width=5)
d.polygon([(280,293),(301,326),(304,409),(284,430)],fill='#397d70')
d.polygon([(216,432),(311,432),(307,458),(217,458)],fill='#604b39',outline=ink,width=5)
# Neck and profile skull: one visible amber eye, projecting muzzle, paired horns in depth.
d.polygon([(239,250),(287,246),(287,289),(254,306),(230,287)],fill=skin,outline=ink,width=4)
d.polygon([(220,159),(248,139),(279,143),(297,170),(302,199),(332,211),(342,228),(333,244),(303,249),(281,270),(240,267),(218,239),(204,200)],fill=skin,outline=ink,width=5)
d.polygon([(224,160),(212,126),(211,94),(239,132),(248,156)],fill='#d4c7a4',outline=ink,width=4)
d.polygon([(258,152),(253,114),(270,78),(279,124),(275,158)],fill='#d4c7a4',outline=ink,width=5)
d.polygon([(207,196),(222,180),(230,207),(220,238),(205,224)],fill='#536e70',outline=ink,width=3)
d.line((278,197,301,201),fill=ink,width=6)
d.ellipse((286,203,297,216),fill='#b69a57',outline=ink,width=2)
d.line((310,235,336,233),fill=ink,width=3)
d.ellipse((326,216,331,220),fill=ink)
# Near shoulder and relaxed armored arm cover the side of the torso.
d.polygon([(241,292),(276,288),(295,311),(296,341),(267,358),(229,347),(216,326)],fill=steel,outline=ink,width=5)
d.line((228,337,263,348,286,332),fill='#b29356',width=6)
d.polygon([(237,350),(279,352),(285,397),(277,448),(245,456),(232,399)],fill=skin,outline=ink,width=4)
d.polygon([(239,403),(282,405),(279,455),(240,455)],fill='#604735',outline=ink,width=4)
d.ellipse((238,446,279,493),fill=skin,outline=ink,width=4)
# Reference-painted metal and horn surfaces prevent the guide reading as cloth/ears.
reference=Image.open(BASE/'bren-773001.png').convert('RGBA')
for bounds,position,size,mirror in [((136,85,198,169),(248,83),(62,84),True),((91,279,194,350),(214,287),(84,69),False)]:
    patch=reference.crop(bounds)
    pixels=patch.load()
    for y in range(patch.height):
        for x in range(patch.width):
            r,g,b,a=pixels[x,y]
            if min(r,g,b)>232 and max(r,g,b)-min(r,g,b)<28:pixels[x,y]=(r,g,b,0)
    if mirror:patch=patch.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    patch=patch.resize(size,Image.Resampling.LANCZOS)
    im.alpha_composite(patch,position)
im.save(BASE/'bren-side-layout.png')
print('BREN_SIDE_GUIDE_OK: profile muzzle, shoulder depth, side tabard, boots and rear tail')
