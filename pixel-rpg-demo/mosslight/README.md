# Mosslight asset integration

Copy this entire generated `mosslight` directory into a Godot project's `res://mosslight/` directory; resource paths currently expect that location. Instance `hero.tscn` beneath a Y-sorted Node2D. The hero uses foot-centered collision and AnimatedSprite2D with 16 named clips. Runtime input is arrows/WASD; set `automated` and `auto_direction` for scripted movement. Use nearest texture filtering.

`hero_frames.tres` can also be used without `hero.gd`. `terrain_tileset.tres` provides atlas cells; it does not configure automatic terrain painting. Place road masks explicitly as in `authoring/build_scene.gd`.

Prop foot anchors are (48,88) inside 96 x 96 images. Chest and lantern strips have four columns. Static props have one image. Configure collision according to gameplay rather than the transparent canvas bounds.

This is an M5 sample. Art acceptance and final buyer packaging remain pending. See the parent README for generation, QA and limitations.
