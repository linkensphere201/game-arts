"""West-side guide: reflected construction only, with far-side keys occluded before redraw."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageOps
OUT=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
source=OUT/'neris-profile-777018.png'
im=ImageOps.mirror(Image.open(source).convert('RGB'));d=ImageDraw.Draw(im)
# Opposite side hides the asymmetric key ring. Continue the coat instead.
cloth=im.crop((233,419,250,476));im.paste(cloth,(210,419))
d.line([(208,424),(212,472)],fill='#52373d',width=2)
im.save(OUT/'neris-W-layout.png')
(OUT/'neris-W-layout.json').write_text(json.dumps({'source':source.name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'operation':'reflection as construction input only; far-side keys removed; requires independent local model redraw','status':'guide, not deliverable'},indent=2))
print('NERIS_W_GUIDE_OK: keys occluded; pending independent redraw')
