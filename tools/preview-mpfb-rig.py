"""Annotate actual rig projections and compose joint-review renders. Requires Pillow."""
import json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
out=Path(sys.argv[1]);report=json.loads((out/'binding-report.json').read_text())
neutral=Image.open(out/'01-neutral.png').convert('RGB')
draw=ImageDraw.Draw(neutral)
for bone in report['poses'][0]['projected_bones']:
    a=tuple(round(v*s) for v,s in zip(bone['head'],neutral.size))
    b=tuple(round(v*s) for v,s in zip(bone['tail'],neutral.size))
    draw.line([a,b],fill=(30,230,225),width=4)
    for x,y in [a,b]:draw.ellipse((x-4,y-4,x+4,y+4),fill=(255,196,70))
neutral.save(out/'skeleton-overlay.png')
items=[(neutral,'Skeleton projection'),(Image.open(out/'02-shoulders.png'),'Shoulder check'),(Image.open(out/'03-elbows-side.png'),'Elbow check'),(Image.open(out/'04-hip-knee-side.png'),'Hip / knee check')]
canvas=Image.new('RGB',(1440,410),(35,41,48));font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
draw=ImageDraw.Draw(canvas)
for i,(im,label) in enumerate(items):
    canvas.paste(im.resize((360,360)),(i*360,45));draw.text((i*360+12,12),label,font=font,fill='white')
canvas.save(out/'rig-review-overview.png')
print('RIG_PREVIEW_OK')
