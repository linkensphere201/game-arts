"""Realistic-only grass with mixed upright/curved silhouettes. Original cartoon meshes/maps remain untouched."""
from pathlib import Path
import math, random, json, sys, argparse
import bpy
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
PROJECT=ROOT/'nature-demo'
parser=argparse.ArgumentParser()
parser.add_argument('--preset',default=None)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
catalog=json.loads((Path(__file__).parent/'grass-presets.json').read_text(encoding='utf-8-sig'))
preset_name=args.preset or catalog['default']
if preset_name not in catalog['presets']: raise ValueError('Unknown grass preset: '+preset_name)
settings={**catalog['presets']['reference_meadow'],**catalog['presets'][preset_name]}
shape_names=['upright','gentle','arched']
weights_config=settings['shape_weights']
if set(weights_config)!=set(shape_names) or any(weights_config[k]<0 for k in shape_names) or abs(sum(weights_config.values())-1)>1e-6:
    raise ValueError('shape_weights must contain three nonnegative proportions totaling 1')
for ranges in ['lean_ranges','half_width_ranges_m']:
    for lo,hi in settings[ranges].values():
        if not 0<=lo<=hi: raise ValueError('Invalid '+ranges)
if not 0<settings['height_scale_range'][0]<=settings['height_scale_range'][1]:
    raise ValueError('Invalid height scale range')
if any(h<=0 or h*settings['height_scale_range'][1]>=1 for h in settings['variant_heights_m'].values()):
    raise ValueError('Blade heights must be positive and below 1 m for the current UV2 height encoding')
if not 0<=settings['wind_strength']<=2: raise ValueError('wind_strength must be 0..2')
if len(settings['scatter_attempts'])!=3 or any(not isinstance(n,int) or not 0<=n<=1000 for n in settings['scatter_attempts']):
    raise ValueError('scatter_attempts requires three integers between 0 and 1000')
for key in ['tall_probability','dry_probability']:
    if not 0<=settings[key]<=1: raise ValueError(key+' must be 0..1')
bpy.ops.wm.read_factory_settings(use_empty=True)
rng=random.Random(681)
N=1024
u,v=np.meshgrid(np.arange(N)/N,np.arange(N)/N)
# Lower chroma, gradual root-to-tip variation, a fine central fold and longitudinal veins.
ribs=.5+.5*np.sin(u*math.tau*23+.35*np.sin(v*math.tau*3))
vein=np.exp(-((u-.5)/.045)**2)
dry=np.clip((v-.67)*2.4,0,.65)
color=np.array((.25,.32,.13))[None,None,:]*(.78+.28*v[:,:,None])
color=color*(1-dry[:,:,None])+np.array((.48,.40,.23))[None,None,:]*dry[:,:,None]
color*= (.96+.06*ribs+.07*vein)[:,:,None]
def image(name,rgb,data=False):
    rgba=np.ones((N,N,4),np.float32);rgba[:,:,:3]=np.clip(rgb,0,1)
    im=bpy.data.images.new(name,width=N,height=N)
    im.colorspace_settings.name='Non-Color' if data else 'sRGB'
    im.pixels.foreach_set(rgba.ravel())
    im.filepath_raw=str(PROJECT/'grass_asset/textures'/name);im.file_format='PNG';im.save()
image('blade_realistic_albedo.png',color)
height=.05*ribs+.12*vein
dx=(np.roll(height,-1,1)-np.roll(height,1,1))*2
dy=(np.roll(height,-1,0)-np.roll(height,1,0))*2
norm=np.stack((-dx,-dy,np.ones_like(dx)),2);norm/=np.linalg.norm(norm,axis=2,keepdims=True)
image('blade_realistic_normal.png',norm*.5+.5,True)
records=[]
for name,count,maxheight in [('short',34,.17),('medium',25,.38),('dry',19,.29)]:
    maxheight=settings['variant_heights_m'][name]
    verts=[];faces=[];uvs=[];weights=[];colors=[]
    forms=[]
    def blade(base,direction,h,width,lean,twist,shade,segments=7):
        start=len(verts)
        for row in range(segments+1):
            t=row/segments
            # Arched centerline and rotation along the blade avoid rigid flat spikes.
            angle=direction+twist*t
            radial=lean*h*t*t
            z=h*(t-min(.3,lean*.2)*t*t*t)
            w=width*(1-t)**.85+.00006
            for side in [-1,1]:
                verts.append((base[0]+math.cos(direction)*radial+side*w*math.sin(angle),
                              base[1]+math.sin(direction)*radial-side*w*math.cos(angle),z))
                uvs.append(((side+1)*.5,t));weights.append((t,h));colors.append((*shade,1))
        for row in range(segments):
            k=start+row*2;faces.extend([(k,k+1,k+3),(k,k+3,k+2)])
    # Deliberate populations, shuffled independently: shape is not tied to width/height.
    quotas=[count*weights_config[k] for k in shape_names]
    counts=[int(q) for q in quotas]
    for j in sorted(range(3),key=lambda j:quotas[j]-counts[j],reverse=True)[:count-sum(counts)]:
        counts[j]+=1
    shapes=[k for k,n in zip(shape_names,counts) for _ in range(n)]
    widths=['narrow','regular','broad']*(count//3+1)
    widths=widths[:count]
    rng.shuffle(shapes);rng.shuffle(widths)
    for i in range(count):
        a=rng.random()*math.tau;r=math.sqrt(rng.random())*.16
        base=(math.cos(a)*r,math.sin(a)*r)
        h=maxheight*rng.uniform(*settings['height_scale_range'])
        width=rng.uniform(*settings['half_width_ranges_m'][widths[i]])
        lean=rng.uniform(*settings['lean_ranges'][shapes[i]])
        twist=rng.uniform(-.25,.25) if shapes[i]=='upright' else rng.uniform(-.8,.8)
        forms.append({'shape':shapes[i],'width_class':widths[i],'height':h,'full_width':width*2,'lean':lean})
        shade=rng.choice([(.8,.86,.69),(1,.96,.8),(.76,.83,.62),(1.1,1.02,.85)])
        blade(base,rng.random()*math.tau,h,width,lean,twist,shade)
    mesh=bpy.data.meshes.new('grass_'+name+'_realistic_v2')
    mesh.from_pydata(verts,[],faces);mesh.update()
    for label,values in [('UVMap',uvs),('BendWeight',weights)]:
        layer=mesh.uv_layers.new(name=label)
        for loop in mesh.loops:layer.data[loop.index].uv=values[loop.vertex_index]
    attr=mesh.color_attributes.new(name='BladeTint',type='FLOAT_COLOR',domain='POINT')
    for i,c in enumerate(colors):attr.data[i].color=c
    for face in mesh.polygons:face.use_smooth=True
    ob=bpy.data.objects.new(mesh.name,mesh);bpy.context.collection.objects.link(ob)
    bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
    bpy.ops.export_scene.gltf(filepath=str(PROJECT/'grass_asset/meshes'/(ob.name+'.glb')),
        export_format='GLB',use_selection=True,export_yup=True,export_tangents=True,
        export_materials='NONE',export_all_vertex_colors=True)
    records.append({'name':ob.name,'triangles':len(faces),'vertices':len(verts),'blade_forms':forms})
    ob.location.x={'short':-1,'medium':0,'dry':1}[name]
(PROJECT/'grass_asset/inventory-realistic-v2.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art-source/nature/grass-realistic-v2.blend'))
(PROJECT/'grass_asset/style-settings.json').write_text(json.dumps({'preset':preset_name,**settings},indent=2),encoding='utf-8')
print('REALISTIC_GRASS_OK preset='+preset_name,flush=True)
