"""Package an explicit local review snapshot; exclude model weights and authoring caches."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,zipfile
ROOT=Path(__file__).resolve().parents[2];SOURCE=ROOT/'pixel-rpg-demo'
p=argparse.ArgumentParser();p.add_argument('--name',default='mosslight-review-01');a=p.parse_args()
assert re.fullmatch(r'[a-z0-9-]+',a.name)
dest=ROOT/'builds'/a.name;archive=dest.with_suffix('.zip')
if dest.exists() or archive.exists():raise RuntimeError('Snapshot exists; preserve it and choose a new --name')
files=['model_courtyard.gd','model_courtyard.tscn','model_playable.gd','model_playable.tscn','mosslight/model_character.gd','mosslight/paving_layer.gd','authoring/check_model_playable.gd']
files += ['model_world.gd','model_interior.gd','authoring/preview_world.gd','authoring/preview_interior.gd']
files += ['mosslight/model_chest.gd']
files += ['mosslight/model_door.gd']
files += ['mosslight/contact_shadow.gd']
files += ['mosslight/model_chest/'+name+'.png' for name in ['closed','half','open']]
files += ['mosslight/model_review/'+n+'.png' for n in ['guild','chest','book','barrel','crate','potion','crystal','sword','shield','herb','coin']]
files += ['mosslight/model_review/'+n+'.png' for n in ['tree','rock']]
files += ['mosslight/model_review/'+n+'.png' for n in ['table','bookshelf']]
files += ['mosslight/model_review/chair.png']
files += ['mosslight/model_review/bed.png']
files += ['mosslight/model_review/'+name+'.png' for name in ['key','scroll','bread','pouch','axe','ring','mushroom']]
files += ['mosslight/furniture/'+name+'.tscn' for name in ['table','bookshelf','chair','bed']]
files += ['mosslight/furniture/README.md','authoring/check_furniture_import.gd']
files += ['mosslight/model_ui/panel.png','mosslight/model_ui/panel.tres','authoring/check_panel_style.gd']
files += ['mosslight/model_ui/theme.tres','mosslight/model_ui/README.md','authoring/check_ui_theme.gd']
files += ['mosslight/model_inventory.gd','authoring/check_inventory.gd']
files += ['mosslight/timber_room.gd','authoring/check_timber_kit.gd']
files += ['mosslight/timber_kit/'+name+suffix for name in ['back','side','front','corner_left','corner_right','front_corner'] for suffix in ['.png','.tscn']]
files += ['mosslight/model_review/door.png']
files += ['mosslight/model_ground/'+n+'.png' for n in ['wood','wall']]
files += ['mosslight/model_ground/'+n for n in ['grass.png','paving.png','paving-corners.png','paving.tres']]
files += ['mosslight/model_motion/rowan_study.tres']
files += ['mosslight/model_motion/'+action+'_'+d+'.png' for action in ['idle','walk','run'] for d in ['S','SE','E','NE','N','NW','W','SW']]
for name in files:assert (SOURCE/name).is_file(),name
for name in files:
 target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(SOURCE/name,target)
# Include the optional front-walk comparison without replacing shared runtime art.
candidate='mosslight/model_motion/front_walk_candidate.png'
shutil.copy2(ROOT/'production/pixel-rpg/model-wave-01/guided/phased-cycle/leg-poses.png',dest/candidate)
review='authoring/front_walk_review.gd'
shutil.copy2(SOURCE/review,dest/review)
# A packaged review must have no fallback dependency outside its own project.
review_text=(dest/review).read_text(encoding='utf-8')
review_text=review_text.replace('\tif not FileAccess.file_exists(source):source="res://../production/pixel-rpg/model-wave-01/guided/phased-cycle/leg-poses.png"\n','')
(dest/review).write_text(review_text,encoding='utf-8')
files += [candidate,review]
(dest/'model_world.tscn').write_text('[gd_scene load_steps=2 format=3]\n\n[ext_resource type="Script" path="res://model_world.gd" id="1"]\n\n[node name="MosslightLinkedStudy" type="Node2D"]\nscript = ExtResource("1")\n',encoding='utf-8')
files += ['model_world.tscn']
(dest/'project.godot').write_text('''config_version=5
[application]
config/name="Mosslight - Linked Art Review"
run/main_scene="res://model_world.tscn"
[display]
window/size/viewport_width=1200
window/size/viewport_height=900
window/stretch/mode="canvas_items"
[rendering]
renderer/rendering_method="gl_compatibility"
textures/canvas_textures/default_texture_filter=0
''',encoding='utf-8')
(dest/'README.md').write_text('''# Mosslight local review snapshot

Open project.godot with Godot 4.7.2 and press F5 for the linked courtyard/interior. WASD/arrows move; Shift runs. Near the guild front door press E to enter; near the wooden door on the back wall press E to play its opening animation and leave. Movement pauses during the 0.6-second opening; repeated E does not queue transitions. Approach the chest and press E to open/close it. Its demonstration potion is awarded once per application session and retained across room visits. This is not disk-saved inventory.

Includes one model-derived character study (eight headings from independent view illustrations; no mirrored runtime heading), walk/run and breathing idle, guild exterior, opening chest, barrel/crate/tree/rock, fourteen inventory icons, grass/paving, native corner-terrain TileSet, and an interior sample with table/chair/bed/bookcase/wood floor/modular rectangular timber room. Two barrel placements are one design; two chair placements are also one design. The interior door uses a six-pose 2D hinged-leaf projection with a fixed frame; the exterior entrance remains static. Items are static previews; concave wall junctions, item use and broader interior coverage remain incomplete.

This is a review snapshot, not the finished requested asset pack or a commercial release. Art approval, camera/style coherence, cross-view costume consistency, character joint/cloth cleanup, terrain variation and the broader roster/catalog remain incomplete. Runtime needs no Python, ComfyUI, model weights or network.

Reuse: retain the mosslight folder hierarchy because native resources use res:// paths. Character cell 96x144, foot anchor [48,122], centered sprite offset [0,-50]. Paving uses 32px tiles and Match Corners terrain; keep a grass underlay. Pixel textures use nearest filtering.

Optional front-walk experiment: run Godot --path . --script res://authoring/front_walk_review.gd. F6 compares the new model-authored contact/arm/weight cycle with the existing south walk. Only this review overrides walk_S; the linked demo still uses the previous shared animations. Add -- --check for input/stop/restart/collision checks. Both remain art studies, not accepted final animation.

Checks: run Godot --path . -- --self-test for linked-room round trips/state retention; run Godot --path . res://model_courtyard.tscn -- --self-test for prop collision/chest interaction; run Godot --path . --script res://authoring/preview_interior.gd -- --self-test for furniture collision; run Godot --path . --script res://authoring/check_model_playable.gd for eight-way movement and breathing. These are technical checks, not art acceptance.
''',encoding='utf-8')
files+=['project.godot','README.md']
manifest={name:hashlib.sha256((dest/name).read_bytes()).hexdigest() for name in sorted(files)}
# Check every literal res:// dependency in the bundle resolves inside it.
for name in files:
 if Path(name).suffix in ['.gd','.tscn','.tres','.godot']:
  for ref in re.findall(r'res://([^"\n]+)',(dest/name).read_text(encoding='utf-8')):
   if ref.endswith('/'):continue # dynamic item names verified in the runtime scene
   assert (dest/ref).is_file(),(name,ref)
(dest/'manifest.json').write_text(json.dumps({'status':'local review only; incomplete art pack','files':manifest},indent=2),encoding='utf-8')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for name in files+['manifest.json']:z.write(dest/name,name)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for name,digest in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==digest
print('REVIEW_PACKAGE_OK:',len(manifest),'hashed files;',archive)
