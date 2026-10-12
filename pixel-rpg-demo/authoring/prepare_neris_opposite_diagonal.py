"""Opposite diagonal construction; equipment is corrected before independent redraw."""
from pathlib import Path
import argparse,hashlib,json
from PIL import Image,ImageDraw,ImageOps
p=argparse.ArgumentParser();p.add_argument('--heading',choices=['NW','SW'],required=True);a=p.parse_args()
OUT=Path(__file__).resolve().parents[2]/'production/pixel-rpg/model-wave-01/guided'
source=OUT/('neris-NE-777022.png' if a.heading=='NW' else 'neris-SE-details-777026.png')
im=ImageOps.mirror(Image.open(source).convert('RGB'));d=ImageDraw.Draw(im)
if a.heading=='SW':
    # Keys on the opposite hip are occluded; preserve arm and cuff at the left.
    im.paste(im.crop((218,419,231,474)),(203,419))
else:
    # On this rear diagonal the equipped hip is near the camera.
    d.polygon([(212,408),(218,408),(218,424),(212,424)],fill='#634b36')
    d.ellipse((210,421,223,435),outline='#b79a64',width=3)
    d.line([(213,434),(212,464),(219,464),(219,459)],fill='#b79a64',width=3)
    d.line([(222,434),(225,456),(230,456)],fill='#b79a64',width=3)
name=f'neris-{a.heading}-layout';im.save(OUT/(name+'.png'))
(OUT/(name+'.json')).write_text(json.dumps({'source':source.name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'heading':a.heading,'operation':'reflected guide with corrected asymmetric equipment; independent model redraw required','status':'construction only'},indent=2))
print('NERIS_OPPOSITE_DIAGONAL_GUIDE_OK',a.heading)
