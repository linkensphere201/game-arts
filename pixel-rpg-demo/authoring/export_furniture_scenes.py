"""Export portable native Godot furniture scenes from verified model sprites."""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'pixel-rpg-demo/mosslight'
OUT=BASE/'furniture';OUT.mkdir(exist_ok=True)
# Dimensions, sole anchor, collision offset from the sole, floor footprint.
SPECS={
    'table':((128,112),(64,108),(0,-21),(100,38)),
    'bookshelf':((144,176),(72,172),(0,-18),(116,28)),
    'chair':((64,96),(32,92),(0,-12),(34,24)),
    'bed':((128,176),(64,172),(0,-74),(104,140)),
}
for name,(size,anchor,offset,footprint) in SPECS.items():
    with Image.open(BASE/'model_review'/f'{name}.png') as image:
        assert image.size==size and image.getbbox()[3]==anchor[1],name
    # Relative texture paths deliberately support a renamed destination folder.
    text=f'''[gd_scene load_steps=3 format=3]

[ext_resource type="Texture2D" path="../model_review/{name}.png" id="1"]

[sub_resource type="RectangleShape2D" id="Footprint"]
size = Vector2({footprint[0]}, {footprint[1]})

[node name="{name.title()}" type="Node2D"]
texture_filter = 1

[node name="Sprite" type="Sprite2D" parent="."]
texture = ExtResource("1")
offset = Vector2(0, {size[1]/2-anchor[1]:g})

[node name="Body" type="StaticBody2D" parent="."]
position = Vector2({offset[0]}, {offset[1]})
collision_layer = 1
collision_mask = 1

[node name="CollisionShape2D" type="CollisionShape2D" parent="Body"]
shape = SubResource("Footprint")
'''
    (OUT/f'{name}.tscn').write_text(text,encoding='utf-8')
print('FURNITURE_EXPORT_OK:',len(SPECS),'native scenes, relative texture paths')
