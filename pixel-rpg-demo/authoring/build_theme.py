"""Editable native pixel geometry for M5.2.3 unified-world review.
Reuses the local character rig; no external artwork or cloud inference.
"""
from pathlib import Path
import runpy, math, json, random
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[2]
base=runpy.run_path(str(Path(__file__).with_name('build_pixels.py')))
OUT=ROOT/'pixel-rpg-demo/mosslight/theme';OUT.mkdir(parents=True,exist_ok=True)
REVIEW=ROOT/'validation/pixel-rpg/theme';REVIEW.mkdir(parents=True,exist_ok=True)
P=base['P'];original=P.copy();DIRECTIONS=base['SPEC']['directions']
C={'ink':'#252737','dark':'#343a4e','wood':'#765343','woodlight':'#a27a50','plaster':'#ded6ae','light':'#fff0c9','shadow':'#a39a83','teal':'#327d80','tealdark':'#234c55','teallight':'#64b6ac','gold':'#d6a052','goldlight':'#f2d183','stone':'#838984','stonelight':'#b8b9a3','stonedark':'#535765','red':'#af6a57'}
def color(c):return C.get(c,c)
def poly(d,pts,c,edge=True):d.polygon(pts,fill=color(c),outline=C['ink'] if edge else None)
def rect(d,box,c,edge=False):d.rectangle(box,fill=color(c),outline=C['ink'] if edge else None)
def line(d,pts,c,w=1):d.line(pts,fill=color(c),width=w)
def ellipse(d,box,c,edge=True):d.ellipse(box,fill=color(c),outline=C['ink'] if edge else None)
def emblem(d,x,y):
    poly(d,[(x,y-4),(x+3,y),(x,y+4),(x-3,y)],'gold')
    line(d,[(x,y-2),(x,y+2)],'light')
PROFILES=[('rowan','Wayfarer'),('sylva','Grove scholar'),('bren','Town warden'),('osric','Veteran swordsman')]
def character(pid,direction,frame,action):
    P.clear();P.update(original)
    if pid=='sylva':P.update(hair_dark='#483c40',hair='#765343',hair_light='#a27a50',teal_dark='#234c55',teal='#327d80',teal_light='#64b6ac',gold='#b8b9a3',gold_light='#fff0c9')
    if pid=='bren':P.update(hair_dark='#252737',hair='#343a4e',hair_light='#535765',teal_dark='#535765',teal='#838984',teal_light='#b8b9a3')
    if pid=='osric':P.update(hair_dark='#838984',hair='#b8b9a3',hair_light='#fff0c9',teal_dark='#483c40',teal='#765343',teal_light='#a27a50')
    im=base['hero'](direction,frame,action);d=ImageDraw.Draw(im)
    theta=DIRECTIONS.index(direction)*math.pi/4;side=math.sin(theta);front=math.cos(theta)>0
    phase=frame*math.pi/3+math.pi/12 if action=='walk' else frame*math.pi/2
    bob=round(abs(math.sin(phase))*.8 if action=='walk' else (frame in (1,2))*.5)
    if pid=='rowan':
        # Short travel cape plus diagonal harness; retain asymmetric satchel.
        line(d,[(19,31-bob),(27,39-bob)],'wood',2)
        emblem(d,22,32-bob)
    elif pid=='sylva':
        # Long split robe, visible feet, wide sleeves, asymmetric staff and pointed ears.
        poly(d,[(18,35-bob),(29,35-bob),(33,48),(26,49),(24,44),(21,49),(15,48)],'tealdark')
        poly(d,[(20,36-bob),(24,37),(23,43),(19,47),(17,47)],'teal',False)
        line(d,[(18,47),(21,39)],'gold')
        line(d,[(28,38),(31,47)],'teallight')
        poly(d,[(14,21-bob),(18,23-bob),(17,26-bob)],'#e2a478')
        poly(d,[(30,22-bob),(34,21-bob),(31,26-bob)],'#e2a478')
        sx=35 if side>=0 else 12
        line(d,[(sx,29),(sx,52)],'ink',3);line(d,[(sx,30),(sx,51)],'woodlight')
        poly(d,[(sx,23),(sx+3,28),(sx,32),(sx-3,28)],'teallight')
        emblem(d,24,32-bob)
    elif pid=='bren':
        # Broad angular pauldrons, steel breastplate and split tabard.
        for x in [13,28]:
            poly(d,[(x,29-bob),(x+6,27-bob),(x+8,33-bob),(x,35-bob)],'stone')
            line(d,[(x+1,30-bob),(x+5,29-bob)],'light')
        poly(d,[(19,31-bob),(28,31-bob),(28,40-bob),(24,43),(19,40-bob)],'stonedark')
        poly(d,[(20,32-bob),(24,32-bob),(24,39),(20,38)],'stonelight',False)
        poly(d,[(20,41),(28,41),(29,48),(25,48),(24,45),(22,48),(19,47)],'teal')
        emblem(d,25,36-bob)
        sx=34 if side>=0 else 12
        line(d,[(sx,38),(sx-2,52)],'ink',3);line(d,[(sx-3,38),(sx+3,39)],'gold',2)
    else:
        # Long weather cape and grey beard create a different silhouette from young hero.
        poly(d,[(18,30-bob),(29,30-bob),(33,45),(27,47),(25,39),(18,45),(14,44)],'wood')
        line(d,[(18,34),(16,43),(20,42)],'woodlight')
        line(d,[(28,33),(31,44)],'shadow')
        if front:
            poly(d,[(20,25-bob),(27,25-bob),(27,29-bob),(23,33-bob),(20,29-bob)],'stonelight')
            line(d,[(22,28-bob),(23,30-bob)],'light')
        sx=34 if side>=0 else 12
        line(d,[(sx,35),(sx-1,52)],'ink',3);line(d,[(sx-3,36),(sx+3,36)],'gold',2)
        emblem(d,29,32-bob)
    P.clear();P.update(original)
    return im
for pid,_ in PROFILES:
    for action,count in [('idle',4),('walk',6)]:
        sheet=Image.new('RGBA',(48*count,512))
        for row,direction in enumerate(DIRECTIONS):
            for frame in range(count):sheet.paste(character(pid,direction,frame,action),(frame*48,row*64))
        sheet.save(OUT/f'{pid}_{action}.png')
# Shared inventory/world artwork. Same pixel source is used on shelves and UI.
ITEMS=['sword','shield','staff','potion','crystal','scroll','coin_purse','bread','herb','key','book','lantern']
def item(name):
    im=Image.new('RGBA',(32,32));d=ImageDraw.Draw(im)
    if name=='sword':
        poly(d,[(21,3),(26,3),(26,8),(12,23),(8,19)],'stone');line(d,[(23,5),(11,19)],'light');line(d,[(7,19),(14,26)],'gold',3);line(d,[(9,24),(5,28)],'wood',3)
    elif name=='shield':
        poly(d,[(7,5),(24,5),(25,19),(16,28),(6,19)],'gold');poly(d,[(9,8),(22,8),(22,18),(16,24),(9,18)],'tealdark');emblem(d,16,15)
    elif name=='staff':
        line(d,[(16,10),(12,29)],'ink',4);line(d,[(16,11),(12,28)],'woodlight',2);poly(d,[(17,2),(23,8),(17,15),(12,8)],'teal');line(d,[(17,4),(15,8),(17,11)],'teallight')
    elif name=='potion':
        poly(d,[(12,5),(20,5),(20,11),(25,17),(24,26),(8,26),(7,17),(12,11)],'stonelight');poly(d,[(10,18),(22,18),(22,24),(10,24)],'teal',False);rect(d,(12,3,20,7),'wood',True);line(d,[(10,15),(10,20)],'light',2);emblem(d,16,20)
    elif name=='crystal':
        poly(d,[(16,3),(25,11),(22,24),(13,29),(7,18),(9,8)],'tealdark');poly(d,[(16,3),(18,16),(13,29),(9,8)],'teallight');line(d,[(18,16),(24,12)],'light')
    elif name=='scroll':
        rect(d,(8,7,24,26),'plaster',True);ellipse(d,(6,4,25,10),'light');ellipse(d,(6,22,25,28),'shadow');line(d,[(11,12),(20,12)],'wood');line(d,[(11,16),(18,16)],'wood');rect(d,(15,19,19,23),'red')
    elif name=='coin_purse':
        poly(d,[(11,6),(21,6),(19,11),(25,19),(23,27),(9,27),(7,19),(13,11)],'wood');line(d,[(11,11),(22,11)],'gold',2);ellipse(d,(16,19,23,26),'gold');line(d,[(19,21),(19,24)],'goldlight')
    elif name=='bread':
        ellipse(d,(4,10,28,24),'woodlight');poly(d,[(7,15),(10,11),(22,11),(26,16),(24,20),(8,20)],'gold',False)
        for x in [11,16,21]:line(d,[(x,13),(x-2,17)],'light',2)
    elif name=='herb':
        line(d,[(10,28),(19,6)],'wood',2)
        for x,y in [(14,12),(19,17),(10,21)]:poly(d,[(x,y+4),(x-6,y-3),(x,y-5),(x+3,y)],'teal');line(d,[(x-3,y-2),(x,y+2)],'teallight')
    elif name=='key':
        ellipse(d,(6,3,19,16),'gold');ellipse(d,(10,7,15,12),'dark');line(d,[(16,15),(24,26)],'gold',3);line(d,[(21,23),(25,20)],'gold',3)
    elif name=='book':
        poly(d,[(7,5),(23,3),(26,24),(10,28),(6,25)],'wood');poly(d,[(9,6),(21,5),(24,23),(11,25)],'teal');line(d,[(7,7),(10,25)],'gold');emblem(d,17,15)
    elif name=='lantern':
        ellipse(d,(11,3,21,13),'gold');rect(d,(9,10,23,25),'wood',True);rect(d,(12,13,20,22),'goldlight');line(d,[(16,13),(16,22)],'light',2);rect(d,(8,25,24,27),'gold')
    return im
for name in ITEMS:item(name).save(OUT/f'item_{name}.png')
def building():
    im=Image.new('RGBA',(224,208));d=ImageDraw.Draw(im)
    poly(d,[(20,181),(178,181),(216,197),(60,200)],'#25273744',False)
    # Front wall and right return share top-left sunlight.
    poly(d,[(24,87),(165,87),(165,180),(24,180)],'plaster')
    poly(d,[(165,87),(194,66),(194,159),(165,180)],'shadow')
    rect(d,(26,163,164,180),'stone');line(d,[(26,166),(163,166)],'stonelight')
    for y in [170,177]:
        for x in range(29,163,18):line(d,[(x+(8 if y==177 else 0),y-5),(x+(8 if y==177 else 0),y)],'stonedark')
    for x in [26,71,119,159]:rect(d,(x,90,x+5,164),'wood',True);line(d,[(x+1,92),(x+1,161)],'woodlight')
    for y in [97,132]:rect(d,(26,y,164,y+4),'wood')
    for x in [35,127]:
        rect(d,(x,109,x+23,135),'wood',True);rect(d,(x+3,111,x+20,130),'tealdark');line(d,[(x+5,112),(x+5,122)],'teallight',2);line(d,[(x+12,111),(x+12,131)],'gold');line(d,[(x+3,121),(x+20,121)],'gold')
        rect(d,(x-2,135,x+26,139),'wood',True)
    rect(d,(81,125,108,180),'wood',True);rect(d,(85,132,104,174),'woodlight',True)
    for x in [88,95,102]:line(d,[(x,134),(x,173)],'wood')
    ellipse(d,(100,152,103,155),'goldlight');rect(d,(77,179,112,184),'stonelight',True)
    # Steep teal roof with shingle rows and chamfered eaves.
    poly(d,[(17,91),(47,34),(177,34),(201,72),(168,98)],'tealdark')
    poly(d,[(17,91),(47,34),(177,34),(165,91)],'teal')
    for y in range(42,91,7):
        left=round(47-(y-34)*30/57);right=round(177-(y-34)*12/57)
        line(d,[(left,y),(right,y)],'tealdark')
        for x in range(left+5+(y%2)*5,right,13):line(d,[(x,y-5),(x-2,y)],'teallight')
    line(d,[(47,33),(177,33)],'teallight',3);line(d,[(17,92),(165,93),(200,73)],'wood',4)
    # Chimney, dormer crest, hanging store sign.
    rect(d,(142,17,154,45),'stone',True);rect(d,(140,16,156,20),'stonelight',True)
    for y in [27,34,41]:line(d,[(144,y),(153,y)],'stonedark')
    poly(d,[(75,72),(94,51),(115,72)],'wood');poly(d,[(79,70),(94,55),(110,70)],'plaster');emblem(d,94,65)
    line(d,[(159,110),(186,110),(186,118)],'wood',3);rect(d,(175,118,198,138),'wood',True);rect(d,(178,121,195,135),'tealdark');emblem(d,186,128)
    return im
building().save(OUT/'guild_shop.png')
def stall():
    im=Image.new('RGBA',(128,112));d=ImageDraw.Draw(im)
    ellipse(d,(8,91,124,108),'#25273744',False)
    for x in [16,105]:rect(d,(x,32,x+4,102),'wood',True)
    rect(d,(15,69,112,98),'wood',True)
    for x in range(19,111,13):line(d,[(x,74),(x,96)],'woodlight')
    poly(d,[(10,66),(108,66),(118,75),(17,75)],'woodlight')
    for index,name in enumerate(['potion','crystal','book']):im.alpha_composite(item(name),(20+index*28,39))
    poly(d,[(12,22),(103,22),(119,42),(4,42)],'tealdark')
    for x in range(13,104,18):poly(d,[(x,23),(x+8,23),(x+13,41),(x-3,41)],'plaster',False)
    rect(d,(4,42,119,49),'teal',True)
    for x in range(8,116,9):line(d,[(x,44),(x,48)],'gold')
    return im
stall().save(OUT/'apothecary_stall.png')
# Terrain source: low-contrast staggered cobbles plus grass; deterministic placement.
rng=random.Random(427)
floor=Image.new('RGBA',(640,448),'#658d50');d=ImageDraw.Draw(floor)
for _ in range(1100):
    x,y=rng.randrange(640),rng.randrange(448);line(d,[(x,y),(x+1,y)],'#72955b')
for y in range(64,417,10):
    for x in range(0,640,18):
        xx=x+(9 if (y//10)%2 else 0)
        if 252<xx<379 or 246<y<329:
            rect(d,(xx,y,xx+16,y+8),rng.choice(['#999b89','#a4a38e','#aaa791']))
            line(d,[(xx+1,y+1),(xx+14,y+1)],'#b8b9a3')
for y in range(74,417,16):
    if 234<y<332:continue
    for x in [245,382]:rect(d,(x,y,x+5,y+13),'stonedark');line(d,[(x+1,y),(x+4,y)],'stonelight')
floor.save(OUT/'street_floor.png')
# Review board contains actual export pixels, not a separate marketing illustration.
board=Image.new('RGBA',(640,480),C['ink']);d=ImageDraw.Draw(board)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',12)
small=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',10)
d.text((16,12),'MOSSLIGHT / WORLD STYLE STUDY 01',font=font,fill=C['light'])
d.text((16,31),'ORIGINAL CAST - SHARED MATERIALS - ONE PIXEL GRID',font=small,fill=C['teallight'])
for i,(pid,label) in enumerate(PROFILES):
    x=16+i*152;rect(d,(x,56,x+140,178),'dark')
    for j,direction in enumerate(['S','E','N']):board.alpha_composite(character(pid,direction,1,'walk'),(x+j*46,65))
    d.text((x+8,139),pid.upper(),font=font,fill=C['goldlight']);d.text((x+8,158),label,font=small,fill=C['plaster'])
rect(d,(16,192,623,251),'dark')
for i,name in enumerate(ITEMS):board.alpha_composite(item(name),(24+i*49,202))
d.text((19,262),'STREET CORNER / IN-ENGINE ASSETS',font=small,fill=C['goldlight'])
board.alpha_composite(building(),(24,268));board.alpha_composite(stall(),(260,338))
for i,(key,c) in enumerate(C.items()):
    x=414+(i%6)*32;y=296+(i//6)*32;rect(d,(x,y,x+23,y+23),c)
d.text((415,419),'Brass / teal crystal',font=small,fill=C['plaster']);d.text((415,437),'Timber / warm plaster',font=small,fill=C['plaster'])
board.resize((1280,960),Image.Resampling.NEAREST).save(REVIEW/'style-board.png')
previews=[]
for frame in range(6):
    b=Image.new('RGBA',(384,288),C['dark']);dd=ImageDraw.Draw(b)
    for row,(pid,_) in enumerate(PROFILES):
        for col,direction in enumerate(DIRECTIONS):b.alpha_composite(character(pid,direction,frame,'walk'),(col*48,row*72+4))
    previews.append(b.resize((1152,864),Image.Resampling.NEAREST).convert('RGB'))
previews[0].save(REVIEW/'cast-walk.gif',save_all=True,append_images=previews[1:],duration=125,loop=0)
manifest={'stage':'M5.2.3 first unified study; visual acceptance pending','characters':[p[0] for p in PROFILES],'directions':DIRECTIONS,'cell':[48,64],'anchor':[24,56],'items':ITEMS,'motif':'brass seed diamond; teal magic crystal','buildings':['guild_shop','apothecary_stall'],'generated_art':'local editable pixel geometry; no third-party images'}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('THEME_ASSETS_OK 4 character studies / 320 slots / 12 item designs / 2 structures')
