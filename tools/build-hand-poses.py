"""M5.2.9.6.12: two reusable finger poses and relaxed-hand walk.
Blender -b -P SCRIPT -- CURRENT_BODY_BLEND OUT
"""
import bpy,sys,json,math,hashlib
from pathlib import Path
from mathutils import Vector,Quaternion,Matrix

source,out=map(Path,sys.argv[sys.argv.index('--')+1:])
if out.exists() and any(out.iterdir()):
    raise RuntimeError('Use a new empty output directory; preserve previous candidates')
out.mkdir(parents=True,exist_ok=True)
digest=hashlib.sha256(source.read_bytes()).hexdigest()
manifest=json.loads((source.parent/'actions.json').read_text(encoding='utf8'))
bpy.ops.wm.open_mainfile(filepath=str(source))
rig=bpy.data.objects['StandardBodyRig'];body=bpy.data.objects['Standard_adult_body'];scene=bpy.context.scene
for track in rig.animation_data.nla_tracks:track.mute=True
rig.animation_data.action=bpy.data.actions['Q_Idle'];scene.frame_set(1)
base={n:p.matrix_basis.copy() for n,p in rig.pose.bones.items()}
presets={
 'Relaxed':{'index':[12,22,12],'middle':[16,26,14],'ring':[20,30,16],'pinky':[24,34,18],'thumb':[8,12,8]}}
poses={}
for name,angles in presets.items():
    pose={}
    for side in ['l','r']:
        across=rig.data.bones['pinky_01_'+side].head_local-rig.data.bones['index_01_'+side].head_local
        middle=rig.data.bones['middle_01_'+side]
        palm=across.cross(middle.tail_local-middle.head_local).normalized()*(1 if side=='l' else -1)
        for finger,values in angles.items():
            for i,angle in enumerate(values,1):
                n=f'{finger}_{i:02d}_{side}';bone=rig.data.bones[n]
                direction=(bone.tail_local-bone.head_local).normalized();rest=bone.matrix_local.to_quaternion()
                axis=rest.inverted()@direction.cross(palm).normalized()
                q=Quaternion(axis,math.radians(angle))
                if i==1:
                    if finger=='thumb':
                        toward=(rig.data.bones['index_01_'+side].head_local-bone.head_local).normalized();amount=.2
                    else:
                        mid=rig.data.bones['middle_01_'+side];toward=(mid.tail_local-mid.head_local).normalized();amount=.35
                    spread=Quaternion().slerp(direction.rotation_difference(toward),amount)
                    q=(rest.inverted()@spread@rest)@q
                pose[n]=q
    poses[name]=pose

# Reuse the established sword grip, including thumb opposition and joint flexion.
# Mirror anatomical rest-space rotations, not quaternion components or Euler signs.
rig.animation_data.action=bpy.data.actions['Q_Sword_Attack'];scene.frame_set(1)
mirror=Matrix.Diagonal((-1.,1.,1.));fist={}
for n in poses['Relaxed']:
    if not n.endswith('_r'):continue
    q=rig.pose.bones[n].rotation_quaternion.copy();fist[n]=q
    left=n[:-1]+'l'
    rr=rig.data.bones[n].matrix_local.to_3x3();rl=rig.data.bones[left].matrix_local.to_3x3()
    delta=rr@q.to_matrix()@rr.inverted()
    fist[left]=(rl.inverted()@mirror@delta@mirror@rl).to_quaternion()
poses['Fist']=fist

def apply(pose):
    for n,q in pose.items():
        p=rig.pose.bones[n];p.rotation_mode='QUATERNION';p.rotation_quaternion=q

# Finger-only assets: reusable independently of body motion.
rig.animation_data.action=None
for name,pose in poses.items():
    a=bpy.data.actions.new('HandPose_'+name);rig.animation_data.action=a
    apply(pose)
    for n in pose:rig.pose.bones[n].keyframe_insert('rotation_quaternion',frame=1)
    a.use_fake_user=True;a.asset_mark()
    a.asset_data.description='Finger-only '+name+' pose for the current standard body; both hands.'
    rig.animation_data.action=None

walk=bpy.data.actions['Q_Walk'];rig.animation_data.action=walk
walkclip=next(c for c in manifest['clips'] if c['name']=='Q_Walk')
for sample in walkclip['samples']:
    apply(poses['Relaxed'])
    for n in poses['Relaxed']:rig.pose.bones[n].keyframe_insert('rotation_quaternion',frame=sample['frame'])
walkclip['hand_pose']='HandPose_Relaxed'
reviews=[]
for name,pose in poses.items():
    rig.animation_data.action=None
    for n,m in base.items():rig.pose.bones[n].matrix_basis=m
    apply(pose);bpy.context.view_layer.update()
    a=bpy.data.actions.new('HandReview_'+name);rig.animation_data.action=a
    for frame in [1,31]:
        for p in rig.pose.bones:
            p.rotation_mode='QUATERNION'
            for prop in ['location','rotation_quaternion','scale']:p.keyframe_insert(prop,frame=frame)
    samples=[{'frame':i,'speed':0.,'actual_feet':{s:list(rig.pose.bones['foot_'+s].head) for s in ['l','r']}} for i in range(1,32)]
    manifest['clips'].append({'name':a.name,'label':'自然放松手（近景）' if name=='Relaxed' else '握拳手（近景）',
        'duration':1.,'loop':True,'frames':31,'samples':samples,'hand_view':True})
    a.use_fake_user=True;reviews.append(a)
rig.animation_data.action=None
for a in reviews:
    tr=rig.animation_data.nla_tracks.new();tr.name=a.name;tr.strips.new(a.name,1,a);tr.mute=True
rig.animation_data.action=walk;scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'body-actions.blend'))
rig.animation_data.action=None
for tr in rig.animation_data.nla_tracks:tr.mute=False
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(out/'body-actions.glb'),export_format='GLB',use_selection=True,
 export_animations=True,export_animation_mode='NLA_TRACKS',export_anim_slide_to_zero=True,export_morph=False)
(out/'actions.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
(out/'hand-poses.json').write_text(json.dumps({'rig':'StandardBodyRig','space':'bone local quaternion wxyz','fist_reference':{'action':'Q_Sword_Attack','frame':1,'side':'r','left':'mirrored rest-space rotations'},'poses':{n:{b:list(q) for b,q in pose.items()} for n,pose in poses.items()}},indent=2),encoding='utf8')
assert hashlib.sha256(source.read_bytes()).hexdigest()==digest
(out/'hand-build.json').write_text(json.dumps({'task':'M5.2.9.6.12','source_sha256':digest,'finger_bones_per_pose':len(poses['Relaxed']),
 'walk_pose':'Relaxed','review_clips':[a.name for a in reviews],'visual_review':'pending orbit inspection'},indent=2),encoding='utf8')
print('HAND_POSES_BUILT',flush=True)
