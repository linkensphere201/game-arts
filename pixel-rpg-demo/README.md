# Mosslight Journey: M5 review sample

Current: [modular multi-species character sample](MODULAR-CHARACTERS.md), with 16 presets and separate walk/run animations. This remains an art sample, not the complete M5-M9 product or a sale-ready pack.

## Local delivery

Open `project.godot` with Godot 4.7.2, or run `../builds/pixel-rpg-modular-m5.exe` for the current character street. The earlier `pixel-rpg-m5.exe` remains available.
Arrows/WASD move in eight directions. Press E near the chest to open it.
The room demonstrates nearest-neighbor rendering, foot collisions, Y sorting and short prop animations.

## Legacy base-sample asset contract

- Orthographic three-quarter top-down; square 32 x 32 map tiles.
- Rowan: original auburn-haired traveler, teal coat, ochre scarf and left hip bag.
- Character cells: 48 x 64; feet anchor (24,56).
- Sprite rows: S, SE, E, NE, N, NW, W, SW.
- Idle: four frame slots at 4 fps, two distinct held poses per heading.
- Walk: six frame slots at 8 fps; distinct poses verified per heading, 80 total idle/walk slots.
- Twelve original prop samples, each in a 96 x 96 transparent canvas with anchor (48,88).
- Chest/lantern: four-frame horizontal strips; other props static.
- Terrain: three grass variants, one stone tile and sixteen path neighbor masks (N1/E2/S4/W8).
- PNGs use transparent surroundings and semitransparent ground shadows.

## Reproduce locally

From the repository root (PowerShell), with the installed local dependencies:

```powershell
& .local/comfy/ComfyUI_windows_portable/python_embeded/python.exe -s pixel-rpg-demo/authoring/build_pixels.py
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --headless --path pixel-rpg-demo --editor --import
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --headless --path pixel-rpg-demo --script res://authoring/build_scene.gd
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --headless --path pixel-rpg-demo --editor --import
& .local/comfy/ComfyUI_windows_portable/python_embeded/python.exe -s pixel-rpg-demo/authoring/verify_assets.py
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --headless --path pixel-rpg-demo --script res://authoring/verify_runtime.gd
```

Editable sources: `authoring/art-spec.json`, `authoring/build_pixels.py`, `authoring/build_scene.gd` and runtime GDScript. Pillow rasterizes explicitly authored pixel geometry and directional joints. This is not a claim that a diffusion model produced consistent animation.

Two local DreamShaper8 concept attempts are retained under `../production/pixel-rpg/candidates/`, with provenance under `runs/`. They were rejected because they produced smooth modern illustrations rather than the target pixel style. No cloud inference or downloaded character artwork was used.

## Review and remaining scope

Inspect `../validation/pixel-rpg/room.png`, `contact-sheet.png` and `hero-eight-directions.gif`.
Technical tests check cell dimensions, transparency margins, distinct headings/poses, eight-direction movement, retained idle facing, boundary collision and E-key interaction through the viewport. Exported runtime captures supplement those tests; automated screenshots opening the chest are not the interaction test.

The current protagonist and props remain simpler than the supplied commercial reference. Tree silhouette, side-view gait, terrain transitions and overall art richness require visual review. M6-M9 characters, environment kits, inventory/UI/effects and final packages are not delivered yet. Review M5 before bulk expansion.

Generated PNGs, Godot scenes/resources, caches, executable and review captures remain local and are excluded from Git. A source checkout must run the above generation/import sequence first.

## Unified world study (M5.2.3)

The user confirmed original characters inspired by Re:Zero's ensemble feel, and a consistent world including items and architecture. See [art direction](../context/pixel-rpg-art-direction.md) for the 16-person target and honest implementation limits.

New source/output paths:
- `authoring/build_theme.py`: four distinct costume studies, shared item/architecture geometry and review board.
- `mosslight/theme/`: generated PNGs and SpriteFrames; 4 x 80 idle/walk frame slots, twelve 32 px item icons, two structures and one street backdrop.
- `theme.tscn`: playable street; keys 1-4 switch character, WASD/arrows move and E opens the chest.
- `../validation/pixel-rpg/theme/style-board.png`: actual asset pixels assembled for visual review.
- `../validation/pixel-rpg/theme/cast-walk.gif`: all 32 character-heading combinations animated.

The default project entry is now theme.tscn. A fresh checkout must run both the base generation/import commands above and this theme sequence before running or exporting:

```powershell
& .local/comfy/ComfyUI_windows_portable/python_embeded/python.exe -s pixel-rpg-demo/authoring/build_theme.py
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --headless --path pixel-rpg-demo --editor --import
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --headless --path pixel-rpg-demo --script res://authoring/build_theme_scene.gd
& .local/comfy/ComfyUI_windows_portable/python_embeded/python.exe -s pixel-rpg-demo/authoring/verify_theme.py
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --headless --path pixel-rpg-demo --script res://authoring/verify_theme_runtime.gd
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --headless --path pixel-rpg-demo --export-release 'Windows Desktop'
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --path pixel-rpg-demo res://theme.tscn
```

The theme generator also reproducibly rebuilds base pixel assets using the existing authoring rig. Godot resources use res://mosslight paths. Current world sprites are not a finished modular environment kit, and character clothing overlays still need directional motion polish. Keep the visual gate open.

## Current character implementation (M5.2.4)

The default entry is now `modular.tscn`, exported as `../builds/pixel-rpg-modular-m5.exe`. See [modular character instructions](MODULAR-CHARACTERS.md) for 16 mixed-species presets, 12-option component categories, profession clothing, five builds, separate shadow, and eight-direction walk/run. TAB changes character and SHIFT runs. A fresh checkout needs base -> theme -> modular generation in that order. Earlier commands describe those prerequisites; complete modular generation before exporting the current default project.

## Current art-quality correction (M5.2.5)

The user accepts the mechanics but rejects the procedural art. [Model-first art study](MODEL-ART-STUDY.md) records the new locally generated illustration direction and static sprite resolution comparisons. The current executable still uses historical prototype artwork. New model artwork has not yet been converted into accepted eight-direction animation.

## Front-walk playable candidate (M5.2.7.3)

From the repository root, after generating/importing the existing model study and the phased-cycle artwork:

```powershell
.local/godot/Godot_v4.7.2-stable_win64_console.exe --path pixel-rpg-demo --script res://authoring/front_walk_review.gd
```

WASD/arrows move; Shift uses the existing run animations. F6 switches between the previous runtime and the new south-walk candidate. Only walk_S is overridden on an in-memory duplicate of SpriteFrames; shared resources are unchanged. This is a playable art review, not final pack acceptance. Add `-- --check` for live-input start/stop/restart, eight-frame playback, F6 switching and wall-collision verification. The trial requires local generated assets under production/pixel-rpg/model-wave-01/guided/phased-cycle; these are intentionally not committed.

## Modular timber room (M5.2.6.3)

Run `authoring/export_timber_kit.py` with the local Python runtime after the model wall/floor conversion, then import the Godot project. `mosslight/timber_room.gd` builds a rectangular room using `bays` (256 pixels per bay) and `depth` (32 pixels per row); configure before adding it to the tree. Its origin is the upper-left floor corner. Back walls extend 128 pixels upward; side/front cutaway rails extend 16 pixels outside the floor. Modules include native collisions and can also be placed separately. Concave/T junctions and full-height side walls are not included. The existing `authoring/preview_interior.gd` entry point now uses this kit.

## Interactive roster art review (M5.2.6.4)

With the current local model-review PNGs present, run from the repository root:

```powershell
.local/godot/Godot_v4.7.2-stable_win64_console.exe --path pixel-rpg-demo --script res://authoring/roster_review.gd
```

The viewer loads Bren, Mira, Osric, Tovin and Neris, each with front/rear/right-side studies. Click a name or use Left/Right to change character; 1/2/3 selects native or integer pixel zoom; B toggles light/dark background; Esc closes. Every view uses nearest-neighbor filtering and the same foot baseline. Missing or invalid local textures stop loading with their path instead of silently substituting old art. Assets remain local and this viewer is not included in review-06.

Add `-- --check` to validate all twelve 96x144 textures and actual alpha foot anchors, exercise keyboard cycling/wrap, zoom, background and button signals, and save `production/pixel-rpg/model-wave-01/guided/roster-review-godot.png`. The screen explicitly identifies static studies and unresolved directions/walk/run. It is an art-review tool, not a completed character pack or animation demo.
