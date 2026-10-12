"""Build modular cutaway walls from the existing locally generated timber material."""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'pixel-rpg-demo/mosslight/timber_kit';OUT.mkdir(exist_ok=True)
source=ROOT/'pixel-rpg-demo/mosslight/model_ground/wall.png'
wall=Image.open(source).convert('RGBA')
assert wall.size==(256,128)
# Preserve the model-painted timber profile; only geometric assembly is new.
beam=wall.crop((16,0,48,16))
rail=beam.rotate(90,expand=True)
post=wall.crop((121,0,137,128))
corner=Image.new('RGBA',(16,144));corner.paste(post,(0,0));corner.paste(rail.crop((0,0,16,16)),(0,128))
pieces={'back':(wall,(128,112),(256,32)),
        'side':(rail,(8,16),(16,32)),
        'front':(beam,(16,8),(32,16)),
        'corner_left':(corner,(8,120),(16,48)),
        'corner_right':(corner.transpose(Image.Transpose.FLIP_LEFT_RIGHT),(8,120),(16,48)),
        'front_corner':(rail.crop((0,0,16,16)),(8,8),(16,16))}
records=[]
for name,(image,center,size) in pieces.items():
    image.save(OUT/f'{name}.png')
    (OUT/f'{name}.tscn').write_text(f'''[gd_scene load_steps=3 format=3]
[ext_resource type="Texture2D" path="{name}.png" id="1"]
[sub_resource type="RectangleShape2D" id="shape"]
size = Vector2({size[0]}, {size[1]})
[node name="{name}" type="Node2D"]
texture_filter = 1
[node name="Sprite" type="Sprite2D" parent="."]
texture = ExtResource("1")
centered = false
[node name="Body" type="StaticBody2D" parent="."]
position = Vector2({center[0]}, {center[1]})
[node name="CollisionShape2D" type="CollisionShape2D" parent="Body"]
shape = SubResource("shape")
''',encoding='utf-8')
    records.append(dict(id=name,size=list(image.size),collision_center=center,collision_size=size))
(ROOT/'production/pixel-rpg/model-wave-01/ground/timber-kit.json').write_text(json.dumps(dict(
    source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),pieces=records,
    scope='rectangular cutaway rooms; back wall, side/front rails, corners',
    limitations=['no arbitrary concave wall junctions','side walls are cutaway rails, not full-height walls',
                 'material art retained from the existing model wall study']
),indent=2),encoding='utf-8')
print('TIMBER_KIT_EXPORT_OK: six native scene modules with local texture paths')
