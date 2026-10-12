"""M5 original pixel authorship: layered poses, eight headings, native-grid props/terrain.
No image-to-animation claim: every pose is rasterized from explicit joint/garment geometry.
"""
from pathlib import Path
import json,math,random
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'pixel-rpg-demo/mosslight'
OUT.mkdir(parents=True,exist_ok=True)
(ROOT/'validation/pixel-rpg').mkdir(parents=True,exist_ok=True)
SPEC=json.loads((Path(__file__).parent/'art-spec.json').read_text(encoding='utf-8-sig'))
P=SPEC['palette']; PI=math.pi
def canvas(w,h):return Image.new('RGBA',(w,h))
def poly(d,pts,c,edge=True):d.polygon([(round(x),round(y)) for x,y in pts],fill=P.get(c,c),outline=P['outline'] if edge else None)
def ell(d,box,c,edge=True):d.ellipse(tuple(round(n) for n in box),fill=P.get(c,c),outline=P['outline'] if edge else None)
def line(d,pts,c,width=1):d.line([(round(x),round(y)) for x,y in pts],fill=P.get(c,c),width=width)
def hero(direction,frame,action):
    im=canvas(48,64);d=ImageDraw.Draw(im)
    angle=SPEC['directions'].index(direction)*PI/4
    ca,sa=math.cos(angle),math.sin(angle)
    phase=frame*2*PI/(6 if action=='walk' else 4)+(PI/12 if action=='walk' else 0)
    stride=math.sin(phase)*(3.5 if action=='walk' else 0)
    bob=(abs(math.sin(phase))*.8 if action=='walk' else (frame in (1,2))*.5)
    def pt(x,y,z):return (24+x*ca+y*sa,55+(y*ca-x*sa)*.48-z-bob)
    # Limbs swing independently; the planted foot remains on a shared ground line.
    ell(d,(15,53,33,57),'#25273744',False)
    pieces=[]
    for side in [-1,1]:
        swing=stride*side
        lift=max(0,-swing)*.65
        hip=pt(side*3,0,14);knee=pt(side*3,swing*.5,8+lift*.4);ankle=pt(side*3,swing,2+lift)
        depth=swing*ca-side*3*sa
        pieces.append((depth,side,hip,knee,ankle))
    for _,side,hip,knee,ankle in sorted(pieces):
        line(d,[hip,knee,ankle],'outline',6)
        line(d,[hip,knee,ankle],'cream_dark',4)
        line(d,[(hip[0]-1,hip[1]),(knee[0]-1,knee[1]),(ankle[0]-1,ankle[1])],'cream',2)
        x,y=ankle
        ell(d,(x-3,y-2,x+3+sa,y+2),'leather')
        line(d,[(x-2,y+1),(x+2,y+1)],'leather_light')
    # Coat wraps in 3D direction, rather than flipping the same front drawing.
    body=[pt(-6,0,27),pt(6,0,27),pt(7,0,15),pt(4,2,13),pt(-5,2,13),pt(-7,0,16)]
    # Maintain torso thickness in side views.
    if abs(ca)<.3:
        body=[(20,28-bob),(27,28-bob),(29,41-bob),(26,43-bob),(19,41-bob)]
    poly(d,body,'teal_dark')
    poly(d,[(21,29-bob),(26,29-bob),(27,40-bob),(21,41-bob)],'teal',False)
    line(d,[(21,30-bob),(21,38-bob)],'teal_light')
    line(d,[pt(-6,1,17),pt(6,1,17)],'leather',2)
    # Arms: opposed gait with elbows and separate hands.
    armorder=sorted([-1,1],key=lambda side:-side*sa)
    for side in armorder:
        swing=-stride*side*.8
        shoulder=pt(side*6,0,25);elbow=pt(side*8,swing*.45,20);hand=pt(side*8,swing,16)
        line(d,[shoulder,elbow,hand],'outline',5)
        line(d,[shoulder,elbow,hand],'teal',3)
        line(d,[shoulder,elbow],'teal_light',1)
        x,y=hand;ell(d,(x-2,y-1,x+2,y+2),'skin')
    # Satchel stays on the character's left hip in all eight headings.
    bx,by=pt(-7,1,17)
    if -(-7)*sa+ca>=-2:
        poly(d,[(bx-3,by-2),(bx+3,by-2),(bx+3,by+4),(bx-3,by+4)],'leather')
        line(d,[(bx-2,by),(bx+2,by)],'leather_light')
        d.point((round(bx),round(by+1)),fill=P['gold'])
    # Head with direction-aware face placement, asymmetrical hair part and ear.
    hx,hy=pt(0,0,35)
    ell(d,(hx-9,hy-9,hx+9,hy+8),'hair_dark')
    front=ca>-.4
    if front:
        fx=hx+sa*3;fy=hy+2
        ell(d,(fx-6,fy-3,fx+6,fy+6),'skin')
        line(d,[(fx-3,fy+5),(fx+2,fy+5)],'skin_shadow')
        # Two front eyes, one profile eye. Brows and nose are intentional clusters.
        eyes=[-3,3] if ca>.6 else ([2] if sa>0 else [-2])
        for ex in eyes:
            x=round(fx+ex);y=round(fy+1)
            line(d,[(x,y),(x,y+2)],'outline',2);d.point((x,y),fill=P['white'])
            line(d,[(x-1,y-2),(x+1,y-2)],'hair_dark')
        d.point((round(fx+sa*3),round(fy+3)),fill=P['skin_shadow'])
        # Forelock part rotates visibly between profile/front views.
        poly(d,[(hx-9,hy-3),(hx-7,hy-8),(hx-2,hy-10),(hx+3,hy-9),
                (hx+8,hy-5),(hx+8,hy),(hx+4,hy-2),(hx+1,hy+1),(hx-1,hy-3),(hx-5,hy+1)],'hair')
        line(d,[(hx-6,hy-5),(hx-2,hy-7),(hx+2,hy-6)],'hair_light',2)
    else:
        poly(d,[(hx-8,hy-4),(hx-5,hy-8),(hx+1,hy-9),(hx+7,hy-5),
                (hx+8,hy+3),(hx+5,hy+6),(hx+2,hy+5),(hx,hy+8),(hx-5,hy+6)],'hair')
        line(d,[(hx-5,hy-4),(hx-3,hy-6),(hx+1,hy-6)],'hair_light',2)
        line(d,[(hx+5,hy-2),(hx+4,hy+3)],'hair_dark')
    # Neck scarf and trailing tip stay below face, above coat.
    poly(d,[(20,28-bob),(27,28-bob),(29,30-bob),(24,32-bob),(19,30-bob)],'gold')
    line(d,[(21,29-bob),(26,29-bob)],'gold_light')
    if ca>0:poly(d,[(25,31-bob),(28,32-bob),(27+math.sin(phase),37-bob),(24,35-bob)],'gold')
    return im
sheets={}
for action in ['idle','walk']:
    n=SPEC[action]['frames'];sheet=canvas(48*n,64*8)
    for row,direction in enumerate(SPEC['directions']):
        for f in range(n):sheet.paste(hero(direction,f,action),(48*f,64*row))
    sheet.save(OUT/(action+'.png'));sheets[action]=sheet
# Enlarged eight-direction strip animation preserves nearest-neighbor pixels.
frames=[]
for f in range(12):
    board=Image.new('RGBA',(48*8,80),'#e3dcc9')
    for col,direction in enumerate(SPEC['directions']):board.alpha_composite(hero(direction,f%6,'walk'),(48*col,8))
    frames.append(board.resize((1152,240),Image.Resampling.NEAREST).convert('RGB'))
frames[0].save(ROOT/'validation/pixel-rpg/hero-eight-directions.gif',save_all=True,append_images=frames[1:],duration=125,loop=0)
# Native-grid hand-authored prop silhouettes and surface clusters.
def prop(name,frame=0):
    im=canvas(96,96);d=ImageDraw.Draw(im);r=random.Random(name)
    if name=='oak_tree':
        poly(d,[(42,84),(43,43),(52,43),(54,84),(61,88),(48,87),(36,89)],'leather')
        line(d,[(47,76),(47,50)],'leather_light',2)
        for x,y,rad in [(30,47,18),(62,43,19),(45,28,23),(27,32,15),(63,29,16),(46,44,24)]:
            ell(d,(x-rad,y-rad,x+rad,y+rad),'grass_dark')
            ell(d,(x-rad+2,y-rad+1,x+rad-2,y+rad-6),'grass',False)
            for _ in range(9):
                px=x+r.randint(-rad+5,rad-5);py=y+r.randint(-rad+4,0)
                line(d,[(px,py),(px+3,py-1),(px+5,py)],'grass_light')
    elif name in ['shrub','flower_patch']:
        for _ in range(14):
            x=r.randint(22,72);y=r.randint(60,78)
            ell(d,(x-7,y-7,x+7,y+4),'grass_dark')
            ell(d,(x-5,y-6,x+5,y),'grass',False)
            if name=='flower_patch':
                ell(d,(x-2,y-5,x+2,y-1),'gold_light',False);d.point((x,y-3),fill=P['gold'])
    elif name=='rock':
        poly(d,[(26,79),(23,69),(33,51),(55,47),(70,60),(74,76),(59,85),(37,84)],'stone_dark')
        poly(d,[(25,68),(34,53),(53,49),(57,64),(43,72)],'stone_light',False)
        poly(d,[(44,73),(59,64),(68,61),(70,75),(58,81)],'stone',False)
        line(d,[(35,54),(42,62),(41,69)],'stone')
    elif name=='wooden_crate':
        poly(d,[(28,49),(62,49),(68,57),(68,83),(28,83)],'leather')
        poly(d,[(28,49),(59,46),(68,54),(36,57)],'leather_light')
        for x in range(32,66,8):line(d,[(x,58),(x,80)],'leather_dark')
        line(d,[(31,60),(63,78)],'gold_dark',4);line(d,[(32,59),(63,76)],'leather_light',2)
        line(d,[(29,81),(66,81)],'leather_light',2)
    elif name=='barrel':
        ell(d,(31,45,65,85),'leather')
        ell(d,(31,44,65,56),'leather_light')
        ell(d,(34,46,62,53),'leather',False)
        for x in [36,43,52,60]:line(d,[(x,57),(x,77)],'leather_dark')
        line(d,[(32,61),(35,63),(62,63),(65,61)],'stone_dark',3)
        line(d,[(32,76),(37,79),(61,79),(64,76)],'stone_dark',3)
    elif name=='chest':
        poly(d,[(26,62),(68,62),(68,82),(26,82)],'leather')
        ell(d,(26,46,68,71),'leather_light')
        poly(d,[(26,61),(68,61),(68,70),(26,70)],'leather')
        line(d,[(27,67),(67,67)],'outline')
        for x in [31,59]:line(d,[(x,51),(x,80)],'gold',3)
        poly(d,[(44,64),(51,64),(51,72),(44,72)],'gold_light')
        line(d,[(47,67),(47,70)],'outline')
    elif name=='signpost':
        poly(d,[(45,48),(51,48),(51,87),(45,87)],'leather')
        poly(d,[(26,47),(61,47),(70,56),(61,65),(26,65)],'leather_light')
        line(d,[(31,53),(58,53)],'leather')
        line(d,[(34,58),(53,58)],'leather')
    elif name=='wooden_fence':
        for x in [21,68]:
            poly(d,[(x,83),(x,50),(x+4,44),(x+8,50),(x+8,83)],'leather')
            line(d,[(x+2,51),(x+2,78)],'leather_light')
        for y in [57,70]:
            poly(d,[(17,y),(80,y),(80,y+5),(17,y+5)],'leather_light')
    elif name=='bench':
        for x in [25,65]:poly(d,[(x,65),(x+5,65),(x+5,85),(x,85)],'leather')
        poly(d,[(21,58),(69,58),(78,68),(25,68)],'leather_light')
        line(d,[(24,63),(72,63)],'leather')
        for x in [25,65]:line(d,[(x,61),(x,44)],'leather',4)
        poly(d,[(21,43),(70,43),(70,53),(21,53)],'leather_light')
    elif name=='well':
        ell(d,(22,52,75,85),'stone_dark')
        ell(d,(22,47,75,70),'stone')
        ell(d,(29,51,68,64),'deep')
        for x in [30,44,59,70]:line(d,[(x,69),(x,79)],'stone_dark')
        for x in [26,67]:line(d,[(x,61),(x,32)],'leather',5)
        poly(d,[(18,34),(47,17),(79,34),(71,40),(47,25),(24,40)],'teal_dark')
        line(d,[(23,33),(47,21),(73,35)],'teal_light',2)
        line(d,[(47,38),(47,61)],'gold_dark')
    elif name=='lantern':
        line(d,[(46,86),(46,38),(60,38)],'leather',4)
        line(d,[(59,38),(59,46)],'outline')
        poly(d,[(53,48),(65,48),(67,66),(51,66)],'gold_dark')
        poly(d,[(55,51),(62,51),(63,62),(54,62)],'gold_light')
        line(d,[(58,52),(58,60)],'cream_light',2)
    # Native-grid surface clusters: leaves and wood grain respect existing silhouettes.
    if name in ['oak_tree','shrub']:
        for _ in range(220 if name=='oak_tree' else 65):
            x=r.randrange(96);y=r.randrange(88)
            if im.getpixel((x,y))[:3] in [tuple(bytes.fromhex(P[k][1:])) for k in ['grass','grass_dark']]:
                color='grass_light' if (x+y)%3==0 else 'grass_dark'
                for dx,dy in [(0,0),(1,-1),(2,0),(3,0)]:
                    if 0<=x+dx<96 and 0<=y+dy<96 and im.getpixel((x+dx,y+dy))[:3] in [tuple(bytes.fromhex(P[k][1:])) for k in ['grass','grass_dark']]:
                        d.point((x+dx,y+dy),fill=P[color])
    if name in ['wooden_crate','barrel','chest','signpost','wooden_fence','bench']:
        for _ in range(40):
            x=r.randrange(96);y=r.randrange(96)
            if im.getpixel((x,y))[:3]==tuple(bytes.fromhex(P['leather_light'][1:])):
                line(d,[(x,y),(min(x+2,95),y)],'leather')
    if name=='chest' and frame>0:
        # Raise the lid, reveal a dark interior and retain the closed base/hinge.
        d.rectangle((25,43,69,65),fill=(0,0,0,0))
        poly(d,[(26,60),(67,60),(67,68),(26,68)],'deep')
        top=49-frame*5
        poly(d,[(26,top),(67,top),(67,top+12),(26,top+12)],'leather')
        for x in [31,59]:line(d,[(x,top+1),(x,top+11)],'gold',3)
        line(d,[(29,top+2),(64,top+2)],'leather_light')
    if name=='lantern':
        d.rectangle((55,52,61,61),fill=P['gold_light' if frame%2 else 'gold'])
        line(d,[(58,54-frame%2),(58,60)],'cream_light',2)
    return im
for name in SPEC['props']:prop(name).save(OUT/(name+'.png'))
for name in ['chest','lantern']:
    sheet=canvas(96*4,96)
    for frame in range(4):sheet.paste(prop(name,frame),(96*frame,0))
    sheet.save(OUT/(name+'_animation.png'))
# Terrain atlas: 16 neighbor-mask path transitions; same seeded base avoids tile seams.
atlas=canvas(32*4,32*5)
def tile(mask=None,stone=False,seed=920):
    im=Image.new('RGBA',(32,32),P['stone'] if stone else P['grass']);d=ImageDraw.Draw(im);r=random.Random(seed)
    for _ in range(10):
        x,y=r.randrange(32),r.randrange(32)
        d.line([(x,y),(x+1,y)],fill=P['stone_light'] if stone else '#689357')
    if mask is not None:
        poly(d,[(8,8),(24,8),(24,24),(8,24)],'earth',False)
        if mask&1:d.rectangle((8,0,24,16),fill=P['earth'])
        if mask&2:d.rectangle((16,8,31,24),fill=P['earth'])
        if mask&4:d.rectangle((8,16,24,31),fill=P['earth'])
        if mask&8:d.rectangle((0,8,16,24),fill=P['earth'])
        for _ in range(30):
            x,y=r.randrange(32),r.randrange(32)
            if im.getpixel((x,y))[:3]==tuple(bytes.fromhex(P['earth'][1:])):
                d.point((x,y),fill=P[r.choice(['earth_dark','earth_light'])])
    return im
atlas.paste(tile(),(0,0));atlas.paste(tile(stone=True),(32,0))
atlas.paste(tile(seed=921),(64,0));atlas.paste(tile(seed=922),(96,0))
for mask in range(16):atlas.paste(tile(mask),(mask%4*32,(1+mask//4)*32))
atlas.save(OUT/'terrain.png')
catalog={'product':SPEC['product'],'stage':'M5 visual review sample','character':{
    'id':'hero_wayfarer','cell':[48,64],'anchor':[24,56],'directions':SPEC['directions'],
    'animations':{k:SPEC[k] for k in ['idle','walk']}},
    'props':[{'id':n,'file':n+'.png','cell':[96,96],'anchor':[48,88]} for n in SPEC['props']],
    'terrain':{'file':'terrain.png','tile':[32,32],'path_masks':'row 1-4, N=1 E=2 S=4 W=8; grass=(0,0), stone=(1,0)'},
    'provenance':'Original explicit pixel geometry authored locally; concept references separately generated on local GPU. No downloaded art incorporated.'}
(OUT/'catalog.json').write_text(json.dumps(catalog,indent=2),encoding='utf-8')
board=Image.new('RGBA',(384,384),'#e3dcc9')
for i,n in enumerate(SPEC['props']):board.alpha_composite(prop(n),(i%4*96,i//4*96))
for i,direction in enumerate(SPEC['directions']):board.alpha_composite(hero(direction,0,'idle'),(i*48,310))
board.resize((768,768),Image.Resampling.NEAREST).save(ROOT/'validation/pixel-rpg/contact-sheet.png')
print('M5_PIXEL_ASSETS_OK 8 directions; 80 pose slots; 12 props; 20 terrain tiles')
