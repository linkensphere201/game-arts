"""M5.2.9.5: bind the accepted bare body and inspect static joint poses only.

Blender -b -P SCRIPT -- MPFB_ROOT BODY_BLEND OUTPUT_DIR
"""
import sys, json, math
from pathlib import Path
import bpy, addon_utils
from mathutils import Vector, Quaternion
from bpy_extras.object_utils import world_to_camera_view

root, source, out = map(Path, sys.argv[sys.argv.index('--') + 1:])
out.mkdir(parents=True, exist_ok=True)
src = root / 'source/mpfb2-d0a32e57a7f915cb2f2b95410e2117648c7bbb7e/src'
bpy.context.preferences.extensions.repos.new(name='MPFB pilot local', module='mpfb_pilot', custom_directory=str(src))
addon_utils.enable('bl_ext.mpfb_pilot.mpfb', default_set=True)
from bl_ext.mpfb_pilot.mpfb.services.humanservice import HumanService

bpy.ops.wm.open_mainfile(filepath=str(source))
body = bpy.data.objects['Standard_adult_body']
rig = HumanService.add_builtin_rig(body, 'game_engine', import_weights=True)
rig.name = 'StandardBodyRig'
rig.show_in_front = True
rig.data.display_type = 'OCTAHEDRAL'
for modifier in body.modifiers:
    if modifier.type == 'ARMATURE':
        modifier.use_deform_preserve_volume = True
scene = bpy.context.scene
scene.render.resolution_x = 800
scene.render.resolution_y = 800
center = Vector((0, 0, .79))
camera = scene.camera
camera.data.ortho_scale = 2.05
camera.location = (0, -5, .79)
camera.rotation_euler = (center-camera.location).to_track_quat('-Z', 'Y').to_euler()

deform = {b.name for b in rig.data.bones if b.use_deform}
groups = {g.index:g.name for g in body.vertex_groups}
visible_group = body.vertex_groups['body'].index
visible = [v for v in body.data.vertices if any(g.group == visible_group and g.weight > .5 for g in v.groups)]
sums = [sum(g.weight for g in v.groups if groups[g.group] in deform) for v in visible]
report = {'source': str(source), 'bone_count':len(rig.data.bones),
          'visible_vertices':len(visible), 'unweighted_visible':sum(s < 1e-6 for s in sums),
          'weight_sum_min':min(sums), 'weight_sum_max':max(sums),
          'preserve_volume':True, 'poses':[]}
assert report['unweighted_visible'] == 0, report

def reset():
    for bone in rig.pose.bones:
        bone.rotation_mode = 'QUATERNION'
        bone.rotation_quaternion = (1,0,0,0)
        bone.location = (0,0,0)
        bone.scale = (1,1,1)

def turn(name, axis, degrees):
    bone = rig.pose.bones[name]
    local_axis = bone.bone.matrix_local.to_quaternion().inverted() @ Vector(axis)
    bone.rotation_quaternion = Quaternion(local_axis, math.radians(degrees))

poses = [
    ('01-neutral',1,[]),
    ('02-shoulders',10,[('upperarm_l',(0,1,0),-65),('upperarm_r',(0,1,0),65)]),
    ('03-elbows',20,[('lowerarm_l',(1,0,0),-65),('lowerarm_r',(1,0,0),-65)]),
    ('04-hip-knee',30,[('thigh_l',(1,0,0),-55),('calf_l',(1,0,0),90)]),
    ('05-wrist-ankle',40,[('hand_l',(1,0,0),25),('hand_r',(1,0,0),-25),('foot_l',(1,0,0),20)]),
]
neutral_feet = {}
for name, frame, rotations in poses:
    reset()
    for rotation in rotations: turn(*rotation)
    for bone in rig.pose.bones:
        bone.keyframe_insert('rotation_quaternion',frame=frame)
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    feet = {side:list(rig.pose.bones['foot_'+side].head) for side in ['l','r']}
    if not neutral_feet: neutral_feet = feet
    if name in ['02-shoulders','03-elbows']:
        assert max((Vector(feet[s])-Vector(neutral_feet[s])).length for s in feet) < 1e-6
    projection = []
    for bone in rig.pose.bones:
        if any(t in bone.name for t in ['index','middle','pinky','ring','thumb','Root']): continue
        a = world_to_camera_view(scene,camera,rig.matrix_world@bone.head)
        b = world_to_camera_view(scene,camera,rig.matrix_world@bone.tail)
        projection.append({'bone':bone.name,'head':[a.x,1-a.y],'tail':[b.x,1-b.y]})
    report['poses'].append({'name':name,'frame':frame,'rotations':rotations,'feet':feet,'projected_bones':projection})
    scene.render.filepath = str(out/(name+'.png'))
    bpy.ops.render.render(write_still=True)
    if name in ['03-elbows','04-hip-knee']:
        camera.location = (4,-3,.79)
        camera.rotation_euler = (center-camera.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath = str(out/(name+'-side.png'))
        bpy.ops.render.render(write_still=True)
        camera.location = (0,-5,.79)
        camera.rotation_euler = (center-camera.location).to_track_quat('-Z','Y').to_euler()

rig.animation_data.action.name = 'Joint_checks_NOT_a_walk'
scene.frame_start = 1
scene.frame_end = 40
scene.frame_set(1)
bpy.ops.object.select_all(action='DESELECT')
rig.select_set(True)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode='POSE')
bpy.ops.wm.save_as_mainfile(filepath=str(out/'standard-body-rig-review.blend'))
(out/'binding-report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('BODY_RIG_REVIEW_OK',json.dumps({k:v for k,v in report.items() if k != 'poses'}),flush=True)
