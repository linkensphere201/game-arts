"""Rear garment layout for local-model redraw, never an accepted sprite itself."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
im=ImageOps.mirror(Image.open(BASE/'sylva-staff-761002.png').convert('RGB'))
d=ImageDraw.Draw(im)
# Back skirt is closed cloth, unlike the cream split front. Keep paired heel silhouettes.
d.polygon([(213,379),(285,379),(318,482),(336,570),(397,608),(358,625),(315,604),(287,565),(279,492),(238,492),(229,565),(203,608),(155,624),(90,610),(170,582),(190,470)],fill='#28675f',outline='#343e36',width=3)
d.polygon([(238,410),(253,422),(245,514),(222,581),(194,610),(207,550)],fill='#3e8275')
d.polygon([(271,410),(282,449),(289,524),(323,598),(299,577),(270,511)],fill='#204f4c')
# Closed rear bodice, plain belt back; no neckline, front clasp or front buckle.
d.polygon([(211,304),(292,303),(305,350),(286,389),(211,389),(200,350)],fill='#28675f',outline='#343e36',width=3)
d.polygon([(211,373),(287,373),(291,397),(210,397)],fill='#674632',outline='#3a302b',width=3)
# Full rear hair mass covers the original face; outward elf ears remain visible.
d.polygon([(160,185),(190,150),(235,145),(270,156),(303,187),(327,282),(355,442),(326,455),(304,365),(285,286),(270,305),(229,309),(207,285),(192,358),(182,444),(162,464),(149,407),(164,317)],fill='#c7a66a',outline='#5b4932',width=3)
d.polygon([(170,217),(190,167),(226,151),(251,158),(219,179),(198,235),(188,326),(172,405),(178,299)],fill='#e6ca90')
d.polygon([(265,165),(285,190),(302,258),(315,350),(335,435),(314,421),(294,342),(277,258)],fill='#a88854')
d.line([(229,159),(223,212),(231,270),(227,301)],fill='#ad8e59',width=3)
d.line([(258,163),(266,217),(263,276),(271,296)],fill='#ead6a2',width=5)
# Visible rear heels, not toe straps drawn on the back of the feet.
for box in [(211,608,231,630),(280,607,299,629)]:
    d.rounded_rectangle(box,3,fill='#604534',outline='#302e29',width=2)
im.save(BASE/'sylva-back-layout.png')
