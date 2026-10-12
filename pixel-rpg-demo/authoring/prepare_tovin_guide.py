"""Owned goblin merchant composition guide for local-model illustration."""
from pathlib import Path
from PIL import Image, ImageDraw

OUT=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,768));d=ImageDraw.Draw(im)
ink='#493f32';skin='#829365';light='#a5af7c';hair='#624734';cream='#ded0ad';ochre='#ae8648'
# Short separated legs, broad simple shoes.
for x in (187,268):
    d.rounded_rectangle((x,511,x+57,624),12,fill='#68634d',outline=ink,width=4)
    d.rounded_rectangle((x-12,605,x+59,652),12,fill='#755238',outline=ink,width=4)
    d.line((x-7,642,x+55,642),fill='#3f372d',width=6)
# Rounded torso and cream shirt under ochre merchant waistcoat.
d.ellipse((158,285,349,533),fill=cream,outline=ink,width=4)
d.polygon([(186,294),(226,282),(252,333),(231,422),(238,500),(183,514),(159,473),(162,365)],fill=ochre,outline=ink,width=4)
d.polygon([(274,282),(317,296),(343,373),(352,476),(321,512),(270,500),(267,417),(255,332)],fill=ochre,outline=ink,width=4)
d.polygon([(226,282),(254,314),(241,343),(218,307)],fill='#f1e4c5',outline=ink,width=3)
d.polygon([(274,282),(254,314),(267,342),(287,307)],fill='#f1e4c5',outline=ink,width=3)
for y in (361,391,421,451):d.ellipse((252,y,260,y+8),fill='#c2a365',outline=ink,width=2)
# Sleeves and open relaxed hands; no weapon.
for flip in (False,True):
    def pts(v):return [(512-x if flip else x,y) for x,y in v]
    d.polygon(pts([(182,305),(156,315),(136,370),(138,419),(173,424),(187,361)]),fill=cream,outline=ink,width=4)
    d.polygon(pts([(140,412),(173,416),(171,451),(178,474),(167,493),(144,488),(134,470)]),fill=skin,outline=ink,width=4)
    d.line(pts([(145,454),(143,473),(152,479)]),fill='#61764d',width=3)
# Cross-body ledger bag (behind a foreground hand at right).
d.line((196,300,321,445),fill=ink,width=15);d.line((196,300,321,445),fill='#795839',width=9)
d.rounded_rectangle((302,426,368,505),9,fill='#7f5b3b',outline=ink,width=4)
d.polygon([(303,430),(367,430),(363,455),(333,466),(306,453)],fill='#a4784a',outline=ink,width=3)
d.rectangle((331,451,343,468),fill='#b39a61',outline=ink,width=2)
d.polygon([(337,456),(352,455),(355,477),(346,487),(335,480)],fill=skin,outline=ink,width=3)
# Large adult goblin head, projecting ears, broad nose and side-parted brown hair.
d.polygon([(202,186),(137,152),(150,207),(203,233)],fill=skin,outline=ink,width=4)
d.polygon([(307,184),(375,153),(360,209),(306,234)],fill=skin,outline=ink,width=4)
d.polygon([(189,190),(150,166),(164,197),(190,214)],fill='#afaa77')
d.polygon([(321,192),(362,167),(348,197),(321,215)],fill='#afaa77')
d.ellipse((187,131,324,284),fill=skin,outline=ink,width=4)
d.polygon([(187,194),(182,154),(197,120),(233,107),(284,113),(315,137),(326,183),(305,173),(288,138),(242,170),(211,164)],fill=hair,outline=ink,width=4)
d.line([(200,148),(225,124),(257,121)],fill='#946a42',width=6)
for x in (209,279):
    d.arc((x-5,186,x+26,211),185,345,fill=ink,width=4)
    d.ellipse((x,199,x+17,216),fill='#e4d5a8',outline=ink,width=2)
    d.ellipse((x+7,201,x+13,215),fill='#55492c')
d.ellipse((237,210,276,240),fill=light,outline=ink,width=3)
d.arc((220,230,292,261),15,165,fill=ink,width=3)
d.line((238,267,271,269),fill='#65784f',width=3)
im.save(OUT/'tovin-layout.png')
print('TOVIN_GUIDE_OK: short round goblin, ochre waistcoat, ledger satchel')
