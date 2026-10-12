"""M3.8 ground/grass sources: Blender meshes and deterministic local texture synthesis.
No downloads or image-model inference. Run from the repository with Blender --python.
"""
from pathlib import Path
import math
import json
import random
import bpy
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT/'nature-demo'
SOURCE = ROOT/'art-source/nature'
SOURCE.mkdir(parents=True, exist_ok=True)
N=1024
gen=np.random.default_rng(381)
bpy.ops.wm.read_factory_settings(use_empty=True)

def noise(cells):
    values=gen.random((cells,cells))
    x=np.arange(N)*cells/N
    i=x.astype(int);f=x-i;f=f*f*(3-2*f)
    a=values[i[:,None]%cells,i[None,:]%cells]
    b=values[i[:,None]%cells,(i[None,:]+1)%cells]
    c=values[(i[:,None]+1)%cells,i[None,:]%cells]
    d=values[(i[:,None]+1)%cells,(i[None,:]+1)%cells]
    return (a*(1-f[None,:])+b*f[None,:])*(1-f[:,None])+(c*(1-f[None,:])+d*f[None,:])*f[:,None]

def image(path, rgb, data=False, alpha=None):
    path.parent.mkdir(parents=True,exist_ok=True)
    if rgb.ndim==2: rgb=np.repeat(rgb[:,:,None],3,axis=2)
    rgba=np.ones((rgb.shape[0],rgb.shape[1],4),np.float32)
    rgba[:,:,:3]=np.clip(rgb,0,1)
    if alpha is not None:rgba[:,:,3]=alpha
    im=bpy.data.images.new(path.stem,width=rgb.shape[1],height=rgb.shape[0],alpha=alpha is not None)
    im.colorspace_settings.name='Non-Color' if data else 'sRGB'
    im.pixels.foreach_set(rgba.ravel())
    im.filepath_raw=str(path);im.file_format='PNG';im.save()
    return im

def normal(height,strength):
    dx=(np.roll(height,-1,axis=1)-np.roll(height,1,axis=1))*strength
    dy=(np.roll(height,-1,axis=0)-np.roll(height,1,axis=0))*strength
    n=np.stack((-dx,-dy,np.ones_like(dx)),axis=2)
    n/=np.linalg.norm(n,axis=2,keepdims=True)
    return n*.5+.5

# All noises are periodic; normal derivatives wrap at image borders.
macro,clods,grit=noise(7),noise(40),noise(230)
u,v=np.meshgrid(np.arange(N)/N,np.arange(N)/N)
for style in ['realistic','cartoon']:
    for kind,base in [('turf',(.24,.31,.12)),('soil',(.32,.23,.145)),('sand',(.66,.58,.43))]:
        patch=macro if style=='realistic' else np.floor(macro*5)/5
        height=.48*clods+.18*grit
        factor=.90+.15*patch+.05*grit
        color=np.array(base)[None,None,:]*factor[:,:,None]
        if kind=='turf':
            # Short fallen blades in distinct directions, over visible soil.
            strokes=(np.sin(u*math.tau*90+np.sin(v*math.tau*11)*2)>.93)&(clods>.51)
            color+=strokes[:,:,None]*np.array((.055,.065,.016))
            height+=strokes*.12
        elif kind=='soil':
            stones=np.maximum(0,clods-.67)*3
            color+=stones[:,:,None]*np.array((.10,.092,.07))
            height+=stones*.3
        else:
            ripples=np.sin(v*math.tau*10+np.sin(u*math.tau*3)*.45)*.5+.5
            height=.10*ripples+.14*grit+.06*clods
            color*= (.93+.09*ripples)[:,:,None]
        folder=PROJECT/'ground_asset/textures'
        image(folder/f'{kind}_{style}_albedo.png',color)
        image(folder/f'{kind}_{style}_normal.png',normal(height,5 if style=='realistic' else 2),True)
        image(folder/f'{kind}_{style}_roughness.png',np.clip(.8+.16*clods,0,1),True)
        print('GROUND_TEXTURES',kind,style,flush=True)

# Each grass blade spans the whole texture: authored longitudinal veins/dry tip.
for style in ['realistic','cartoon']:
    vein=np.exp(-((u-.5)/.035)**2)
    ribs=np.sin(u*math.tau*18+np.sin(v*math.tau*2)*.25)*.5+.5
    dry=np.clip((v-.73)*5,0,1)*(noise(6)*.6+.4)
    green=np.array((.22,.43,.075)) if style=='realistic' else np.array((.32,.52,.11))
    color=green[None,None,:]*(.52+.65*v[:,:,None])
    color=color*(1-dry[:,:,None]*.65)+np.array((.54,.43,.18))[None,None,:]*dry[:,:,None]*.65
    color+=vein[:,:,None]*np.array((.045,.052,.014))
    if style=='realistic':color*= (.92+.12*ribs)[:,:,None]
    image(PROJECT/'grass_asset/textures'/f'blade_{style}_albedo.png',color)
    image(PROJECT/'grass_asset/textures'/f'blade_{style}_normal.png',normal(.08*ribs+.15*vein,2),True)

def mesh_object(name,verts,faces,uvs,weights=None,colors=None):
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    uv=mesh.uv_layers.new(name='Surface UV')
    for loop in mesh.loops:uv.data[loop.index].uv=uvs[loop.vertex_index]
    if weights is not None:
        aux=mesh.uv_layers.new(name='BendWeight')
        for loop in mesh.loops:aux.data[loop.index].uv=weights[loop.vertex_index]
    if colors is not None:
        attr=mesh.color_attributes.new(name='LayerWeights',type='FLOAT_COLOR',domain='POINT')
        for i,c in enumerate(colors):attr.data[i].color=c
    for p in mesh.polygons:p.use_smooth=True
    ob=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(ob)
    return ob

def export(ob,asset):
    folder=PROJECT/asset/'meshes';folder.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
    bpy.ops.export_scene.gltf(filepath=str(folder/(ob.name+'.glb')),export_format='GLB',use_selection=True,
        export_yup=True,export_tangents=True,export_materials='NONE',export_all_vertex_colors=True)
    return {'name':ob.name,'triangles':sum(len(p.vertices)-2 for p in ob.data.polygons),'vertices':len(ob.data.vertices)}

def smooth(a,b,x):
    t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)

verts=[];faces=[];uvs=[];colors=[]
for y in range(33):
    for x in range(33):
        px=-2+x/8;py=-2+y/8
        verts.append((px,py,0));uvs.append(((px+2)/4,(py+2)/4))
        path=1-smooth(.27,.60,abs(px-.25*math.sin(py*2)))
        sand=smooth(.70,1.55,-py+.12*math.sin(px*3))
        colors.append(((1-sand)*(1-path),(1-sand)*path,sand,1))
for y in range(32):
    for x in range(32):
        a=y*33+x;faces.extend([(a,a+1,a+34),(a,a+34,a+33)])
ground=mesh_object('ground_patch',verts,faces,uvs,colors=colors)
record=export(ground,'ground_asset')
(PROJECT/'ground_asset/inventory.json').write_text(json.dumps(record,indent=2))
ground.hide_set(True)
rng=random.Random(383)
records=[]
for name,count,height in [('short',22,.25),('medium',30,.48),('dry',13,.39)]:
    verts=[];faces=[];uvs=[];weights=[]
    for i in range(count):
        a=rng.random()*math.tau;r=rng.random()*.13
        base=(math.cos(a)*r,math.sin(a)*r)
        direction=rng.random()*math.tau
        h=height*rng.uniform(.65,1.15);width=rng.uniform(.012,.026)
        start=len(verts)
        for step in range(5):
            t=step/4;w=width*(1-t)**.7+.0003
            lean=h*.48*t*t
            for side in [-1,1]:
                verts.append((base[0]+math.cos(direction)*lean+side*w*math.sin(direction),
                    base[1]+math.sin(direction)*lean-side*w*math.cos(direction),h*t))
                uvs.append(((side+1)*.5,t));weights.append((t,h))
        for step in range(4):
            k=start+step*2;faces.extend([(k,k+1,k+3),(k,k+3,k+2)])
    ob=mesh_object('grass_'+name,verts,faces,uvs,weights)
    records.append(export(ob,'grass_asset'));ob.location.x={'short':-1,'medium':0,'dry':1}[name]
(PROJECT/'grass_asset/inventory.json').write_text(json.dumps(records,indent=2))
# Source maps are separate editable inputs; no export-time material packing required.
bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE/'ground-grass.blend'))
print('NATURE_SOURCES_OK',json.dumps(records),flush=True)
