"""Owned key, scroll, bread and pouch silhouettes for local-model redraw."""
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
for name in ['key','scroll','bread','pouch']:
    im=Image.new('RGBA',(512,512));d=ImageDraw.Draw(im)
    if name=='key':
        d.ellipse((124,90,294,260),fill='#b99858',outline='#51432e',width=9)
        d.ellipse((163,129,255,221),fill=(0,0,0,0),outline='#715933',width=6)
        d.polygon([(250,217),(390,357),(367,380),(341,354),(315,380),(293,357),(321,329),(230,238)],fill='#b99858',outline='#51432e',width=8)
    elif name=='scroll':
        d.rectangle((142,133,356,380),fill='#ded5b6',outline='#665239',width=8)
        d.rounded_rectangle((118,98,380,158),23,fill='#e9ddbc',outline='#665239',width=7)
        d.ellipse((120,100,163,156),fill='#b3a07b',outline='#665239',width=5)
        d.rounded_rectangle((121,351,382,412),22,fill='#e9ddbc',outline='#665239',width=7)
        d.ellipse((338,353,379,409),fill='#b3a07b',outline='#665239',width=5)
        d.rectangle((239,157,263,351),fill='#397a70',outline='#35483b',width=4)
        d.ellipse((222,239,279,296),fill='#b99858',outline='#665239',width=5)
    elif name=='bread':
        d.ellipse((90,178,424,375),fill='#94613c',outline='#4c382b',width=8)
        d.ellipse((95,144,419,340),fill='#bf955c',outline='#4c382b',width=7)
        for x in [161,237,309]:
            d.polygon([(x,173),(x+22,168),(x+55,265),(x+30,268)],fill='#e0bd7d',outline='#966d40',width=4)
    else:
        d.polygon([(215,142),(294,142),(298,210),(358,310),(357,371),(319,407),(190,407),(153,370),(156,308),(213,209)],fill='#987049',outline='#49392d',width=8)
        d.polygon([(213,143),(190,95),(249,112),(310,94),(292,147)],fill='#b39160',outline='#49392d',width=6)
        d.line((210,177,298,178),fill='#397a70',width=17)
        d.line((250,181,273,247),fill='#397a70',width=10)
        d.arc((185,246,329,391),90,195,fill='#c09b62',width=7)
    im.save(root/f'{name}-layout.png')
