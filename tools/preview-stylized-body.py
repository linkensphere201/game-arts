"""Create a labeled comparison from actual Blender proportion renders."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(sys.argv[1])
font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 23)
small = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 18)
sheet = Image.new('RGB', (1500, 680), '#242a32')
draw = ImageDraw.Draw(sheet)
items = [('original-front', '原白模'), ('front', '新版 · 约 6.25 头身'),
         ('side', '新版 · 侧面'), ('three-quarter', '新版 · 斜前方')]
for i, (name, label) in enumerate(items):
    sheet.paste(Image.open(root/(name+'.png')).convert('RGB').resize((300, 400)), (i*300, 70))
    draw.text((i*300+12, 25), label, font=font, fill='white')
draw.text((1212, 25), '俯视尺寸检查', font=font, fill='white')
game = Image.open(root/'game-view.png').convert('RGB')
sheet.paste(game.resize((240,320)), (1230,70))
for x, h in [(1240,96),(1390,64)]:
    sheet.paste(game.resize((h*3//4,h)),(x,415))
    draw.text((x,520),f'{h}px 画布',font=small,fill='white')
draw.text((22,580),'保留原始身高；头部放大、躯干缩短、腰身收紧、腿部略拉长。',font=font,fill='white')
draw.text((22,625),'静态比例预览：五官仍为基础模型；骨架与动作尚未适配新版。',font=small,fill='#cbd1da')
sheet.save(root/'proportions-overview.png')
