"""M3.4.1: bounded, art-directed source construction; not a text-to-3D model.
Run with Blender --background --factory-startup --python this_file.
Writes editable Blender sources and explicit GLBs. No filesystem deletions.
"""
from pathlib import Path
import math
import random
import json
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'scene-demo' / 'sunward_coast' / 'meshes'
SOURCE = ROOT / 'art-source' / 'environment'
SOURCE.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
random.seed(731)
inventory=[]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.scene.unit_settings.system = 'METRIC'

def material(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = .85
    return m

bark = material('Warm bark', (.19, .115, .055))
leaves = [material('Canopy '+str(i), c) for i,c in enumerate([
    (.19,.32,.075), (.29,.43,.10), (.38,.51,.14), (.24,.39,.09)])]
stone = material('Warm limestone', (.48,.45,.35))
stem = material('Flower stem', (.18,.34,.075))
petal = material('Ivory petals', (.94,.91,.69))
gold = material('Golden pollen', (.96,.52,.055))
grassmat = material('Grass blade base', (.32,.46,.12))

def ico(name, location, scale, mat, subdivisions=1):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=1, location=location)
    ob = bpy.context.object
    ob.name = name
    ob.scale = scale
    ob.data.materials.append(mat)
    return ob

def branch(start, end, r1, r2):
    vec = Vector(end)-Vector(start)
    bpy.ops.mesh.primitive_cone_add(vertices=7, radius1=r1, radius2=r2,
        depth=vec.length, location=(Vector(start)+Vector(end))/2)
    ob = bpy.context.object
    ob.name = 'Branch'
    ob.rotation_euler = vec.to_track_quat('Z','Y').to_euler()
    ob.data.materials.append(bark)
    return ob

def join_export(name, objects):
    bpy.ops.object.select_all(action='DESELECT')
    for ob in objects: ob.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    if len(objects)>1:
        bpy.ops.object.join()
    ob = bpy.context.object
    ob.name = name
    bpy.context.scene.cursor.location = (0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bpy.ops.export_scene.gltf(filepath=str(OUT/(name+'.glb')), export_format='GLB',
        use_selection=True, export_yup=True)
    inventory.append({'name':name,'vertices':len(ob.data.vertices),'triangles':sum(len(poly.vertices)-2 for poly in ob.data.polygons),'dimensions_m':[round(float(v),3) for v in ob.dimensions]})
    return ob

# The kit is laid out in a source workshop after each origin-centered export.
rock = ico('Limestone', (0,0,.52), (1.25,.9,.8), stone, 2)
for v in rock.data.vertices:
    v.co *= random.uniform(.87,1.13)
rock = join_export('limestone', [rock])
rock.location.x = -12

def make_tree(name, lean, height_scale, radius, source_x):
    joints=[(0,0,0),(.1,0,1.3*height_scale),(lean*.5,.06,2.7*height_scale),(lean,.1,3.8*height_scale)]
    parts=[branch(joints[i],joints[i+1],.24*(1-i*.24)*height_scale,.18*(1-i*.26)*height_scale) for i in range(3)]
    clusters=[(-1.1,.15,3.7,.95),(.9,.5,4.0,1.1),(.1,-.9,4.15,1.0),(-.5,1.0,4.35,.9),(.5,.35,4.8,1.0)]
    for i,(x,y,z,size) in enumerate(clusters):
        center=(x*radius+lean,y*radius,z*height_scale)
        parts.append(branch(joints[2],center,.085*height_scale,.028))
        for j in range(3):
            a=j*2.2+i*.8
            loc=(center[0]+.4*radius*math.cos(a),center[1]+.4*radius*math.sin(a),center[2]+.13*(j%2))
            ob=ico('Leaf cluster',loc,(size*radius*.76,size*radius*.67,size*height_scale*.62),leaves[(i+j)%4],2)
            for v in ob.data.vertices:
                v.co *= 1+.12*math.sin(v.co.x*8+i*2)*math.cos(v.co.y*9+j)
            parts.append(ob)
    ob=join_export(name,parts)
    ob.location.x=source_x
    return ob

tree=make_tree('coastal_tree',.3,1.0,1.05,-6)
make_tree('tree_windswept',1.6,.9,1.0,-13).location.y=8
make_tree('tree_sapling',.1,.58,.65,-6).location.y=8

parts=[]
for i in range(5):
    a=i*math.tau/5
    parts.append(ico('Bush',(.45*math.cos(a),.45*math.sin(a),.35+.12*(i%2)),(.65,.55,.5),leaves[i%4],2))
bush=join_export('shrub',parts)
bush.location.x=3

# Seven tapered blades. One mesh is instanced with a Godot wind material.
vs,fs=[],[]
for i in range(7):
    a=i*2.4
    x,y=math.cos(a)*.14,math.sin(a)*.14
    w=.045
    h=.35+(i%3)*.1
    dx,dy=math.cos(a)*w,math.sin(a)*w
    k=len(vs)
    vs += [(x-dx,y-dy,0),(x+dx,y+dy,0),(x+dx*.5+.06,y+dy*.5,h*.6),
        (x-dx*.5+.06,y-dy*.5,h*.6),(x+.13,y+.03,h)]
    fs += [(k,k+1,k+2,k+3),(k+3,k+2,k+4)]
mesh=bpy.data.meshes.new('Blade geometry')
mesh.from_pydata(vs,[],fs)
mesh.update()
uv=mesh.uv_layers.new(name='Blade height')
for loop in mesh.loops:
    uv.data[loop.index].uv=(0,mesh.vertices[loop.vertex_index].co.z/.55)
ob=bpy.data.objects.new('Grass',mesh)
bpy.context.collection.objects.link(ob)
ob.data.materials.append(grassmat)
grass=join_export('grass_tuft',[ob])
grass.location.x=7

parts=[branch((0,0,0),(0,0,.47),.012,.009)]
parts[0].data.materials.clear()
parts[0].data.materials.append(stem)
for i in range(5):
    a=i*math.tau/5
    parts.append(ico('Petal',(.09*math.cos(a),.09*math.sin(a),.48),(.09,.055,.025),petal,1))
parts.append(ico('Pollen',(0,0,.5),(.05,.05,.035),gold,1))
flower=join_export('daisy',parts)
flower.location.x=10
# Additional variants are separate editable meshes, not just scene scale changes.
for name,sc,loc in [('rock_flat',(1.1,.85,.28),(0,8,0)),('rock_tall',(.78,.65,.8),(4,8,0))]:
    ob=ico(name,(0,0,sc[2]*.8),sc,stone,2)
    for v in ob.data.vertices: v.co *= random.uniform(.86,1.12)
    ob=join_export(name,[ob]);ob.location=loc
parts=[ico('Low shrub',(-.5,0,.28),(.8,.48,.38),leaves[0],2),ico('Low shrub',(.4,.1,.32),(.7,.65,.44),leaves[2],2)]
ob=join_export('shrub_low',parts);ob.location=(8,8,0)
# Duplicates are independently editable source variants after export.
for source,name,scale,loc in [(grass,'grass_short',(.85,.85,.58),(12,8,0)),(flower,'flower_blue',(1.0,1.0,1.35),(16,8,0))]:
    ob=source.copy();ob.data=source.data.copy();bpy.context.collection.objects.link(ob)
    ob.location=(0,0,0);ob.scale=scale
    if name=='flower_blue':
        blue=material('Blue coastal petals',(.34,.31,.63))
        for i,m in enumerate(ob.data.materials):
            if m.name=='Ivory petals':ob.data.materials[i]=blue
    ob=join_export(name,[ob]);ob.location=loc
def plank(name,at,size,mat):
    bpy.ops.mesh.primitive_cube_add(size=1,location=at)
    ob=bpy.context.object;ob.name=name;ob.scale=size;ob.data.materials.append(mat)
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    bevel=ob.modifiers.new('Soft timber edges','BEVEL');bevel.width=.025;bevel.segments=1
    bpy.context.view_layer.objects.active=ob;bpy.ops.object.modifier_apply(modifier=bevel.name)
    return ob
wood=material('Weathered timber',(.28,.20,.11))
drift=material('Sun bleached driftwood',(.49,.39,.25))
parts=[]
for y in [-.19,0,.19]:parts.append(plank('Seat',(0,y,.65),(2.0,.17,.09),wood))
for x in [-.77,.77]:
    for y in [-.17,.17]:parts.append(plank('Leg',(x,y,.31),(.1,.1,.62),wood))
    parts.append(plank('Back support',(x,-.29,.84),(.09,.09,.94),wood))
for z in [.96,1.17]:parts.append(plank('Backrest',(0,-.31,z),(2.0,.08,.16),wood))
ob=join_export('coastal_bench',parts);ob.location=(-12,15,0)
parts=[branch((-1,0,.14),(.9,.1,.22),.15,.11),branch((.1,.04,.18),(.55,.43,.32),.09,.035)]
for ob in parts:ob.data.materials.clear();ob.data.materials.append(drift)
ob=join_export('driftwood',parts);ob.location=(-7,15,0)
parts=[]
for i in range(5):
    a=i*2.4
    parts.append(ico('Pebble',(.3*math.cos(a),.25*math.sin(a),.065),(.15,.11,.08),stone,2))
ob=join_export('pebbles',parts);ob.location=(-3,15,0)
ob=grass.copy();ob.data=grass.data.copy();bpy.context.collection.objects.link(ob)
ob.location=(0,0,0);ob.scale=(.75,.75,1.6)
ob=join_export('beach_reeds',[ob]);ob.location=(2,15,0)
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE/'coastal-kit.blend'))

# Separate editable terrain source: +Y in Blender becomes -Z in Godot.
bpy.ops.wm.read_factory_settings(use_empty=True)
def smooth(a,b,x):
    t=max(0,min(1,(x-a)/(b-a)))
    return t*t*(3-2*t)
def shore(x): return -7+2.5*math.sin(x*.13)+1.1*math.sin(x*.31)
def height(x,z):
    d=z-shore(x)
    return -1.8+3.2*smooth(-4,7,d)+smooth(4,15,d)*(.65+.55*math.sin(x*.12+z*.07)+.35*math.cos(z*.15-x*.06))

vs,fs,colors=[],[],[]
nx,nz=80,72
for j in range(nz+1):
    z=-14+j*.5
    for i in range(nx+1):
        x=-20+i*.5
        h=height(x,z)
        vs.append((x,-z,h))
        d=z-shore(x)
        green=smooth(4,7,d)
        patch=.5+.5*math.sin(x*.18+math.sin(z*.2)*1.8)*math.cos(z*.15)
        sand=(.64,.51,.30)
        turf=(.17+patch*.09,.27+patch*.10,.055+patch*.024)
        c=[sand[n]*(1-green)+turf[n]*green for n in range(3)]
        path_x=2+2*math.sin(z*.17)
        path=(1-smooth(.55,1.1,abs(x-path_x)))*smooth(5,9,d)*.8
        c=[c[n]*(1-path)+(.49,.38,.19)[n]*path for n in range(3)]
        colors.append((*c,1))
for j in range(nz):
    for i in range(nx):
        a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1
        fs.extend([(a,c,b),(b,c,d)])
# Close the finite display patch with a stone/soil skirt, including its underside.
ring=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,nz+1)]+[nz*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(nz-1,0,-1)]
upper=[];lower=[]
for index in ring:
    x,y,z=vs[index]
    upper.append(len(vs));vs.append((x,y,z));colors.append((.31,.27,.18,1))
    lower.append(len(vs));vs.append((x,y,-3.0));colors.append((.19,.18,.13,1))
for i in range(len(ring)):
    n=(i+1)%len(ring)
    fs.extend([(upper[i],lower[i],upper[n]),(upper[n],lower[i],lower[n])])
fs.append(tuple(reversed(lower)))
mesh=bpy.data.meshes.new('Coastal terrain mesh')
mesh.from_pydata(vs,[],fs)
mesh.update()
attr=mesh.color_attributes.new(name='CoastColor',type='FLOAT_COLOR',domain='POINT')
for i,c in enumerate(colors): attr.data[i].color=c
uv=mesh.uv_layers.new(name='Terrain UV')
for loop in mesh.loops:
    co=mesh.vertices[loop.vertex_index].co
    uv.data[loop.index].uv=((co.x+20)/40,(-co.y+14)/36)
for p in mesh.polygons: p.use_smooth=True
ob=bpy.data.objects.new('Terrain',mesh)
bpy.context.collection.objects.link(ob)
mat=material('Coastal vertex palette',(1,1,1))
vcol=mat.node_tree.nodes.new('ShaderNodeVertexColor')
vcol.layer_name='CoastColor'
mat.node_tree.links.new(vcol.outputs['Color'],mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
ob.data.materials.append(mat)
join_export('terrain',[ob])
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE/'coastal-terrain.blend'))
(OUT/'inventory.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
print('COAST_ASSETS_EXPORTED:',len(inventory),'GLBs and two editable .blend sources')
