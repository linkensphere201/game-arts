"""One standard MPFB character, staged outputs. Blender -b -P SCRIPT -- ROOT OUT."""
import sys,json,math
from pathlib import Path
import bpy,addon_utils
from mathutils import Vector

root,out=map(Path,sys.argv[sys.argv.index('--')+1:])
out.mkdir(parents=True,exist_ok=True)
src=root/'source/mpfb2-d0a32e57a7f915cb2f2b95410e2117648c7bbb7e/src'
bpy.ops.wm.read_factory_settings(use_empty=True)
repo=bpy.context.preferences.extensions.repos.new(name='MPFB pilot local',module='mpfb_pilot',custom_directory=str(src))
addon_utils.enable('bl_ext.mpfb_pilot.mpfb',default_set=True)
from bl_ext.mpfb_pilot.mpfb.services.humanservice import HumanService
from bl_ext.mpfb_pilot.mpfb.services.targetservice import TargetService
macro=TargetService.get_default_macro_info_dict()
macro.update(gender=1.0,age=.35,muscle=.5,weight=.5,height=.5)
body=HumanService.create_human(macro_detail_dict=macro)
body.name='Standard_adult_body'
print('BODY_CREATED',len(body.data.vertices),len(body.data.polygons),flush=True)
white=bpy.data.materials.new('White_clay');white.diffuse_color=(.68,.68,.68,1);white.use_nodes=True
white.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.68,.68,.68,1)
white.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.85
body.data.materials.clear();body.data.materials.append(white)
for p in body.data.polygons:p.use_smooth=True
bpy.context.view_layer.update()
evaluated=body.evaluated_get(bpy.context.evaluated_depsgraph_get())
coords=[body.matrix_world@v.co for v in evaluated.data.vertices]
lo=Vector(tuple(min(v[i] for v in coords) for i in range(3)))
hi=Vector(tuple(max(v[i] for v in coords) for i in range(3)))
center=(lo+hi)/2;height=hi.z-lo.z
print('BODY_BOUNDS',list(lo),list(hi),flush=True)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=16;scene.cycles.use_denoising=True
scene.render.resolution_x=600;scene.render.resolution_y=800;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Studio');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.25,.28,.33,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.65
bpy.ops.object.camera_add();camera=bpy.context.object;camera.data.type='ORTHO';camera.data.ortho_scale=height*1.13;scene.camera=camera
for x,y,z,energy in [(-2,-3,4,450),(2,-1,3,250),(0,2,3,350)]:
    bpy.ops.object.light_add(type='AREA',location=(x,y,z));light=bpy.context.object;light.data.energy=energy;light.data.size=3
    light.rotation_euler=(center-light.location).to_track_quat('-Z','Y').to_euler()
for name,angle in [('front',0),('side',90),('back',180)]:
    a=math.radians(angle);camera.location=center+Vector((math.sin(a)*height*3,-math.cos(a)*height*3,0))
    camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/f'body-{name}.png');bpy.ops.render.render(write_still=True)
camera.location=center+Vector((0,-height*3,0));camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=str(out/'01-standard-body.blend'))
(out/'body.json').write_text(json.dumps({'macro':macro,'bounds':[list(lo),list(hi)],'raw_vertices':len(body.data.vertices),'visible_vertices':len(coords),'mpfb':'2.0.18'},indent=2),encoding='utf-8')
print('BODY_STAGE_COMPLETE',flush=True)
