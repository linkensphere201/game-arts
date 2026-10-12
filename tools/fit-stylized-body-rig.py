"""M5.2.9.6.5: fit original rig/weights to the restored proportion variant.
Blender -b -P SCRIPT -- ORIGINAL_RIG_BLEND RESTORED_BODY_BLEND OUT
"""
import bpy,sys,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.kdtree import KDTree

source,restored,out=map(Path,sys.argv[sys.argv.index('--')+1:])
out.mkdir(parents=True,exist_ok=True)
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,restored]}
bpy.ops.wm.open_mainfile(filepath=str(source))
if bpy.context.object and bpy.context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
rig=bpy.data.objects['StandardBodyRig'];old=bpy.data.objects['Standard_adult_body']
rig.animation_data_clear()
for bone in rig.pose.bones:bone.matrix_basis.identity()
for m in old.modifiers:m.show_viewport=False
bpy.context.view_layer.update()
evaluated=old.evaluated_get(bpy.context.evaluated_depsgraph_get())
group_names={g.index:g.name for g in old.vertex_groups}
bodygroup=old.vertex_groups['body'].index
tree=KDTree(len(old.data.vertices))
count=0
for v in old.data.vertices:
    if any(g.group==bodygroup and g.weight>.5 for g in v.groups):
        tree.insert(evaluated.data.vertices[v.index].co,v.index);count+=1
tree.balance()
old.name='Original_weight_source';old.hide_render=True;old.hide_set(True)
with bpy.data.libraries.load(str(restored),link=False) as (available,loaded):
    loaded.objects=['Stylized_body_PROPORTIONS_ONLY','White_eye_L','White_eye_R']
for obj in loaded.objects:bpy.context.collection.objects.link(obj)
ref=loaded.objects[0]
assert ref.data.shape_keys.key_blocks['Manga_face'].value==0
assert ref.data.shape_keys.key_blocks['Manga_6_25_heads'].value==1
bpy.context.view_layer.update()
mesh=bpy.data.meshes.new_from_object(ref.evaluated_get(bpy.context.evaluated_depsgraph_get()),depsgraph=bpy.context.evaluated_depsgraph_get())
body=bpy.data.objects.new('Standard_adult_body',mesh);bpy.context.collection.objects.link(body)
body.matrix_world=ref.matrix_world.copy()
for group in old.vertex_groups:body.vertex_groups.new(name=group.name)
indices=list(range(len(mesh.vertices)))
for group in body.vertex_groups:group.remove(indices)
mapping=[];errors=[]
for i,v in enumerate(ref.data.shape_keys.key_blocks['Basis'].data):
    _,index,distance=tree.find(v.co);mapping.append(index);errors.append(distance)
    for g in old.data.vertices[index].groups:
        body.vertex_groups[group_names[g.group]].add([i],g.weight,'REPLACE')
assert max(errors)<1e-6, max(errors)
assert len(set(mapping))==13380
ref.hide_render=True;ref.hide_set(True)

# Identical rest-space map to the approved body builder, checked against every
# body's mapped vertex. Do not transfer the rejected facial deformation.
height=1.5535954236984253;chin=1.344
anchors=[(0,0),(.065,.065),(.451,.475),(.816,.842),(.96,.982),
         (1.145,1.133),(1.245,1.205),(chin,height-height/6.25),(height,height)]
def smooth(a,b,t):
    t=min(1.,max(0.,(t-a)/(b-a)));return t*t*(3-2*t)
def transform(co):
    x,y,z=co
    nz=z
    for (a,u),(b,v) in zip(anchors,anchors[1:]):
        if z<=b:nz=u+(z-a)/(b-a)*(v-u);break
    head=smooth(1.27,chin+.025,z);central=1-smooth(.13,.25,abs(x))
    waist=math.exp(-((z-.97)/.105)**2)*central
    chest=math.exp(-((z-1.135)/.105)**2)*central
    neck=math.exp(-((z-1.30)/.045)**2)*central
    jaw=math.exp(-((z-1.375)/.042)**2)*head
    leg=(1-smooth(.72,.83,z))*smooth(.08,.19,z)
    axis=.179+min(1.,max(0.,(z-.065)/.751))*(.097-.179)
    sx=axis+(abs(x)-axis)*(1-.10*leg)
    sx*=1-.10*waist-.035*chest-.10*neck+.18*head-.075*jaw
    return Vector((math.copysign(sx,x),y*(1-.075*waist-.07*chest-.10*neck+.12*head),nz))
shape_error=max((transform(ref.data.shape_keys.key_blocks['Basis'].data[i].co)-v.co).length for i,v in enumerate(mesh.vertices))
assert shape_error<1e-6,shape_error
bpy.ops.object.select_all(action='DESELECT');rig.hide_set(False);rig.select_set(True)
bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT')
changes=[]
for bone in rig.data.edit_bones:
    h,t=bone.head.copy(),bone.tail.copy();axis=bone.z_axis.copy()
    bone.head=transform(h);bone.tail=transform(t)
    bone.align_roll(transform(h+axis*.01)-transform(h))
    changes.append({'bone':bone.name,'old_head':list(h),'new_head':list(bone.head)})
bpy.ops.object.mode_set(mode='OBJECT')

# Freeze eye geometry and join into the body, with rigid head weights so it
# remains attached during attacks/hits and is included in the existing exporter.
join=[body]
for refeye in loaded.objects[1:]:
    em=bpy.data.meshes.new_from_object(refeye.evaluated_get(bpy.context.evaluated_depsgraph_get()),depsgraph=bpy.context.evaluated_depsgraph_get())
    eye=bpy.data.objects.new(refeye.name+'_bound',em);bpy.context.collection.objects.link(eye)
    eye.matrix_world=refeye.matrix_world.copy()
    # Discard unused source deform data before assigning head-only membership.
    for name in ['head','body']:
        group=eye.vertex_groups.new(name=name);group.add(list(range(len(em.vertices))),1,'REPLACE')
    refeye.hide_render=True;refeye.hide_set(True);join.append(eye)
bpy.ops.object.select_all(action='DESELECT')
for obj in join:obj.select_set(True)
bpy.context.view_layer.objects.active=body;bpy.ops.object.join()
mod=body.modifiers.new('Adapted_rig','ARMATURE');mod.object=rig;mod.use_deform_preserve_volume=False
body.parent=rig
rig.show_in_front=True
bpy.context.view_layer.update()
report={'task':'M5.2.9.6.5','source_hashes':hashes,'body_vertex_correspondence':len(mapping),
        'max_correspondence_error_m':max(errors),'max_rest_shape_error_m':shape_error,
        'bound_vertices_with_eyes':len(body.data.vertices),'joints':changes,'face_key':0}
for path,sha in hashes.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha
bpy.ops.wm.save_as_mainfile(filepath=str(out/'adapted-rig.blend'))
(out/'adaptation.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('STYLIZED_RIG_FIT_OK',len(body.data.vertices),shape_error,flush=True)
