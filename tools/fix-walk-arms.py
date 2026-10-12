"""M5.2.9.6.11: natural hanging arms with checked lateral hand clearance.
Blender -b -P SCRIPT -- SHOULDER_CORRECTED_BLEND OUT
"""
import bpy, sys, json, math, hashlib
from pathlib import Path
from mathutils import Vector, Matrix, Quaternion

source,out=map(Path,sys.argv[sys.argv.index('--')+1:]);out.mkdir(parents=True,exist_ok=True)
digest=hashlib.sha256(source.read_bytes()).hexdigest()
manifest=json.loads((source.parent/'actions.json').read_text(encoding='utf8'))
bpy.ops.wm.open_mainfile(filepath=str(source))
rig=bpy.data.objects['StandardBodyRig'];body=bpy.data.objects['Standard_adult_body'];scene=bpy.context.scene
for track in rig.animation_data.nla_tracks:track.mute=True
action=bpy.data.actions['Q_Walk'];rig.animation_data.action=action
clip=next(c for c in manifest['clips'] if c['name']=='Q_Walk')
groups={g.index:g.name for g in body.vertex_groups}
hand_ids={s:[v.index for v in body.data.vertices if sum(g.weight for g in v.groups if groups[g.group].endswith('_'+s) and groups[g.group].split('_')[0] in ['hand','thumb','index','middle','ring','pinky'])>.5] for s in ['l','r']}
obstacle_ids=[v.index for v in body.data.vertices if sum(g.weight for g in v.groups if groups[g.group].split('_')[0] in ['pelvis','spine','thigh','calf'])>.6]
assert all(hand_ids.values()) and obstacle_ids
mean_y={s:sum(a['actual_feet'][s][1] for a in clip['samples'])/len(clip['samples']) for s in ['l','r']}

def solve(side,wrist):
    upper=rig.data.bones['upperarm_'+side];lower=rig.data.bones['lowerarm_'+side]
    shoulder=rig.pose.bones[upper.name].head.copy();delta=wrist-shoulder
    a,b=upper.length,lower.length;d=delta.length;axis=delta.normalized()
    assert abs(a-b)<d<a+b
    along=(a*a-b*b+d*d)/(2*d);height=math.sqrt(max(0.,a*a-along*along))
    preference=Vector((.15 if side=='l' else -.15,1,0))
    bend=(preference-axis*preference.dot(axis)).normalized()
    elbow=shoulder+axis*along+bend*height
    ru=(upper.tail_local-upper.head_local).normalized();rl=(lower.tail_local-lower.head_local).normalized()
    rn=ru.cross(rl).normalized();normal=(elbow-shoulder).cross(wrist-elbow).normalized()
    for bone,head,direction,rest_direction in [(upper,shoulder,elbow-shoulder,ru),(lower,elbow,wrist-elbow,rl)]:
        y=direction.normalized();desired=Matrix((normal,y,normal.cross(y))).transposed()
        rest=Matrix((rn,rest_direction,rn.cross(rest_direction))).transposed()
        q=(desired@rest.transposed()).to_quaternion()@bone.matrix_local.to_quaternion()
        rig.pose.bones[bone.name].matrix=Matrix.Translation(head)@q.to_matrix().to_4x4()
        bpy.context.view_layer.update()

def clearance(side):
    mesh=body.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
    points=[mesh.vertices[i].co for i in hand_ids[side]]
    lo=min(p.z for p in points)-.015;hi=max(p.z for p in points)+.015
    sign=1 if side=='l' else -1
    boundary=max(sign*mesh.vertices[i].co.x for i in obstacle_ids if lo<=mesh.vertices[i].co.z<=hi)
    return min(sign*p.x for p in points)-boundary

modified=[n for n in rig.pose.bones.keys() if n.split('_')[0] in ['upperarm','lowerarm','hand','thumb','index','middle','ring','pinky']]+['spine_01']
checks=[]
# Clear active animation while posing; otherwise dependency evaluation can restore keyed rotations.
cache=[]
for sample in clip['samples']:
    scene.frame_set(sample['frame']);cache.append({n:p.matrix_basis.copy() for n,p in rig.pose.bones.items()})
rig.animation_data.action=None
for sample,basis in zip(clip['samples'],cache):
    for n,matrix in basis.items():rig.pose.bones[n].matrix_basis=matrix
    for n in modified:
        if n.split('_')[0] in ['hand','thumb','index','middle','ring','pinky']:rig.pose.bones[n].matrix_basis.identity()
    bpy.context.view_layer.update()
    # Reduce sagittal torso lean while preserving pelvis/leg motion and yaw.
    for _ in range(3):
        axis=rig.pose.bones['neck_01'].head-rig.pose.bones['spine_01'].head
        pitch=math.atan2(-axis.y,axis.z)
        p=rig.pose.bones['spine_01'];matrix=p.matrix.copy()
        q=Quaternion((1,0,0),math.radians(2)-pitch)@matrix.to_quaternion()
        p.matrix=Matrix.Translation(matrix.translation)@q.to_matrix().to_4x4()
        bpy.context.view_layer.update()
    # Small distributed finger flexion, with the thumb brought slightly inward.
    for side in ['l','r']:
        for finger in ['index','middle','ring','pinky','thumb']:
            for segment,angle in [('01',12),('02',18),('03',10)]:
                name=f'{finger}_{segment}_{side}';p=rig.pose.bones[name];b=p.bone
                direction=(b.tail_local-b.head_local).normalized()
                curl_axis=direction.cross(Vector((0,-1,0))).normalized()
                local_axis=b.matrix_local.to_quaternion().inverted()@curl_axis
                p.rotation_quaternion=Quaternion(local_axis,math.radians(angle if finger!='thumb' else angle*.5))
        p=rig.pose.bones['thumb_01_'+side];b=p.bone
        direction=(b.tail_local-b.head_local).normalized()
        toward=(rig.data.bones['index_01_'+side].head_local-b.head_local).normalized()
        q=direction.rotation_difference(toward)
        local=b.matrix_local.to_quaternion()
        p.rotation_quaternion=(local.inverted()@Quaternion().slerp(q,.18)@local)@p.rotation_quaternion
    bpy.context.view_layer.update()
    gaps={};offsets={}
    for side,sign in [('l',1),('r',-1)]:
        shoulder=rig.pose.bones['upperarm_'+side].head.copy()
        length=rig.data.bones['upperarm_'+side].length+rig.data.bones['lowerarm_'+side].length
        swing=-(sample['actual_feet'][side][1]-mean_y[side])*.3-.01
        # Keep a constant clearance offset for this body, avoiding framewise
        # lateral stepping when a moving thigh changes the safety envelope.
        offset=.10
        for attempt in range(12):
            drop=math.sqrt((length*.955)**2-offset**2-swing**2)
            wrist=shoulder+Vector((sign*offset,swing,-drop))
            solve(side,wrist);gap=clearance(side)
            if gap>=.012:break
            offset+=.006
        assert gap>=.012,(sample['frame'],side,gap)
        gaps[side]=gap;offsets[side]=offset
    # Write upper limbs and the torso correction only into the walk action.
    rig.animation_data.action=action
    for n in modified:
        p=rig.pose.bones[n];p.rotation_mode='QUATERNION'
        for prop in ['location','rotation_quaternion','scale']:p.keyframe_insert(prop,frame=sample['frame'])
    rig.animation_data.action=None
    axis=rig.pose.bones['neck_01'].head-rig.pose.bones['spine_01'].head
    elbows={s:math.degrees((rig.pose.bones['upperarm_'+s].tail-rig.pose.bones['upperarm_'+s].head).angle(
        rig.pose.bones['lowerarm_'+s].tail-rig.pose.bones['lowerarm_'+s].head)) for s in ['l','r']}
    checks.append({'frame':sample['frame'],'hand_clearance_m':gaps,'wrist_lateral_offset_m':offsets,
                   'torso_pitch_degrees':math.degrees(math.atan2(-axis.y,axis.z)),'elbow_flexion_degrees':elbows})
rig.animation_data.action=action
max_foot_error=0.
for sample in clip['samples']:
    scene.frame_set(sample['frame'])
    for side in ['l','r']:
        max_foot_error=max(max_foot_error,(rig.pose.bones['foot_'+side].head-Vector(sample['actual_feet'][side])).length)
        assert clearance(side)>=.011
assert max_foot_error<.002
assert all(abs(c['torso_pitch_degrees']-2)<.1 for c in checks)
assert all(30<v<40 for c in checks for v in c['elbow_flexion_degrees'].values())
clip['arm_correction']={'style':'hanging arms, bent elbows, opposite-leg swing, softly curled fingers, upright torso',
                        'min_lateral_hand_clearance_m':min(v for c in checks for v in c['hand_clearance_m'].values())}
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'body-actions.blend'))
rig.animation_data.action=None
for track in rig.animation_data.nla_tracks:track.mute=False
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(out/'body-actions.glb'),export_format='GLB',use_selection=True,
    export_animations=True,export_animation_mode='NLA_TRACKS',export_anim_slide_to_zero=True,export_morph=False)
assert hashlib.sha256(source.read_bytes()).hexdigest()==digest
(out/'actions.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
(out/'arm-verification.json').write_text(json.dumps({'task':'M5.2.9.6.11','source_sha256':digest,
    'max_foot_error_m':max_foot_error,'frames':checks,'limits':'Lateral clearance of weighted hand vertices from torso/leg envelope, not whole-body triangle collision.'},indent=2),encoding='utf8')
print('WALK_ARMS_OK',flush=True)
