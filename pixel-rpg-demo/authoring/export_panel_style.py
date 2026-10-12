"""Convert the local model frame into a native nine-patch UI style."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from scipy import ndimage
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
OUT=ROOT/'pixel-rpg-demo/mosslight/model_ui';OUT.mkdir(exist_ok=True)
source=BASE/'panel-767001.png'
im=Image.open(source).convert('RGB');a=np.asarray(im)
white=(a.min(2)>233)&(a.max(2).astype(int)-a.min(2)<28)
labels,_=ndimage.label(~white);counts=np.bincount(labels.ravel());counts[0]=0
mask=labels==counts.argmax()
im=im.convert('RGBA');im.putalpha(Image.fromarray((mask*255).astype('uint8')))
im=im.crop(im.getbbox()).resize((96,96),Image.Resampling.LANCZOS)
alpha=im.getchannel('A').point(lambda v:255 if v>=160 else 0)
im=im.convert('RGB').quantize(colors=24,dither=Image.Dither.NONE).convert('RGBA');im.putalpha(alpha)
im.save(OUT/'panel.png')
assert set(np.unique(np.asarray(im)[:,:,3]))=={0,255}
(OUT/'panel.tres').write_text('''[gd_resource type="StyleBoxTexture" load_steps=2 format=3]

[ext_resource type="Texture2D" path="panel.png" id="1"]

[resource]
texture = ExtResource("1")
texture_margin_left = 12.0
texture_margin_top = 12.0
texture_margin_right = 12.0
texture_margin_bottom = 12.0
content_margin_left = 12.0
content_margin_top = 12.0
content_margin_right = 12.0
content_margin_bottom = 12.0
axis_stretch_horizontal = 1
axis_stretch_vertical = 1
''',encoding='utf-8')
(BASE/'panel-conversion.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256((OUT/'panel.png').read_bytes()).hexdigest(),'size':[96,96],'corner_margin':12,'colors':24,'status':'model-derived nine-patch study; art approval pending'},indent=2))
print('PANEL_EXPORT_OK: 96x96, binary alpha, 12px corners, relative texture resource')
