"""Package the local white-body animation review project (no assets in Git)."""
from pathlib import Path
import sys,shutil,re
out=Path(sys.argv[1]).resolve();demo=out/'godot-demo';demo.mkdir(exist_ok=True)
(demo/'captures').mkdir(exist_ok=True)
(demo/'captures/.gdignore').write_text('',encoding='utf8')
for name in ['body-actions.glb','actions.json']:shutil.copy2(out/name,demo/name)
import_file=demo/'body-actions.glb.import'
settings='''_subresources={
"nodes": {
"PATH:AnimationPlayer": {"optimizer/enabled": false, "compression/enabled": false}
}
}'''
if import_file.exists():
    text=import_file.read_text(encoding='utf8')
    text=re.sub(r'_subresources=\{.*?\}\n(?=\w)',settings+'\n',text,flags=re.S)
else:
    text='[remap]\nimporter="scene"\ntype="PackedScene"\n\n[params]\n'+settings+'\n'
import_file.write_text(text,encoding='utf8')
shutil.copy2(Path(__file__).with_name('body-actions-demo.gd'),demo/'main.gd')
(demo/'project.godot').write_text('''config_version=5
[application]
config/name="White Body Action Review"
run/main_scene="res://main.tscn"
[display]
window/size/viewport_width=1100
window/size/viewport_height=720
[rendering]
renderer/rendering_method="gl_compatibility"
textures/default_filters/use_nearest_mipmap_filter=false
anti_aliasing/quality/msaa_3d=2
''',encoding='utf8')
(demo/'main.tscn').write_text('''[gd_scene load_steps=2 format=3]
[ext_resource type="Script" path="res://main.gd" id="1"]
[node name="ActionReview" type="Node3D"]
script = ExtResource("1")
''',encoding='utf8')
print(demo)
