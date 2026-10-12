"""Create readable GIFs/contact sheets from actual Godot captures, no AI redraw."""
from pathlib import Path
import sys,json
from PIL import Image,ImageDraw,ImageFont
out=Path(sys.argv[1]);captures=out/'godot-demo/captures';data=json.loads((out/'actions.json').read_text())
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
overview=Image.new('RGB',(1500,800),(25,32,42));draw=ImageDraw.Draw(overview)
for i,clip in enumerate(data['clips']):
    files=sorted(captures.glob(clip['name']+'-*.png'))
    assert len(files)==int(clip['duration']*20)+1,(clip['name'],len(files))
    frames=[]
    for f in files:
        im=Image.open(f).convert('RGB')
        # Remove UI column, retaining actual rendered body and ground.
        im=im.crop((350,20,950,700)).resize((360,408))
        frames.append(im)
    durations=[50]*len(frames);durations[-1]=50 if clip['loop'] else 500
    frames[0].save(out/(clip['name']+'.gif'),save_all=True,append_images=frames[1:],duration=durations,loop=0)
    index=round((len(frames)-1)*(.5 if clip['name']=='Jump' else .4))
    x=(i%5)*300;y=(i//5)*400
    overview.paste(frames[index].resize((300,340)),(x,y+40))
    draw.text((x+8,y+10),clip['name'],font=font,fill='white')
    draw.text((x+8,y+376),f"{clip['duration']:.1f}s",font=font,fill=(155,180,200))
overview.save(out/'action-overview.png')
# Multi-phase side-by-side views make anticipation, strike, recovery and steps inspectable.
for name in ['Jump','AttackLeft','AttackRight','HitHeavy','Run','Walk']:
    files=sorted(captures.glob(name+'-*.png'));sheet=Image.new('RGB',(1500,360),(25,32,42));d=ImageDraw.Draw(sheet)
    for i,phase in enumerate([0,.2,.4,.6,.8,1]):
        im=Image.open(files[round((len(files)-1)*phase)]).crop((350,20,950,700)).resize((250,283))
        sheet.paste(im,(i*250,45));d.text((i*250+6,15),f'{name} {phase:.0%}',font=font,fill='white')
    sheet.save(out/(name+'-phases.png'))
print('BODY_ACTION_PREVIEWS_OK')
