"""M3.4.1: bounded, art-directed source construction; not a text-to-3D model.
Run with Blender --background --factory-startup --python this_file.
Writes editable Blender sources and explicit GLBs. No filesystem deletions.
"""
from pathlib import Path
import math
import random
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'scene-demo' / 'assets'
SOURCE = ROOT / 'art-source' / 'environment'
SOURCE.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
random.seed(731)
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
    bpy.ops.object.join()
    ob = bpy.context.object
    ob.name = name
    bpy.context.scene.cursor.location = (0,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    bpy.ops.export_scene.gltf(filepath=str(OUT/(name+'.glb')), export_format='GLB',
        use_selection=True, export_yup=True)
    return ob

# The kit is laid out in a source workshop after each origin-centered export.
rock = ico('Limestone', (0,0,.52), (1.25,.9,.8), stone, 2)
for v in rock.data.vertices:
    v.co *= random.uniform(.87,1.13)
rock = join_export('limestone', [rock])
rock.location.x = -12

parts = [branch((0,0,0),(.3,0,3.4),.27,.13)]
for endpoint in [(-1.4,.1,4), (1.7,.4,4.3), (.4,-1.2,4.2),(.2,1.3,4.6)]:
    parts.append(branch((.18,0,2.5),endpoint,.13,.055))
for i, (x,y,z,s) in enumerate([(-1.4,.1,4.2,1.6),(1.3,.2,4.6,1.9),(.2,-1.1,4.6,1.7),
    (.2,1.2,4.9,1.6),(-.7,.6,5.1,1.8),(.25,.1,5.5,1.8)]):
    parts.append(ico('Canopy', (x,y,z), (s,s*.85,s*.58), leaves[i%4],2))
tree = join_export('coastal_tree', parts)
tree.location.x = -5

parts=[]
for i in range(5):
    a=i*math.tau/5
    parts.append(ico('Bush',(.55*math.cos(a),.55*math.sin(a),.55),(.8,.65,.65),leaves[i%4],1))
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
print('COAST_ASSETS_EXPORTED: six GLBs and two editable .blend sources')
