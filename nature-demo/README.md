# Nature surface study

First reusable ground / grass / tree samples, 2026-10-06. Open project.godot in Godot 4.7.2, F5; or run builds/nature-study-0.1.3.exe. Both routes have textured surfaces. No coast resources are required.

Controls: 1 comparison; 2 ground; 3 grass; 4 realistic tree; 5 cartoon tree; 6 bark closeup. RMB-drag orbits; wheel zooms; L rotates sunlight. The camera may leave the finite test patch. Realistic/cartoon are first material-study treatments, not final art acceptance.

The Windows ZIP contains nature-study-0.1.3.exe at its root.

Independent packages: ground_asset/ (two patches, three material layers); grass_asset/ (three clumps, two styles); tree_asset/ (near/far models, two styles). See each package README for asset-specific parameters, UV contract, collision and known limits. Demo lighting, cameras and scatter are outside those packages. The older coast is unchanged.

Rebuild from repository root after preserving manual edits:
1. Blender --background --factory-startup --python nature-demo/authoring/build_nature.py
2. Blender --background --factory-startup --python nature-demo/authoring/build_realistic_grass.py (after base generation; preserves cartoon)
3. Blender --background --factory-startup --python nature-demo/authoring/build_tree.py
   Then Blender --background --python nature-demo/authoring/build_realistic_ground.py
4. Godot --headless --path nature-demo --editor --import --quit (first pass may report the not-yet-built demo)
5. Godot --headless --path nature-demo --script res://authoring/build_tree_scenes.gd
6. Godot --path nature-demo --script res://authoring/build_demo.gd (real renderer preserves MultiMesh buffers)
7. Godot --headless --path nature-demo --export-release "Windows Desktop" ../builds/nature-study-0.1.3.exe
8. python tools/package-nature.py

Portable tools remain at .local/blender/blender-4.5.14-windows-x64/blender.exe and .local/godot/Godot_v4.7.2-stable_win64_console.exe. Generated resources, PNGs, logs, sources and archives stay local. Fresh source-only clones must generate the assets first. Authoring is deterministic local procedural production; no new model inference or downloads were used.

Realistic grass v2 (M3.8.7): narrower curved/twisted leaves, independent meshes, muted vertex/texture colors, shorter irregular verges and mixed clump heights. Cartoon geometry/maps/materials are preserved. For a realistic-only rebuild, run build_realistic_grass.py, import, then build_demo.gd with -- --realistic-only using the real renderer. Do not use headless to save the MultiMesh scene. Fine silhouettes still need motion/aliasing review; seed heads and broadleaf species remain future work.


## Grass style presets (M3.8.8)

Edit authoring/grass-presets.json, then rebuild realistic grass, import and rebuild the demo with --realistic-only. The default reference_meadow is an interpretation of the public RDR2 reference, not a recreation of its underlying assets. It mixes approximately 50% upright / 35% gently curved / 15% arched blades with independently shuffled narrow, regular and broad widths. Low coverage and sparse tall tufts are configured separately.

Available presets: reference_meadow, upright_meadow, wind_swept. Alternative presets inherit unspecified fields from reference_meadow. Select one with Blender --background --python nature-demo/authoring/build_realistic_grass.py -- --preset reference_meadow.

Parameters: shape_weights (sum 1), lean_ranges (horizontal displacement relative to height), half_width_ranges_m (full width is twice this), height_scale_range, variant_heights_m, wind_strength, scatter_attempts (density attempts per chunk/variant), tall_probability and dry_probability. Width classes are evenly mixed independently of bend and height. These are authoring settings, not live controls; regenerate to apply geometry changes. Materials retain an editable wind_strength in Godot. Current UV2 encoding supports blade heights below 1 m. Cartoon outputs are unaffected by this realistic-only route.


## Realistic ground styles (M3.8.9)

authoring/ground-presets.json defines meadow (default), dry_path and coastal_sand. Select with Blender --background --python nature-demo/authoring/build_realistic_ground.py -- --preset meadow, then import, rebuild the demo using the real renderer and export. These are authoring presets; only meadow has been visually reviewed in this delivery.

Controls: litter_count, pebbles, turf_bias, edge_breakup, wetness and normal_strength. The last four can also be adjusted on the realistic ShaderMaterial in Godot (duplicate it for instance-specific edits). New 2K maps cover the entire finite 4 x 4 m sample once, avoiding the old obvious repeated pattern. These unique patch maps are not a seamless terrain atlas. Dry litter is in the surface maps; scattered 1.4-5 cm gravel has actual geometry. Main ground remains flat to preserve existing grass placement. Cartoon shader/maps/mesh are unchanged.
