"""Create restrained idle and IK walk, export a separate game mesh copy."""
import bpy,sys,math,json
from pathlib import Path
from mathutils import Vector,Quaternion,Matrix
out=Path(sys.argv[sys.argv.index('--')+1]);bpy.ops.wm.open_mainfile(filepath=str(out/'03-rigged.blend'))
rig=bpy.data.objects['AdventurerRig'];body=bpy.data.objects['Standard_adult_body'];scene=bpy.context.scene
shirt=next(o for o in scene.objects if 'fisherman' in o.name)
for v in shirt.data.vertices:
    if v.co.z < .92:
        v.co.x*=1.10;v.co.y*=1.16
# Carry the equipment rigidly at the back; preserve the source fitted trial.
sword=next(o for o in scene.objects if 'sword' in o.name)
points=[v.co.copy() for v in sword.data.vertices];center=sum(points,Vector())/len(points)
longaxis=max(range(3),key=lambda i:max(v[i] for v in points)-min(v[i] for v in points))
direction=Vector(tuple(1 if i==longaxis else 0 for i in range(3)))
rot=direction.rotation_difference(Vector((.30,0,.95)).normalized())
extent=max(v[longaxis] for v in points)-min(v[longaxis] for v in points)
for v in sword.data.vertices:v.co=rot@(v.co-center)*(.60/extent)+Vector((.06,.19,1.24))
sword.vertex_groups.clear();sword.vertex_groups.new(name='spine_03').add(list(range(len(points))),1,'REPLACE')
covered=body.vertex_groups.new(name='UnderOutfit')
covered.add([v.index for v in body.data.vertices if v.co.z < .86],1,'REPLACE')
mask=body.modifiers.new('Hide covered legs','MASK');mask.vertex_group=covered.name;mask.invert_vertex_group=True
def rotation(name,axis,angle):
    p=rig.pose.bones[name];p.rotation_mode='QUATERNION'
    local=p.bone.matrix_local.to_quaternion().inverted()@Vector(axis)
    p.rotation_quaternion=Quaternion(local,angle)
def base():
    for p in rig.pose.bones:p.location=(0,0,0);p.rotation_mode='QUATERNION';p.rotation_quaternion=(1,0,0,0);p.scale=(1,1,1)
    rotation('upperarm_l',(0,1,0),math.radians(32));rotation('upperarm_r',(0,1,0),math.radians(-32))
def keys(frame):
    for p in rig.pose.bones:
        for prop in ['location','rotation_quaternion','scale']:p.keyframe_insert(prop,frame=frame)
rig.animation_data_create();actions=[];scene.render.fps=24
idle=bpy.data.actions.new('Idle');rig.animation_data.action=idle
for f in range(1,73):
    base();phase=2*math.pi*(f-1)/72
    rotation('spine_03',(1,0,0),.007*math.sin(phase));keys(f)
actions.append(idle)
walk=bpy.data.actions.new('Walk');rig.animation_data.action=walk
controls=[]
for side in ['l','r']:
    ankle=rig.data.bones['foot_'+side].head_local.copy()
    bpy.ops.object.empty_add();target=bpy.context.object;target.name='IK_ankle_'+side
    bpy.ops.object.empty_add(location=(ankle.x,-1,.6));pole=bpy.context.object;pole.name='IK_knee_'+side
    ik=rig.pose.bones['calf_'+side].constraints.new('IK');ik.target=target;ik.pole_target=pole;ik.chain_count=2
    # The supplied rig bends in its local X plane; solve pole alignment from rest axes.
    thigh=rig.data.bones['thigh_'+side];axis=(rig.data.bones['calf_'+side].tail_local-thigh.head_local).normalized()
    projected=Vector((0,-1,0));projected-=axis*projected.dot(axis);projected.normalize()
    # Calibrate against the evaluated knee: choose the pole rotation that bends forward.
    target.location=ankle+Vector((0,0,.04));base();bpy.context.view_layer.update()
    samples=[]
    for step in range(72):
        ik.pole_angle=step*2*math.pi/72;bpy.context.view_layer.update()
        samples.append((rig.pose.bones['calf_'+side].head.y,ik.pole_angle))
    ik.pole_angle=min(samples)[1]
    bpy.ops.object.empty_add();orient=bpy.context.object;orient.rotation_mode='QUATERNION';orient.rotation_quaternion=rig.data.bones['foot_'+side].matrix_local.to_quaternion()
    c=rig.pose.bones['foot_'+side].constraints.new('COPY_ROTATION');c.target=orient;c.target_space='WORLD';c.owner_space='WORLD'
    controls.extend([target,pole,orient])
    for f in range(1,26):
        phase=2*math.pi*(f-1)/24+(0 if side=='l' else math.pi)
        target.location=ankle+Vector((0,.10*math.cos(phase),.035*max(0,math.sin(phase))))
        target.keyframe_insert('location',frame=f)
for f in range(1,26):
    base();phase=2*math.pi*(f-1)/24
    rig.pose.bones['pelvis'].location.y=-.016
    for side,sign in [('l',1),('r',-1)]:
        p=rig.pose.bones['upperarm_'+side];p.rotation_quaternion=Quaternion(p.bone.matrix_local.to_quaternion().inverted()@Vector((1,0,0)),sign*.12*math.sin(phase))@p.rotation_quaternion
    keys(f)
bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig
bpy.ops.nla.bake(frame_start=1,frame_end=25,step=1,only_selected=False,visual_keying=True,clear_constraints=True,use_current_action=True,bake_types={'POSE'})
actions.append(walk)
rig.animation_data.action=None
for action in actions:
    track=rig.animation_data.nla_tracks.new();track.name=action.name;strip=track.strips.new(action.name,1,action);track.mute=True
rig.animation_data.action=idle;scene.frame_set(1)
for o in controls:o.hide_render=True;o.hide_set(True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'04-animated.blend'))
# Freeze shape keys and masks on copies only, retaining weighted vertices and UVs.
exportobjects=[rig]
for obj in [o for o in scene.objects if o.type=='MESH' and any(m.type=='ARMATURE' for m in o.modifiers)]:
    dup=obj.copy();dup.data=obj.data.copy();scene.collection.objects.link(dup);dup.name='Game_'+obj.name
    bpy.context.view_layer.objects.active=dup
    if dup.data.shape_keys:bpy.ops.object.shape_key_remove(all=True,apply_mix=True)
    for mod in list(dup.modifiers):
        if mod.type=='MASK':bpy.ops.object.modifier_apply(modifier=mod.name)
    exportobjects.append(dup);obj.hide_render=True
bpy.ops.object.select_all(action='DESELECT')
for obj in exportobjects:obj.select_set(True)
rig.animation_data.action=None
for track in rig.animation_data.nla_tracks:track.mute=False
bpy.ops.export_scene.gltf(filepath=str(out/'adventurer.glb'),export_format='GLB',use_selection=True,export_animations=True,export_animation_mode='NLA_TRACKS',export_apply=False,export_morph=False)
for track in rig.animation_data.nla_tracks:track.mute=True
rig.animation_data.action=walk
scene.render.resolution_x=450;scene.render.resolution_y=600
center=Vector((0,0,.8));scene.camera.location=(2,-4,1.6);scene.camera.rotation_euler=(center-scene.camera.location).to_track_quat('-Z','Y').to_euler()
for f in [1,7,13,19]:
    scene.frame_set(f);scene.render.filepath=str(out/f'walk-{f:02}.png');bpy.ops.render.render(write_still=True)
stats={'actions':[a.name for a in actions],'bones':len(rig.data.bones),'meshes':[{'name':o.name,'vertices':len(o.data.vertices),'triangles':sum(len(p.vertices)-2 for p in o.data.polygons)} for o in exportobjects if o.type=='MESH']}
(out/'export.json').write_text(json.dumps(stats,indent=2),encoding='utf8');print('CHARACTER_EXPORT_COMPLETE',flush=True)
