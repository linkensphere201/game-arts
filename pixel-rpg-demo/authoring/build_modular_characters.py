"""Original modular native-pixel character authoring. No third-party artwork.
Parts are authored geometry, not palette swaps. Edit character-parts.json recipes.
"""
from pathlib import Path
import json,math
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
SPEC=json.loads(Path(__file__).with_name('character-parts.json').read_text(encoding='utf-8-sig'))
OUT=ROOT/'pixel-rpg-demo/mosslight/modular';REVIEW=ROOT/'validation/pixel-rpg/modular'
INK='#292937';GOLD='#d6a052';LIGHT='#ffe7ae';LEATHER='#775846'
def rgb(c):return tuple(bytes.fromhex(c.lstrip('#')))
def shade(c,f):return tuple(min(255,max(0,round(v*f))) for v in rgb(c))
def pts(values):return [(round(x),round(y)) for x,y in values]
def poly(d,p,c,edge=True):d.polygon(pts(p),fill=c,outline=INK if edge else None)
def line(d,p,c,w=1):d.line(pts(p),fill=c,width=w)
def ellipse(d,b,c,edge=True):d.ellipse(tuple(round(v) for v in b),fill=c,outline=INK if edge else None)
def recipe(index=0,**change):
    r=SPEC['presets'][index].copy();r.update(change);return r
def pose(direction,frame,action):
    a=SPEC['directions'].index(direction)*math.pi/4
    phase=frame*2*math.pi/SPEC['animations'][action]['frames']+math.pi/12
    running=action=='run';moving=action!='idle'
    stride=math.sin(phase)*(6.4 if running else 3.1) if moving else 0
    bounce=(1.0+abs(math.sin(phase))*1.7 if running else abs(math.sin(phase))*.65) if moving else float(frame in [1,2])
    return a,phase,stride,bounce,(3.2 if running else .3),running

def render(r,direction='S',frame=0,action='idle',only=None):
    # All named layers have the same 48 x 64 canvas; shadow is exported separately.
    layers={k:Image.new('RGBA',(48,64)) for k in ['rear_hair','body','face','hair','headgear']}
    a,phase,stride,bounce,lean,running=pose(direction,frame,action)
    ca,sa=math.cos(a),math.sin(a);front=ca>-.4
    hc=SPEC['hair_colors'][r['hair_color']];cl=SPEC['cloth_colors'][r['cloth_color']];skin=SPEC['skin_colors'][r['skin_color']]
    species=r.get('species',0)
    if species==3:skin=['#87a765','#73935e','#a0af70'][r['skin_color']%3]
    if species==4:skin=['#b28968','#749797','#a8907c'][r['skin_color']%3]
    hd=shade(hc,.62);hl=shade(hc,1.28);cd=shade(cl,.64);ch=shade(cl,1.3);sd=shade(skin,.74);sl=shade(skin,1.12)
    body_type=r.get('body_type',0)
    body_scale=[1.0,1.3,.83,.72,1.45][body_type]
    limb_width=[5,7,4,3,6][body_type]
    def p(x,y,z):
        x*=body_scale
        y*=[1.0,1.2,.87,.72,1.4][body_type]
        if body_type==3 and 15<z<30:z-=1
        return (24+x*ca+y*sa+lean*sa*z/40,56+(y*ca-x*sa*.45)*.48-z-bounce+lean*ca*z/85)
    hx,hy=p(0,0,35);hair=r['hair'];face=SPEC['faces'][r['face']];outfit=r['outfit'];gear=r['headgear']
    d=ImageDraw.Draw(layers['rear_hair'])
    tail=math.sin(phase-0.6)*(2 if running else .6)
    # Back-hair silhouettes: bob, long, pony, twin tails, braid, buns, curls.
    if hair in [3,4,7]:
        length={3:10,4:19,7:17}[hair]
        poly(d,[(hx-10,hy-5),(hx+10,hy-5),(hx+11+tail,hy+length),(hx+5,hy+length-2),(hx-2,hy+length+1),(hx-11+tail,hy+length-1)],hd)
        for x in [-7,-3,4,8]:line(d,[(hx+x,hy+1),(hx+x+tail,hy+length-3)],hc)
        if hair==7:
            for j in range(6):ellipse(d,(hx+8+tail-j*.3,hy+3+j*2,hx+12+tail-j*.3,hy+7+j*2),hc)
            line(d,[(hx+6+tail,hy+18),(hx+10+tail,hy+18)],GOLD,2)
    if hair in [5,6]:
        sides=[-1,1] if hair==6 else [-1]
        for side in sides:
            tx=hx+side*(11 if hair==6 else 7)-sa*4
            poly(d,[(tx,hy-5),(tx+side*5,hy-2),(tx+side*7+tail,hy+9),(tx+side*3+tail,hy+15),(tx+side*2,hy+5)],hc)
            line(d,[(tx+side*2,hy),(tx+side*4+tail,hy+10)],hl)
            line(d,[(tx-1,hy-3),(tx+2,hy-3)],GOLD,2)
    if hair==8:
        for x in [-11,6]:ellipse(d,(hx+x,hy-10,hx+x+7,hy-3),hc);line(d,[(hx+x+2,hy-8),(hx+x+5,hy-7)],hl)
    if hair==9:
        for x,y in [(-11,-4),(-10,2),(6,-5),(7,2),(-7,7),(3,8)]:ellipse(d,(hx+x,hy+y,hx+x+6,hy+y+6),hc)
    # Species tail is a rear layer rooted at the pelvis, independent of body bob.
    if species in [1,4]:
        tx,ty=p(0,-3,13);sway=math.sin(phase-.7)*(3 if running else 1.5)
        endx=tx-10*sa+(8 if sa>=0 else -8)+sway;endy=ty+5*ca+4
        line(d,[(tx,ty),(endx,endy-2),(endx+3,endy-8)],INK,5)
        line(d,[(tx,ty),(endx,endy-2),(endx+3,endy-8)],hc if species==1 else skin,3)
        if species==1:line(d,[(endx+2,endy-6),(endx+3,endy-8)],LIGHT,3)
        else:poly(d,[(endx,endy-5),(endx+6,endy-8),(endx+2,endy-12)],shade(skin,.75))
    d=ImageDraw.Draw(layers['body'])
    legs=[]
    for side in [-1,1]:
        swing=stride*side
        lift=max(0,-math.cos(phase+(0 if side==1 else math.pi)))*(5 if running else 1.5) if action!='idle' else 0
        # Knee flexion and heel recovery are independent from stride position.
        hip=p(side*3,0,15);knee=p(side*3,swing*.6,8+lift*.7);ankle=p(side*3,swing,2+lift)
        legs.append((swing*ca-side*3*sa,side,hip,knee,ankle))
    for _,side,hip,knee,ankle in sorted(legs):
        line(d,[hip,knee,ankle],INK,limb_width+1);line(d,[hip,knee,ankle],'#b7ad94',limb_width-1);line(d,[hip,knee],'#e1d5b2',2)
        x,y=ankle;ellipse(d,(x-3,y-2,x+3,y+2),LEATHER);line(d,[(x-2,y),(x+1,y)],'#b48d62')
    # Silhouette-specific garments, projected independently from limbs.
    width=8 if outfit==2 else 6
    torso=[p(-width,0,28),p(width,0,28),p(width+1,0,15),p(0,2,13),p(-width-1,0,15)]
    if abs(ca)<.3:torso=[p(-4,-5,28),p(4,5,28),p(5,5,15),p(-5,-5,15)]
    poly(d,torso,cl)
    line(d,[p(-4,1,26),p(-4,1,17)],ch,2)
    if body_type==4:
        bx,by=p(0,2,20);ellipse(d,(bx-10,by-6,bx+10,by+8),cl)
        line(d,[(bx-7,by-2),(bx-7,by+3)],ch,2)
    if outfit in [1,3,4,10]:
        hem=9 if outfit==4 else 7;wave=math.sin(phase)*(1.5 if running else .5)
        poly(d,[p(-6,0,23),p(6,0,23),p(10+wave,0,hem),p(2,2,hem-1),p(0,1,hem+4),p(-8+wave,0,hem)],cl)
        for x in [-5,3,7]:line(d,[p(x*.65,1,20),p(x+wave,1,hem+1)],cd)
        line(d,[p(-7+wave,1,hem+1),p(-1,1,hem)],GOLD)
    if outfit in [0,3,6,9]:
        length={0:14,3:6,6:10,9:17}[outfit]
        poly(d,[p(-7,-2,26),p(7,-2,26),p(9,-3+tail,length),p(3,-3,length-1),p(0,-2,length+4),p(-8,-3,length)],cd)
        if front:poly(d,[p(-4,2,25),p(4,2,25),p(4,2,16),p(-4,2,16)],cl)
        line(d,[p(-6,0,24),p(-7,0,length+2)],ch)
    if outfit==10:
        for side in [-1,1]:
            line(d,[p(side*3,3,26),p(side*4,3,9)],LIGHT,2)
            line(d,[p(side*5,3,12),p(side*6,3,9)],GOLD)
    if outfit==11:
        poly(d,[p(0,0,29),p(11,0,21),p(3,2,16),p(-10,0,21)],cl);line(d,[p(-8,1,21),p(2,2,18),p(9,1,21)],GOLD)
    # Clothing construction details belong on front, seams on back.
    if front:
        if outfit in [4,7]:
            poly(d,[p(-4,3,25),p(4,3,25),p(6,3,12),p(-6,3,12)],'#d6c9a1' if outfit==4 else LEATHER)
            line(d,[p(-3,4,17),p(3,4,17)],cd);line(d,[p(-2,4,24),p(-2,4,20)],LIGHT)
        elif outfit==8:
            for x in [-3,3]:line(d,[p(x,3,27),p(x,3,16)],'#b6a174',2)
            poly(d,[p(-4,3,22),p(4,3,22),p(4,3,15),p(-4,3,15)],cd)
        elif outfit==5:
            poly(d,[p(-5,2,27),p(-1,3,23),p(0,3,16),p(-5,2,16)],cd)
            poly(d,[p(5,2,27),p(1,3,23),p(0,3,16),p(5,2,16)],cd)
        else:
            line(d,[p(0,3,24),p(0,3,16)],cd)
            for z in [24,20]:ellipse(d,(*p(2,3,z),p(2,3,z)[0]+1,p(2,3,z)[1]+1),GOLD,False)
    else:line(d,[p(0,-1,25),p(0,-1,16)],cd)
    line(d,[p(-6,2 if front else -1,15),p(6,2 if front else -1,15)],LEATHER,2)
    if front:line(d,[p(-1,3,15),p(1,3,15)],GOLD,2)
    # Profession equipment and trims: distinct construction, not only a hue.
    if outfit in [0,6]:
        sx,sy=p(-7,1,17);ex,ey=p(-8,-1,2)
        line(d,[(sx,sy),(ex,ey)],INK,4);line(d,[(sx,sy),(ex,ey)],LEATHER,2)
        line(d,[(sx-3,sy),(sx+3,sy)],GOLD,2)
    if outfit==2:
        poly(d,[p(-5,2,26),p(5,2,26),p(6,2,18),p(0,3,15),p(-6,2,18)],'#89959a')
        line(d,[p(-3,3,24),p(-3,3,19)],'#d6d9c5',2)
        if front:line(d,[p(0,3,23),p(0,3,17)],GOLD)
    if outfit==3:
        line(d,[p(-7,2,25),p(0,3,21),p(7,2,25)],GOLD,2)
        if front:poly(d,[p(0,4,24),p(2,4,22),p(0,4,20),p(-2,4,22)],'#87b8ae')
    if outfit==4:
        line(d,[p(-4,3,26),p(0,4,23),p(4,3,26)],LIGHT,2)
        if front:line(d,[p(0,4,22),p(0,4,18)],GOLD);line(d,[p(-2,4,20),p(2,4,20)],GOLD)
    # Arms bend more in a run, rather than playing the walk faster.
    for side in sorted([-1,1],key=lambda v:-v*sa):
        swing=-stride*side
        shoulder=p(side*6,0,26);elbow=p(side*8,swing*.35,20);hand=p(side*7,swing*.8,23 if running else 16)
        line(d,[shoulder,elbow,hand],INK,limb_width);line(d,[shoulder,elbow,hand],cl,max(1,limb_width-2));line(d,[shoulder,elbow],ch)
        if outfit==2:
            x,y=shoulder;poly(d,[(x-4,y-2),(x+3,y-2),(x+5,y+3),(x-4,y+4)],'#929b9d');line(d,[(x-2,y-1),(x+2,y-1)],'#d4d7c3')
        x,y=hand;ellipse(d,(x-2,y-1,x+2,y+2),skin)
    d=ImageDraw.Draw(layers['face'])
    w=face['width'];jaw=face['jaw'];height=face['height'];profile=abs(ca)<.5
    fx=hx+sa*2;fw=w*(.77 if profile else 1)
    poly(d,[(fx-fw,hy-5),(fx+fw,hy-5),(fx+fw,hy+height-4),(fx+jaw*.7,hy+height),(fx-jaw*.7,hy+height),(fx-fw,hy+height-4)],skin)
    line(d,[(fx-fw+1,hy+height-4),(fx-jaw*.7,hy+height-1),(fx+jaw*.5,hy+height-1)],sd)
    if front:
        eyes=[face['eyes']*sa/abs(sa)] if profile else [-face['eyes'],face['eyes']]
        for ex in eyes:
            x=fx+ex;y=hy+2
            line(d,[(x-1,y-1),(x+1,y-1)],hd)
            line(d,[(x,y),(x,y+2)],INK,2);line(d,[(x,y+1),(x,y+2)],'#467675');line(d,[(x,y),(x,y)],'#fff2d9')
        line(d,[(fx+sa*2,hy+5),(fx+sa*2+1,hy+5)],sd)
        line(d,[(fx-1,hy+height-2),(fx+1,hy+height-2)],'#9b6254')
        detail=face['detail']
        if detail in ['blush','freckles']:
            for x in [-5,4]:line(d,[(fx+x,hy+5),(fx+x+1,hy+5)],'#bb796a')
        if detail in ['brow','lines']:line(d,[(fx-5,hy),(fx-2,hy)],hd);line(d,[(fx+2,hy),(fx+5,hy)],hd)
        if detail=='scar':line(d,[(fx+5,hy+1),(fx+4,hy+6)],sd)
        if detail=='lines':line(d,[(fx-6,hy+4),(fx-4,hy+4)],sd);line(d,[(fx+4,hy+4),(fx+6,hy+4)],sd)
        if detail=='beard':
            poly(d,[(fx-6,hy+5),(fx-2,hy+7),(fx+2,hy+7),(fx+6,hy+5),(fx+4,hy+11),(fx,hy+14),(fx-4,hy+11)],hc)
            line(d,[(fx-2,hy+9),(fx,hy+12)],hl)
    else:
        ellipse(d,(hx-9,hy-7,hx+9,hy+9),hc)
    # Species anatomy remains visible at gameplay scale.
    if species in [2,3]:
        for side in [-1,1]:
            if profile and side*sa<0:continue
            ex=hx+side*7
            poly(d,[(ex,hy-1),(ex+side*(9 if species==2 else 7),hy-4),(ex+side*6,hy+2),(ex,hy+4)],skin)
            line(d,[(ex+side*2,hy+1),(ex+side*5,hy-1)],sd)
    if front and species==3:
        for side in [-1,1]:poly(d,[(fx+side*3,hy+height-1),(fx+side*4,hy+height-5),(fx+side*5,hy+height-1)],LIGHT,False)
    if front and species==4:
        for side in [-1,1]:
            for zz in [4,6]:line(d,[(fx+side*5,hy+zz),(fx+side*7,hy+zz-1)],sd)
    # Hairstyle-specific crown and fringe geometry, not only recoloring.
    d=ImageDraw.Draw(layers['hair'])
    crowns=[
      [(-9,0),(-9,-6),(-5,-10),(4,-10),(9,-6),(9,0),(5,-2),(1,-3),(-4,-1)],
      [(-10,1),(-9,-7),(-3,-11),(5,-9),(10,-4),(9,3),(5,-3),(0,-5),(-4,1)],
      [(-11,0),(-9,-5),(-12,-7),(-5,-7),(-6,-12),(-1,-9),(3,-13),(5,-8),(10,-9),(9,-3),(12,0),(5,-2),(1,1),(-3,-3)],
      [(-10,7),(-11,-4),(-7,-10),(5,-10),(10,-5),(10,8),(7,8),(6,-1),(-6,-1),(-7,7)],
      [(-10,8),(-10,-5),(-5,-11),(6,-10),(10,-4),(10,9),(7,7),(6,-3),(1,1),(-2,-4),(-7,1),(-7,8)],
      [(-9,1),(-9,-6),(-5,-10),(5,-10),(10,-5),(9,2),(4,-2),(0,-1),(-4,-3)],
      [(-10,2),(-9,-7),(-4,-10),(4,-10),(9,-7),(10,2),(7,4),(5,-1),(0,-4),(-5,1),(-8,3)],
      [(-9,5),(-10,-4),(-6,-10),(5,-10),(9,-6),(10,3),(6,2),(3,-4),(-1,-2),(-5,1),(-7,5)],
      [(-9,1),(-8,-6),(-3,-10),(4,-10),(8,-6),(9,1),(4,-1),(0,-3),(-4,-1)],
      [(-11,3),(-11,-4),(-8,-8),(-3,-11),(3,-10),(8,-8),(11,-3),(10,4),(6,2),(3,0),(0,2),(-4,0),(-7,3)],
      [(-10,2),(-9,-6),(-5,-10),(3,-12),(10,-9),(12,-5),(6,-5),(9,-1),(3,-2),(-2,0),(-6,4)],
      [(-9,0),(-8,-6),(-4,-11),(4,-11),(9,-7),(7,-3),(3,-3),(-1,-5),(-5,-3),(-7,1)]
    ]
    scale=.82 if profile else 1
    cp=[(hx+x*scale,hy+y) for x,y in crowns[hair]]
    poly(d,cp,hc)
    if not front:
        poly(d,[(hx-8,hy-3),(hx+8,hy-3),(hx+7,hy+8),(hx+3,hy+10),(hx,hy+8),(hx-4,hy+10),(hx-8,hy+7)],hc)
    for x in [-5,-1,4]:
        line(d,[(hx+x*scale,hy-7),(hx+(x-2)*scale,hy-4)],hl)
    if hair==9:
        for x,y in [(-7,-6),(-2,-8),(3,-6),(7,-2)]:ellipse(d,(hx+x-2,hy+y-2,hx+x+2,hy+y+2),hc);line(d,[(hx+x-1,hy+y-1),(hx+x,hy+y-1)],hl)
    if not front:line(d,[(hx-3,hy+1),(hx-3,hy+7)],hd);line(d,[(hx+4,hy),(hx+4,hy+6)],hd)
    d=ImageDraw.Draw(layers['headgear'])
    if outfit==4:
        # Nun veil and white wimple belong to the outfit; accessories layer above it.
        poly(d,[(hx-12,hy+13),(hx-12,hy-5),(hx-7,hy-11),(hx+7,hy-11),(hx+12,hy-5),(hx+12,hy+13),(hx+8,hy+9),(hx+7,hy-3),(hx-7,hy-3),(hx-8,hy+9)],cd)
        line(d,[(hx-8,hy-3),(hx-6,hy-7),(hx+6,hy-7),(hx+8,hy-3)],LIGHT,2)
    if gear>=0:
        if gear==0:
            x=hx-8*ca;y=hy-7
            poly(d,[(x,y),(x-5,y-3),(x-5,y+4),(x,y+1),(x+5,y+4),(x+5,y-3)],cl);ellipse(d,(x-1,y-1,x+1,y+2),GOLD)
        elif gear==1:
            line(d,[(hx-8,hy-3),(hx,hy-1),(hx+8,hy-3)],GOLD,2)
            if front:poly(d,[(hx,hy-5),(hx+2,hy-2),(hx,hy+1),(hx-2,hy-2)],'#76bcbd')
        elif gear==2:
            poly(d,[(hx-11,hy-7),(hx-8,hy-12),(hx+6,hy-13),(hx+12,hy-8),(hx+8,hy-4),(hx-8,hy-4)],cl);line(d,[(hx-7,hy-9),(hx+5,hy-11)],ch,2)
        elif gear==3:
            poly(d,[(hx-14,hy-3),(hx-6,hy-7),(hx-1,hy-16),(hx+5,hy-16),(hx+7,hy-7),(hx+14,hy-3),(hx+5,hy),(hx-7,hy)],cl);line(d,[(hx-6,hy-6),(hx+7,hy-6)],GOLD,2)
        elif gear==4:
            poly(d,[(hx-12,hy+8),(hx-12,hy-6),(hx-4,hy-14),(hx+6,hy-12),(hx+12,hy-4),(hx+12,hy+9),(hx+8,hy+8),(hx+7,hy-5),(hx-6,hy-5),(hx-8,hy+8)],cl)
            line(d,[(hx-10,hy-5),(hx-3,hy-11)],ch)
        elif gear==5:
            for x in range(-10,11,4):ellipse(d,(hx+x-2,hy-10,hx+x+2,hy-5),'#e3d7b6')
            line(d,[(hx-10,hy-5),(hx-10,hy+7)],LIGHT,2);line(d,[(hx+10,hy-5),(hx+10,hy+7)],LIGHT,2)
        elif gear==6:
            line(d,[(hx-10,hy-4),(hx+10,hy-4)],LEATHER,2)
            for x in [-6,3]:ellipse(d,(hx+x,hy-7,hx+x+5,hy-2),GOLD);ellipse(d,(hx+x+1,hy-6,hx+x+4,hy-3),'#537885')
        elif gear==7:
            poly(d,[(hx-12,hy-5),(hx-5,hy-12),(hx+6,hy-12),(hx+10,hy-5)],cl);line(d,[(hx-11,hy-4),(hx+10,hy-4)],cd,2);poly(d,[(hx+5,hy-8),(hx+9,hy-15),(hx+12,hy-15),(hx+9,hy-9)],LIGHT)
        elif gear==8:
            x=hx-8*ca;y=hy-4
            for dx,dy in [(-2,0),(2,0),(0,-2),(0,2)]:ellipse(d,(x+dx-1,y+dy-1,x+dx+1,y+dy+1),'#d29b97')
            ellipse(d,(x-1,y-1,x+1,y+1),GOLD)
        elif gear==9:
            line(d,[(hx-9,hy-3),(hx+9,hy-3)],cl,3);line(d,[(hx+8,hy-2),(hx+12+tail,hy+5)],cl,2)
        elif gear==10:
            poly(d,[(hx-11,hy+3),(hx-11,hy-6),(hx-6,hy-12),(hx+6,hy-12),(hx+11,hy-6),(hx+11,hy+3),(hx+8,hy+4),(hx+7,hy-3),(hx-7,hy-3),(hx-8,hy+4)],'#909a9c');line(d,[(hx,hy-10),(hx,hy-5)],'#d2d5bf',2)
        elif gear==11:
            x=hx-7*ca;line(d,[(x-2,hy-5),(x+3,hy-1)],GOLD,2);line(d,[(x-2,hy-2),(x+3,hy-6)],GOLD)
    # Horns/ears use a separate overlay with hat cutouts: they are not erased by helmets.
    if species in [1,4]:
        for side in [-1,1]:
            if profile and side*sa<0:continue
            ex=hx+side*8
            if species==1:
                poly(d,[(ex-side*3,hy-7),(ex+side*3,hy-16),(ex+side*6,hy-5)],hc)
                poly(d,[(ex,hy-8),(ex+side*3,hy-13),(ex+side*4,hy-7)],sd,False)
            else:
                poly(d,[(ex-side*1,hy-7),(ex+side*4,hy-10),(ex+side*5,hy-16),(ex+side*8,hy-13),(ex+side*6,hy-6),(ex+side*2,hy-3)],'#bbae8c')
                line(d,[(ex+side*4,hy-8),(ex+side*6,hy-12)],LIGHT)
    if only:return layers[only]
    im=Image.new('RGBA',(48,64))
    for layer in layers.values():im.alpha_composite(layer)
    return im

def shadow():
    im=Image.new('RGBA',(48,64));d=ImageDraw.Draw(im)
    ellipse(d,(13,53,35,59),'#25273724',False);ellipse(d,(16,54,32,58),'#25273748',False)
    return im

def build():
    OUT.mkdir(parents=True,exist_ok=True);REVIEW.mkdir(parents=True,exist_ok=True)
    shadow().save(OUT/'shadow.png')
    for r in SPEC['presets']:
        for action,clip in SPEC['animations'].items():
            n=clip['frames'];sheet=Image.new('RGBA',(48*n,512))
            for row,direction in enumerate(SPEC['directions']):
                for frame in range(n):sheet.paste(render(r,direction,frame,action),(frame*48,row*64))
            sheet.save(OUT/f"{r['id']}_{action}.png")
    font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',11)
    # Component proof: same recipe held fixed while exactly one category changes.
    board=Image.new('RGBA',(768,572),'#e3dcc9');d=ImageDraw.Draw(board)
    d.text((12,8),'MODULAR CAST / 12 OPTIONS PER CATEGORY / SAME BASE PER ROW',font=font,fill=INK)
    for row,category in enumerate(['hair','face','headgear','outfit','hair_color','cloth_color']):
        y=33+row*87;d.text((12,y),category.upper(),font=font,fill=INK)
        for i in range(12):
            r=recipe(0,body_type=0,species=0,hair=0,face=0,headgear=-1,outfit=0,hair_color=0,cloth_color=0,skin_color=0)
            r[category]=i
            if category=='face':r['hair']=11
            x=i*63+8
            board.alpha_composite(shadow(),(x,y+12));board.alpha_composite(render(r),(x,y+12))
            d.text((x+19,y+72),f'{i+1:02}',font=font,fill=INK)
    board.resize((1536,1144),Image.Resampling.NEAREST).save(REVIEW/'parts-board.png')
    board=Image.new('RGBA',(512,368),'#343a4e');d=ImageDraw.Draw(board)
    d.text((12,8),'16 RECIPES / IDLE - WALK - RUN / EIGHT DIRECTIONS',font=font,fill=LIGHT)
    for i,r in enumerate(SPEC['presets']):
        x=(i%8)*64+8;y=(i//8)*156+40
        board.alpha_composite(shadow(),(x,y));board.alpha_composite(render(r),(x,y))
        board.alpha_composite(shadow(),(x,y+65));board.alpha_composite(render(r,'SE',2,'run'),(x,y+65))
        d.text((x,y+133),r['name'][:8],font=font,fill=LIGHT)
    board.resize((1024,736),Image.Resampling.NEAREST).save(REVIEW/'cast-board.png')
    frames=[]
    for f in range(8):
        board=Image.new('RGBA',(384,176),'#e3dcc9');d=ImageDraw.Draw(board)
        d.text((4,4),'WALK / 8 distinct poses',font=font,fill=INK)
        d.text((4,89),'RUN / bent arms, lift and forward lean',font=font,fill=INK)
        for row,action in enumerate(['walk','run']):
            for col,direction in enumerate(SPEC['directions']):
                at=(col*48,row*85+19);board.alpha_composite(shadow(),at);board.alpha_composite(render(recipe(0,headgear=-1),direction,f,action),at)
        frames.append(board.resize((1152,528),Image.Resampling.NEAREST).convert('RGB'))
    frames[0].save(REVIEW/'walk-run.gif',save_all=True,append_images=frames[1:],duration=110,loop=0)
    raceboard=Image.new('RGBA',(480,240),'#e3dcc9');rd=ImageDraw.Draw(raceboard)
    rd.text((8,8),'SPECIES / same clothes, front-side-back',font=font,fill=INK)
    for i,race in enumerate(SPEC['species']):
        rd.text((i*96+4,30),race,font=font,fill=INK)
        for row,direction in enumerate(['S','E','N']):
            at=(i*96+20,45+row*64)
            raceboard.alpha_composite(shadow(),at);raceboard.alpha_composite(render(recipe(0,species=i,headgear=-1),direction),at)
    raceboard.resize((960,480),Image.Resampling.NEAREST).save(REVIEW/'species-board.png')
    bodyboard=Image.new('RGBA',(480,180),'#e3dcc9');bd=ImageDraw.Draw(bodyboard)
    bd.text((8,8),'BODY TYPES / same species, outfit and colors',font=font,fill=INK)
    for i,kind in enumerate(SPEC['body_types']):
        bd.text((i*96+6,30),kind,font=font,fill=INK)
        for row,direction in enumerate(['S','E']):
            at=(i*96+20,45+row*64);bodyboard.alpha_composite(shadow(),at)
            bodyboard.alpha_composite(render(recipe(0,body_type=i,species=0,headgear=-1),direction),at)
    bodyboard.resize((960,360),Image.Resampling.NEAREST).save(REVIEW/'body-board.png')
    (OUT/'catalog.json').write_text(json.dumps(SPEC,indent=2),encoding='utf-8')
    print('MODULAR_CAST_BUILT 12 options x 6 categories; 16 recipes; 2560 frame slots; separate shadow')
if __name__=='__main__':build()
