"""Realistic ground: unique 4m surface maps, dry litter and sparse gravel. Cartoon untouched."""
from pathlib import Path
import argparse,json,sys,math,random
import bpy
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
PROJECT=ROOT/'nature-demo'
parser=argparse.ArgumentParser()
parser.add_argument('--preset',default=None)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
catalog=json.loads((Path(__file__).parent/'ground-presets.json').read_text(encoding='utf-8-sig'))
name=args.preset or catalog['default']
cfg=catalog['presets'][name]
assert 0<=cfg['litter_count']<=10000 and 0<=cfg['pebbles']<=500
bpy.ops.wm.read_factory_settings(use_empty=True)
N=2048
gen=np.random.default_rng(912);rng=random.Random(912)
def noise(cells):
    values=gen.random((cells,cells))
    x=np.arange(N)*cells/N;i=x.astype(int);f=x-i;f=f*f*(3-2*f)
    a=values[i[:,None]%cells,i[None,:]%cells]
    b=values[i[:,None]%cells,(i[None,:]+1)%cells]
    c=values[(i[:,None]+1)%cells,i[None,:]%cells]
    d=values[(i[:,None]+1)%cells,(i[None,:]+1)%cells]
    return (a*(1-f[None,:])+b*f[None,:])*(1-f[:,None])+(c*(1-f[None,:])+d*f[None,:])*f[:,None]
def save(label,rgb,data=False):
    if rgb.ndim==2:rgb=np.repeat(rgb[:,:,None],3,axis=2)
    rgba=np.ones((N,N,4),np.float32);rgba[:,:,:3]=np.clip(rgb,0,1)
    im=bpy.data.images.new(label,width=N,height=N)
    im.colorspace_settings.name='Non-Color' if data else 'sRGB'
    im.pixels.foreach_set(rgba.ravel());im.filepath_raw=str(PROJECT/'ground_asset/textures'/label)
    im.file_format='PNG';im.save()
macro=noise(6);clods=noise(130);fine=noise(580)
# Rasterized physical-size dry blades, rather than regular sinusoidal stripes.
litter=np.zeros((N,N));litter_tone=np.zeros((N,N))
for _ in range(cfg['litter_count']):
    x,y=rng.randrange(N),rng.randrange(N);a=rng.random()*math.tau
    length=rng.uniform(7,30);shade=rng.uniform(.4,1)
    for t in np.linspace(-.5,.5,int(length*2)):
        px=int(x+math.cos(a)*length*t)%N;py=int(y+math.sin(a)*length*t)%N
        litter[py,px]=1;litter_tone[py,px]=shade
for kind,base in [('soil',(.29,.235,.17)),('turf',(.225,.25,.135)),('sand',(.55,.48,.35))]:
    factor=.76+.28*macro+.13*clods+.08*fine
    rgb=np.array(base)[None,None,:]*factor[:,:,None]
    bumps=(clods-.5)*.0015+(fine-.5)*.0007
    if kind=='sand':bumps*=.4
    # Earth visible below muted grass litter; no bright green carpet.
    amount=1 if kind=='turf' else (.5 if kind=='soil' else .12)
    mask=litter*amount
    rgb=rgb*(1-mask[:,:,None])+np.array((.43,.36,.21))[None,None,:]*(.7+.3*litter_tone[:,:,None])*mask[:,:,None]
    bumps+=mask*.0005
    derivative=N/8
    dx=(np.roll(bumps,-1,1)-np.roll(bumps,1,1))*derivative
    dy=(np.roll(bumps,-1,0)-np.roll(bumps,1,0))*derivative
    normal=np.stack((-dx,-dy,np.ones_like(dx)),2);normal/=np.linalg.norm(normal,axis=2,keepdims=True)
    save(kind+'_realistic_albedo.png',rgb)
    save(kind+'_realistic_normal.png',normal*.5+.5,True)
    save(kind+'_realistic_roughness.png',.86+.10*fine,True)
    print('GROUND_MAP_OK',kind,flush=True)
def smooth(a,b,x):
    t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
verts=[];faces=[];uvs=[];colors=[]
def add(x,y,z,w):
    verts.append((x,y,z));uvs.append(((x+2)/4,(y+2)/4));colors.append((*w,1))
for y in range(33):
    for x in range(33):
        px=-2+x/8;py=-2+y/8
        path=1-smooth(.22,.65,abs(px-.25*math.sin(py*2)))
        sand=smooth(.70,1.55,-py+.12*math.sin(px*3))
        if name=='coastal_sand':sand=max(sand,.4)
        add(px,py,0,((1-sand)*(1-path),(1-sand)*path,sand))
for y in range(32):
    for x in range(32):
        k=y*33+x;faces.extend([(k,k+1,k+34),(k,k+34,k+33)])
for _ in range(cfg['pebbles']):
    x=rng.uniform(-1.85,1.85);y=rng.uniform(-1.85,1.85)
    radius=rng.uniform(.007,.025);h=radius*rng.uniform(.3,.7);start=len(verts)
    add(x,y,h,(0,.7,.3))
    for j in range(7):
        a=j*math.tau/7;r=radius*rng.uniform(.7,1.2)
        add(x+math.cos(a)*r,y+math.sin(a)*r,-.001,(0,.7,.3))
    for j in range(7):faces.append((start,start+1+j,start+1+(j+1)%7))
mesh=bpy.data.meshes.new('ground_patch_realistic_v2');mesh.from_pydata(verts,[],faces);mesh.update()
uv=mesh.uv_layers.new(name='Surface UV')
for loop in mesh.loops:uv.data[loop.index].uv=uvs[loop.vertex_index]
attr=mesh.color_attributes.new(name='LayerWeights',type='FLOAT_COLOR',domain='POINT')
for i,c in enumerate(colors):attr.data[i].color=c
ob=bpy.data.objects.new(mesh.name,mesh);bpy.context.collection.objects.link(ob)
ob.select_set(True);bpy.context.view_layer.objects.active=ob
bpy.ops.export_scene.gltf(filepath=str(PROJECT/'ground_asset/meshes'/(mesh.name+'.glb')),export_format='GLB',
    use_selection=True,export_yup=True,export_tangents=True,export_materials='NONE',export_all_vertex_colors=True)
(PROJECT/'ground_asset/style-settings.json').write_text(json.dumps({'preset':name,**cfg},indent=2),encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art-source/nature/ground-realistic-v2.blend'))
print('GROUND_REALISTIC_OK triangles='+str(len(faces)),flush=True)
