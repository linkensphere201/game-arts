"""Left-facing layout; mirrored pose scaffold is redrawn by the local model.

The front design's left-hip utility sheath is now on the camera-facing side.
This file does not replace gameplay's currently mirrored movement frames.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
im=ImageOps.mirror(Image.open(BASE/'rowan-side-shoulder-755004.png').convert('RGB'))
d=ImageDraw.Draw(im)
# Near-side hip attachment behind the forearm, not a second frontal belt buckle.
d.polygon([(253,359),(265,356),(282,412),(275,428),(265,418)],fill='#6f4931',outline='#382e28',width=2)
d.polygon([(252,339),(259,337),(269,367),(262,371)],fill='#b28d54',outline='#59432c',width=2)
d.line([(255,361),(270,358)],fill='#c6a66c',width=4)
im.save(BASE/'rowan-left-layout.png')
