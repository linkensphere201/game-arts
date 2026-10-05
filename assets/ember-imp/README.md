# Ember Imp: Godot Sprite Resource

Technical MVP, created on 2026-10-04. Tested with Godot 4.7.2 standard edition, Compatibility renderer.

## Import and Use

1. Copy this entire folder anywhere inside a Godot project, for example `res://characters/ember_imp/`.
2. Wait for Godot to import the PNGs.
3. Drag `ember_imp.tscn` into your scene. Its root is an `AnimatedSprite2D`, and idle plays automatically.
4. Call `play("walk")` or `play("idle")` on the instance. Set `flip_h` if horizontal mirroring suits your game.

The `.tscn` and `.tres` use relative references. Copying to a differently named nested folder was tested in a fresh project. No plugin, model, Python environment or ComfyUI server is required to use the finished resource.

```gdscript
var imp = preload("res://characters/ember_imp/ember_imp.tscn").instantiate()
add_child(imp)
imp.position = Vector2(160, 120)
imp.play("walk")
```

## Contract

| Property | Value |
|---|---|
| Cell | 64 x 64 RGBA, binary transparency |
| Idle | 4 frames, 8 FPS, looping; includes breathing and blink |
| Walk | 6 frames, 8 FPS, looping |
| Sheets | idle.png 256x64; walk.png 384x64; no trim or spacing |
| Origin | Pixel (32,56) from top-left; centered sprite offset (0,-24) places that anchor at node origin |
| Filtering | Nearest; prefer integer scales for crisp display |
| Palette | 23 opaque colors shared by animation frames |

`canonical.png` is the finished first idle frame. `frames/` contains separate animation frames. `upper-body.png` is an intermediate editing layer; only the two strips and Godot resources are needed at runtime. `character.json` contains basic interchange metadata and is not an automatic Godot importer.

## Creation and Limits

The original character draft was generated on the local RTX 5060 Laptop GPU using Lykon/DreamShaper, DreamShaper 8, seed 420052. Background removal, palette reduction, horn/eye edits, redrawn pixel legs and animation poses were performed locally with art-directed scripts. The animation is a cutout prototype, not a model-generated coherent action sequence. See the repository's production records for prompts, hashes and measured times.

This sample establishes a usable integration path. It has one three-quarter view, a restrained upper-body walk cycle and no combat logic, collision, attack or death animations. Art direction and commercial readiness have not been accepted by the user. The model is not included; upstream model/input terms need review before commercial distribution. No marketplace clearance is asserted.
