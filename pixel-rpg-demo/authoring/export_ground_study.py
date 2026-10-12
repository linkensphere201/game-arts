"""Convert the locally generated paving study to a repeatable pixel texture."""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/pixel-rpg/model-wave-01/ground'
source=BASE/'warm-paving-759002.png';out=ROOT/'pixel-rpg-demo/mosslight/model_ground';out.mkdir(exist_ok=True)
im=Image.open(source).convert('RGB').resize((128,128),Image.Resampling.LANCZOS).quantize(colors=24,dither=Image.Dither.NONE).convert('RGB')
# Repeat at whole-pattern boundaries; do not claim arbitrary 32px atlas cells connect.
im.save(out/'paving.png')
board=Image.new('RGB',(512,512))
for y in range(4):
 for x in range(4):board.paste(im,(x*128,y*128))
board.save(BASE/'paving-repeat.png')
(BASE/'conversion.json').write_text(json.dumps({'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256((out/'paving.png').read_bytes()).hexdigest(),'size':[128,128],'colors':len(im.getcolors()),'status':'repeat study; edge tiles, terrain transitions and art acceptance missing','rejected_source':'warm-paving-759001.png: triangular ceramic-like pattern and excessive surface realism'},indent=2))
assert im.size==(128,128) and len(im.getcolors())<=24
print('PAVING_CONVERSION_OK: 128px repeat pattern, <=24 colors')

source=BASE/'meadow-grass-759004.png'
grass=Image.open(source).convert('RGB').resize((128,128),Image.Resampling.LANCZOS).quantize(colors=16,dither=Image.Dither.NONE).convert('RGB')
grass.save(out/'grass.png')
board=Image.new('RGB',(512,512))
for y in range(4):
 for x in range(4):board.paste(grass,(x*128,y*128))
board.save(BASE/'grass-repeat.png')
(BASE/'grass-conversion.json').write_text(json.dumps({'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256((out/'grass.png').read_bytes()).hexdigest(),'size':[128,128],'colors':len(grass.getcolors()),'status':'low-contrast grass study; terrain transitions and art acceptance missing','rejected_source':'meadow-grass-759003.png: unrelated ring graphic'},indent=2))
assert grass.size==(128,128) and len(grass.getcolors())<=16
print('GRASS_CONVERSION_OK: 128px repeat pattern, <=16 colors')
