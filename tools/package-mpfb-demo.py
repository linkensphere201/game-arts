"""Package generated GLB into an isolated, importable Godot demonstration."""
from pathlib import Path
import sys,shutil
out=Path(sys.argv[1]).resolve();demo=out/'godot-demo';demo.mkdir(exist_ok=True)
shutil.copy2(out/'adventurer.glb',demo/'adventurer.glb')
shutil.copy2(Path(__file__).with_name('mpfb-demo.gd'),demo/'main.gd')
(demo/'project.godot').write_text('''config_version=5
[application]
config/name="MPFB Standard Character Pilot"
run/main_scene="res://main.tscn"
[display]
window/size/viewport_width=960
window/size/viewport_height=800
[rendering]
renderer/rendering_method="gl_compatibility"
''',encoding='utf8')
(demo/'main.tscn').write_text('''[gd_scene load_steps=2 format=3]
[ext_resource type="Script" path="res://main.gd" id="1"]
[node name="CharacterPilot" type="Node3D"]
script = ExtResource("1")
''',encoding='utf8')
print(demo)
