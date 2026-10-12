# Sunward Coast

M3.4: a small stylized outdoor environment, authored on 2026-10-05.

Open `project.godot` in Godot **4.7.2 standard** and press F6 on `levels/coast.tscn`, or F5. The main scene has a 40 x 36 m terrain patch, a coastal meadow, five trees, shrubs, daisies, limestone, a short path and beach. The large sea plane is visual background, not a large playable level. Wind and water run locally on the GPU; no AI model, server, plug-in or Blender installation is needed to run the result.

## Controls

- Hold right mouse button and move the mouse to look.
- WASD moves the free camera; Q/E moves down/up; Shift increases speed.
- 1 / 2 / 3 selects the overview, meadow or beach view.
- H hides/shows the interface. Escape releases the mouse. Close the window to exit.

This is a free-camera art demonstration. It is not a character controller or a complete game. Collision is provided for the ground, rocks and tree trunks; a separate test capsule validates the ground route. The free camera can pass through geometry and leave the finite scenery patch.

## Edit and reuse (0.2.0-rc1)

The current canonical package is `sunward_coast/`: 16 props plus terrain, linked GLB wrappers, shaders, independent Inspector controls and component gallery. Copy this one folder to another project root, keeping its name. Instance `sunward_coast/scenes/environment.tscn` for the composition, or individual `props/*.tscn` for components. Older `assets/`, `materials/` and `levels/coast_environment.tscn` are retained historical outputs and are not the current reusable package.

Press Tab in the demonstration for bilingual grass, sunlight, wind, wave and foam controls. Runtime preview edits are temporary; save Inspector edits in your own Godot scene for persistence. You do not need Blender for normal placement and tuning.

See [buyer guide](sunward_coast/docs/README.md), [catalog](sunward_coast/docs/CATALOG.md), [release evidence and remaining gates](sunward_coast/docs/RELEASE.md), and [provenance/terms draft](sunward_coast/docs/LICENSE-DRAFT.md). Model reimport updates prop/terrain visuals; collisions remain independent. Scattered grass/flower mesh snapshots still require deliberate replacement or assembly rebuild.

## Production and local tools

Blender 4.5.14 LTS portable: `E:\projects\game-arts\.local\blender\blender-4.5.14-windows-x64\blender.exe`.
Godot 4.7.2: `E:\projects\game-arts\.local\godot\Godot_v4.7.2-stable_win64.exe`.
Local Windows build: `E:\projects\game-arts\builds\sunward-coast.exe`.

These tools live in ignored project-local storage; no system installation, file association or PATH change was made. The Blender official ZIP was SHA-256 verified:
`b9533d2397ac1984db4466fb23a7a4649391cca93f6e84209f9bcc60d071c8b9`.
Source: [official Blender 4.5 directory](https://download.blender.org/release/Blender4.5/).

The actual production route is AI-assisted source authoring: an explicit Blender Python recipe builds editable mesh primitives and exports GLBs; an offline Godot script assembles the level and scatters vegetation. This is not a completed mouse-only manual workflow, trained 3D generation, or Stage 2 productization. The Blender files and native scenes are the editable handoff. All geometry is project-authored; no purchased/downloaded art or generated raster images are used.

## Rebuild (overwrites generated assets/scenes)

From the repository root in PowerShell, after backing up any manual edits:

```powershell
& .local/blender/blender-4.5.14-windows-x64/blender.exe --background --factory-startup --python scene-demo/authoring/build_blender_assets.py
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --headless --path scene-demo --editor --import --quit
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --path scene-demo --script res://authoring/build_scene.gd
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --headless --path scene-demo --export-release 'Windows Desktop' ../builds/sunward-coast.exe
```

The scene-construction command must use a real rendering backend: a headless dummy renderer does not retain the required MultiMesh instance buffers. Runtime does not regenerate the terrain or vegetation. Windows export uses the existing local export templates declared in `export_presets.cfg`.

## Scope and limits

Forward+ is the tested target on this Windows laptop; other renderers/platforms are not delivery targets. No lightmap bake, terrain streaming, shoreline physics, swimming, tree foliage collision or characters. Water is an opaque stylized shader with analytical shore foam, not a fluid simulation; the foam is tied to this terrain's shoreline. The finite terrain borders can be exposed by unrestricted free-camera flight. User visual acceptance remains separate from technical tests.

See [validation](../validation/coast/README.md) for actual checks and screenshots.

## Visual polish pass (M3.4.5, 2026-10-06)

The first polish pass replaces repeated ocean glitter/parallel foam bands with noise-warped swells, distance-faded detail and a broken advancing/receding shore front. Shallow/deep colors, wave speed and foam strength are shader parameters. Grass density now varies in broad patches, tapers at the path and beach, and uses spatially coherent tint; flowers favor denser patches. The current layout contains 6,202 grass tufts and 184 flowers. Terrain bounds, five tree locations and saved camera views remain unchanged; rebuilding resamples secondary prop rotations/scales/placements through the seeded recipe.

This is a visual iteration, not sale-ready acceptance. Next priorities are distinctive tree/shrub silhouettes, better sand/grass ground surfaces and a small set of reusable prop variants. Inspector-facing controls can follow once the visual defaults settle. The latest local screenshots/checks are in [polish validation](../validation/coast-polish/README.md); older validation is historical evidence for the previous build.

## Current candidate archives

Run `python tools/package-coast-release.py` from the repository root after rebuilding the scene, executable and engine notices (`--headless --path scene-demo --script res://authoring/export_engine_notices.gd`). Outputs are `builds/sunward-coast-0.2.0-rc1-{godot,demo,windows,blender}.zip` plus an archive manifest. These remain local. Developer export presets and tools are intentionally absent from the buyer demo; install Godot export templates separately if exporting a modified demo.

M3.5 supersedes the prototype reimport limitation for linked props/terrain and the old six-model inventory. Earlier visual-pass notes below are historical. See [current validation](../validation/coast-release/README.md).
