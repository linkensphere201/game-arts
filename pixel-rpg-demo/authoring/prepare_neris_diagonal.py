"""Construct Neris NE garment projection for local model redraw; not final art."""
from pathlib import Path
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,768));d=ImageDraw.Draw(im)
ink='#463639';coat='#75434f';skin='#d7b698'
def poly(points,color):d.polygon(points,fill=color,outline=ink,width=3)
# Far leg/heel is higher; near shoe toe points diagonally away to the right.
poly([(226,528),(252,532),(250,624),(226,626)],'#514a41')
poly([(224,614),(250,615),(261,627),(267,634),(254,645),(225,645),(220,638)],'#654b36')
poly([(267,538),(296,538),(296,644),(272,649)],'#514a41')
poly([(271,635),(296,634),(309,642),(327,643),(326,654),(309,663),(272,662),(267,654)],'#654b36')
d.line([(273,655),(306,658),(323,650)],fill='#352d29',width=3)
# Far sleeve is partly hidden by the oblique back panel.
poly([(218,278),(235,286),(234,350),(222,406),(204,402),(200,351),(204,301)],coat)
poly([(204,401),(223,405),(223,424),(205,422)],'#ddd3b6')
poly([(206,423),(222,426),(220,444),(211,446),(205,436)],skin)
# Closed back: seam offset to left by rotation, no front buttons or buckle.
poly([(218,273),(270,266),(301,284),(306,338),(288,393),(294,453),(315,568),(291,585),(266,576),(249,555),(232,581),(210,574),(217,460),(218,396),(206,322)],coat)
d.line([(242,283),(240,391)],fill='#51353e',width=3)
d.line([(224,424),(218,553),(230,567)],fill='#9a616c',width=4)
d.line([(277,433),(294,567)],fill='#51353e',width=4)
poly([(245,467),(252,466),(260,568),(249,555),(241,572)],'#39302e')
poly([(218,392),(285,386),(293,400),(219,409)],'#654b38')
# Near arm overlaps side of torso; simple cuff and hand.
poly([(284,281),(307,285),(320,331),(311,371),(319,411),(300,423),(288,373),(290,332)],coat)
poly([(300,413),(319,408),(322,429),(304,436)],'#ddd3b6')
poly([(305,436),(322,431),(327,448),(320,460),(310,454)],skin)
# Keys stay on far hip and are largely occluded in this view.
d.line([(213,414),(210,441)],fill='#aa925e',width=3)
poly([(245,239),(286,236),(288,271),(270,283),(243,270)],skin)
poly([(243,267),(270,277),(288,264),(293,278),(272,291),(238,280)],'#ddd3b6')
# A single constructed skull/ear silhouette avoids overlapped source ears.
poly([(294,157),(317,172),(320,195),(332,208),(322,218),(321,236),(301,246),(284,218)],skin)
poly([(177,169),(159,154),(168,187),(185,200)],skin)
poly([(178,143),(194,111),(222,94),(260,95),(290,113),(306,144),(307,182),(301,211),(283,237),(248,252),(211,241),(190,219),(177,183)],'#353431')
d.line([(190,138),(211,111),(243,105),(274,116)],fill='#56534b',width=5)
d.line([(247,110),(243,166),(251,228)],fill='#252724',width=3)
poly([(285,179),(332,156),(316,191),(291,206)],skin)
d.line([(320,169),(302,189),(291,195)],fill='#ae8166',width=2)
d.ellipse((166,211,195,246),fill='#353431',outline=ink,width=3)
d.ellipse((279,217,318,253),fill='#353431',outline=ink,width=3)
d.arc((285,223,312,247),10,300,fill='#575149',width=2)
im.save(OUT/'neris-NE-layout.png')
print('NERIS_NE_GUIDE_OK: oblique closed coat, asymmetric sleeve and diagonal heels')
