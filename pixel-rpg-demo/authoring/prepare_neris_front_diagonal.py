"""Owned southeast Neris guide with rotated front tailoring and hip equipment."""
from pathlib import Path
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
im=Image.new('RGBA',(512,768));d=ImageDraw.Draw(im)
ink='#443739';coat='#75434f';skin='#d7b698';hair='#353431';cream='#ddd3b6'
def poly(points,color):d.polygon(points,fill=color,outline=ink,width=3)
# Far leg and toe sit higher than the near leg on the diagonal floor plane.
poly([(274,532),(299,532),(296,623),(273,625)],'#514a41')
poly([(273,615),(296,615),(308,633),(322,638),(320,648),(282,647),(269,637)],'#654b36')
poly([(224,534),(254,537),(251,638),(225,641)],'#514a41')
poly([(224,632),(252,631),(264,647),(283,654),(280,665),(238,663),(221,653)],'#654b36')
d.line([(227,655),(246,659),(279,660)],fill='#342b27',width=3)
# Far arm behind the torso.
poly([(290,285),(312,295),(321,343),(309,397),(314,420),(298,426),(288,383),(293,334)],coat)
poly([(299,414),(314,413),(317,432),(302,437)],cream)
poly([(303,437),(318,433),(321,451),(313,459),(304,452)],skin)
# Asymmetric front panel, offset placket, and side silhouette.
poly([(222,276),(267,270),(294,280),(306,317),(294,393),(307,558),(282,588),(269,573),(258,537),(248,586),(218,583),(206,557),(216,393),(204,323)],coat)
d.line([(275,293),(281,387),(281,463)],fill='#4f333b',width=3)
poly([(273,461),(284,464),(288,565),(270,575),(259,547)],'#42372e')
d.line([(222,425),(216,553),(232,570)],fill='#a06471',width=4)
poly([(216,391),(294,391),(297,408),(216,408)],'#654b38')
d.rectangle((278,391,290,408),outline='#b39a62',width=3)
for y in (330,357,379,433,457):d.ellipse((279,y,286,y+7),fill='#b39a62',outline=ink,width=1)
# Visible hip keys forward of near arm.
d.ellipse((288,411,303,427),outline='#b39a62',width=4)
for x,y in [(291,425),(301,430)]:
    d.line((x,y,x,y+32),fill='#b39a62',width=3)
    d.line((x,y+28,x+6,y+28),fill='#b39a62',width=3)
# Near sleeve occludes side panel and ends above a relaxed hand.
poly([(220,282),(242,291),(251,331),(241,383),(248,414),(228,426),(211,385),(213,334)],coat)
poly([(229,415),(247,411),(252,432),(232,439)],cream)
poly([(234,439),(252,434),(257,452),(251,466),(238,463)],skin)
poly([(243,238),(282,239),(285,273),(267,290),(239,273)],skin)
poly([(238,269),(266,280),(282,267),(290,280),(269,296),(235,282)],cream)
# Three-quarter face: far eye narrower, nose offset, near ear exposed.
poly([(199,144),(226,112),(269,104),(302,121),(319,149),(321,187),(330,210),(322,228),(299,250),(266,260),(233,248),(211,221),(194,185)],skin)
poly([(198,191),(182,165),(184,131),(203,104),(237,86),(274,88),(305,106),(323,137),(313,153),(301,137),(277,115),(252,122),(222,129),(211,162),(215,204)],hair)
d.line([(197,130),(223,107),(255,99),(280,105)],fill='#58564e',width=4)
d.ellipse((182,219,218,253),fill=hair,outline=ink,width=3)
poly([(220,187),(171,160),(184,193),(215,212)],skin)
d.line([(185,174),(207,196)],fill='#a87861',width=2)
d.line([(254,163),(279,161)],fill=ink,width=3)
d.line([(304,162),(315,165)],fill=ink,width=2)
d.ellipse((254,174,280,195),fill='#efe2cd',outline=ink,width=2)
d.ellipse((269,176,279,194),fill='#634932')
d.ellipse((304,176,316,193),fill='#efe2cd',outline=ink,width=2)
d.ellipse((310,178,316,192),fill='#634932')
d.line([(299,194),(305,212),(299,215)],fill='#9d785e',width=2)
d.line([(291,232),(306,231)],fill='#936a55',width=2)
im.save(OUT/'neris-SE-layout.png')
print('NERIS_SE_GUIDE_OK: oblique front coat, key ring and diagonal toes')
