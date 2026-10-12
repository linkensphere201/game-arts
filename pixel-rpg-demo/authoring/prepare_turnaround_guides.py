"""Owned illustration-derived back-view layout guide; never a finished sprite."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'production/pixel-rpg/model-wave-01/guided'
im=Image.open(ROOT/'production/pixel-rpg/model-sprite-study/segmented-source.png').convert('RGBA')
original_alpha=im.getchannel('A')
d=ImageDraw.Draw(im)
# Paint over frontal facial features while preserving the approved head silhouette.
d.polygon([(176,98),(304,91),(343,151),(347,235),(280,252),(190,235),(176,177)],fill='#74391f')
d.polygon([(193,111),(277,100),(326,145),(323,211),(296,233),(229,232),(192,202)],fill='#a74e25')
for x in [201,223,249,278,304,324]:
 d.line([(x,130),(x+8,170),(x-3,218)],fill='#6e311f',width=4)
d.arc((196,106,323,202),190,337,fill='#d1833e',width=8)
# Rear shoulder cape hangs over torso: do not leave the front buckle or chest visible.
d.polygon([(209,251),(319,251),(337,289),(376,457),(344,485),(300,475),(258,495),(212,477),(157,480),(190,305)],fill='#166b65',outline='#263d36',width=4)
d.polygon([(213,262),(255,276),(315,261),(327,313),(303,457),(255,476),(207,459),(190,454)],fill='#278778')
d.line([(255,278),(247,359),(255,464)],fill='#1c5753',width=5)
d.line([(209,290),(204,349),(183,444)],fill='#164a47',width=5)
d.line([(318,288),(329,373),(344,463)],fill='#164a47',width=6)
im.putalpha(original_alpha)
# Replace lower clothing silhouette too; front boot toes/cuffs must not survive.
d=ImageDraw.Draw(im)
d.rectangle((170,488,342,720),fill=(0,0,0,0))
d.polygon([(208,466),(316,466),(323,497),(204,497)],fill='#dddccc',outline='#4e5956',width=3)
d.line([(237,473),(235,495)],fill='#aeb4aa',width=3)
d.line([(287,473),(291,495)],fill='#aeb4aa',width=3)
for x in [214,278]:
 d.polygon([(x,498),(x+29,498),(x+27,540),(x+3,540)],fill='#e7c8af',outline='#745549',width=3)
 # Rear shafts, plain top edges, vertical rear seam and compact rectangular heels.
 d.polygon([(x-3,535),(x+32,535),(x+28,573),(x+24,620),(x+28,649),(x+25,660),(x+2,660),(x-1,649),(x+5,620),(x+1,575)],fill='#53352c',outline='#2e292a',width=4)
 d.line([(x+14,546),(x+14,622),(x+13,646)],fill='#805440',width=3)
 d.line([(x+2,650),(x+25,650)],fill='#251f23',width=5)
 d.rectangle((x+3,653,x+24,661),fill='#2c2526')
im.save(OUT/'rowan-back-layout-v2.png')
print('Back-view composition guide saved; not final art.')
