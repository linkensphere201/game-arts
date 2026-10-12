"""Side-view layout only; local model supplies the character artwork."""
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[2]
out=ROOT/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,768));d=ImageDraw.Draw(im)
ink='#3e3b32';teal='#28675f';gold='#c7a66a'
# Profile facing right: hair behind the face, nose and chin project right.
d.polygon([(214,181),(243,150),(278,160),(299,183),(303,218),(319,232),(306,238),(302,258),(287,270),(283,302),(239,302),(230,265)],fill='#e8c6a2',outline=ink,width=3)
d.polygon([(213,179),(233,153),(268,149),(292,166),(302,192),(285,182),(280,216),(259,232),(248,275),(245,352),(223,414),(192,439),(204,354),(196,290),(198,222)],fill=gold,outline=ink,width=3)
d.polygon([(223,169),(244,157),(230,215),(226,287),(217,361),(203,410),(211,323),(207,244)],fill='#e4c68b')
d.polygon([(263,225),(234,211),(241,240),(258,247)],fill='#d6ab82',outline=ink,width=2)
d.line([(289,218),(301,219)],fill=ink,width=3)
# Closed side torso, side seam rather than front neckline/buckle.
d.polygon([(246,284),(281,286),(298,318),(286,390),(267,413),(223,396),(222,327)],fill=teal,outline=ink,width=3)
d.polygon([(222,373),(286,373),(286,394),(224,398)],fill='#674632',outline=ink,width=3)
d.polygon([(229,395),(281,395),(293,479),(289,557),(307,618),(281,625),(257,580),(243,509),(236,586),(210,635),(171,642),(202,598),(209,495)],fill=teal,outline=ink,width=3)
d.polygon([(221,411),(233,429),(225,530),(211,586),(187,629),(206,579)],fill='#438779')
# One near bell sleeve, cream cuff and hand; staff stays on the near side.
d.polygon([(260,303),(279,310),(283,351),(309,399),(282,423),(258,394),(248,350)],fill=teal,outline=ink,width=3)
d.polygon([(282,414),(305,396),(311,404),(288,429)],fill='#ded5b6',outline=ink,width=2)
d.ellipse((287,416,304,438),fill='#e8c6a2',outline=ink,width=2)
d.line([(301,429),(318,634)],fill='#604534',width=7)
d.line([(301,429),(294,370)],fill='#604534',width=7)
d.polygon([(291,337),(306,355),(297,375),(283,358)],fill='#49a998',outline=ink,width=3)
d.polygon([(291,342),(292,369),(286,357)],fill='#a0d8bd')
# Side-profile shoes have forward toe length, not front/rear symmetric soles.
for dx,dy in [(0,0),(-32,-6)]:
    d.polygon([(257+dx,588+dy),(275+dx,588+dy),(278+dx,626+dy),(298+dx,636+dy),(296+dx,646+dy),(259+dx,647+dy)],fill='#79553b',outline=ink,width=3)
# Match the accepted short character proportions before model redraw.
# Enlarge the head around the neck; shorten the body without narrowing sleeves.
compact=Image.new('RGBA',im.size)
head=im.crop((150,140,340,284)).resize((238,180),Image.Resampling.LANCZOS)
compact.alpha_composite(head,(126,104))
body=im.crop((0,284,512,660)).resize((512,271),Image.Resampling.LANCZOS)
compact.alpha_composite(body,(0,284))
compact.save(out/'sylva-side-layout.png')
print('SYLVA_SIDE_LAYOUT_ONLY')
