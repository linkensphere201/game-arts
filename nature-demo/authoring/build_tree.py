"""One editable branching tree, textured leaf cards and a reduced far mesh."""
from pathlib import Path
import bpy
import numpy as np
import math
import random
import json
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[2]
PACK=ROOT/'nature-demo/tree_asset'
(PACK/'meshes').mkdir(exist_ok=True)
(PACK/'textures').mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
N=1024
u,v=np.meshgrid(np.arange(N)/N,np.arange(N)/N)
def image(name,rgb,data=False,alpha=None):
    if rgb.ndim==2:rgb=np.repeat(rgb[:,:,None],3,axis=2)
    rgba=np.ones((N,N,4),np.float32);rgba[:,:,:3]=np.clip(rgb,0,1)
    if alpha is not None:rgba[:,:,3]=alpha
    im=bpy.data.images.new(name,width=N,height=N,alpha=alpha is not None)
    im.colorspace_settings.name='Non-Color' if data else 'sRGB'
    im.pixels.foreach_set(rgba.ravel());im.filepath_raw=str(PACK/'textures'/(name+'.png'))
    im.file_format='PNG';im.save()
def normal(h,s):
    dx=(np.roll(h,-1,axis=1)-np.roll(h,1,axis=1))*s
    dy=(np.roll(h,-1,axis=0)-np.roll(h,1,axis=0))*s
    n=np.stack((-dx,-dy,np.ones_like(dx)),axis=2);n/=np.linalg.norm(n,axis=2,keepdims=True)
    return n*.5+.5
# Elongated cellular bark plates and broken fissures, not uniform stripes.
px=u*36+np.sin(v*math.tau*3)*.65
py=v*9+np.sin(u*math.tau*2)*.2
ix=np.floor(px);iy=np.floor(py)
f1=np.full_like(u,99);f2=np.full_like(u,99)
for dx in [-1,0,1]:
    for dy in [-1,0,1]:
        cx=ix+dx;cy=iy+dy
        hx=np.mod(np.sin(np.mod(cx,36)*127.1+np.mod(cy,9)*311.7)*43758.5453,1)
        hy=np.mod(np.sin(np.mod(cx,36)*269.5+np.mod(cy,9)*183.3)*43758.5453,1)
        distance=(cx+hx-px)**2+(cy+hy-py)**2
        f2=np.minimum(f2,np.maximum(f1,distance));f1=np.minimum(f1,distance)
furrow=np.exp(-((np.sqrt(f2)-np.sqrt(f1))/.095)**2)
flecks=(np.sin(u*math.tau*190)*np.sin(v*math.tau*220)+1)*.5
grain=np.clip(.72-.65*furrow+.12*flecks,0,1)
vein=np.exp(-((u-.5)/.018)**2)
sideveins=(.5+.5*np.cos((v-np.abs(u-.5)*.72)*math.tau*11))**12
leaf_height=.18*vein+.035*sideveins
width=.44*np.sin(v*math.pi)**.8*(1+.022*np.sin(v*math.tau*28))
alpha=(np.abs(u-.5)<width).astype(np.float32)
for style in ['realistic','cartoon']:
    if style=='realistic':
        bark=np.array((.43,.30,.17))[None,None,:]*(.80+.32*grain-.25*furrow+.07*flecks)[:,:,None]
        leaf=np.array((.24,.43,.085))[None,None,:]*(.7+.38*v+.13*sideveins)[:,:,None]
    else:
        regions=np.floor(grain*4)/4
        bark=np.array((.50,.33,.17))[None,None,:]*(.83+.28*regions-.19*furrow)[:,:,None]
        leaf=np.array((.36,.53,.13))[None,None,:]*(.76+.28*v+.12*sideveins)[:,:,None]
    leaf+=vein[:,:,None]*np.array((.10,.12,.035))
    image('bark_'+style+'_albedo',bark)
    image('bark_'+style+'_normal',normal(.4*grain-.2*furrow,5),True)
    image('bark_'+style+'_roughness',.78+.17*flecks,True)
    image('leaf_'+style+'_albedo',leaf,alpha=alpha)
    image('leaf_'+style+'_normal',normal(leaf_height,4),True)

rng=random.Random(384)
verts=[];faces=[];uvs=[]
def tube(points,radii,sides=10):
    start=len(verts);length=0.0
    for k,p in enumerate(points):
        p=Vector(p)
        direction=Vector(points[min(k+1,len(points)-1)])-Vector(points[max(k-1,0)])
        direction.normalize()
        basis=direction.cross(Vector((0,1,0))).normalized()
        other=direction.cross(basis).normalized()
        if k:length+=(p-Vector(points[k-1])).length
        for i in range(sides+1):
            a=i/sides*math.tau
            radius=radii[k]*(1+.07*math.sin(a*5+k*.7))
            point=p+(basis*math.cos(a)+other*math.sin(a))*radius
            if k==0 and abs(p.z)<.00001:point.z=0
            verts.append(tuple(point))
            uvs.append((i/sides,length*.7))
        if k:
            for i in range(sides):
                a=start+(k-1)*(sides+1)+i;b=a+sides+1
                faces.extend([(a,a+1,b+1),(a,b+1,b)])
    # Closed caps, no physics assigned to the visual mesh.
    faces.append(tuple(reversed([start+i for i in range(sides)])))
    faces.append(tuple(start+(len(points)-1)*(sides+1)+i for i in range(sides)))

trunk=[(.055*math.sin(t*2),.035*math.sin(t*1.7),t) for t in [0,.15,.5,1,1.5,2,2.5,3,3.5,4]]
tube(trunk,[.42,.29,.22,.20,.17,.145,.12,.10,.07,.025],14)
clusters=[]
for i in range(11):
    a=i*2.399
    base=Vector((0,0,1.4+i*.19))
    reach=1.55-.045*i
    end=Vector((math.cos(a)*reach,math.sin(a)*reach,3.15+i*.125))
    mid=base.lerp(end,.5)+Vector((0,0,-.15))
    tube([base,mid,end],[.11-.004*i,.065,.022],9)
    for j in range(3):
        turn=a+(j-1)*.65
        twig=end+Vector((math.cos(turn)*.6,math.sin(turn)*.6,.30+j*.08))
        tube([end,twig],[.024,.005],6)
        clusters.append(twig)

def object_mesh(name,vs,fs,uv,weights=None):
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(vs,[],fs);mesh.update()
    layer=mesh.uv_layers.new(name='Surface UV')
    for loop in mesh.loops:layer.data[loop.index].uv=uv[loop.vertex_index]
    for poly in mesh.polygons:
        if len(poly.vertices)>4:
            for index in poly.loop_indices:
                co=mesh.vertices[mesh.loops[index].vertex_index].co
                layer.data[index].uv=(co.x,co.y)
    if weights is not None:
        layer=mesh.uv_layers.new(name='LeafBend')
        for loop in mesh.loops:layer.data[loop.index].uv=weights[loop.vertex_index]
    for p in mesh.polygons:p.use_smooth=True
    ob=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(ob)
    return ob
bark=object_mesh('Bark',verts,faces,uvs)
bpy.context.view_layer.objects.active=bark;bark.select_set(True)
tri=bark.modifiers.new('Explicit cap triangles','TRIANGULATE')
bpy.ops.object.modifier_apply(modifier=tri.name)

def leaves(name,stride):
    vs=[];fs=[];uv=[];weights=[]
    # Reset seed: far cards are a deterministic subset with slightly broader coverage.
    randomizer=random.Random(385)
    for center in clusters:
        for i in range(34):
            az=randomizer.random()*math.tau
            offset=Vector((math.cos(az)*randomizer.uniform(.05,.65),math.sin(az)*randomizer.uniform(.05,.65),randomizer.uniform(-.25,.38)))
            at=center+offset
            length=randomizer.uniform(.22,.37)
            side=Vector((math.cos(az),math.sin(az),0))
            forward=Vector((-math.sin(az)*.75,math.cos(az)*.75,randomizer.uniform(-.5,.7))).normalized()
            if i%stride:continue
            length*=1 if stride==1 else 1.6
            k=len(vs)
            for t in [0,.5,1]:
                for sign in [-1,1]:
                    p=at+forward*length*t+side*sign*length*.33+Vector((0,0,.035*math.sin(t*math.pi)))
                    vs.append(tuple(p));uv.append(((sign+1)*.5,t));weights.append((t,0))
            fs.extend([(k,k+1,k+3),(k,k+3,k+2),(k+2,k+3,k+5),(k+2,k+5,k+4)])
    return object_mesh(name,vs,fs,uv,weights)
near=leaves('Leaves',1);far=leaves('LeavesFar',3)
def export(name,objects):
    bpy.ops.object.select_all(action='DESELECT')
    for ob in objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    bpy.ops.export_scene.gltf(filepath=str(PACK/'meshes'/(name+'.glb')),export_format='GLB',use_selection=True,export_yup=True,export_tangents=True,export_materials='NONE')
    return {'name':name,'triangles':sum(sum(len(p.vertices)-2 for p in ob.data.polygons) for ob in objects),'leaf_cards':len(objects[1].data.polygons)//4}
records=[export('tree_near',[bark,near]),export('tree_far',[bark,far])]
far.hide_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art-source/nature/coastal-tree.blend'))
(PACK/'inventory.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print('TREE_SOURCES_OK',json.dumps(records),flush=True)
