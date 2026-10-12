"""Original elven steward guide: burgundy tailoring, low buns and brass keys."""
from pathlib import Path
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,768));d=ImageDraw.Draw(im)
ink='#443739';hair='#393735';coat='#794954';light='#a06470';cream='#e2d5b5';skin='#ddbea0';brass='#b09a61'
# Slim legs, closed dark shoes and long tailored split coat.
for x in (218,274):
    d.polygon([(x,528),(x+29,528),(x+27,636),(x+1,636)],fill='#57524b',outline=ink,width=3)
    d.rounded_rectangle((x-7,625,x+35,659),8,fill='#584334',outline=ink,width=3)
    d.line((x-5,653,x+32,653),fill='#39322b',width=4)
d.polygon([(218,276),(289,276),(311,318),(293,392),(317,568),(284,602),(257,553),(233,603),(196,571),(214,396),(195,319)],fill=coat,outline=ink,width=4)
d.polygon([(223,285),(256,312),(242,346),(215,308)],fill=cream,outline=ink,width=3)
d.polygon([(288,285),(256,312),(270,346),(298,307)],fill=cream,outline=ink,width=3)
d.polygon([(245,319),(266,319),(271,404),(246,401)],fill='#c5b898',outline=ink,width=2)
d.line([(221,409),(212,544),(230,580)],fill=light,width=4)
d.line([(281,414),(293,559)],fill='#53383f',width=4)
d.rectangle((214,394,295,408),fill='#654a38',outline=ink,width=3)
d.rectangle((249,394,266,408),fill=brass,outline=ink,width=2)
for y in (354,378,430,456):d.ellipse((254,y,261,y+7),fill=brass,outline=ink,width=1)
# Restrained sleeves with cream cuffs; relaxed hands.
for flip in (False,True):
    def pts(v):return [(512-x if flip else x,y) for x,y in v]
    d.polygon(pts([(213,282),(192,293),(181,356),(184,417),(208,420),(215,358),(230,308)]),fill=coat,outline=ink,width=4)
    d.polygon(pts([(183,407),(208,410),(210,431),(184,430)]),fill=cream,outline=ink,width=3)
    d.polygon(pts([(185,430),(207,431),(207,455),(200,469),(184,461)]),fill=skin,outline=ink,width=3)
# Visible brass key ring at hip, distinct from clothing buttons.
d.ellipse((282,408,300,426),outline=brass,width=4)
for x,y in [(286,424),(297,425)]:
    d.line((x,y,x,y+31),fill=ink,width=7);d.line((x,y,x,y+31),fill=brass,width=4)
    d.line((x,y+25,x+8,y+25),fill=brass,width=4)
# Black low side buns and long elf ears, no animal ears or horns.
d.ellipse((167,201,209,246),fill=hair,outline=ink,width=4)
d.ellipse((304,201,346,246),fill=hair,outline=ink,width=4)
d.polygon([(198,181),(158,159),(168,202),(197,220)],fill=skin,outline=ink,width=3)
d.polygon([(314,181),(354,159),(344,202),(315,220)],fill=skin,outline=ink,width=3)
d.ellipse((192,122,321,265),fill=skin,outline=ink,width=4)
d.polygon([(188,181),(190,142),(206,113),(249,101),(291,111),(320,139),(324,187),(299,169),(281,131),(252,151),(225,142),(211,187)],fill=hair,outline=ink,width=4)
d.line([(206,143),(225,119),(249,114)],fill='#666055',width=5)
for x in (217,279):
    d.line((x-2,187,x+18,184),fill=ink,width=3)
    d.ellipse((x,193,x+17,210),fill='#77774d',outline=ink,width=2)
    d.ellipse((x+5,194,x+10,198),fill='#eadfbd')
d.line((247,235,265,235),fill='#926754',width=2)
d.polygon([(238,263),(276,263),(278,282),(257,300),(235,281)],fill=skin,outline=ink,width=3)
im.save(OUT/'neris-layout.png')
print('NERIS_GUIDE_OK: elf ears, low black buns, burgundy coat, keys')
