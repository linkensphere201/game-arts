"""M5.2.9.6.10: relax retargeted walk clavicles, keeping all other clips.
Blender -b -P SCRIPT -- CURRENT_BODY_BLEND OUT
"""
import bpy
import sys
import json
import hashlib
from pathlib import Path
from mathutils import Quaternion, Vector

source,out=map(Path,sys.argv[sys.argv.index('--')+1:])
out.mkdir(parents=True,exist_ok=True)
digest=hashlib.sha256(source.read_bytes()).hexdigest()
manifest=json.loads((source.parent/'actions.json').read_text(encoding='utf8'))
bpy.ops.wm.open_mainfile(filepath=str(source))
rig=bpy.data.objects['StandardBodyRig'];body=bpy.data.objects['Standard_adult_body'];scene=bpy.context.scene
for track in rig.animation_data.nla_tracks:track.mute=True
action=bpy.data.actions['Q_Walk'];rig.animation_data.action=action
clip=next(c for c in manifest['clips'] if c['name']=='Q_Walk')
names=['clavicle_l','clavicle_r']
cache=[]
for sample in clip['samples']:
    scene.frame_set(sample['frame'])
    cache.append({n:rig.pose.bones[n].rotation_quaternion.copy() for n in names})
for sample,original in zip(clip['samples'],cache):
    for n in names:
        p=rig.pose.bones[n]
        p.rotation_quaternion=Quaternion().slerp(original[n],.2)
        p.keyframe_insert('rotation_quaternion',frame=sample['frame'])
max_error=0.
for sample in clip['samples']:
    scene.frame_set(sample['frame'])
    for side in ['l','r']:
        max_error=max(max_error,(rig.pose.bones['foot_'+side].head-Vector(sample['actual_feet'][side])).length)
assert max_error<.002,max_error
clip['shoulder_correction']={'clavicle_rotation_scale':.2,'scope':'walk only; no weight or mesh edits'}
scene.frame_set(11)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'body-actions.blend'))
scene.render.resolution_x=700;scene.render.resolution_y=650;scene.render.resolution_percentage=100;scene.cycles.samples=16
scene.camera.data.ortho_scale=.9;center=Vector((0,0,1.22))
for name,offset in [('back',(2,4,.2)),('side',(4,0,.2))]:
    scene.camera.location=center+Vector(offset)
    scene.camera.rotation_euler=(center-scene.camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/('shoulder-'+name+'.png'));bpy.ops.render.render(write_still=True)
rig.animation_data.action=None
for track in rig.animation_data.nla_tracks:track.mute=False
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);rig.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(out/'body-actions.glb'),export_format='GLB',use_selection=True,
    export_animations=True,export_animation_mode='NLA_TRACKS',export_anim_slide_to_zero=True,export_morph=False)
assert hashlib.sha256(source.read_bytes()).hexdigest()==digest
(out/'actions.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
(out/'shoulder-verification.json').write_text(json.dumps({'task':'M5.2.9.6.10','source_sha256':digest,
    'changed_clip':'Q_Walk','changed_bones':names,'rotation_scale':.2,'max_ankle_difference_m':max_error},indent=2),encoding='utf8')
print('WALK_SHOULDER_FIX_OK',flush=True)
