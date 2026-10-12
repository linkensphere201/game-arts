"""Verify hand-pose isolation and walk clearance in Blender.
Usage: blender -b --python-exit-code 1 -P SCRIPT -- SOURCE_BLEND RESULT_BLEND
"""
import bpy, sys, json, hashlib
from pathlib import Path

source, result = map(Path, sys.argv[sys.argv.index('--')+1:])
clips = json.loads((source.parent/'actions.json').read_text())['clips']
poses = json.loads((result.parent/'hand-poses.json').read_text())['poses']
fingers = set(poses['Relaxed'])
assert len(fingers) == 30 and fingers == set(poses['Fist'])

def load(path):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    rig = bpy.data.objects['StandardBodyRig']
    for track in rig.animation_data.nla_tracks: track.mute = True
    return rig, bpy.data.objects['Standard_adult_body']

def geometry(body):
    data = [(tuple(v.co), [(g.group, g.weight) for g in v.groups]) for v in body.data.vertices]
    data += [tuple(p.vertices) for p in body.data.polygons]
    return hashlib.sha256(repr(data).encode()).hexdigest()

def sample(rig):
    values = {}
    for clip in clips:
        rig.animation_data.action = bpy.data.actions[clip['name']]
        for row in clip['samples']:
            bpy.context.scene.frame_set(row['frame'])
            for name, bone in rig.pose.bones.items():
                if clip['name'] == 'Q_Walk' and name in fingers: continue
                values[(clip['name'], row['frame'], name)] = tuple(x for r in bone.matrix for x in r)
    return values

rig, body = load(source)
before, mesh_hash = sample(rig), geometry(body)
rig.animation_data.action = bpy.data.actions['Q_Sword_Attack']
bpy.context.scene.frame_set(1)
for name,q in poses['Fist'].items():
    if name.endswith('_r'):
        assert max(abs(a-b) for a,b in zip(rig.pose.bones[name].rotation_quaternion,q)) < 1e-6
rig, body = load(result)
after = sample(rig)
assert geometry(body) == mesh_hash, 'Base mesh or weights changed'
error = max(abs(a-b) for key in before for a,b in zip(before[key],after[key]))
assert error < 1e-5, error
groups = {g.index:g.name for g in body.vertex_groups}
hand_ids = {s:[v.index for v in body.data.vertices if sum(g.weight for g in v.groups if groups[g.group].endswith('_'+s) and groups[g.group].split('_')[0] in ['hand','thumb','index','middle','ring','pinky']) > .5] for s in ['l','r']}
obstacles = [v.index for v in body.data.vertices if sum(g.weight for g in v.groups if groups[g.group].split('_')[0] in ['pelvis','spine','thigh','calf']) > .6]
rig.animation_data.action = bpy.data.actions['Q_Walk']
gaps = []
for row in next(c for c in clips if c['name']=='Q_Walk')['samples']:
    bpy.context.scene.frame_set(row['frame'])
    for name,q in poses['Relaxed'].items():
        assert max(abs(a-b) for a,b in zip(rig.pose.bones[name].rotation_quaternion,q)) < 1e-5
    mesh = body.evaluated_get(bpy.context.evaluated_depsgraph_get()).data
    for side,sign in [('l',1),('r',-1)]:
        points = [mesh.vertices[i].co for i in hand_ids[side]]
        lo,hi = min(p.z for p in points)-.015,max(p.z for p in points)+.015
        edge = max(sign*mesh.vertices[i].co.x for i in obstacles if lo <= mesh.vertices[i].co.z <= hi)
        gaps.append(min(sign*p.x for p in points)-edge)
assert min(gaps) > .01, min(gaps)
for label,pose in poses.items():
    rig.animation_data.action = bpy.data.actions['HandReview_'+label]
    bpy.context.scene.frame_set(1)
    for name,q in pose.items():
        assert max(abs(a-b) for a,b in zip(rig.pose.bones[name].rotation_quaternion,q)) < 1e-5
report = {'unchanged_matrix_max_error':error,'mesh_weights_unchanged':True,'finger_bones':30,
          'fist_matches_sword_right_hand':True,'review_poses_match_library':True,
          'min_walk_lateral_gap_m':min(gaps),'limitation':'Lateral envelope test, not complete triangle collision testing'}
(result.parent/'hand-verification.json').write_text(json.dumps(report,indent=2))
print('HAND_VERIFICATION_OK',report)
