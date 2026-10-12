"""Fit independent CC0 garments, then rig the standard body. Blender script."""
import sys,json,math
from pathlib import Path
import bpy,addon_utils
from mathutils import Vector
root,out=map(Path,sys.argv[sys.argv.index('--')+1:])
src=root/'source/mpfb2-d0a32e57a7f915cb2f2b95410e2117648c7bbb7e/src'
bpy.context.preferences.extensions.repos.new(name='MPFB pilot local',module='mpfb_pilot',custom_directory=str(src))
addon_utils.enable('bl_ext.mpfb_pilot.mpfb',default_set=True)
from bl_ext.mpfb_pilot.mpfb.services.humanservice import HumanService
from bl_ext.mpfb_pilot.mpfb.services.clothesservice import ClothesService
from bl_ext.mpfb_pilot.mpfb.entities.clothes.mhclo import Mhclo
bpy.ops.wm.open_mainfile(filepath=str(out/'01-standard-body.blend'))
body=bpy.data.objects['Standard_adult_body']
assets=[('shirts01','toigo_fisherman_sweater'),('pants01','toigo_wool_pants'),('shoes01','toigo_ankle_boots_male'),('equipment01','joepal_crude_sword')]
clothes=[]
for pack,name in assets:
    path=root/'assets'/pack/'clothes'/name/(name+'.mhclo')
    obj=HumanService.add_mhclo_asset(str(path),body,subdiv_levels=0,material_type='GAMEENGINE',set_up_rigging=False)
    clothes.append((obj,path));print('FITTED',name,len(obj.data.vertices),flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'02-dressed.blend'))
rig=HumanService.add_builtin_rig(body,'game_engine',import_weights=True)
for obj,path in clothes:
    mh=Mhclo();mh.load(str(path))
    ClothesService.set_up_rigging(body,obj,rig,mh,interpolate_weights=True,import_subrig=False,import_weights=True)
rig.name='AdventurerRig'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'03-rigged.blend'))
report={'bones':{b.name:{'head':list(b.head_local),'tail':list(b.tail_local)} for b in rig.data.bones},'objects':[{'name':o.name,'vertices':len(o.data.vertices),'uv_layers':len(o.data.uv_layers),'modifiers':[m.type for m in o.modifiers]} for o in [body]+[c[0] for c in clothes]]}
(out/'rig.json').write_text(json.dumps(report,indent=2),encoding='utf8')
scene=bpy.context.scene;camera=scene.camera;center=Vector((0,0,.78))
for name,angle in [('front',0),('threequarter',35),('back',180)]:
    a=math.radians(angle);camera.location=center+Vector((math.sin(a)*5,-math.cos(a)*5,0));camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/f'dressed-{name}.png');bpy.ops.render.render(write_still=True)
print('DRESSED_RIG_COMPLETE',flush=True)
