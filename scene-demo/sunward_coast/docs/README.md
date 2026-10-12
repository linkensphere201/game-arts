# Sunward Coast 0.2.0-rc1

Internal review candidate, 2026-10-06. A compact stylized 40 x 36 m sunny meadow and coast, with 16 reusable props and one terrain. Commercial release is pending owner terms and visual/buyer acceptance.

## Install and view

Use Godot 4.7.2 standard, Forward+, on Windows. Extract the godot archive at your project's root, keeping the folder named `sunward_coast`. Allow the editor to import GLBs. Drag `sunward_coast/scenes/environment.tscn` into your scene. Add your own camera; the environment includes sunlight and WorldEnvironment, so resolve any existing lighting/environment duplication in your project. No project settings are automatically changed. Do not rename the package folder without updating its absolute resource paths.

To see the complete demonstration, extract the demo archive to an empty folder and open `project.godot`, then F5. Open `sunward_coast/scenes/gallery.tscn` and press F6 to inspect the component collection. The Windows archive runs directly via `sunward-coast.exe`; no Blender, AI model, Python, server or plugin is needed.

## Adjust without Blender

Select the SunwardCoast environment instance in Godot's scene tree. Its Inspector exposes sunlight and elevation, grass density/distance/color, wind, shallow/deep water colors, waves and foam. Save your scene to retain Inspector changes. Independent instances have separate grass buffers and shader controls. Environment lighting still follows Godot's viewport/global lighting rules: separate instances do not create separate sky worlds.

In the demo, Tab opens the bilingual preview panel. Choose Low/High or use sliders. Preview changes are temporary. Hold RMB to look; WASD moves, Q/E down/up, Shift faster; 1/2/3 select views; H hides the interface; Escape releases the mouse. This is a free camera, which passes through scenery. No player character is supplied.

Use `props/*.tscn` for individual placement; these wrappers contain linked GLB models and, where applicable, collision. Make an inherited scene or save your composition separately before editing. Keep an untouched copy of the delivered folder for comparison.

## Source edits and reimport

The Blender archive contains `coastal-kit.blend` (component workshop) and `coastal-terrain.blend`. Workshop objects are spread along X for viewing; reset the export object's location to its intended origin when exporting a selected component. Units are meters; Blender Z-up maps to Godot Y-up. Use explicit GLB export and retain filenames.

Prop and terrain wrappers reference GLBs. Replacing a GLB and reimporting updates its visible model while retaining wrapper settings. Collision shapes are independent and must be reviewed/rebuilt after geometry changes. Tree cylinders are approximate trunk collision, including the leaning tree; canopy has no collision. The bench uses a box; rocks/terrain use static triangle collision. Decorative vegetation, driftwood and pebbles have no collision.

Scattered grass and flower MultiMeshes use saved mesh snapshots for batching. Editing their source GLB does NOT automatically update existing batches; rebuild the assembly or replace the batch mesh deliberately. The repository authoring recipe overwrites named outputs and does not merge manual edits. Back up edited outputs first. These are bounded authoring scripts for this scene, not arbitrary text-to-scene automation.

## Limits

Water is an opaque stylized shader with an analytical coastline matched to this terrain, not simulated water. There is no swimming, buoyancy, navigation mesh, character controller, terrain painting, streaming, lightmap bake, texture atlas or hand-authored LOD collection. The terrain has closed sides but is a finite display patch; unrestricted flight exposes its boundaries. Materials use vertex colors and shaders, not a full UV/PBR texture workflow. Moving the whole environment translates its shore pattern; arbitrary deformation, rotation or nonuniform scaling of the assembled coast is not certified. The pack is designed for a stylized small scene, not close-up photorealism.

Only Godot 4.7.2 Windows Forward+ has been tested. Mobile, web, Compatibility, Unity and other Godot versions are unverified. Low quality reduces grass density and distance; it does not guarantee a frame-rate improvement on every device. See RELEASE.md for measured evidence and CATALOG.md for geometry inventory.
