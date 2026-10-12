"""Paginated action overview and GIFs from actual Godot captures, no redraw."""
import sys,json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

root=Path(sys.argv[1]);clips=json.loads((root/'actions.json').read_text())['clips']
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
sheet=Image.new('RGB',(1440,475*math.ceil(len(clips)/4)),'#202832');draw=ImageDraw.Draw(sheet)
for column,clip in enumerate(clips):
    files=sorted((root/'godot-demo/captures').glob(clip['name']+'-*.png'))
    assert len(files)==math.ceil(clip['duration']*20)+1
    frames=[Image.open(f).convert('RGB').crop((350,20,950,700)).resize((360,408)) for f in files]
    timing=[50]*len(frames);timing[-1]=50 if clip['loop'] else 500
    frames[0].save(root/(clip['name']+'.gif'),save_all=True,append_images=frames[1:],duration=timing,loop=0)
    x=(column%4)*360;y=(column//4)*475
    sheet.paste(frames[round((len(frames)-1)*.4)],(x,y+45))
    draw.text((x+12,y+10),clip['label'],font=font,fill='white')
    phases=Image.new('RGB',(1440,320),'#202832');d=ImageDraw.Draw(phases)
    for i,p in enumerate([0,.2,.4,.6,.8,1]):
        phases.paste(frames[round((len(frames)-1)*p)].resize((240,272)),(i*240,40))
        d.text((i*240+8,8),f'{p:.0%}',font=font,fill='white')
    phases.save(root/(clip['name']+'-phases.png'))
sheet.save(root/'pilot-overview.png')
print('QUATERNIUS_PREVIEWS_OK')
