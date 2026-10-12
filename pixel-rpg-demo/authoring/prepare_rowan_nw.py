"""NW composition scaffold for local model redraw, not final mirrored artwork."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
im=ImageOps.mirror(Image.open(BASE/'rowan-NE-shoulder-758002.png').convert('RGB'))
d=ImageDraw.Draw(im)
# Near left hip: utility sheath below the cape edge, away from the back panel.
d.polygon([(213,376),(227,378),(240,435),(231,449),(222,440)],fill='#704c34',outline='#392f28',width=2)
d.polygon([(213,358),(220,356),(230,385),(222,387)],fill='#a88750',outline='#55402d',width=2)
d.line([(216,384),(230,381)],fill='#c6a66c',width=3)
im.save(BASE/'rowan-NW-layout.png')
print('NW_LAYOUT_READY: camera-facing left hip; local redraw required')
