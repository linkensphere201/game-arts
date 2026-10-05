"""Package finished strips into relocatable Godot resources (no image synthesis)."""
import argparse
import json
from pathlib import Path

def package(folder, title):
    folder.mkdir(parents=True, exist_ok=True)
    lines = ['[gd_resource type="SpriteFrames" load_steps=13 format=3]', '',
             '[ext_resource type="Texture2D" path="idle.png" id="1"]',
             '[ext_resource type="Texture2D" path="walk.png" id="2"]', '']
    for animation, count, texture in [('idle', 4, 1), ('walk', 6, 2)]:
        for i in range(count):
            lines += [f'[sub_resource type="AtlasTexture" id="{animation}_{i}"]',
                      f'atlas = ExtResource("{texture}")', f'region = Rect2({64*i}, 0, 64, 64)', '']
    lines += ['[resource]', 'animations = [']
    for idx, (name, count) in enumerate([('idle', 4), ('walk', 6)]):
        frames = ', '.join(f'{{"duration": 1.0, "texture": SubResource("{name}_{i}")}}' for i in range(count))
        lines += [f'{{"frames": [{frames}], "loop": true, "name": &"{name}", "speed": 8.0}}' + (',' if idx == 0 else '')]
    lines += [']', '']
    (folder / 'ember_imp_frames.tres').write_text('\n'.join(lines), encoding='utf-8')
    (folder / 'ember_imp.tscn').write_text('''[gd_scene load_steps=2 format=3]

[ext_resource type="SpriteFrames" path="ember_imp_frames.tres" id="1"]

[node name="EmberImp" type="AnimatedSprite2D"]
texture_filter = 1
sprite_frames = ExtResource("1")
animation = &"idle"
autoplay = "idle"
offset = Vector2(0, -24)
''', encoding='utf-8')
    (folder / 'character.json').write_text(json.dumps({'title': title, 'cell': [64,64], 'anchor': [32,56], 'fps': 8, 'idle_frames': 4, 'walk_frames': 6}, indent=2), encoding='utf-8')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('destination', type=Path)
    parser.add_argument('--title', default='Ember Imp')
    args = parser.parse_args()
    package(args.destination, args.title)
