"""Export studied eight-way motion to a common cell/anchor and native Godot SpriteFrames."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'production/pixel-rpg/model-wave-01/guided'
OUT=BASE/'unified-motion';OUT.mkdir(exist_ok=True)
ASSETS=ROOT/'pixel-rpg-demo/mosslight/model_motion';ASSETS.mkdir(parents=True,exist_ok=True)
config=json.loads(Path(__file__).with_name('rowan-proportion-study.json').read_text())
views={v['direction']:v for v in config['views']}
views['NW']={'source':'production/pixel-rpg/model-wave-01/guided/rowan-NW-cloth-769002.png','center_x':237,'source_y':[155,270,290,367,457,516,617],'horizontal_scale':.256}
views['SW']={'source':'production/pixel-rpg/model-wave-01/guided/rowan-SW-770001.png','center_x':240,'source_y':[155,266,290,356,443,499,617],'horizontal_scale':.256}
CELL=(96,144);ANCHOR=(48,122);ZOOM=3

def normalize(im,view):
    tx=np.array(config['target_y'],float);sy=np.array(view['source_y'],float)
    # Extrapolate past static crown/sole, preserving raised heads and forward-moving feet.
    extra_y=np.r_[sy[0]-tx[0]*(sy[1]-sy[0])/(tx[1]-tx[0]),sy,sy[-1]+(CELL[1]-tx[-1])*(sy[-1]-sy[-2])/(tx[-1]-tx[-2])]
    extra_t=np.r_[0,tx,CELL[1]]
    yy=np.interp((np.arange(CELL[1]*ZOOM)+.5)/ZOOM,extra_t,extra_y)
    xx=view['center_x']+((np.arange(CELL[0]*ZOOM)+.5)/ZOOM-ANCHOR[0])/view.get('horizontal_scale',config['horizontal_scale'])
    gy,gx=np.meshgrid(yy,xx,indexing='ij')
    a=np.asarray(im.convert('RGBA'),dtype=float);a[:,:,:3]*=a[:,:,3:4]/255
    sample=np.stack([ndimage.map_coordinates(a[:,:,c],[gy,gx],order=1,mode='constant') for c in range(4)],axis=2)
    alpha=sample[:,:,3:4]/255
    sample[:,:,:3]=np.divide(sample[:,:,:3],alpha,out=np.zeros_like(sample[:,:,:3]),where=alpha>0)
    cell=Image.fromarray(np.clip(sample,0,255).astype('uint8')).resize(CELL,Image.Resampling.LANCZOS)
    cell.putalpha(cell.getchannel('A').point(lambda v:255 if v>=150 else 0))
    labels,_=ndimage.label(np.asarray(cell.getchannel('A'))>0,structure=np.ones((3,3)))
    counts=np.bincount(labels.ravel());counts[0]=0
    # Drop 1-2 pixel detached cutout residue, but preserve substantial occluded limb components.
    cell.putalpha(Image.fromarray((np.isin(labels,np.flatnonzero(counts>=3))*255).astype('uint8')))
    return cell

def standing_source(path):
    im=Image.open(path).convert('RGBA');rgba=np.asarray(im).astype(int);rgb=rgba[:,:,:3]
    bg=((rgb.min(2)>233)&(rgb.max(2)-rgb.min(2)<28))|(rgba[:,:,3]<128)
    labels,_=ndimage.label(bg);edge=np.unique(np.r_[labels[0],labels[-1],labels[:,0],labels[:,-1]]);edge=edge[edge!=0]
    parts,_=ndimage.label((~np.isin(labels,edge))&(rgba[:,:,3]>=128));counts=np.bincount(parts.ravel());counts[0]=0
    mask=ndimage.binary_erosion(np.isin(parts,np.flatnonzero(counts>=max(64,counts.max()*.005))),iterations=2)
    im.putalpha(Image.fromarray((mask*255).astype('uint8')));return im

def breathing_frames(cell):
    # One-pixel inhale at the crown fades smoothly to zero above the legs.
    a=np.asarray(cell,dtype=float);a[:,:,:3]*=a[:,:,3:4]/255
    y,x=np.mgrid[:CELL[1],:CELL[0]]
    weight=np.clip((82-y)/44,0,1);weight=weight*weight*(3-2*weight)
    frames=[]
    for lift in [0,.5,1,.5]:
        sampled=np.stack([ndimage.map_coordinates(a[:,:,c],[y+weight*lift,x],order=1,mode='constant') for c in range(4)],axis=2)
        alpha=sampled[:,:,3:4]/255
        sampled[:,:,:3]=np.divide(sampled[:,:,:3],alpha,out=np.zeros_like(sampled[:,:,:3]),where=alpha>0)
        frame=Image.fromarray(np.clip(sampled,0,255).astype('uint8'))
        frame.putalpha(frame.getchannel('A').point(lambda v:255 if v>=150 else 0))
        frames.append(frame)
    return frames

animations={};sources={};base_directions=['S','SE','E','NE','N','NW','SW']
directions=['S','SE','E','NE','N','NW','W','SW']
for direction in base_directions:
    path=ROOT/views[direction]['source']
    animations['idle_'+direction]=breathing_frames(normalize(standing_source(path),views[direction]))
    sources['idle_'+direction]=[{'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'method':'four-frame two-second breathing loop, three distinct poses, fixed lower body'}]
    for action in ['walk','run']:
        name=f'{action}_{direction}';seq=[];source_records=[]
        for i in range(8):
            path=BASE/'motion'/f'{action}-{i}-source.png' if direction=='E' else BASE/'axial-motion'/f'{direction}-{action}-{i}-source.png'
            if direction=='NW':path=BASE/'nw-motion'/f'NW-{action}-{i}-source.png'
            if direction=='SW':path=BASE/'sw-motion'/f'SW-{action}-{i}-source.png'
            seq.append(normalize(Image.open(path),views[direction]))
            source_records.append({'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        animations[name]=seq;sources[name]=source_records
# Independent left illustration, temporarily aligned right for the cutout rig.
# Reflect this source's own pixels back to W, never the E illustration.
left_root=BASE/'left-motion'
left_alignment=json.loads((left_root/'alignment.json').read_text())
left_path=left_root/'canonical-source.png'
assert hashlib.sha256(left_path.read_bytes()).hexdigest()==left_alignment['canonical_sha256']
assert hashlib.sha256((ROOT/left_alignment['source']).read_bytes()).hexdigest()==left_alignment['source_sha256']
left_idle=normalize(standing_source(left_path),views['E']).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
animations['idle_W']=breathing_frames(left_idle)
sources['idle_W']=[{'path':str(left_path.relative_to(ROOT)),'sha256':left_alignment['canonical_sha256'],'alignment':left_alignment,'method':'independent W model illustration aligned to side rig, restored to W, breathing warp'}]
for action in ['walk','run']:
    seq=[];source_records=[]
    for i in range(8):
        path=left_root/'rig'/f'{action}-{i}-source.png'
        seq.append(normalize(Image.open(path),views['E']).transpose(Image.Transpose.FLIP_LEFT_RIGHT))
        source_records.append({'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'method':'independent W source cutout restored from rig orientation','alignment':left_alignment})
    animations[action+'_W']=seq;sources[action+'_W']=source_records
mirror_sources={}
for direction,source_direction in mirror_sources.items():
    for action in ['idle','walk','run']:
        name=f'{action}_{direction}';source_name=f'{action}_{source_direction}'
        animations[name]=[cell.transpose(Image.Transpose.FLIP_LEFT_RIGHT) for cell in animations[source_name]]
        sources[name]=[{'derived_from_animation':source_name,'method':'horizontal reflection about cell center; hair part and asymmetric straps also mirrored'}]
frame_total=sum(len(seq) for seq in animations.values())
pool=Image.new('RGB',(96*frame_total,144))
for i,cell in enumerate([c for seq in animations.values() for c in seq]):pool.paste(cell.convert('RGB'),(i*96,0))
palette=pool.quantize(colors=128,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
records=[];board=Image.new('RGB',(8*144,len(animations)*240+40),'#ded8ca');draw=ImageDraw.Draw(board)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
draw.text((10,8),'8-WAY STUDY / EIGHT INDEPENDENT VIEW SOURCES / ANCHOR 48,122',font=font,fill='#29333a')
unique=set()
for row,(name,seq) in enumerate(animations.items()):
    sheet=Image.new('RGBA',(96*len(seq),144))
    for i,cell in enumerate(seq):
        alpha=cell.getchannel('A');pix=cell.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');pix.putalpha(alpha)
        box=pix.getbbox();assert box and 0<box[0]<box[2]<96 and 0<box[1]<box[3]<144,(name,i,box)
        assert set(np.unique(np.asarray(alpha)))=={0,255}
        digest=hashlib.sha256(pix.tobytes()).hexdigest()
        if not name.startswith('idle'):assert digest not in unique,(name,i)
        unique.add(digest)
        sheet.alpha_composite(pix,(i*96,0))
        preview=pix.resize((144,216),Image.Resampling.NEAREST);board.paste(preview,(i*144,40+row*240),preview)
    path=ASSETS/(name+'.png');sheet.save(path)
    fps=2 if name.startswith('idle') else (10 if name.startswith('walk') else 40/3)
    records.append({'name':name,'fps':fps,'frames':len(seq),'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    draw.text((8,40+row*240+215),name,font=font,fill='#29333a')
board.save(OUT/'motion-contact.png')

# Stable res:// paths make the generated folder usable inside the existing Godot project.
lines=[f'[gd_resource type="SpriteFrames" load_steps={len(records)+frame_total+1} format=3]','']
for i,record in enumerate(records):lines.append(f'[ext_resource type="Texture2D" path="res://mosslight/model_motion/{record["name"]}.png" id="sheet_{i}"]')
for i,record in enumerate(records):
    for f in range(record['frames']):
        lines.extend(['',f'[sub_resource type="AtlasTexture" id="frame_{i}_{f}"]',f'atlas = ExtResource("sheet_{i}")',f'region = Rect2({f*96}, 0, 96, 144)'])
lines.extend(['','[resource]','animations = ['])
for i,record in enumerate(records):
    frames=', '.join('{"duration": 1.0, "texture": SubResource("frame_'+str(i)+'_'+str(f)+'")}' for f in range(record['frames']))
    lines.append('{"frames": ['+frames+'], "loop": true, "name": &"'+record['name']+'", "speed": '+str(record['fps'])+'}'+(',' if i<len(records)-1 else ''))
lines.extend([']',''])
resource=ASSETS/'rowan_study.tres';resource.write_text('\n'.join(lines),encoding='utf-8')
(ROOT/'pixel-rpg-demo/model_playable.tscn').write_text('[gd_scene load_steps=2 format=3]\n\n[ext_resource type="Script" path="res://model_playable.gd" id="1"]\n\n[node name="ModelPlayableStudy" type="Node2D"]\nscript = ExtResource("1")\n',encoding='utf-8')
(ROOT/'pixel-rpg-demo/model_courtyard.tscn').write_text('[gd_scene load_steps=2 format=3]\n\n[ext_resource type="Script" path="res://model_courtyard.gd" id="1"]\n\n[node name="ModelCourtyard" type="Node2D"]\nscript = ExtResource("1")\n',encoding='utf-8')
(OUT/'manifest.json').write_text(json.dumps({'status':'eight-way technical study; art unapproved','cell':CELL,'anchor':ANCHOR,'sprite_offset':[0,-50],'directions':directions,'mirror_sources':mirror_sources,'animations':records,'source_poses':sources,'resource':str(resource.relative_to(ROOT)),'resource_sha256':hashlib.sha256(resource.read_bytes()).hexdigest(),'limitations':['all eight view sources independently drawn; hair, hem and accessory continuity still requires art review','idle is a subtle image-warp breathing study; no blink or independent cloth animation','landmark warping is not camera reprojection','projected elbow seams and depth occlusion need refinement','joint and cloth pixel cleanup remain']},indent=2),encoding='utf-8')
print('UNIFIED_MOTION_EXPORT_OK:',len(unique),'distinct bounded cells;',frame_total,'timeline cells;',len(records),'animations; native SpriteFrames generated')
