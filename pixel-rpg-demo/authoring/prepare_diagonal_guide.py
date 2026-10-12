"""NE garment construction guide, to be redrawn by the local model, never final art."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'production/pixel-rpg/model-wave-01/guided'
im = Image.new('RGBA', (512, 768))
d = ImageDraw.Draw(im)
ink = '#3d3430'

def poly(points, color):
    d.polygon(points, fill=color, outline=ink, width=3)

# Far leg and heel are higher in the projected ground plane.
poly([(235,461),(263,467),(261,537),(237,540)], '#d8b49b')
poly([(234,530),(265,529),(264,582),(255,628),(274,636),(271,649),(237,653),(230,642),(238,594)], '#51372d')
d.line([(246,543),(249,584),(241,637)], fill='#866047', width=3)
d.line([(235,646),(269,643)], fill='#27272a', width=5)
# Dress seen from behind and the near side: no frontal buckle or chest panel.
poly([(244,270),(296,264),(322,311),(306,365),(327,478),(294,494),(225,478),(235,359)], '#e9e6db')
d.line([(299,368),(310,474),(291,484)], fill='#a7b6ae', width=4)
# Near leg / diagonal boot, rear seam and right-pointing foreshortened toe.
poly([(280,481),(308,480),(309,552),(281,555)], '#eac6aa')
poly([(279,548),(310,545),(306,605),(301,649),(320,653),(332,645),(337,652),(331,668),(289,677),(277,668),(283,620)], '#604132')
d.line([(291,559),(292,606),(287,661)], fill='#957055', width=3)
d.line([(282,667),(292,671),(327,663)], fill='#29282a', width=5)
# Near arm remains alongside the torso, plain bracer with no circular ornament.
poly([(306,277),(324,286),(330,327),(320,364),(335,405),(326,420),(308,407),(300,365),(306,324)], '#eccab0')
poly([(309,366),(324,361),(338,408),(321,417)], '#654331')
poly([(322,417),(336,410),(342,435),(332,445),(322,433)], '#eccab0')
# Oblique cape wraps across the rear shoulder and occludes most of the back.
poly([(233,260),(279,252),(311,273),(303,309),(291,382),(310,480),(275,486),(262,515),(237,564),(205,589),(219,510),(187,479),(198,394),(218,309)], '#216f6a')
poly([(235,277),(270,267),(291,280),(277,374),(279,469),(250,479),(225,530),(228,462),(206,456),(216,354)], '#328783')
d.line([(267,283),(254,361),(255,447),(248,478)], fill='#18524f', width=5)
d.line([(217,324),(211,404),(198,467)], fill='#184e4b', width=4)
poly([(232,259),(278,250),(310,270),(307,293),(274,306),(227,286)], '#2b7f77')
d.line([(276,265),(273,290)], fill='#23524d', width=4)
# Neck and small right cheek/ear, with the face pointed away. No frontal eyes.
poly([(268,224),(296,224),(301,263),(276,270),(260,254)], '#dab398')
poly([(284,150),(310,156),(316,185),(320,198),(313,207),(314,218),(302,231),(281,219)], '#edc9ac')
# Reuse the actual rear hair painting as a style-rich guide; crop only the hair region.
rear = Image.open(OUT / 'rowan-back-masked-754012.png').convert('RGBA')
hair = rear.crop((158,81,344,235))
pixels = hair.load()
for y in range(hair.height):
    for x in range(hair.width):
        r,g,b,a = pixels[x,y]
        if min(r,g,b)>220 and max(r,g,b)-min(r,g,b)<35:
            pixels[x,y]=(r,g,b,0)
hair = hair.resize((155,150), Image.Resampling.LANCZOS)
im.alpha_composite(hair,(169,88))
im.save(OUT / 'rowan-NE-layout.png')
print('NE_LAYOUT_GUIDE_ONLY: rear/side garments, asymmetric shoulder and heel projection')
