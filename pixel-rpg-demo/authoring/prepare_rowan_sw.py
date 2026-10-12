"""Front-left composition guide for an independent local-model redraw."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
im=ImageOps.mirror(Image.open(BASE/'rowan-SE-cape-757005.png').convert('RGB'))
d=ImageDraw.Draw(im)
# Left hip is now the visible outer hip; the buckle remains on the front waist.
d.polygon([(263,352),(277,354),(277,410),(269,424),(260,414)],fill='#704b32',outline='#392c24',width=2)
d.polygon([(266,332),(274,333),(273,363),(265,362)],fill='#ab8950',outline='#56402d',width=2)
d.line([(262,362),(278,363)],fill='#c6a66c',width=3)
im.save(BASE/'rowan-SW-layout.png')
print('SW_LAYOUT_READY')
