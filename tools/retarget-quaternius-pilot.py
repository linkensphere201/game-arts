"""M5.2.9.6.6 / .8: CC0 Quaternius retarget and expanded review.
Blender -b -P SCRIPT -- CURRENT_ACTION_BLEND SOURCE_IMPORT_BLEND OUT [--expanded]
Expanded mode adds ten source clips and preserves four existing turn/hit drafts.
Source import uses Blender 24 fps; sample seconds explicitly and bake at 30 fps.
"""
import bpy,sys,json,math,hashlib
from pathlib import Path
from mathutils import Vector,Matrix

args=sys.argv[sys.argv.index('--')+1:]
expanded='--expanded' in args
targetfile,sourcefile,out=map(Path,[a for a in args if a!='--expanded'])
out.mkdir(parents=True,exist_ok=True)
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [targetfile,sourcefile]}
bpy.ops.wm.open_mainfile(filepath=str(targetfile))
rig=bpy.data.objects['StandardBodyRig'];body=bpy.data.objects['Standard_adult_body']
legacy_names=['TurnLeft','TurnRight','HitLight','HitHeavy'] if expanded else []
legacy_actions={name:bpy.data.actions[name] for name in legacy_names}
legacy_clips=json.loads((targetfile.parent/'actions.json').read_text(encoding='utf8'))['clips'] if expanded else []
rig.animation_data_clear()
for p in rig.pose.bones:p.matrix_basis.identity()
with bpy.data.libraries.load(str(sourcefile),link=False) as (available,loaded):
    loaded.objects=available.objects
for obj in loaded.objects:
    bpy.context.collection.objects.link(obj)
    obj.hide_render=True
src=next(o for o in loaded.objects if o.type=='ARMATURE')
srcmesh=next(o for o in loaded.objects if o.type=='MESH' and any(m.type=='ARMATURE' and m.object==src for m in o.modifiers))
for track in src.animation_data.nla_tracks:track.mute=True
src.hide_render=True;srcmesh.hide_render=True
mapping={b.name:('root' if b.name=='Root' else 'Head' if b.name=='head' else b.name) for b in rig.data.bones}
assert all(n in src.data.bones for n in mapping.values())
correction={}
for name,sname in mapping.items():
    tb=rig.data.bones[name];sb=src.data.bones[sname]
    tq=tb.matrix_local.to_quaternion();sq=sb.matrix_local.to_quaternion()
    align=(tb.tail_local-tb.head_local).rotation_difference(sb.tail_local-sb.head_local)
    correction[name]=sq.inverted()@(align@tq)
scale=rig.data.bones['pelvis'].head_local.z/src.data.bones['pelvis'].head_local.z

def foot_indices(obj):
    indices={g.index for g in obj.vertex_groups if g.name.lower() in ['foot_l','foot_r','ball_l','ball_r']}
    return [v.index for v in obj.data.vertices if sum(g.weight for g in v.groups if g.group in indices)>.7]
ti=foot_indices(body);si=foot_indices(srcmesh)
assert ti and si
def floor(obj,indices):
    ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    return min((obj.matrix_world@ev.data.vertices[i].co).z for i in indices)

spec=[('Walk_Loop','行走',True),('Sprint_Loop','冲刺',True),('Punch_Cross','直拳',False),('Sword_Attack','挥剑（空手）',False)]
if expanded:
    spec=[('Idle_Loop','待机',True),('Walk_Loop','行走',True),('Jog_Fwd_Loop','慢跑',True),
          ('Sprint_Loop','冲刺',True),('Jump_Start','起跳阶段',False),('Jump_Loop','腾空阶段',True),
          ('Jump_Land','落地阶段',False),('Punch_Jab','刺拳',False),('Punch_Cross','交叉拳',False),
          ('Sword_Attack','挥剑（空手）',False)]
scene=bpy.context.scene;scene.render.fps=30
manifest={'fps':30,'source':'Quaternius Universal Animation Library Standard / CC0','clips':[]}
actions=[];checks=[]
for name,label,loop in spec:
    action=bpy.data.actions[name]
    src.animation_data.action=action
    if action.slots:src.animation_data.action_slot=action.slots[0]
    start,end=action.frame_range;duration=(end-start)/24
    frames=round(duration*30)
    # Cache source motion before keying any target action.
    cache=[]
    for frame in range(frames+1):
        f=start+frame/30*24;scene.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update()
        cache.append(({n:src.pose.bones[s].matrix.copy() for n,s in mapping.items()},floor(srcmesh,si)))
    rig.animation_data_create();baked=bpy.data.actions.new('Q_'+name.removesuffix('_Loop'));rig.animation_data.action=baked
    samples=[];floor_errors=[]
    for frame,(matrices,source_floor) in enumerate(cache):
        for p in rig.pose.bones:p.matrix_basis.identity()
        for bone in rig.data.bones:
            name_t=bone.name;p=rig.pose.bones[name_t]
            if bone.parent:
                head=rig.pose.bones[bone.parent.name].matrix@bone.parent.matrix_local.inverted()@bone.head_local
            else:head=bone.head_local.copy()
            if name_t=='pelvis':
                head=bone.head_local+(matrices[name_t].translation-src.data.bones['pelvis'].head_local)*scale
            q=matrices[name_t].to_quaternion()@correction[name_t]
            p.matrix=Matrix.Translation(head)@q.to_matrix().to_4x4()
            bpy.context.view_layer.update()
        # Match the source's lowest skinned foot height, preserving flight.
        wanted=max(0.,source_floor)*scale
        dz=wanted-floor(body,ti)
        root=rig.pose.bones['Root'];matrix=root.matrix.copy();matrix.translation.z+=dz;root.matrix=matrix
        bpy.context.view_layer.update()
        floor_errors.append(abs(floor(body,ti)-wanted))
        for p in rig.pose.bones:
            p.rotation_mode='QUATERNION'
            for prop in ['location','rotation_quaternion','scale']:p.keyframe_insert(prop,frame=frame+1)
        samples.append({'frame':frame+1,'speed':0.,'actual_feet':{s:list(rig.pose.bones['foot_'+s].head) for s in ['l','r']},
                        'source_foot_floor':source_floor,'target_foot_floor':floor(body,ti),'floor_adjustment':dz})
    assert max(floor_errors)<1e-5
    hand_travel={s:sum((cache[i][0]['hand_'+s].translation-cache[i-1][0]['hand_'+s].translation).length
                      for i in range(1,len(cache))) for s in ['l','r']}
    if name.startswith('Punch_'):
        side=max(hand_travel,key=hand_travel.get)
        label=('左手' if side=='l' else '右手')+label
    baked.use_fake_user=True;actions.append(baked)
    manifest['clips'].append({'name':baked.name,'source_clip':name,'label':label,'duration':frames/30,'loop':loop,'frames':frames+1,'samples':samples})
    checks.append({'clip':baked.name,'source_seconds':duration,'target_seconds':frames/30,'max_floor_error_m':max(floor_errors),'hand_travel_m':hand_travel})
    print('RETARGETED',baked.name,frames,max(floor_errors),flush=True)
for clip in legacy_clips:
    if clip['name'] not in legacy_names:continue
    clip['label']={'TurnLeft':'左转（旧版）','TurnRight':'右转（旧版）','HitLight':'轻受击退步（旧版）','HitHeavy':'重受击退步（旧版）'}[clip['name']]
    clip['source_clip']='Previous procedural draft'
    manifest['clips'].append(clip);actions.append(legacy_actions[clip['name']])
rig.animation_data.action=None
for a in actions:
    track=rig.animation_data.nla_tracks.new();track.name=a.name;track.strips.new(a.name,1,a);track.mute=True
rig.animation_data.action=actions[0];scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'body-actions.blend'))
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True)
rig.animation_data.action=None
for track in rig.animation_data.nla_tracks:track.mute=False
bpy.ops.export_scene.gltf(filepath=str(out/'body-actions.glb'),export_format='GLB',use_selection=True,
    export_animations=True,export_animation_mode='NLA_TRACKS',export_anim_slide_to_zero=True,export_morph=False)
for track in rig.animation_data.nla_tracks:track.mute=True
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.cycles.samples=20
scene.camera.data.ortho_scale=2.1
for a,clip in zip(actions,manifest['clips']):
    rig.animation_data.action=a;scene.frame_set(1+round(clip['duration']*30*.4))
    center=rig.pose.bones['pelvis'].head+Vector((0,0,-.04))
    scene.camera.location=center+Vector((3,-5,.5));scene.camera.rotation_euler=(center-scene.camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/(a.name+'.png'));bpy.ops.render.render(write_still=True)
for p,h in hashes.items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
(out/'actions.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
(out/'retarget-report.json').write_text(json.dumps({'task':'M5.2.9.6.8' if expanded else 'M5.2.9.6.6','source_hashes':hashes,'bone_map':mapping,'motion_scale':scale,'clips':checks,
    'limits':'Draft adaptation. Vertical foot-height compensation only, not horizontal foot locking or final collision clearance. Sword motion has no weapon prop. Jump phases are separate clips, not a physics-driven jump controller. Prior turn/hit drafts are retained when expanded.'},indent=2),encoding='utf8')
print('QUATERNIUS_PILOT_OK',flush=True)
