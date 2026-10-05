"""Art-directed pixel cleanup and a small cutout animation, derived from the local AI draft.

This is hand-authored pose data, NOT model-generated animation. All processing is local.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/ember-imp'
OUT.mkdir(parents=True, exist_ok=True)
base = Image.open(ROOT / 'production/selected/canonical.png').convert('RGBA')
pixels = base.load()
original = base.copy()
# Keep the AI-designed upper body; discard the raised legs and floor remnants.
for y in range(40, 64):
    for x in range(64):
        pixels[x, y] = (0, 0, 0, 0)
# Warm ivory horn interior highlights, preserving the silhouette's dark outline.
alpha = original.getchannel('A')
for y in range(4, 22):
    for x in range(16, 51):
        r, g, b, a = pixels[x, y]
        in_horn = (x < 29 and y < 20) or (x > 39 and y < 21)
        interior = a and all(alpha.getpixel((x+dx, y+dy)) for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)])
        if in_horn and interior and max(r,g,b)-min(r,g,b) < 35:
            shade = (107, 75, 46) if max(r,g,b) < 30 else (218, 177, 110)
            pixels[x,y] = (*shade,255)
# An intentional warm eye highlight and a visible second glint.
for x,y in [(32,22),(33,22),(37,23)]:
    if pixels[x,y][3]: pixels[x,y] = (255, 211, 86, 255)
base.save(OUT / 'upper-body.png')

OUTLINE = (35, 15, 16, 255)
DARK = (105, 25, 8, 255)
RED = (171, 46, 9, 255)
LIGHT = (210, 68, 13, 255)

def leg(canvas, hip, knee, foot, rear=False):
    d=ImageDraw.Draw(canvas)
    d.line([hip,knee,foot],fill=OUTLINE,width=8)
    for p in [hip,knee]:
        d.rectangle((p[0]-3,p[1]-3,p[0]+3,p[1]+3),fill=OUTLINE)
    d.line([hip,knee,foot],fill=DARK if rear else RED,width=5)
    d.line([(hip[0]-1,hip[1]),(knee[0]-1,knee[1]),(foot[0]-1,foot[1])],fill=RED if rear else LIGHT,width=2)
    x,y=foot
    d.polygon([(x-3,y-1),(x+1,y-1),(x+5,y+1),(x+5,y+3),(x-3,y+3)],fill=OUTLINE)
    d.polygon([(x-2,y),(x+1,y),(x+4,y+1),(x+4,y+2),(x-2,y+2)],fill=DARK if rear else RED)
    d.point((x+3,y+1),fill=(218,177,110,255))

def make_frame(rear_foot, front_foot, bob=0, sway=0, blink=False):
    result=Image.new('RGBA',(64,64))
    rear_hip=(28+sway,39+bob)
    front_hip=(32+sway,40+bob)
    rear_knee=(round((rear_hip[0]+rear_foot[0])/2)-1,round((rear_hip[1]+rear_foot[1])/2))
    front_knee=(round((front_hip[0]+front_foot[0])/2)+1,round((front_hip[1]+front_foot[1])/2))
    leg(result,rear_hip,rear_knee,rear_foot,True)
    leg(result,front_hip,front_knee,front_foot)
    body=base.copy()
    if blink:
        d=ImageDraw.Draw(body)
        d.line((31,22,34,22),fill=DARK,width=1)
    result.alpha_composite(body,(sway,bob))
    return result

poses={
 'idle': [dict(rear=(24,52),front=(35,52),bob=0,sway=0),
          dict(rear=(24,52),front=(35,52),bob=-1,sway=0),
          dict(rear=(24,52),front=(35,52),bob=-1,sway=0,blink=True),
          dict(rear=(24,52),front=(35,52),bob=0,sway=0)],
 'walk': [dict(rear=(23,52),front=(37,52),bob=0,sway=0),
          dict(rear=(27,50),front=(32,52),bob=-1,sway=0),
          dict(rear=(32,49),front=(27,52),bob=0,sway=1),
          dict(rear=(37,52),front=(23,52),bob=0,sway=0),
          dict(rear=(32,52),front=(27,50),bob=-1,sway=0),
          dict(rear=(27,52),front=(32,49),bob=0,sway=-1)]
}
frames={name:[make_frame(p['rear'],p['front'],p['bob'],p['sway'],p.get('blink',False)) for p in items] for name,items in poses.items()}
# One palette shared by every animation; do not quantize each frame independently.
all_frames=frames['idle']+frames['walk']
contact=Image.new('RGBA',(640,64))
for i,frame in enumerate(all_frames): contact.alpha_composite(frame,(i*64,0))
palette=contact.convert('RGB').quantize(colors=32,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
for name,items in frames.items():
    sheet=Image.new('RGBA',(64*len(items),64))
    for i,frame in enumerate(items):
        result=frame.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA')
        result.putalpha(frame.getchannel('A'))
        # Canonical transparent RGB avoids halos in downstream editors.
        a=np.array(result); a[a[:,:,3]==0]=0; result=Image.fromarray(a)
        frames[name][i]=result
        sheet.alpha_composite(result,(64*i,0))
        frame_dir=OUT/'frames'; frame_dir.mkdir(exist_ok=True)
        result.save(frame_dir/f'{name}_{i:02d}.png')
    sheet.save(OUT/f'{name}.png')
frames['idle'][0].save(OUT/'canonical.png')
(ROOT/'production/animation-poses.json').write_text(json.dumps({'method':'Art-directed cutout upper body with hand-authored pixel legs; not generated animation','fps':8,'poses':poses},indent=2),encoding='utf-8')
# A clearly presented sprite preview, not a substitute for the Godot render.
preview=[]
for frame in frames['idle']*2+frames['walk']*2:
    bg=Image.new('RGBA',(64,64),'#182437'); bg.alpha_composite(frame)
    preview.append(bg.resize((384,384),Image.Resampling.NEAREST).convert('RGB'))
preview[0].save(ROOT/'validation/sprite-preview.gif',save_all=True,append_images=preview[1:],duration=125,loop=0)
frames['idle'][0].resize((512,512),Image.Resampling.NEAREST).save(ROOT/'validation/character-preview.png')
print('SPRITES_AUTHORED',OUT)
