"""M5.2.9.2.2: sculpt a reversible manga-face key on the proportion study.
Blender -b -P SCRIPT -- SOURCE_BLEND OUTPUT_DIRECTORY
"""
import sys, math, json, hashlib
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.kdtree import KDTree

source, out = map(Path, sys.argv[sys.argv.index('--')+1:])
out.mkdir(parents=True, exist_ok=True)
sha = hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(source))
body = bpy.data.objects['Stylized_body_PROPORTIONS_ONLY']
base = body.data.shape_keys.key_blocks['Manga_6_25_heads']
face = body.shape_key_add(name='Manga_face')
face.relative_key = base

def smooth(a,b,t):
    q = max(0., min(1., (t-a)/(b-a)))
    return q*q*(3-2*q)

def region(x,z,cx,cz,rx,rz):
    return math.exp(-((x-cx)/rx)**2-((z-cz)/rz)**2)

for i, src in enumerate(base.data):
    x,y,z = src.co
    ax = abs(x)
    front = 1-smooth(-.115,-.065,y)
    gate = front*smooth(1.27,1.31,z)
    eye = region(ax,z,.035,1.426,.031,.023)*gate
    nose = region(x,z,0,1.386,.020,.027)*gate
    mouth = region(x,z,0,1.352,.033,.015)*gate
    jaw = region(ax,z,.047,1.325,.046,.040)*gate
    brow = region(ax,z,.034,1.443,.038,.009)*gate
    cheek = region(ax,z,.048,1.387,.026,.031)*gate
    # Continuous symmetric fields preserve the existing eyelid/lip loops.
    nx = x + (1 if x >= 0 else -1)*(ax-.035)*.40*eye*smooth(0,.018,ax)
    nx *= 1-.23*nose-.16*mouth-.23*jaw
    nz = z + (z-1.426)*.95*eye
    nz += .020*region(x,z,0,1.318,.13,.050)*gate
    # User-directed lower forehead: compress the upper cranial height smoothly.
    # No hairline exists yet, so this edits volume rather than hair placement.
    nz -= .027*smooth(1.443,1.554,z)
    ny = y + .011*nose + .005*mouth + .0025*brow - .002*cheek
    face.data[i].co = (nx,ny,nz)

# Neutral eyeballs make socket evaluation possible without painted pupils.
eyes=[]
for sign, name in [(1,'L'),(-1,'R')]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=32,radius=1,
                                       location=(sign*.035,-.136,1.426))
    eye=bpy.context.object
    eye.name='White_eye_'+name
    eye.scale=(.020,.014,.015)
    eye.data.materials.append(body.data.materials[0])
    for p in eye.data.polygons: p.use_smooth=True
    for axis,expr in [(0,'.020*(1+.30*f)'),(2,'.015*(1+.50*f)')]:
        driver=eye.driver_add('scale',axis).driver
        variable=driver.variables.new();variable.name='f'
        variable.targets[0].id_type='KEY'
        variable.targets[0].id=body.data.shape_keys
        variable.targets[0].data_path='key_blocks["Manga_face"].value'
        driver.expression=expr
    eyes.append(eye)

scene=bpy.context.scene
scene.render.resolution_x=650;scene.render.resolution_y=700
scene.cycles.samples=32
camera=scene.camera
center=Vector((0,-.075,1.423))
camera.data.ortho_scale=.33
for value,label in [(0,'before'),(1,'after')]:
    face.value=value
    bpy.context.view_layer.update()
    for name,pos in [('front',(0,-3,0)),('side',(3,0,0)),('three-quarter',(1.6,-3,0))]:
        camera.location=center+Vector(pos)
        camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath=str(out/(label+'-'+name+'.png'))
        bpy.ops.render.render(write_still=True)
face.value=1
camera.data.ortho_scale=1.78
center=Vector((0,0,.78));camera.location=center+Vector((0,-5,0))
camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
scene.render.resolution_x=600;scene.render.resolution_y=800
scene.render.filepath=str(out/'body-front.png');bpy.ops.render.render(write_still=True)
bpy.ops.object.select_all(action='DESELECT')
body.select_set(True);bpy.context.view_layer.objects.active=body
body.active_shape_key_index=len(body.data.shape_keys.key_blocks)-1
bpy.ops.wm.save_as_mainfile(filepath=str(out/'stylized-body-face.blend'))
displacements=[(b.co-a.co).length for a,b in zip(base.data,face.data)]
below=[displacements[i] for i,v in enumerate(base.data) if v.co.z<1.27]
assert max(below,default=0)==0
assert len(base.data)==13380
assert all(math.isfinite(c) for v in face.data for c in v.co)
assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
tree=KDTree(len(base.data))
for i,v in enumerate(base.data): tree.insert(v.co,i)
tree.balance()
mirror_errors=[]
for i,v in enumerate(base.data):
    if v.co.z < 1.27: continue
    reflected=Vector((-v.co.x,v.co.y,v.co.z))
    _,j,distance=tree.find(reflected)
    if distance < 1e-5:
        a=face.data[i].co;b=face.data[j].co
        mirror_errors.append((Vector((-a.x,a.y,a.z))-b).length)
assert max(mirror_errors,default=0)<1e-5
report={'task':'M5.2.9.2.2','source_sha256':sha,'vertices':len(base.data),
        'max_displacement_m':max(displacements),'body_below_neck_unchanged':True,
        'shape_key':'Manga_face','relative_key':base.name,
        'mirrored_vertices_checked':len(mirror_errors),'max_mirror_error_m':max(mirror_errors,default=0),
        'direction':'Lower forehead, short chin, larger eyes, tapered oval face',
        'scope':'Static sculpt plus driven white eyeballs; no facial rig or animation adaptation.'}
(out/'face-report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('STYLIZED_FACE_OK',json.dumps(report),flush=True)
