"""Bounded Ivara-only rig trial, not a generic autorigger. Blender -b -t 4 -P ... -- INPUT OUTPUT."""
import bpy, bmesh, sys, json, math, hashlib
from pathlib import Path
from mathutils import Vector

source, out = map(Path, sys.argv[sys.argv.index('--')+1:])
out.mkdir(parents=True, exist_ok=True)
if (out/'trial.blend').exists(): raise RuntimeError('Use a fresh output directory')
digest = hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(source))
obj = next(o for o in bpy.context.scene.objects if o.type == 'MESH')
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
report = {'source_sha256': digest, 'purpose': 'Decimation and automatic-weight stress test; not production retopology or a finished walk.'}
bm = bmesh.new(); bm.from_mesh(obj.data)
bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=0.000001)
report['welded_vertices'] = len(bm.verts)
report['boundary_edges_after_weld'] = sum(e.is_boundary for e in bm.edges)
report['nonmanifold_edges_after_weld'] = sum(not e.is_manifold for e in bm.edges)
bm.to_mesh(obj.data); bm.free()
print('WELDED', report, flush=True)
dec = obj.modifiers.new('Trial reduction 60k triangles', 'DECIMATE')
dec.ratio = 60000 / len(obj.data.polygons)
bpy.ops.object.modifier_apply(modifier=dec.name)
obj.data.calc_loop_triangles()
report['reduced_triangles'] = len(obj.data.loop_triangles)
print('REDUCED', report['reduced_triangles'], flush=True)
obj.name = 'Ivara_trial_mesh'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.armature_add()
rig = bpy.context.object; rig.name = 'Ivara_trial_rig'
bpy.ops.object.mode_set(mode='EDIT')
for bone in list(rig.data.edit_bones): rig.data.edit_bones.remove(bone)
def bone(name, head, tail, parent=None):
    b = rig.data.edit_bones.new(name); b.head=head; b.tail=tail
    if parent: b.parent=rig.data.edit_bones[parent]
bone('pelvis',(0,0,.46),(0,0,.54))
bone('spine',(0,0,.54),(0,0,.64),'pelvis')
bone('chest',(0,0,.64),(0,0,.73),'spine')
bone('neck',(0,0,.73),(0,0,.78),'chest')
bone('head',(0,0,.78),(0,0,.90),'neck')
for side, sign in [('L',1),('R',-1)]:
    bone('upper_arm.'+side,(sign*.088,0,.725),(sign*.120,0,.595),'chest')
    bone('forearm.'+side,(sign*.120,0,.595),(sign*.126,-.008,.478),'upper_arm.'+side)
    bone('hand.'+side,(sign*.126,-.008,.478),(sign*.129,-.012,.425),'forearm.'+side)
    bone('thigh.'+side,(sign*.051,0,.48),(sign*.063,-.009,.275),'pelvis')
    bone('shin.'+side,(sign*.063,-.009,.275),(sign*.070,0,.070),'thigh.'+side)
    bone('foot.'+side,(sign*.070,0,.070),(sign*.070,-.065,.035),'shin.'+side)
# Approximate tail chain: a trial landmark placement, requiring visual review.
bone('tail_base',(0,.05,.49),(.065,.105,.40),'pelvis')
bone('tail_mid',(.065,.105,.40),(.185,.11,.40),'tail_base')
bone('tail_tip',(.185,.11,.40),(.16,.09,.51),'tail_mid')
bpy.ops.object.mode_set(mode='OBJECT')
obj.select_set(True); rig.select_set(True); bpy.context.view_layer.objects.active=rig
print('AUTO_WEIGHTS_START',flush=True)
bpy.ops.object.parent_set(type='ARMATURE_AUTO')
report['unweighted_vertices'] = sum(not any(g.weight>0 for g in v.groups) for v in obj.data.vertices)
report['bones'] = len(rig.data.bones)
print('AUTO_WEIGHTS_END',report,flush=True)
scene=bpy.context.scene
scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=16; scene.cycles.use_denoising=True
scene.render.resolution_x=640; scene.render.resolution_y=800; scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Inspection world'); scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.55,.55,.55,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.7
scene.view_settings.view_transform='Standard'
bpy.ops.object.camera_add(location=(0,-3,.52)); cam=bpy.context.object; scene.camera=cam
cam.data.type='ORTHO'; cam.data.ortho_scale=1.13
cam.rotation_euler=(Vector((0,0,.49))-cam.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.light_add(type='AREA',location=(0,-2,2.5)); light=bpy.context.object
light.data.energy=100; light.data.size=3
light.rotation_euler=(Vector((0,0,.49))-light.location).to_track_quat('-Z','Y').to_euler()
for p in rig.pose.bones: p.rotation_mode='XYZ'; p.rotation_euler=(0,0,0); p.keyframe_insert('rotation_euler',frame=1)
scene.render.filepath=str(out/'reduced-rest.png'); bpy.ops.render.render(write_still=True)
for name,degrees in [('thigh.L',-25),('shin.L',35),('upper_arm.R',-25),('forearm.R',25),('upper_arm.L',20)]:
    rig.pose.bones[name].rotation_euler.x=math.radians(degrees)
for p in rig.pose.bones: p.keyframe_insert('rotation_euler',frame=16)
for p in rig.pose.bones: p.rotation_euler=(0,0,0); p.keyframe_insert('rotation_euler',frame=32)
scene.frame_end=32; scene.render.fps=24
rig.animation_data.action.name='Deformation_Test_NOT_Walk'
scene.frame_set(16)
scene.render.filepath=str(out/'stress-front.png'); bpy.ops.render.render(write_still=True)
cam.location=(2,-2,.55); cam.rotation_euler=(Vector((0,0,.49))-cam.location).to_track_quat('-Z','Y').to_euler()
scene.render.filepath=str(out/'stress-oblique.png'); bpy.ops.render.render(write_still=True)
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'trial.blend'))
bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True); rig.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(out/'trial.glb'),use_selection=True,export_animations=True)
report['source_unchanged']=hashlib.sha256(source.read_bytes()).hexdigest()==digest
assert report['source_unchanged']
(out/'trial.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('TRIAL_COMPLETE',flush=True)
