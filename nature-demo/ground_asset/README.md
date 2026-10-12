# Ground asset 0.1.0

Copy only `ground_asset/` into a new Godot project root. Drag `ground_patch_realistic.tscn` or `ground_patch_cartoon.tscn` into a scene. Each patch is 4 x 4 m with static ground collision. The package needs no grass or tree files.

Three 1K repeatable surface sets (turf-covered soil, exposed soil, sand) each have albedo, normal and roughness, separately authored for realistic/cartoon treatment. Albedo is sRGB; normals and roughness are linear data. 4 repeats across the default patch give a 1 m repeat scale. Change the material's repeats, wetness and normal_strength values; make shared materials unique before per-instance edits.

Mesh vertex RGB stores normalized turf/soil/sand weights, not final color. UV0 covers 0-1. The shader normalizes weights and blends tangent normals with renormalization; no triplanar mapping is used. For your own terrain, author the same channels and matching tangent UVs. Collision does not follow shader detail. This sample has a flat 4 m plane; grain/ripples are surface shading, not geometry. Sand macro repetition and lack of hand-authored stones/decals remain visible close up; this is not a terrain-painting tool or scanned ground.

Editable mesh: art-source/nature/ground-grass.blend (the ground object is hidden to inspect grass; unhide it). Textures remain separate editable PNGs. Rebuild recipe: nature-demo/authoring/build_nature.py, which expects this repository layout and overwrites named generated outputs. Preserve manual edits first.

## Provenance, support and limits

First local review sample, version 0.1.0, 2026-10-06. Tested target: Godot 4.7.2 Windows Forward+; other engines/renderers/platforms are unverified. Geometry and textures are authored locally through Blender and deterministic procedural scripts, with AI coding assistance. No downloaded art, image-model output or external runtime service is included. Realistic/cartoon are material study routes, not claims of photorealism or accepted commercial quality. Final asset redistribution/license terms are pending owner approval.

Keep the folder name at the project root: resource paths are absolute within this package. Allow Godot to import GLBs and PNGs before placing scenes. Models are geometry-only GLBs; use the supplied wrappers or reconnect the external maps manually in other tools. Generated outputs are local and excluded from source-only Git publication.


## Realistic ground 0.1.3

Realistic wrapper now uses ground_patch_realistic_v2.glb (2,643 triangles for default meadow, including sparse gravel), separate ground_realistic.gdshader and unique 2K albedo/normal/roughness maps per layer. Older 1K/repeated/shared-mesh descriptions above apply to the original/cartoon treatment only. Soil/turf/sand weights sum to one; shader breakup changes their local boundary. Main ground plane stays flat; gravel reaches roughly 2 cm. Generated trimesh collision follows the combined mesh.

Editable source: art-source/nature/ground-realistic-v2.blend. Recipe: build_realistic_ground.py and ground-presets.json. Presets meadow/dry_path/coastal_sand control debris density and material blending; generated style-settings.json records the chosen preset. Rebuild geometry/maps to change litter or pebble count. Shader turf_bias, edge_breakup, wetness and normal_strength can be edited live. Unique patch maps are not guaranteed seamless for tiled terrain. This remains a material/contact study, not sale-ready photorealism.
