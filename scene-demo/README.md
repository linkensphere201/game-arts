# Sunward Coast

M3.4: a small stylized outdoor environment, authored on 2026-10-05.

Open `project.godot` in Godot **4.7.2 standard** and press F6 on `levels/coast.tscn`, or F5. The main scene has a 40 x 36 m terrain patch, a coastal meadow, five trees, shrubs, daisies, limestone, a short path and beach. The large sea plane is visual background, not a large playable level. Wind and water run locally on the GPU; no AI model, server, plug-in or Blender installation is needed to run the result.

## Controls

- Hold right mouse button and move the mouse to look.
- WASD moves the free camera; Q/E moves down/up; Shift increases speed.
- 1 / 2 / 3 selects the overview, meadow or beach view.
- H hides/shows the interface. Escape releases the mouse. Close the window to exit.

This is a free-camera art demonstration. It is not a character controller or a complete game. Collision is provided for the ground, rocks and tree trunks; a separate test capsule validates the ground route. The free camera can pass through geometry and leave the finite scenery patch.

## Edit and reuse

`levels/coast_environment.tscn` is the environment without UI or camera. Instance it in another scene to reuse the complete composition. Keep `assets/`, `materials/` and `levels/` at their relative project paths when copying it. The six original GLBs can also be imported individually into Godot or Blender.

- `assets/`: terrain, tree, shrub, grass tuft, daisy and limestone GLBs; saved wind-grass mesh.
- `materials/`: editable ocean and grass shaders/materials.
- `levels/`: native editable environment and importing demo.
- `scripts/coast_demo.gd`: free camera, HUD and explicit validation-only capture flags.
- `../art-source/environment/coastal-kit.blend`: editable component workshop; objects spread across X for inspection.
- `../art-source/environment/coastal-terrain.blend`: editable terrain, UVs and vertex palette.

In Godot, open the environment scene to move trees/rocks, tune `AfternoonSun` and `SkyAndAtmosphere`, or adjust the sea material. The grass is saved in 20 spatial MultiMesh batches; each batch has editable transforms and uses the shared wind mesh. The source Blender terrain uses vertex colors rather than downloaded textures.

**Reimport boundary:** this prototype saves snapshots of imported meshes into the assembled native scene. Re-exporting a GLB updates that GLB's imported scene but does not automatically replace those snapshots. For manual iteration, replace the relevant native mesh/model while keeping its collision wrapper, or deliberately rebuild from the authoring recipe. Back up edited scenes before rebuilding: the authoring scripts overwrite their named outputs and do not preserve subsequent hand edits. Fully linked reimport-safe wrappers are a future improvement, not a passed claim.

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
