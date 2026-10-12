"""Owned rear garment/hair reconstruction of the Neris front study."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
OUT=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
im=ImageOps.mirror(Image.open(OUT/'neris-keys-777006.png').convert('RGB'))
d=ImageDraw.Draw(im);ink='#423537';hair='#353431';coat='#75434f'
# Rear ear surfaces replace inner ear detail.
d.polygon([(190,176),(153,148),(164,180),(193,207)],fill='#d5b294',outline=ink,width=3)
d.polygon([(322,176),(359,148),(348,180),(320,207)],fill='#d5b294',outline=ink,width=3)
# Nape, back skull and paired low buns; no facial features retained.
d.polygon([(231,216),(278,216),(278,266),(258,279),(232,265)],fill='#c9a88a',outline=ink,width=3)
d.polygon([(177,161),(190,116),(217,91),(254,84),(290,94),(318,122),(333,168),(324,208),(305,231),(280,243),(249,249),(218,241),(194,225),(180,198)],fill=hair,outline=ink,width=4)
d.polygon([(192,157),(209,119),(243,103),(275,104),(300,120),(266,115),(234,124),(214,156),(200,192)],fill='#555249')
d.line([(253,110),(244,164),(250,221)],fill='#242722',width=3)
for x in (159,310):
    d.ellipse((x,199,x+44,241),fill=hair,outline=ink,width=3)
    d.arc((x+6,205,x+37,236),15,310,fill='#59564c',width=3)
# Plain rear collar, closed back panel and long center vent.
d.polygon([(233,258),(277,258),(280,276),(258,285),(230,275)],fill='#dcd4b9',outline=ink,width=3)
d.polygon([(190,285),(229,274),(255,284),(284,274),(320,285),(311,351),(294,399),(296,457),(316,587),(276,601),(255,551),(236,602),(196,588),(215,457),(216,398),(199,351)],fill=coat,outline=ink,width=3)
d.line([(252,288),(253,397)],fill='#51343d',width=2)
d.line([(219,424),(211,566),(226,587)],fill='#9a5f6c',width=4)
d.line([(286,427),(299,574)],fill='#54343e',width=4)
d.polygon([(252,469),(259,469),(264,565),(256,552),(247,570)],fill='#3c3430')
d.polygon([(215,399),(294,399),(295,417),(216,417)],fill='#654b38',outline=ink,width=3)
# The far-side keys are mostly hidden; only the outer brass edge is visible at left hip.
d.line([(206,422),(203,456)],fill='#aa925e',width=3)
# Heel panels replace front shoe tongues/toes.
for left,right in [(213,255),(265,307)]:
    d.rounded_rectangle((left,650,right,681),6,fill='#604937',outline=ink,width=3)
    d.line(((left+right)//2,651,(left+right)//2,673),fill='#42352b',width=2)
    d.rectangle((left+2,674,right-2,681),fill='#3f342b')
im.save(OUT/'neris-back-layout.png')
print('NERIS_BACK_GUIDE_OK: rear buns, closed coat panel, belt back and heels')
