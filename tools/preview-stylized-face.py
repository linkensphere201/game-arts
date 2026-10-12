"""Compose like-for-like white-material face sculpt comparison renders."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root=Path(sys.argv[1])
sheet=Image.new('RGB',(1200,970),'#242a32')
draw=ImageDraw.Draw(sheet)
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
for row,(prefix,title) in enumerate([('before','修改前'),('after','新版 · 低额头 / 短下巴 / 大眼睛 / 瓜子脸')]):
    y=row*440
    draw.text((18,y+8),title,font=font,fill='white')
    for column,name in enumerate(['front','three-quarter','side']):
        frame=Image.open(root/(prefix+'-'+name+'.png')).convert('RGB')
        frame.thumbnail((390,385))
        sheet.paste(frame,(column*400+(400-frame.width)//2,y+45))
draw.text((18,887),'同一白色材质、灯光与镜头；两版均加入白色测试眼球。',font=font,fill='white')
draw.text((18,929),'独立脸部形态键；身体保持不变，五官仍为无贴图的白模。',font=font,fill='white')
sheet.save(root/'face-comparison.png')
