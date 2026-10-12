"""M5.2.9.6.9: replace only the heavy-hit clip with a two-step lateral stagger.
Blender -b -P SCRIPT -- EXPANDED_BODY_BLEND OUT
Preserves source meshes, weights and every other animation; outputs a new copy.
"""
import bpy
import sys
import json
import math
import hashlib
from pathlib import Path
from mathutils import Vector, Quaternion, Matrix

source, out = map(Path, sys.argv[sys.argv.index('--') + 1:])
out.mkdir(parents=True, exist_ok=True)
source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
manifest = json.loads((source.parent / 'actions.json').read_text(encoding='utf8'))
bpy.ops.wm.open_mainfile(filepath=str(source))
rig = bpy.data.objects['StandardBodyRig']
body = bpy.data.objects['Standard_adult_body']
scene = bpy.context.scene
scene.render.fps = 30
retained = {c['name']: bpy.data.actions[c['name']] for c in manifest['clips'] if c['name'] != 'HitHeavy'}
rig.animation_data_clear()
rig.animation_data_create()
action = bpy.data.actions.new('HitHeavy_Stagger2')
rig.animation_data.action = action
ankles = {s: rig.data.bones['foot_' + s].head_local.copy() for s in ['l', 'r']}


def smooth(x):
    x = max(0., min(1., x))
    return x * x * (3 - 2 * x)


def curve(t, points):
    for (a, x), (b, y) in zip(points, points[1:]):
        if t <= b:
            return x + (y - x) * smooth((t - a) / (b - a))
    return points[-1][1]


def rotate(name, axis, degrees, add=False):
    p = rig.pose.bones[name]
    q = Quaternion(p.bone.matrix_local.to_quaternion().inverted() @ Vector(axis), math.radians(degrees))
    p.rotation_quaternion = q @ p.rotation_quaternion if add else q


def move(name, delta):
    p = rig.pose.bones[name]
    p.location = p.bone.matrix_local.to_3x3().inverted() @ Vector(delta)


def orient(name, head, direction):
    bone = rig.data.bones[name]
    rest = bone.matrix_local.to_quaternion()
    q = (rest @ Vector((0, 1, 0))).rotation_difference(direction.normalized()) @ rest
    rig.pose.bones[name].matrix = Matrix.Translation(head) @ q.to_matrix().to_4x4()
    bpy.context.view_layer.update()


def leg(side, target):
    hip = rig.pose.bones['thigh_' + side].head.copy()
    a = rig.data.bones['thigh_' + side].length
    b = rig.data.bones['calf_' + side].length
    delta = target - hip
    d = max(abs(a-b)+1e-5, min(delta.length, a+b-1e-5))
    axis = delta.normalized()
    along = (a*a-b*b+d*d)/(2*d)
    bend = Vector((0, -1, 0))
    bend = (bend-axis*bend.dot(axis)).normalized()
    knee = hip + axis*along + bend*math.sqrt(max(0., a*a-along*along))
    end = hip + axis*d
    orient('thigh_' + side, hip, knee-hip)
    orient('calf_' + side, knee, end-knee)
    rig.pose.bones['foot_' + side].matrix = Matrix.Translation(end) @ rig.data.bones['foot_' + side].matrix_local.to_quaternion().to_matrix().to_4x4()
    bpy.context.view_layer.update()
    return abs(delta.length-d)


samples = []
duration = 1.9
steps = [('l', .23, .69, .30, .14), ('r', .77, 1.23, .52, .14)]
for frame in range(round(duration*30)+1):
    t = frame/30
    for p in rig.pose.bones:
        p.matrix_basis.identity()
        p.rotation_mode = 'QUATERNION'
    tilt = curve(t, [(0, 0), (.16, 1), (.46, .9), (.78, .72), (1.12, .45), (1.5, -.12), (1.9, 0)])
    recoil = curve(t, [(0, 0), (.12, 1), (.36, .75), (.8, .4), (1.4, 0), (1.9, 0)])
    compression = curve(t, [(0, 0), (.18, 1), (.50, .85), (.70, 1),
                            (.90, .72), (1.23, .8), (1.65, .18), (1.9, 0)])
    feet = {s: Vector((p.x*.78, p.y, p.z)) for s, p in ankles.items()}
    contact = {s: True for s in ankles}
    for side, start, end, backward, lateral in steps:
        phase = max(0., min(1., (t-start)/(end-start)))
        feet[side].y += backward*smooth(phase)
        feet[side].x += lateral*smooth(phase)
        feet[side].z += .075*math.sin(math.pi*phase)**1.5
        contact[side] = not start < t < end
    root = Vector((curve(t, [(0, 0), (.18, .055), (.65, .085), (1.23, .14), (1.9, .14)]),
                   sum(feet[s].y-ankles[s].y for s in ankles)/2, 0))
    move('Root', root)
    # Sit the hips back and down; grounded ankle targets then produce deeper
    # hip/knee flexion without pushing the feet through the floor.
    pelvis_drop = .035 + .12*compression
    move('pelvis', (0, .025*compression, -pelvis_drop))
    for name, lateral, backward in [('spine_01', 7, 4), ('spine_02', 13, 9), ('spine_03', 8, 3)]:
        rotate(name, (0, 1, 0), lateral*tilt)
        rotate(name, (1, 0, 0), -backward*recoil, True)
    rotate('head', (0, 1, 0), -5*tilt)
    for side, sign in [('l', 1), ('r', -1)]:
        # Open the arms asymmetrically to catch balance, then settle.
        rotate('upperarm_'+side, (0, 1, 0), sign*(32-(27 if side=='l' else 18)*max(tilt, 0)))
        rotate('upperarm_'+side, (1, 0, 0), (-24 if side=='l' else 12)*recoil, True)
        rotate('lowerarm_'+side, (1, 0, 0), 25-35*max(tilt, 0))
    bpy.context.view_layer.update()
    reach = max(leg(s, feet[s]) for s in ankles)
    knee_flexion = {s: math.degrees((rig.pose.bones['thigh_'+s].tail-rig.pose.bones['thigh_'+s].head).angle(
        rig.pose.bones['calf_'+s].tail-rig.pose.bones['calf_'+s].head)) for s in ankles}
    axis = rig.pose.bones['head'].head-rig.pose.bones['spine_01'].head
    lateral_angle = math.degrees(math.atan2(axis.x, axis.z))
    for p in rig.pose.bones:
        for prop in ['location', 'rotation_quaternion', 'scale']:
            p.keyframe_insert(prop, frame=frame+1)
    samples.append({'frame': frame+1, 'speed': 0., 'root': list(root), 'contact': contact,
                    'targets': {s:list(v) for s,v in feet.items()}, 'reach_error':reach,
                    'lateral_torso_degrees': lateral_angle,
                    'pelvis_drop_m': pelvis_drop, 'knee_flexion_degrees': knee_flexion,
                    'actual_feet': {s:list(rig.pose.bones['foot_'+s].head) for s in ankles}})

lifts = {s:sum(not a['contact'][s] and (i==0 or samples[i-1]['contact'][s]) for i,a in enumerate(samples)) for s in ankles}
assert lifts == {'l':1, 'r':1}, lifts
assert max(a['reach_error'] for a in samples)<.002
assert max(a['lateral_torso_degrees'] for a in samples)>15
contact_drift = max((Vector(a['actual_feet'][s])-Vector(samples[i-1]['actual_feet'][s])).length
                    for i,a in enumerate(samples) if i>0 for s in ankles if a['contact'][s] and samples[i-1]['contact'][s])
assert contact_drift<.002, contact_drift
action.use_fake_user=True
replacement={'name':action.name,'label':'重受击：侧倾后退两步','duration':duration,'loop':False,
             'frames':len(samples),'source_clip':'Authored two-step lateral stagger','root_motion':True,'samples':samples}
manifest['clips']=[replacement if c['name']=='HitHeavy' else c for c in manifest['clips']]
assert len(manifest['clips'])==14
manifest['source']='Quaternius CC0 + retained procedural turns/light hit + authored heavy stagger'
retained[action.name]=action
rig.animation_data.action=None
for clip in manifest['clips']:
    a=retained[clip['name']]
    track=rig.animation_data.nla_tracks.new()
    track.name=a.name
    track.strips.new(a.name,1,a)
    track.mute=True
rig.animation_data.action=action
scene.frame_set(7)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'body-actions.blend'))
rig.animation_data.action=None
for track in rig.animation_data.nla_tracks:track.mute=False
bpy.ops.object.select_all(action='DESELECT')
body.select_set(True)
rig.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(out/'body-actions.glb'),export_format='GLB',use_selection=True,
    export_animations=True,export_animation_mode='NLA_TRACKS',export_anim_slide_to_zero=True,export_morph=False)
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
(out/'actions.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
(out/'stagger-verification.json').write_text(json.dumps({'task':'M5.2.9.6.9','source_sha256':source_hash,
    'lifts':lifts,'contact_drift_m':contact_drift,'max_reach_error_m':max(a['reach_error'] for a in samples),
    'peak_lateral_torso_degrees':max(a['lateral_torso_degrees'] for a in samples),
    'peak_pelvis_drop_m':max(a['pelvis_drop_m'] for a in samples),
    'peak_knee_flexion_degrees':{s:max(a['knee_flexion_degrees'][s] for a in samples) for s in ankles},
    'root_end':samples[-1]['root'],'duration':duration},indent=2),encoding='utf8')
print('HEAVY_STAGGER_OK',flush=True)
