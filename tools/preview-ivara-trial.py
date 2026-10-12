"""Render exported trial GLB, verifying skin/action survival after round trip."""
import bpy, sys, json
from pathlib import Path
from mathutils import Vector
out=Path(sys.argv[sys.argv.index('--')+1])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(out/'trial.glb'))
rig=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE')
mesh=next(o for o in bpy.context.scene.objects if o.type=='MESH')
assert len(rig.data.bones)==20
assert mesh.vertex_groups and any(m.type=='ARMATURE' for m in mesh.modifiers)
assert bpy.data.actions
scene=bpy.context.scene
scene.render.fps=24
scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=8; scene.cycles.use_denoising=True
scene.render.resolution_x=400; scene.render.resolution_y=500; scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Preview'); scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.55,.55,.55,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.7
scene.view_settings.view_transform='Standard'
bpy.ops.object.camera_add(location=(1.5,-3,.55)); cam=bpy.context.object; scene.camera=cam
cam.data.type='ORTHO'; cam.data.ortho_scale=1.13
cam.rotation_euler=(Vector((0,0,.49))-cam.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.light_add(type='AREA',location=(0,-2,2.5)); light=bpy.context.object; light.data.energy=100; light.data.size=3
light.rotation_euler=(Vector((0,0,.49))-light.location).to_track_quat('-Z','Y').to_euler()
frames=[]; positions=[]
for frame in [1,5,9,13,17,21,25,29,32]:
    scene.frame_set(frame)
    evaluated=mesh.evaluated_get(bpy.context.evaluated_depsgraph_get())
    positions.append([tuple(v.co) for v in evaluated.data.vertices])
    filename=out/f'preview-{frame:02}.png'; scene.render.filepath=str(filename)
    bpy.ops.render.render(write_still=True); frames.append(str(filename))
delta=max((Vector(a)-Vector(b)).length for a,b in zip(positions[0],positions[4]))
assert delta>0.001, 'Exported animation is static'
(out/'roundtrip.json').write_text(json.dumps({'bones':len(rig.data.bones),'actions':[a.name for a in bpy.data.actions],
    'max_vertex_displacement_frame1_to17':delta,'frames':frames,'note':'Exporter retained four largest joint weights; these previews validate the exported file, not Godot integration.'},indent=2),encoding='utf-8')
print('ROUNDTRIP_PREVIEW_COMPLETE',delta,flush=True)
