"""Owned composition guides; final art is redrawn by the local model."""
from pathlib import Path
from PIL import Image,ImageDraw

OUT=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
for name in ['axe','ring','mushroom']:
    image=Image.new('RGBA',(512,512));d=ImageDraw.Draw(image)
    if name=='axe':
        d.polygon([(286,83),(318,99),(195,426),(160,414)],fill='#926c49',outline='#44382e',width=8)
        d.polygon([(160,99),(248,112),(304,136),(275,221),(224,196),(116,205),(89,173)],fill='#afbab3',outline='#39433f',width=8)
        d.polygon([(160,99),(146,167),(116,205),(89,173)],fill='#d7d6bc',outline='#68756a',width=4)
        d.polygon([(256,115),(302,131),(282,181),(239,164)],fill='#b49860',outline='#594936',width=5)
        for y in [300,320,340,360]:d.line((204-(y-300)//3,y,229-(y-300)//3,y+10),fill='#39786c',width=12)
    elif name=='ring':
        d.ellipse((122,152,395,408),fill='#ad874b',outline='#51432e',width=9)
        d.ellipse((174,206,343,355),fill=(0,0,0,0),outline='#78592f',width=9)
        d.polygon([(187,142),(242,90),(306,106),(337,165),(284,214),(219,205)],fill='#b69a5c',outline='#544730',width=7)
        d.polygon([(207,144),(246,111),(293,123),(311,165),(278,191),(234,185)],fill='#3c8d80',outline='#294f4a',width=6)
        d.polygon([(207,144),(246,111),(252,153),(234,185)],fill='#74b5a1')
    else:
        d.polygon([(227,246),(299,246),(315,386),(284,414),(213,399)],fill='#dfd0ad',outline='#554733',width=7)
        d.ellipse((104,142,407,302),fill='#795334',outline='#4a392c',width=8)
        d.pieslice((105,79,407,334),180,360,fill='#b1764b',outline='#4a392c',width=8)
        d.ellipse((147,157,188,179),fill='#e3ca97')
        d.ellipse((232,116,275,136),fill='#e3ca97')
        d.ellipse((325,163,364,182),fill='#e3ca97')
    image.save(OUT/f'{name}-layout.png')
print('EQUIPMENT_GUIDES_OK: axe, ring, mushroom')
