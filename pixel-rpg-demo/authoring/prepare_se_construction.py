"""Explicit front-quarter anatomical/costume guide for local-model redrawing only."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
im=Image.new('RGBA',(512,768));d=ImageDraw.Draw(im)
ink='#49362e';skin='#edc7ad';brown='#604132';white='#e8e6da'
def poly(points,c):d.polygon(points,fill=c,outline=ink,width=3)
# Far leg higher in the projected plane, toe points down/right.
poly([(274,437),(304,435),(304,529),(281,535)],skin)
poly([(278,516),(309,516),(302,590),(303,632),(323,641),(321,653),(282,653),(275,641),(283,585)],brown)
d.line([(282,647),(320,647)],fill='#27272a',width=5)
# Cape behind the body, asymmetric drape, no extra equipment.
poly([(231,266),(294,260),(317,291),(331,426),(314,503),(300,563),(289,578),(292,490),(225,472),(180,560),(195,470),(161,452),(183,379),(216,301)],'#206e65')
poly([(228,294),(249,295),(223,388),(202,471),(178,489),(190,444),(177,441)],'#2d8a7b')
# Far exposed shoulder and forearm.
poly([(293,261),(311,270),(317,299),(312,351),(326,386),(321,401),(307,395),(297,352),(296,304)],skin)
poly([(308,362),(319,359),(333,399),(319,406)],brown)
poly([(319,405),(332,399),(337,421),(328,430),(318,421)],skin)
# Oblique bodice and waist, buckle shifted onto front plane at right.
poly([(238,277),(284,265),(308,286),(307,321),(292,350),(241,355),(235,326)],white)
d.polygon([(239,290),(253,293),(256,330),(250,350),(239,350)],fill='#acbcb2')
poly([(242,345),(293,340),(299,360),(243,371)],brown)
d.rectangle((282,345,297,359),fill='#b99550',outline=ink,width=2)
d.rectangle((286,348,294,356),fill=brown)
# Tunic hem follows the angled waist; dark shorts beneath it.
poly([(238,367),(295,358),(310,444),(284,459),(221,470),(223,420)],white)
d.line([(259,373),(252,457)],fill='#aab5ac',width=4)
d.line([(286,373),(296,443)],fill='#aab5ac',width=4)
poly([(224,460),(253,460),(253,491),(226,495)],'#382c28')
poly([(277,451),(306,444),(305,475),(282,485)],'#382c28')
# Near leg / boot; far boot must not copy the near leg's footprint.
poly([(226,490),(254,486),(255,544),(230,549)],skin)
poly([(225,534),(257,533),(253,600),(247,650),(270,664),(270,677),(230,679),(219,669),(226,611)],brown)
poly([(225,537),(238,548),(255,536),(251,567),(238,554),(224,567)],'#483026')
d.line([(225,672),(267,671)],fill='#282529',width=5)
# Near exposed shoulder and arm, cloth band below the bare shoulder.
poly([(231,266),(250,271),(255,299),(243,348),(234,391),(218,391),(220,346),(218,300)],skin)
poly([(219,369),(239,376),(231,415),(211,408)],brown)
poly([(212,406),(230,414),(228,436),(216,443),(206,433)],skin)
poly([(222,286),(249,294),(252,305),(223,300)],'#287e70')
poly([(292,280),(311,285),(314,298),(294,293)],'#287e70')
# Neck ties and visible clasp on the forward-right part of the torso.
poly([(270,231),(289,230),(295,265),(278,278),(258,261)],skin)
poly([(261,252),(282,263),(304,278),(298,286),(278,273),(242,292),(235,282)],'#257668')
d.ellipse((278,264,288,275),fill='#a99154',outline=ink,width=2)
# Face looks right: uneven eye sizes and visible right-pointing nose silhouette.
poly([(248,131),(295,127),(315,151),(317,181),(330,195),(320,204),(318,224),(300,240),(278,234),(251,213)],skin)
d.ellipse((277,173,293,188),fill='#f7f3e7',outline=ink,width=2)
d.ellipse((286,176,293,188),fill='#41644e')
d.ellipse((308,169,316,181),fill='#f7f3e7',outline=ink,width=2)
d.ellipse((312,171,316,181),fill='#41644e')
d.line([(307,217),(316,213)],fill='#a96c59',width=2)
poly([(203,117),(243,97),(280,103),(303,122),(316,156),(296,142),(283,154),(271,180),(264,199),(270,229),(249,244),(220,235),(200,216),(194,180),(185,188),(193,148)],'#97502f')
d.polygon([(207,129),(240,111),(276,116),(294,137),(268,134),(241,148),(213,167),(200,172)],fill='#ba7548')
d.line([(223,153),(214,187),(219,221)],fill='#663a27',width=4)
d.line([(248,151),(239,190),(248,228)],fill='#663a27',width=4)
im.save(ROOT/'production/pixel-rpg/model-wave-01/guided/rowan-SE-constructed-layout.png')
print('SE_CONSTRUCTION_GUIDE_ONLY')
