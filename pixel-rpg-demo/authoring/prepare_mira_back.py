"""Rear garment layout derived from the original Mira design for local redraw."""
from pathlib import Path
from PIL import Image,ImageDraw
BASE=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
im=Image.open(BASE/'mira-herbs-774002.png').convert('RGB');d=ImageDraw.Draw(im)
ink='#44382e';hair='#875a36';sage='#526445';linen='#ded5b4'
# Back skull/hair hides the face and the frontal neckline.
d.polygon([(175,151),(194,120),(248,116),(284,135),(301,173),(299,216),(280,252),(247,273),(204,256),(179,222),(169,180)],fill=hair,outline=ink,width=4)
d.polygon([(186,163),(206,132),(240,124),(264,130),(235,145),(207,180),(194,217),(185,226)],fill='#a87146')
d.line((277,145,284,180,279,217,267,245),fill='#69472e',width=5)
# Rear dress has no apron bib; cream straps cross and tie at the waist.
d.polygon([(198,279),(274,279),(288,309),(291,396),(306,475),(313,570),(281,588),(196,581),(169,561),(183,447),(188,377),(183,310)],fill=sage,outline=ink,width=4)
d.polygon([(191,439),(202,447),(190,541),(184,557),(182,514)],fill='#718461')
d.line((276,440,292,556),fill='#394b35',width=5)
d.line((202,284,276,393),fill=linen,width=12)
d.line((273,284,204,393),fill=linen,width=12)
d.rectangle((184,397,291,413),fill=linen,outline='#a49c7f',width=3)
d.polygon([(236,403),(213,390),(201,400),(215,413),(236,408),(259,390),(276,400),(261,414),(239,409)],fill=linen,outline='#928b70',width=3)
d.line((232,412,220,452),fill=linen,width=8);d.line((241,412,253,450),fill=linen,width=8)
# Move the ponytail to the opposite screen side when seen from behind.
d.polygon([(141,183),(169,168),(195,206),(188,281),(177,344),(142,342),(122,266)],fill='white')
d.polygon([(197,159),(187,182),(185,220),(197,251),(216,249),(222,216),(215,185)],fill=hair,outline=ink,width=3)
d.polygon([(264,221),(285,231),(303,267),(312,316),(296,357),(275,375),(284,329),(271,291),(256,263)],fill=hair,outline=ink,width=4)
d.line((282,250,294,291,299,324,286,355),fill='#ad7a4c',width=5)
# Remove the front pouch/herbs; only a narrow far-side leather edge is visible.
d.polygon([(292,365),(344,357),(346,481),(299,489),(284,452),(285,409)],fill='white')
d.polygon([(283,365),(304,365),(300,414),(306,444),(293,455),(280,443)],fill='#ddb797',outline=ink,width=3)
d.rounded_rectangle((167,412,188,474),5,fill='#81553a',outline=ink,width=3)
# Tail is attached at the rear pelvis instead of floating beside the skirt.
d.polygon([(247,436),(272,440),(302,480),(333,511),(351,560),(344,603),(316,629),(283,638),(297,614),(308,586),(296,550),(269,518),(244,482)],fill=hair,outline=ink,width=4)
d.polygon([(308,584),(325,577),(337,589),(344,584),(337,612),(315,630),(286,638),(300,615)],fill='#d6c3a0',outline=ink,width=3)
# Boot backs: plain heel panels rather than front lacing/toe caps.
for left,right in [(181,232),(249,297)]:
    d.polygon([(left+5,628),(right-4,628),(right,675),(right-4,681),(left,681),(left-3,665)],fill='#775039',outline=ink,width=3)
    d.line(((left+right)//2,634,(left+right)//2,664),fill='#49372c',width=2)
    d.rectangle((left+1,668,right-2,678),fill='#513c2d',outline=ink,width=2)
im.save(BASE/'mira-back-layout.png')
print('MIRA_BACK_GUIDE_OK: rear hair, crossed apron ties, tail root and boot heels')
