# Grass asset 0.1.2

Copy only `grass_asset/` to the new project root. Place `grass_short_realistic.tscn`, `grass_medium_realistic.tscn` or `grass_dry_realistic.tscn`; matching `_cartoon` scenes are supplied. Realistic v2 source triangle counts: short 476, medium 350, dry 266 (seven bending segments). Cartoon retains short 176, medium 240, dry 104 (four segments). All have full-width UV0. No collision is included.

Two 1K blade color/normal sets contain longitudinal detail and a dry-tip gradient. Geometry is opaque and double-sided; this version does not use alpha cards. Roughness is fixed at 0.88. UV2.x is normalized root-to-tip weight (0 = root). UV2.y contains the blade height in meters after glTF V inversion; the shader reads 1-UV2.y. Never substitute UV0.y as the bend mask. Root positions remain fixed; normals follow an approximate shear correction, not a physical blade simulation.

Material controls: wind_strength, tint, normal_strength. wind_time_override is for deterministic QA; leave -1 for animation. Materials are shared: duplicate one before editing a single clump. Demo scattering uses 4 spatial chunks per patch and three variants, with visibility end 25 m and hysteresis margin 3 m. The margin is not a crossfade. Grass cast shadows are disabled in the demo after excessive dense-root self-shadowing; individual clump scenes retain normal mesh shadow settings. The current demo has no automatic grass LOD/card conversion, player interaction or navigation.

Roots should sit slightly inside the surface, with a soil/grass base color chosen to match their surroundings. Randomize clump scale/rotation/density rather than placing a grid. The Blender workshop spreads clumps along X after origin-centered export; reset placement when re-exporting manually. Cartoon source: ground-grass.blend / build_nature.py. Realistic v2 source: grass-realistic-v2.blend / build_realistic_grass.py; run the latter after base generation. Export new GLBs and rebuild demo batches after changing geometry: MultiMesh batches hold saved mesh snapshots.

## Provenance, support and limits

First local review sample, version 0.1.0, 2026-10-06. Tested target: Godot 4.7.2 Windows Forward+; other engines/renderers/platforms are unverified. Geometry and textures are authored locally through Blender and deterministic procedural scripts, with AI coding assistance. No downloaded art, image-model output or external runtime service is included. Realistic/cartoon are material study routes, not claims of photorealism or accepted commercial quality. Final asset redistribution/license terms are pending owner approval.

Keep the folder name at the project root: resource paths are absolute within this package. Allow Godot to import GLBs and PNGs before placing scenes. Models are geometry-only GLBs; use the supplied wrappers or reconnect the external maps manually in other tools. Generated outputs are local and excluded from source-only Git publication.

Version 0.1.2 uses the reference_meadow authoring preset: mixed upright/gentle/arched profiles with independently varied width and height. style-settings.json records the chosen settings; editing that generated record alone does not rebuild geometry. Change authoring/grass-presets.json and rebuild from the source project. Runtime wind_strength defaults to 0.35 for realistic grass; cartoon remains unchanged.
