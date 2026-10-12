# Modular character system — M5.2.4

## Confirmed user correction

The user rejected the near-identical head/body designs and requested 10-20 options for hair, faces, headgear, outfits, hair color and outfit color; separate shadows; distinct walk/run poses; multiple species; profession-based clothing; and normal/strong/slender/frail/heavy builds. This replaces the earlier four shared-rig costume studies as the active character direction. Keep eight viewing directions and original designs.

## Implemented inventory

| Dimension | Implemented options |
|---|---|
| Hair | 12: crop, side part, spikes, bob, long straight, high ponytail, twin tails, braid, double buns, curls, swept, undercut |
| Face | 12 named shape/detail profiles: oval, round, narrow, square, heart, long, soft, angular, wide, petite, mature, bearded |
| Headgear | 12 accessories plus an optional empty slot: ribbon, circlet, beret, pointed hat, hood, bonnet, goggles, feather cap, flower, headband, helmet, hairpin |
| Profession outfit | 12: swordsman, mage, warrior, witch, nun, merchant, duelist, blacksmith, farmer, scout, cleric, ranger |
| Hair / cloth palettes | 12 palettes each; each derives shadows/highlights consistently |
| Species | Human, beastfolk, elf, goblin-type monster, dragonborn |
| Build | Normal, strong, slender, frail, heavy |
| Presets | 16 concrete recipes: 4 humans and 3 each of the other four species |

Options are independently selected in `authoring/character-parts.json`; no claim that every possible combination has been visually approved. Race anatomy adds pointed ears, animal ears/fur tail, goblin skin/teeth, or horns/scales/tail. These are currently bipedal humanoid archetypes: the monster category is represented by goblins, not a complete monster bestiary, and dragonborn are not full dragons. Beastfolk currently use pointed-eared, tailed anatomy rather than multiple animal subtypes.

Builds alter shoulder/torso width and depth, limb thickness, and abdominal or slouched shape. They are not a uniform whole-image scale operation. Profession-specific garments add plate, split robes, cloaks, aprons, veils, tabards, straps, swords or devotional trim. Existing names remain placeholder preset names; the recipe's outfit field is authoritative for the current class appearance.

## Animation and integration

- 48 x 64 cell, foot anchor (24,56); row order S, SE, E, NE, N, NW, W, SW.
- Idle: 4 slots at 4 fps (held breathing poses); walk: 8 slots at 8 fps; run: 8 slots at 12 fps.
- Run changes stride, knee/heel recovery, elbow bend, torso lean and vertical lift. It is not only a faster playback of walking images.
- 160 frame slots per preset; 2,560 for sixteen presets. Frame slots are not unique character designs.
- `shadow.png` is a separate semitransparent layer anchored to the ground. Body bounce does not move that layer. Cast PNG sheets contain no baked ground shadow.
- Each preset also supplies `mosslight/modular/cast_01.tscn` through `cast_16.tscn`, directly instantiable with its controller, foot collision and shadow. Preserve the `res://mosslight/` path when copying this asset directory into another project.
- Each generated SpriteFrames contains 24 named clips. Walk speed 65 px/s, run speed 115 px/s.
- Current demo: `modular.tscn`, `mosslight/modular_hero.gd` and `modular.gd`. TAB cycles 16 presets, keys 1-4 select the first four, SHIFT runs, arrows/WASD move, E opens the chest.
- Existing four-person theme and earlier sample scenes/executables remain available.

## Change a combination

Edit one entry in `authoring/character-parts.json` under `presets`. Values are zero-based indices into hair/faces/headgear/outfits/hair_colors/cloth_colors/species/body_types/skin_colors. `headgear: -1` means no additional accessory; the nun outfit still includes its own veil. Keep the sixteen stable preset IDs when using the current demonstration. Rebuild images, import them, regenerate resources and export. This is an editable configuration workflow, not yet a graphical character editor.

```powershell
& .local/comfy/ComfyUI_windows_portable/python_embeded/python.exe -s pixel-rpg-demo/authoring/build_modular_characters.py
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --headless --path pixel-rpg-demo --editor --import
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --headless --path pixel-rpg-demo --script res://authoring/build_modular_scene.gd
& .local/comfy/ComfyUI_windows_portable/python_embeded/python.exe -s pixel-rpg-demo/authoring/verify_modular.py
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --headless --path pixel-rpg-demo --script res://authoring/verify_modular_runtime.gd
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --headless --path pixel-rpg-demo --export-release 'Windows Desktop'
```

Fresh source checkouts must first build the base and theme scenes described in the parent README. Generation is local deterministic authoring from editable geometry. No model download or cloud service is needed. Intermediate authoring layers are named rear_hair/body/face/hair/headgear; only assembled sheets and separate shadow are exported in this version.

## Verification and remaining art work

Verified: 12 distinct front-view choices per component category, five species/build differences, all preset sheet dimensions and clipping margins, distinct walk/run imagery, pose diversity, and additional running bounds across 300 species/build/headgear configurations. Godot verifies 256 walk/run clips, speeds, grounded shadow position, idle-facing retention, TAB wrapping, building collision and chest interaction. Exported runtime is checked separately.

Technical checks do not establish commercial animation quality. Remaining art work includes richer face/eye clusters, distinct height/age proportions, more natural foot contact, far-limb and tail occlusion refinement, costume-specific secondary motion, and visually reviewing unusual hat/hair/species combinations. Current headgear/anatomy layering permits ears/horns to pass through head coverings as cutout designs; not every combination is attractive. Shadow is a stylized ellipse, not light-dependent cast geometry.

Review outputs under `validation/pixel-rpg/modular/`: parts-board.png, species-board.png, body-board.png, cast-board.png, walk-run.gif, and actual room.png. The comparison GIF uses equal display durations to make pose differences easy to compare; runtime uses different walk/run rates.
