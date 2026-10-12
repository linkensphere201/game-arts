# Limestone - independent asset, 0.1.0

A first standalone stone sample with two material styles, 2026-10-06. One shared mesh: 1,282 source vertices, 2,560 triangles, approximately 2.619 x 1.933 x 1.563 m in Blender width/depth/height. Godot is Y-up, one unit = one meter. Origin is at the bottom plane, near the center. High bake source: 20,480 triangles.

## Use in Godot

Copy the entire `stone_asset` folder into your project root, retaining its name. Let Godot import the GLB and PNGs. Drag `realistic.tscn` or `cartoon.tscn` into your scene. They share the detailed mesh; cartoon is material stylization, not a simplified mesh. No coast project, addon, Blender, Python or AI runtime is required. Tested in Godot 4.7.2 Windows Forward+ only.

Each wrapper has a linked GLB, material override and simple convex static collision. Replace/reimport the GLB to update visible geometry; review collision after changing geometry. Material files are shared between instances: make a material unique before per-instance editing. Color tint controls are exposed on the cartoon shader material. Scale/rotate/place the wrapper as a normal Node3D. Collision approximates the silhouette and fills concavities.

## Files and material contract

- `meshes/limestone.glb`: geometry, UVs and tangent data; no embedded material textures. A bare GLB is intentionally untextured. Use the Godot wrappers, or reconnect the maps in another engine.
- `textures/limestone_albedo.png`: 1024 square, sRGB, color without baked lighting.
- `textures/limestone_normal.png`: 1024 square, tangent-space OpenGL normal map, linear data.
- `textures/limestone_roughness.png`: 1024 square, linear grayscale; use red channel, metallic = 0.
- `materials/realistic.tres`: PBR material, normal strength 0.35.
- `materials/cartoon.tres` and `cartoon.gdshader`: designed palette/region contrast, softer normal response and toon lighting, sharing the surface maps.
- `stone.gd`: applies wrapper material after loading, leaving the imported GLB untouched.

Blender source archive includes `limestone-study.blend`: visible runtime mesh with linked/packed textures and hidden high-resolution bake source, plus the generation recipe (which expects this repository layout when rerun). Enable the hidden object for source inspection. Its procedural source material is not expected to transfer as arbitrary Blender nodes to Godot; runtime uses baked images.

## Demo and limits

Open the separate demo project and press F5, or run the Windows demo. Keys 1/2 show realistic/cartoon closeups, 3 shows original rough model / new geometry only / realistic / cartoon. RMB-drag orbits and wheel zooms. The comparison's original coast rock is a reference fixture, not an additional finished asset.

This is a first art-direction sample, not photogrammetry or an accepted photorealistic product. It has procedural weathering and baked relief but no authored distinctive cracks, moss/wetness variants, custom LOD family or measured mobile budget. Texture projection/edge seams and silhouette should receive further art review at the intended game camera distance. Cartoon styling can be adjusted without changing mesh quality. No full coast replacement was made.

## Provenance and terms

Geometry and procedural textures were made locally in Blender with AI-assisted code; no downloaded art or generative image/3D model output was used. The owner has not finalized a commercial asset license; this is an internal review delivery, not a new public redistribution grant. Godot notices accompany the executable and do not license the art. Sources and artifacts remain local; repository commits contain code/docs only.
