"""Ivara-only 20k mesh, reversible surface split, proxy mannequin and breathing test.

blender -b -t 4 -P tools/ivara-element-study.py -- TRIAL_BLEND FRESH_OUTPUT
The mannequin is newly constructed, not recovered hidden anatomy. Surface groups
are heuristic study selections, not production-ready independently closed clothing.
"""
import bpy, sys, math, json, hashlib, colorsys
from pathlib import Path
from mathutils import Vector
import numpy as np

source,out=map(Path,sys.argv[sys.argv.index('--')+1:])
out.mkdir(parents=True,exist_ok=True)
if (out/'elements.blend').exists():raise RuntimeError('Use a fresh output directory')
digest=hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(source))
scene=bpy.context.scene; scene.frame_set(1)
for o in scene.objects:
    if o.type in {'MESH','ARMATURE'}:o.hide_render=True; o.hide_set(True)
source_obj=bpy.data.objects['Ivara_trial_mesh']
obj=bpy.data.objects.new('Working_20k',source_obj.data.copy()); scene.collection.objects.link(obj)
# Coordinates measured at neck/torso, not the tail-inclusive whole-object midpoint.
offset=Vector((.067,.065,0))
for v in obj.data.vertices:v.co+=offset
obj.data.update()
bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True); bpy.context.view_layer.objects.active=obj
dec=obj.modifiers.new('20k debugging budget','DECIMATE');dec.ratio=20000/len(obj.data.polygons)
bpy.ops.object.modifier_apply(modifier=dec.name)
obj.data.calc_loop_triangles(); total=len(obj.data.loop_triangles)
scene.cycles.samples=12; scene.render.resolution_x=560; scene.render.resolution_y=700
def camera(target=(.02,0,.49),location=(.02,-3,.53),scale=1.12):
    cam=scene.camera;cam.location=location;cam.data.ortho_scale=scale
    cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()
camera()
def render(name):
    scene.render.filepath=str(out/name);bpy.ops.render.render(write_still=True)
render('20k-assembled.png')
mesh=obj.data;uv=mesh.uv_layers.active.data
texture=next(i for i in bpy.data.images if 'basecolor' in i.name)
w,h=texture.size; pixels=np.empty(w*h*4,dtype=np.float32);texture.pixels.foreach_get(pixels);pixels=pixels.reshape(h,w,4)
groups={name:[] for name in ['head_hair_horns','outer_jacket','equipment','inner_front','trousers_boots','hands','tail']}
for p in mesh.polygons:
    x,y,z=p.center;ax=abs(x)
    coord=sum((uv[k].uv for k in p.loop_indices),Vector((0,0)))/len(p.loop_indices)
    r,g,b=map(float,pixels[int(coord.y*h)%h,int(coord.x*w)%w,:3]);hue,sat,value=colorsys.rgb_to_hsv(r,g,b)
    teal=.38<hue<.61 and sat>.15 and g>r*1.08
    if z>.782: group='head_hair_horns'
    elif y>.074 and z<.54:group='tail'
    elif z<.46 and ax>.085:group='hands' if z>.409 else 'trousers_boots'
    elif z<.487:group='trousers_boots'
    elif .487<z<.559:group='equipment'
    elif ax>.09 and z<.615:group='equipment'
    elif teal or ax>.082 or y>.012 or z>.743:group='outer_jacket'
    else:group='inner_front'
    groups[group].append(p.index)

parts_collection=bpy.data.collections.new('10_Separated_original_surfaces_20k');scene.collection.children.link(parts_collection)
def subset(name,indices):
    used=sorted({v for i in indices for v in mesh.polygons[i].vertices});mapping={v:i for i,v in enumerate(used)}
    d=bpy.data.meshes.new(name);d.from_pydata([mesh.vertices[i].co[:] for i in used],[],[[mapping[v] for v in mesh.polygons[i].vertices] for i in indices])
    for m in mesh.materials:d.materials.append(m)
    layer=d.uv_layers.new(name='UVMap')
    for a,i in zip(d.polygons,indices):
        p=mesh.polygons[i];a.material_index=p.material_index;a.use_smooth=True
        for l,k in zip(a.loop_indices,p.loop_indices):layer.data[l].uv=uv[k].uv
    result=bpy.data.objects.new(name,d);parts_collection.objects.link(result);return result
parts={name:subset(name,indices) for name,indices in groups.items()}
obj.hide_render=True;obj.hide_set(True)
parts['outer_jacket'].hide_render=True;parts['equipment'].hide_render=True
render('hidden-surfaces-only.png')

proxy_collection=bpy.data.collections.new('20_NEW_white_mannequin_proxy');scene.collection.children.link(proxy_collection)
def mat(name,color):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.8
    return m
white=mat('Mannequin white - reconstruction',(.7,.7,.7));dark=mat('Temporary inner fabric',(.045,.055,.10))
def tube(name,rings,material,collection):
    n=24;vs=[];fs=[]
    for x,y,z,rx,ry in rings:
        for i in range(n):
            t=i*2*math.pi/n;vs.append((x+rx*math.cos(t),y+ry*math.sin(t),z))
    for j in range(len(rings)-1):
        for i in range(n):
            a=j*n+i;b=j*n+(i+1)%n;fs.append((a,b,b+n,a+n))
    fs+=[tuple(reversed(range(n))),tuple((len(rings)-1)*n+i for i in range(n))]
    d=bpy.data.meshes.new(name);d.from_pydata(vs,[],fs);d.materials.append(material)
    for p in d.polygons:p.use_smooth=True
    o=bpy.data.objects.new(name,d);collection.objects.link(o)
    sub=o.modifiers.new('Proxy smoothing','SUBSURF');sub.levels=1;sub.render_levels=1
    return o
torso_rings=[(0,.005,.45,.067,.039),(0,.003,.48,.074,.041),(0,0,.52,.070,.038),
 (0,0,.56,.059,.033),(0,0,.60,.047,.029),(0,0,.635,.054,.035),
 (0,-.002,.674,.073,.040),(0,0,.707,.079,.033),(0,0,.728,.081,.032),
 (0,0,.750,.036,.026),(0,0,.766,.023,.022),(0,0,.791,.022,.022)]
torso=tube('NEW_proxy_torso',torso_rings,white,proxy_collection)
arm_rings=[];proxies=[torso]
for sign in [-1,1]:
    rings=[(sign*.079,0,.725,.024,.025),(sign*.097,0,.703,.026,.026),
      (sign*.113,-.005,.647,.023,.023),(sign*.12,-.01,.592,.020,.020),
      (sign*.125,-.011,.555,.021,.021),(sign*.128,-.017,.51,.017,.018),
      (sign*.13,-.019,.459,.015,.016),(sign*.13,-.02,.434,.015,.014)]
    arm_rings.append(rings);proxies.append(tube('NEW_proxy_arm_'+str(sign),rings,white,proxy_collection))
    proxies.append(tube('NEW_proxy_leg_'+str(sign),[(sign*.04,.004,.49,.039,.041),
      (sign*.053,.003,.45,.037,.039),(sign*.058,-.002,.36,.029,.030),
      (sign*.060,-.008,.28,.022,.024),(sign*.061,-.004,.235,.026,.025),
      (sign*.061,.008,.14,.021,.021),(sign*.061,.015,.067,.015,.019),
      (sign*.061,-.018,.035,.025,.058),(sign*.061,-.018,.018,.025,.058)],white,proxy_collection))
def ellipsoid(name,location,scale):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=16,location=location)
    o=bpy.context.object;o.name=name;o.scale=scale
    for c in list(o.users_collection):c.objects.unlink(o)
    proxy_collection.objects.link(o);o.data.materials.append(white)
    for p in o.data.polygons:p.use_smooth=True
    return o
proxies.append(ellipsoid('NEW_proxy_head',(0,-.007,.843),(.06,.055,.077)))
for sign in [-1,1]:proxies.append(ellipsoid('NEW_proxy_hand_'+str(sign),(sign*.13,-.02,.430),(.02,.015,.029)))
for o in parts.values():o.hide_render=True
render('white-mannequin.png')
for o in proxies:o.hide_render=True;o.hide_set(True)

# Covered diagnostic version: original inner-front surface over a dark proxy shell.
breath_collection=bpy.data.collections.new('30_Breathing_covered_test');scene.collection.children.link(breath_collection)
shell=tube('PROXY_inner_back_and_torso',torso_rings,dark,breath_collection)
arms=[tube('PROXY_inner_sleeve_'+str(i),r,dark,breath_collection) for i,r in enumerate(arm_rings)]
for name,o in parts.items():o.hide_render=name in {'outer_jacket','equipment'};o.hide_set(o.hide_render)
def smooth(a,b,x):
    t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
maximum=0
for o in [parts['inner_front'],shell]:
    o.shape_key_add(name='Basis');key=o.shape_key_add(name='Gentle_inhale')
    for v,k in zip(o.data.vertices,key.data):
        x,y,z=v.co;mask=smooth(.54,.64,z)*(1-smooth(.718,.773,z))*(1-smooth(.06,.09,abs(x)))
        delta=Vector((x*.006*mask,y*.017*mask,.00055*mask));k.co=v.co+delta;maximum=max(maximum,delta.length)
    for frame in range(1,98,4):
        key.value=.5-.5*math.cos(2*math.pi*(frame-1)/96);key.keyframe_insert('value',frame=frame)
    o.data.shape_keys.animation_data.action.name='Gentle_breath_4s_'+o.name
scene.frame_start=1;scene.frame_end=97;scene.render.fps=24
render('covered-breath-rest.png');scene.frame_set(49);render('covered-breath-inhale.png')
camera(target=(0,0,.64),location=(.15,-3,.665),scale=.4)
scene.render.resolution_x=480;scene.render.resolution_y=480
for frame in range(1,97,4):
    scene.frame_set(frame);render(f'breath-{frame:03}.png')
scene.frame_set(1);camera()
scene.render.resolution_x=560;scene.render.resolution_y=700

# Exact unchanged feet check on evaluated visible lower-body mesh, not a label.
lower=parts['trousers_boots'];scene.frame_set(1)
verts1=[v.co.copy() for v in lower.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.vertices]
scene.frame_set(49)
verts2=[v.co.copy() for v in lower.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.vertices]
foot_delta=max(((a-b).length for a,b in zip(verts1,verts2) if a.z<.12),default=0)
assert foot_delta==0
assert sum(len(v) for v in groups.values())==total
assert hashlib.sha256(source.read_bytes()).hexdigest()==digest
scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(out/'elements.blend'))
report={'source':str(source),'sha256_unchanged':digest,'triangles':total,'coordinate_offset':list(offset),
 'surface_groups':{k:len(v) for k,v in groups.items()},'proxy_objects':[o.name for o in proxies],
 'feet_max_displacement':foot_delta,'breath_period_seconds':4,'max_breath_displacement':maximum,
 'limits':['Proxy mannequin is newly built and needs anatomical/fit refinement.',
 'Surface segmentation is heuristic; garment boundaries and thickness are not production-ready.',
 'Covered breathing preview uses replacement underlayer on absent surfaces; no reusable walk claimed.']}
(out/'elements.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('ELEMENT_STUDY_COMPLETE',report,flush=True)
