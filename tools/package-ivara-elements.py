"""Export independent element studies and a review-friendly assembled Blender file."""
import bpy,sys,json
from pathlib import Path
from mathutils import Vector
out=Path(sys.argv[sys.argv.index('--')+1])
# Re-running replaces only this script's derived exports/review, never its source.
bpy.ops.wm.open_mainfile(filepath=str(out/'elements.blend'))
scene=bpy.context.scene;scene.frame_set(1)
parts=list(bpy.data.collections['10_Separated_original_surfaces_20k'].objects)
proxies=list(bpy.data.collections['20_NEW_white_mannequin_proxy'].objects)
shells=list(bpy.data.collections['30_Breathing_covered_test'].objects)
exports=out/'parts';exports.mkdir(exist_ok=True)
for o in scene.objects:
    if o.type in {'MESH','ARMATURE'}:o.hide_render=True;o.hide_set(True)
def export(name,objects):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:o.hide_set(False);o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    bpy.ops.export_scene.gltf(filepath=str(exports/(name+'.glb')),use_selection=True,export_animations=False)
    for o in objects:o.select_set(False);o.hide_set(True)
for o in parts:export(o.name,[o])
export('NEW_white_mannequin_proxy',proxies)
export('assembled_20k',parts)
# Side-by-side white proxy and exploded original surface groups, no invented anatomy claim.
proxy_locations={o.name:o.location.copy() for o in proxies}
for o in proxies:o.hide_render=False;o.location.x-=.48
for o in parts:
    o.hide_render=False;o.location.x=.32
    if o.name=='outer_jacket':o.location.x+=.35
    if o.name=='equipment':o.location.x+=.34;o.location.z-=.04
scene.camera.location=(.15,-3,.53)
scene.camera.rotation_euler=(Vector((.15,0,.49))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
scene.camera.data.ortho_scale=2.0
scene.render.resolution_x=1200;scene.render.resolution_y=700
scene.render.filepath=str(out/'elements-overview.png');bpy.ops.render.render(write_still=True)
for o in proxies:o.location=proxy_locations[o.name];o.hide_render=True;o.hide_set(True)
for o in parts:o.location=(0,0,0);o.hide_render=False;o.hide_set(False)
for o in shells:o.hide_render=True;o.hide_set(True)
scene.camera.location=(.02,-3,.53)
scene.camera.rotation_euler=(Vector((.02,0,.49))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
scene.camera.data.ortho_scale=1.12
scene.render.resolution_x=560;scene.render.resolution_y=700
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            space=area.spaces.active
            space.shading.type='MATERIAL'
            space.region_3d.view_distance=1.55
            space.region_3d.view_location=Vector((0,0,.49))
            space.clip_start=.001
scene['README']='10: original 20k surface groups; 20: NEW proxy mannequin (hidden); 30: temporary covered breathing shell (hidden). Each original group can be hidden separately. Proxy is not recovered original anatomy.'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'elements-review.blend'))
# Validate actual GLB export counts/skins with the embedded JSON chunk.
import struct
summary={}
for f in exports.glob('*.glb'):
    data=f.read_bytes();length=struct.unpack_from('<I',data,12)[0];doc=json.loads(data[20:20+length])
    triangles=sum(doc['accessors'][p['indices']]['count']//3 for m in doc.get('meshes',[]) for p in m['primitives'])
    summary[f.name]={'bytes':len(data),'meshes':len(doc.get('meshes',[])),'triangles':triangles}
assert summary['assembled_20k.glb']['triangles']==19999
assert len(summary)==9
(out/'exports.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print('PACKAGE_COMPLETE',summary,flush=True)
