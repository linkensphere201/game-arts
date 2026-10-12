"""Rear cloak and hair layout derived from Osric's owned front design."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
BASE=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
# Mirroring only places asymmetric equipment; rear anatomy/garments are redrawn.
im=ImageOps.mirror(Image.open(BASE/'osric-sword-775003.png').convert('RGB'));d=ImageDraw.Draw(im)
ink='#483c34';cloak='#715543';grey='#b8b9ad'
d.polygon([(204,134),(229,111),(275,112),(310,136),(320,179),(309,222),(287,246),(258,257),(221,244),(197,221),(188,181)],fill=grey,outline=ink,width=3)
d.polygon([(202,157),(211,136),(244,120),(271,121),(251,136),(224,159),(210,188),(202,207),(197,182)],fill='#d9d8c8')
d.polygon([(299,144),(310,167),(311,204),(287,237),(263,247),(244,243),(276,226),(291,198)],fill='#8f958a')
d.line((228,149,219,178,225,213,241,237),fill='#a0a496',width=4)
# No visible beard, shirt front, belt buckle or cloak fastening on the back.
d.polygon([(229,244),(281,244),(282,269),(257,285),(228,268)],fill='#ba9579',outline=ink,width=3)
d.polygon([(200,262),(231,254),(252,269),(284,254),(316,274),(332,356),(329,455),(340,548),(313,558),(286,546),(260,560),(232,550),(198,563),(175,548),(190,435),(186,348)],fill=cloak,outline=ink,width=4)
d.polygon([(200,268),(232,265),(253,279),(283,265),(312,279),(307,299),(284,286),(253,299),(224,283),(200,289)],fill='#594436',outline=ink,width=3)
d.polygon([(199,315),(214,331),(213,433),(198,535),(188,544),(200,431)],fill='#8c6d52')
d.polygon([(292,319),(310,303),(313,432),(327,538),(312,549),(291,439)],fill='#564136')
d.line((251,309,246,402,254,491,254,545),fill='#614b3c',width=3)
d.line((278,336,276,413,286,527),fill='#8a6a50',width=4)
# Quiet rear heel panels; no front-facing toe cap detail.
for left,right in [(205,257),(267,311)]:
 d.polygon([(left+3,614),(right-3,614),(right,658),(right-3,679),(left,679),(left-4,662)],fill='#69513e',outline=ink,width=3)
 d.line(((left+right)//2,621,(left+right)//2,661),fill='#47392f',width=2)
 d.rectangle((left,669,right-2,678),fill='#44382f')
im.save(BASE/'osric-back-layout.png')
print('OSRIC_BACK_GUIDE_OK: rear grey hair, closed cloak, opposite-side sword and heels')
