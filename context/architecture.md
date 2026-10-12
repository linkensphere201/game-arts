# Architecture and Minimum Validation Proposal

Research date: 2026-10-03. Tasks: `M2.2.1`-`M2.2.3`. Status: researched proposal, not implemented or benchmarked. Defaults below are recommendations, not approved asset specifications.

## Confirmed Requirements

- Generate game art using a local GPU; mandatory hosted inference is excluded (`M2.1.4`).
- Stage 1 produces a usable finished asset; Stage 2 formalizes a workflow only after effectiveness is demonstrated (`M2.1.5`).
- Target pixel-art characters such as a demon, with assets usable in both Godot and Unity. Both engines are required; one does not substitute for the other.
- This request authorizes research and documentation only. No installation, model download, asset generation, or engine project creation is part of this slice.

## Recommended Minimum Experiment

Produce one original side-view demon with two looping animations, and import the same PNG content into two independent engine fixtures. First validate the fixtures with a simple calibration sprite, so generation failures can be distinguished from import/rendering failures.

| Proposed specification | Value |
|---|---|
| Character/view | One demon, right-facing side view; perspective still requires selection |
| Final cell | 64 x 64 pixels, transparent RGBA PNG |
| Animation | Idle: 4 frames; walk: 6 frames; 8 FPS, looping |
| Sheets | idle.png: 256 x 64; walk.png: 384 x 64; no spacing or trimming |
| Timing | 125 ms per frame; idle loop 0.5 s, walk loop 0.75 s |
| Anchor | Fixed canvas coordinate (32, 56), measured from top-left; keep all frames on this canvas |
| Pixel style | Proposed maximum 32 opaque colors across the character; binary alpha; manually cleaned edges |
| Presentation | Native scale and integer 4x scale, nearest-neighbor filtering |
| Deferred | Attack, death, eight directions, combat logic, automatic rigging, training, marketplace publication |

The anchor is a shared origin, not a requirement that every foot stays motionless. Deliberate animation motion must be distinguished from accidental frame displacement. Mirroring is optional and only acceptable if asymmetric equipment and anatomy permit it.

## Local Tool and Model Candidates

Previously observed during the conversation: NVIDIA GeForce RTX 5060 Laptop GPU, 8151 MiB VRAM, driver 592.27. This is hardware inventory evidence, not a successful model run. Available RAM, disk capacity, installed engines, Python/PyTorch environment, and licenses remain unverified.

Proposed baseline: ComfyUI Windows Portable, SDXL base 1.0 plus Pixel Art XL LoRA, and Pixelorama for frame editing. Aseprite is an alternative if already available or separately selected. ComfyUI can be used as a local generation interface during Stage 1 without making a reusable workflow product the deliverable. Its portable package isolates its Python environment [T5].

Use batch size 1, initially without Refiner, ControlNet, or video modules. Test suitable generation resolutions such as 512 and 1024 separately; final cell resolution is a different property. CPU offloading may make a model fit but needs RAM and may reduce throughput. No exact VRAM fit or seconds-per-image claim is made for this laptop.

RTX 50-series compatibility must be checked against the actual packaged PyTorch/CUDA build. A new driver alone does not prove support. Do not blindly reuse older CUDA installation recipes; first verify device detection, a real CUDA tensor operation, and a small inference. Pin the successful environment rather than upgrading components independently [T6].

| Route | Local candidate/process | Strength | Main uncertainty | Recommendation |
|---|---|---|---|---|
| A: draft then pixel animation | SDXL + nerijs/pixel-art-xl; select one character, clean it, manually author short animations | Small dependency set; direct control over final pixels | Manual art effort and quality on this GPU are unknown | First baseline |
| B: direct sprite-sheet generation | Onodofthenorth/SD_PixelArt_SpriteSheet_Generator; repair and slice output | Specialized sprite-sheet candidate | Author still describes img2img adjustments, consistency work, background removal and resizing; does not establish reliable action cycles | Bounded comparison, not assumed automation |
| C: guided frame generation | Approved reference + img2img/inpaint; optional compatible ControlNet pose/silhouette guides | More control over composition and pose | Nonhuman horns/tails and small limbs may drift; added memory/dependencies | Try if baseline manual effort is excessive |
| D: video to sprites | AnimateDiff, extract frames, remove background and clean | Can explore motion | Temporal artifacts, camera motion, inconsistent pixel grid, resource use and cleanup | Defer from minimum experiment |

Sources: model cards [T7-T9], Comfy tutorials [T10-T11], AnimateDiff repository [T12]. Route rankings are project judgments, not measured comparisons. A fixed seed helps controlled comparisons but does not guarantee character identity across poses. ControlNet and LoRA must match the base-model family.

## Text to Deliverable Process

1. Convert the user's description into a short explicit brief: silhouette, horns/tail, clothing, palette, viewpoint, final cell size, animation list, timing and intended engine versions. A local language model is unnecessary for this first trial; a human can structure the brief.
2. Generate a bounded set of static concepts locally. Save prompt, negative prompt, seed, sampler, steps, guidance, resolution, model/LoRA/VAE identifiers and hashes. Select for readability at final pixel size, not just appearance when enlarged.
3. Establish one canonical character frame. Remove background locally or manually, clean alpha, reduce/repair colors and pixel clusters, and align the fixed canvas. An AI-rendered checkerboard is not transparency. Nearest-neighbor reduction alone does not guarantee good pixel art.
4. Build idle and walk frames from the canonical design. Baseline uses manual pixel editing; optional local guided generation supplies rough poses. Check anatomy, accessories, outline, lighting and color consistency frame by frame. Record all manual time.
5. Export untrimmed PNG strips and individual frames, plus a manifest containing frame rectangles, animation names, frame order, durations, loop flags and anchor convention. Aseprite can export PNG and JSON; editor export schemas need mapping to the agreed manifest [T13].
6. Configure engine-native animation resources from this common source. The manifest is a proposed interchange contract; neither engine is assumed to consume it automatically. Manual setup is acceptable in Stage 1.
7. Validate editor playback, independent Windows builds, and import into fresh projects of the pinned engine versions. Save screenshots/short recordings and build/import logs.

## Verifiable Engine Environments

| Concern | Godot fixture | Unity fixture |
|---|---|---|
| Proposed baseline | Stable Godot 4.x Windows standard edition, GDScript, Compatibility renderer; pin exact patch at setup | Unity 6.3 LTS via Hub, pin exact patch; 2D Built-in Render Pipeline project [T3] |
| Required setup | Matching export templates for Windows desktop | Editor, usable license/account state, and required Windows build support for selected scripting backend |
| Animation representation | AnimatedSprite2D with SpriteFrames; atlas regions or individual frames [T1] | SpriteRenderer with AnimationClips and Animator; reusable prefab |
| Import | Nearest texture filtering; fixed frame rectangles; consistent anchor [T2] | Sprite (2D and UI), Multiple, fixed-cell slicing; Point filter, no compression/mipmaps, Full Rect mesh; proposed 64 pixels per unit [T4] |
| Pixel display | Integer viewport scaling and stable camera | Integer orthographic display; optional compatible 2D Pixel Perfect package for Built-in pipeline |
| Anchor mapping | Preserve frame canvas and set sprite offset so common anchor is node origin | Convert top-left pixel anchor to Unity normalized bottom-left pivot: (0.5, 0.125), under the stated coordinate convention |
| Deliverable | Small source project and reusable character scene/resources; Windows export | Small source project and character prefab/clips/controller; Windows standalone build |
| Reproducibility | Engine patch, renderer, project settings, export preset, source assets and hashes | ProjectVersion.txt, Packages manifest/lock, ProjectSettings, Assets and .meta files |

Do not mix Built-in and URP Pixel Perfect setup instructions: Unity documents different package arrangements [T14]. Native engine resources differ even though their source PNG hashes should match. GPU inference and engine testing can run sequentially to reduce competition for laptop VRAM.

Each fixture should show the same character, a ground/anchor marker, current animation and FPS, idle/walk switching, native/4x views, and black/white/checker backgrounds. A calibration strip with numbered frames and known transparent edges should establish frame order, timing, pivot and filtering before the generated art is used. Input or buttons can switch animation; a full game or combat controller is unnecessary.

The verification package is more than a screenshot: retain editable projects, engine-native reusable resources, source PNGs, import instructions, and a runnable build. Exclude generated engine caches, large model weights and local build outputs from normal source commits when implementation begins.

## Planned Gates and Evidence

All rows below are NOT RUN. They define future checks, not results.

| Gate / task | Check | Evidence required to pass |
|---|---|---|
| E0 / M3.1.1 | Local hardware/runtime and exact versions | Device and CUDA checks, small inference, versions, memory and disk inventory; no hosted inference |
| E1 / M3.1.2 | Godot calibration | Correct frames, timing, alpha and integer rendering in editor and Windows export; no relevant errors |
| E1 / M3.1.3 | Unity calibration | Same checks in editor and Windows build; required packages/license state verified |
| E2 / M3.2.1 | Static character approval | Readable final-size silhouette, complete anatomy, clean transparency and agreed palette |
| E3 / M3.2.2 | Animation and packaging | 4 idle + 6 walk frames, correct order/durations, stable identity and anchor, no unintended clipping or visible loop jump |
| E4 / M3.3.1 | Both-engine fresh import | Matching common-source hashes, reusable native resources import into fresh projects, both builds run and switch animation for at least 60 seconds |
| E5 / M3.3.2 | Effectiveness review | Human quality judgment plus generation/cleanup/integration effort and reproducibility evidence; explicit go/revise/stop finding |

Machine checks can verify dimensions, RGBA, frame counts, bounds, timings and file integrity. Human review must judge design readability, anatomy, motion and consistency. Neither layer alone establishes usable quality.

Record cold load separately from warm inference, peak VRAM, generation parameters, attempted/accepted candidates, failures, generation time, manual cleanup/animation time, engine-integration time and reviewer findings. Performance thresholds remain open; do not claim profitability or market demand from this technical experiment.

Suggested bounded trial: up to 8 initial concepts for route A; if necessary compare up to 8 for route B. Review after two correction rounds instead of generating indefinitely. This is a proposed effort cap, not a measured success rate. If a static character fails, pause before animation. If engines pass but art fails, revise art; if both pass but effort is excessive, evaluate route C before Stage 2.

## Delivery Contract and Remaining Decisions

Proposed output package: brief, canonical frame, idle/walk PNG strips, individual frames, manifest, editable pixel source, generation provenance, Godot scene/resources, Unity prefab/animations, demo projects, validation record and import README. Technical usability here covers sprite animation integration, not combat behavior, collision design or universal engine-version compatibility.

Before execution select perspective, final cell size, acceptable manual work, time budget, exact engine patches and editor. Retain model/LoRA/base-model license records and input provenance; model-card tags alone are not a completed commercial-rights review. No commercial clearance is asserted in this research.

Proceed to M4 only after M3 produces an accepted asset in both engines with acceptable measured effort. M4 can then automate the steps that proved useful; generalized UI, batch production and model training are outside this proposal.

Sources and evidence limits: [Research notes](research-notes.md#technical-research-2026-10-03).

## Current Execution Override: 2026-10-04

The user authorized the Godot-first MVP. The research proposal above is retained as design history. Current scope and ordered acceptance steps are in [active tasks](../tasks/active.md); asset specifications are in [production brief](../production/brief.json). Unity is deferred from this MVP. Local GPU generation, reusable Godot resources and a demo that actually imports them are required. M4 remains conditional.

## Current Delivered Architecture: 2026-10-04

The Godot MVP uses a pinned DreamShaper 8 checkpoint through local ComfyUI 0.38.0, followed by character-specific Python pixel processing, art-directed animation, and Godot 4.7.2 resources. SDXL trials failed on this machine; the original proposed SDXL route above is historical, not the delivered stack.

Source data flows from `production/brief.json` and retained candidate/run records to `assets/ember-imp/`, then byte-identical runtime files in `demo/ember_imp/`. The asset scene refers to its SpriteFrames and PNGs relatively, allowing relocation. The demo depends only on those Godot resources. Model/runtime storage stays under ignored `.local/`; delivery archives and standalone builds stay under ignored `builds/`.

The upper-body layer comes from the local AI draft with cleanup; leg shapes, horn/eye corrections and pose motion are art-directed. This does not establish arbitrary text-to-animation automation. Current acceptance evidence and limitations are in [validation](../validation/README.md).

## 2026-10-05: Manual Godot 3D Environment Workflow (M2.3.4)

Status: researched implementation proposal. The user explicitly prioritizes environments before characters. This ordering supersedes the combined scene/character prototype ordering in M2.3.2. No software installation or scene authoring is started by this research. Scope and art direction of the first environment still require selection. A small stylized room is the recommended bounded example, not a confirmed asset order.

### Scope and Working Method

Build the first scene manually in the Godot and Blender editors. AI may explain operations, review screenshots or propose reference imagery; image generation, procedural construction, scripts and third-party add-ons are not prerequisites. First establish a repeatable manual process, then consider automating proven repetitive steps. Character modeling, rigging, skinning and animation are deferred. An editor free camera and, when needed, a primitive test capsule are validation fixtures, not character deliverables.

Blender owns geometry, UVs, pivots and base material assignments. Godot owns level layout, collision integration, final material tuning, lighting, camera and runtime behavior. Choose one owner per final material; for this proposal use external Godot material resources/remaps for engine tuning, and preserve mesh material-slot names on re-export. Do not depend on arbitrary Blender shader graphs surviving glTF export.

### Proposed Workspace and Version Contract

Use the verified project Godot version as the starting candidate, and pin a compatible official Blender release before setup. Keep the new 3D project separate from the existing 2D demo. Proposed paths (not created): `art-source/environment/` for editable .blend files and references; `scene-demo/` for a new project; `scene-demo/assets/environment/` for GLBs/textures; `scene-demo/materials/`, `scene-demo/props/` and `scene-demo/levels/` for engine resources. Record versions and export/import settings alongside the source assets.

For a Windows desktop-only first scene, evaluate Forward+ with a small baseline lighting setup. This is a proposal requiring launch validation, not a reason to change the existing Compatibility-renderer sprite demo. If web/older-GPU support becomes a requirement, select the renderer and supported lighting features before look development. Retain local inference memory checks; do not run model inference during lighting bakes when memory is constrained.

### Ordered Manual Procedure

| Step | Editor actions | Saved output and gate |
|---|---|---|
| 1. Define the scene | Choose camera, indoor/outdoor theme, style, intended route and target platform. Sketch a top-down layout and create an asset checklist. | Scene brief; reject scope expansion before modeling |
| 2. Make a whitebox | In Godot create a Node3D level and use BoxMesh/primitives or CSG to represent floor, walls, openings and stairs. Use a reference ruler/capsule to assess scale. | `level_whitebox.tscn`; route, clearances and camera views work |
| 3. Define module dimensions | Choose a grid and consistent origins. Suggested trial: one unit = one meter; 2 m floor/wall segments, 3 m room height, a suitably wider-than-capsule doorway. These are editable design defaults. | Module dimension/pivot sheet; two neighboring modules align |
| 4. Model the kit manually | In Blender set metric dimensions, add primitives, edit vertices/faces, extrude and bevel where useful. Use manual duplication/modifiers for repetition. Apply rotation/scale before export and before any future rigging. Keep wall thickness and inspect normals. | Editable .blend with named modules; no unintended holes, reversed faces or overlapping surfaces |
| 5. Establish simple surfaces | Start with a small shared palette and Principled-style base materials. If textured, mark seams, unwrap UVs and check a checkerboard for scale/distortion. Use consistent texture density. | Named material slots; optional 512/1K textures as a proposed starting budget, not a requirement |
| 6. Export one module first | Select the intended objects, export glTF Binary (.glb), exclude unintended cameras/lights and inspect modifier/triangulation results. Test a single wall/crate before exporting the whole kit. | GLB imports at intended size, orientation and pivot with correct surfaces |
| 7. Create reusable engine scenes | Copy GLB/textures into Godot, inspect import settings and create a wrapper .tscn containing the imported model instance. Add collision and material overrides to the wrapper/import configuration. | One reusable module scene; source re-export preserves intended engine changes |
| 8. Assemble the environment | Instance modules into the level, enable snapping and replace the whitebox progressively. Add a few focal props after architecture works. Keep a separate whitebox source rather than destructively replacing it. | Finished layout; no gaps, duplicate coplanar faces or blocked intended routes |
| 9. Add collision and lighting | Use simple collider shapes for floors/walls/props; add WorldEnvironment, a camera and a small number of appropriate lights. Start without GI baking. Inspect several viewing angles in Godot. | Navigable/readable scene; lighting supports forms rather than hiding mesh errors |
| 10. Optional bake and optimize | Once layout is stable, evaluate LightmapGI for mostly static scenery, generate non-overlapping UV2 through import settings and bake modest-resolution lightmaps. Profile before adding LOD/occlusion complexity. | Measured visual/performance comparison; baked assets retained when used |
| 11. Validate delivery | Export a Windows build, inspect representative camera views and walk the test route. Re-export one edited module, then test the complete resource folder in a fresh project. | Reproducible source, reusable assets, demo, screenshots and validation record |

The recommended first kit is floor, straight wall, corner, doorway, pillar and a few static crate/stone props. Doors can initially be static; opening/closing interaction is optional and not needed to prove environment production. Ceilings are included only if the selected camera requires them. Terrain, vegetation systems, water, large streaming maps and procedural level generation are outside the first trial.

### Godot-Specific Choices and Pitfalls

- **Explicit GLB export first:** Godot recommends glTF 2.0. Direct .blend import is supported by invoking Blender under the hood, but creates an installation dependency for anyone importing the project. Keep editable sources separately and hand off explicit exports for the first reproducible package. OBJ is insufficient as a general scene pipeline because of its feature limits.
- **Reimport-safe edits:** Fix geometry/pivots at the Blender source. Use import settings and separate wrapper/inherited scenes for Godot-specific behavior. Do not modify generated `.godot` cache files. Test one source change early; do not discover lost overrides after decorating the whole level.
- **Instances before GridMap:** Ordinary scenes are easiest to inspect for a small room. GridMap/MeshLibrary is an option for many repeated grid-aligned static tiles, not a mandatory dependency. Interactive objects remain separate scenes. Neither workflow automatically creates a good layout.
- **CSG is a whitebox tool:** It is useful for rapid primitive composition. Prefer final reusable meshes for delivery or explicitly validate a baked CSG mesh; preserve the editable source. Do not use a deeply nested runtime CSG hierarchy as the unmeasured production default.
- **Collision is separate from appearance:** Begin with box colliders; concave/trimesh collision is appropriate for static level geometry where justified, not moving rigid-body props. Dynamic props require convex/simple collision. Navigation meshes are deferred unless agent pathfinding is added.
- **Two kinds of UV:** UV1 maps visible surface textures; UV2 used for lightmaps needs unique space without overlapping faces. A material can look correct while baked lighting still fails due to UV2.
- **Materials and light:** Procedural Blender nodes may need baking into maps or rebuilding in Godot. Test normals, backface culling, roughness and scale in-engine. Prefer correct geometry/normals over globally disabling culling to hide defects.
- **Baked lighting is optional:** LightmapGI suits mostly static geometry but consumes bake time and GPU memory. Changes to baked geometry/lights may require rebaking; moving doors should not be treated as fixed baked geometry. Use the selected renderer's supported features. Do not assume features from live stable docs exist unchanged in the pinned editor.

### Acceptance and Delivery

Proposed first deliverable: one small manually assembled environment and a reusable module kit, no finished character. Measure a target such as 1080p/60 FPS only after fixing the camera path, renderer and scene contents; it is not a claimed result. Check:

1. Consistent scale, grid alignment, pivots, naming and asset ownership/source records.
2. No obvious mesh gaps, z-fighting, missing textures or unintended backface disappearance from permitted views.
3. Test capsule can traverse intended routes without falling through floors, snagging on seams or entering blocked space; free camera alone does not prove collision.
4. Re-export/reimport preserves Godot collision/material configuration and all instances update as expected.
5. A copied resource kit works in a fresh project; the exported Windows scene runs without relevant errors.
6. Retain .blend sources, GLBs, textures/materials, .tscn modules/level, import configuration and a short manual reproduction guide. When LightmapGI is used, retain required baked resources and UV unwrap caches; do not rely on the local `.godot` cache.

Approve layout before detailed modeling; approve one complete imported module before bulk production; approve final composition before expensive baking. Human review covers shape, composition and style; technical tests cover portability, collision and runtime behavior. Only after this environment slice is accepted should character production start.

### Primary Sources (Checked 2026-10-05)

- [3D formats and Blender/glTF import](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html)
- [Import configuration](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/import_configuration.html)
- [Model export conventions](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/model_export_considerations.html)
- [CSG whiteboxing](https://docs.godotengine.org/en/stable/tutorials/3d/csg_tools.html)
- [GridMap](https://docs.godotengine.org/en/stable/tutorials/3d/using_gridmaps.html)
- [3D collision shapes](https://docs.godotengine.org/en/stable/tutorials/physics/collision_shapes_3d.html)
- [Renderer comparison](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html)
- [LightmapGI and UV2](https://docs.godotengine.org/en/stable/tutorials/3d/global_illumination/using_lightmap_gi.html)

This plan synthesizes documented editor capabilities into a project-specific manual workflow. No claim of tested local 3D performance, finished art quality or a completed scene is made.

## Two-route asset quality contract (2026-10-06, M3.6.4)

| Layer | Realistic route | Cartoon route |
|---|---|---|
| Geometry | Natural silhouette, structural breaks and meaningful large relief | Deliberate silhouette and simplified but finished forms |
| Surface color | Mineral/bark variation, wear, dirt and appropriate scale | Designed palette, painted details and controlled variation |
| Surface response | Normal/bump, roughness and physically plausible reflection as needed | Selective normal/roughness or stylized shading supporting the design |
| Scene integration | Contact, wetness and consistent lighting | Consistent palette, shading and detail language |

Both routes require richer authored surface detail than the current flat-color coastal prototype. Select texture resolution and polygon budgets based on viewing distance and profiling; do not prescribe every map for every object. Extra faces improve silhouettes and actual relief, while normal maps change shading without replacing missing silhouettes. Start future rock work with geometry-only and fully surfaced comparisons, then evaluate the chosen route before extending it to trees or the whole kit. Current trees/rocks remain a prototype, not accepted final art.

Technical reference: [Godot material channels](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html), checked 2026-10-06.

## Vegetation and ground production plan (2026-10-06, M3.8.1)

Scope: inspect current assets and define the next independent samples. This record does not claim completed replacement assets. Realistic and cartoon routes both require finished geometry/surface detail; cartoon is art direction, not a cheaper unfinished model. Reuse topology/UVs where appropriate, but allow deliberately different crown silhouettes or texture art when styling requires them. A color filter alone does not guarantee a successful cartoon direction.

### Observed local baseline

- Tree GLB: no embedded images, five plain material slots. Crown is opaque intersecting icosphere lobes, not leaf structure. Existing UVs come from primitives, not a designed bark/foliage atlas.
- Grass GLB: no images; every UV0 U coordinate is zero. V was used as a height channel. It cannot carry a two-dimensional blade texture without new UVs. Height-based root anchoring is now fixed and must remain independent of texture UV.
- Terrain GLB: no images; one 0-1 UV rectangle covers 40 x 36 m. Current shader modulates painted vertex colors with noise and wetness; no layered terrain texture set exists.
- Existing prop.gd sets one material override recursively. Do not reuse this unchanged for a tree with separate bark/leaf materials: it would replace every surface with the same material.
- Existing grass uses spatial MultiMesh batches and no cast shadows. Current distance controls are not an authored LOD collection and short prior runs did not prove a material performance gain.

### Ground: make a reusable surface system

Start with a 4 x 4 m test patch and three surface layers: grass-covered soil, exposed soil/path, sand. Produce seamless albedo, normal and roughness maps at an initial 1K per layer, with a defined repeat size in meters. This is a starting budget, not a hardware guarantee. A single 1K map stretched across 40 m supplies only about 25.6 texels per meter; tiled maps retain close-range detail.

Use explicit normalized layer weights (control texture or newly authored vertex channels), separate from artistic color tint. Existing terrain COLOR stores final palette colors and cannot simply be reinterpreted as soil/sand/grass weights. Blend normals in a consistent tangent frame and renormalize; test grazing-light seams. Begin with ordinary mapped tiling on the gentle terrain; use triplanar only if steep areas need it and validate normal orientation. Break visible repetition with broad tint/macro variation, not by arbitrarily rotating tangent normal samples incorrectly. Wet sand alters color and roughness together. Geometry supplies real slope/large rut shape; normal maps supply small grains.

Realistic route: natural grain, soil clods, sparse dried plant matter, restrained dampness. Cartoon route: designed color groupings and simplified but authored soil/grain marks, coherent normal strength and roughness. Do not bake directional sunlight into base color. Deliver material layers, sample mesh, blending shader and parameter explanation; a ground material library is portable while this coast's terrain shape remains scene-specific.

### Grass: replace the blade mesh/UV contract before adding maps

Make three small clumps (short, medium, sparse/dry accent). Give each blade a bendable segmented strip, tapered shape, full-width UVs, varied height and lean. Start with opaque geometry for near-view blades to avoid unnecessary transparency; for denser mid-distance clumps compare compact alpha-cutout cards rather than assuming either approach is always faster. Map authored vein, color gradient and dry-tip detail onto a shared atlas. Realistic/cartoon maps may differ while preserving blade structure.

Store normalized per-blade bend weight explicitly in a documented auxiliary channel, separate from texture UV and per-instance color. Zero weight at every attachment/root vertex; increasing toward tips. Do not reuse the current 0.55 m normalization unchanged for all future heights. Keep root anchoring and add clustered gust/phase variation; normals must remain plausible under deformation. No requirement for physical simulation or player interaction in the first sample.

Place clumps in irregular patches with short/tall transitions, sparse margins and exposed ground; color roots to agree with the ground layer. Use shared geometry/materials and spatial MultiMesh chunks, then validate visibility transitions and cost. Individual blades need no collision. Evaluate near shadows and cutout overdraw at actual camera height before selecting defaults.

### Tree: structure, bark and leaf clusters are separate tasks

Produce one 4-6 m coastal broadleaf sample with visible root flare, tapered trunk, nonuniform branching and deliberate gaps in the crown. Preserve editable trunk/branch/leaf components. Build usable bark UVs along branches and a seamless bark color/normal/roughness set, initially 1K; inspect stretching, junctions and trunk closeups before increasing resolution.

For the first detailed canopy, author small leafy twigs/clusters and render/bake a tightly packed transparent foliage atlas with real leaf outlines and interior detail. Assemble those clusters around the branch structure using several orientations; avoid a few intersecting rectangles or solid balls. Use cutout foliage with mipmap/edge/shadow testing; evaluate backface shading and modest transmission in backlight. Thin-leaf lighting is distinct from ordinary opaque rock shading. A cartoon version may use more intentional leaf group shapes and textures, while retaining twig/crown depth and gaps.

Bind bark and foliage materials separately by surface/node name; do not apply the stone's one-material recursive override. Expose wind controls with stable trunk base and weighted small-branch/leaf motion. Simple trunk collision should follow the visible main stem; foliage needs no collision. Start with one near model and one deliberately reduced distant representation, then compare transitions. Automatic mesh simplification alone may damage thin leaf cards/crown density, so inspect the canopy rather than relying only on triangle counts.

### Ordered samples and acceptance

1. M3.8.2: 4 x 4 m ground patch, three layer materials, realistic/cartoon surface choices. Verify seamless tiling, layer edges, texture scale and normal response under moving/grazing light.
2. M3.8.3: three grass clumps on that patch. Verify full UVs, fixed roots at multiple phases, varied silhouettes, consistent root-ground color and near/distant transitions.
3. M3.8.4: one tree with separate bark/foliage materials, independent preview and a reduced distant representation. Verify all-around silhouette, trunk junctions, cutout edges/backlight, rooted wind and matching collision.
4. M3.8.5: only after sample review, test the small combined patch and fresh-copy asset packages. Use the same camera path, duration, resolution, light and device for before/after CPU/GPU/frame-time comparisons; record draw calls and transparency cost. Do not claim optimization from a different view or shorter run. Full-coast replacement is a separate integration step.

Proposed portable package boundaries: ground_asset/, grass_asset/, tree_asset/. Each owns its runtime dependencies, realistic/cartoon material variants and guide; lighting/cameras/old models belong to the demo. Supply editable source, GLB where applicable, texture maps, supported-engine record, provenance and observed limits. Derive textures locally by deliberate authoring/baking; do not introduce an external AI service requirement. Downloaded/scan material sources would require an explicit provenance/redistribution check before inclusion.

### Official references checked 2026-10-06

- [Godot material documentation](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html): surface channels, foliage cutouts and alpha-edge antialiasing. Cutouts are a supported foliage option, not a claim of performance in this proposed scene.
- [MultiMesh optimization](https://docs.godotengine.org/en/stable/tutorials/performance/using_multimesh.html): instances are culled as a group; spatial batches help. Page is marked not yet updated for 4.7, so validate behavior locally.
- [Mesh LOD](https://docs.godotengine.org/en/stable/tutorials/3d/mesh_lod.html) and [visibility ranges](https://docs.godotengine.org/en/stable/tutorials/3d/visibility_ranges.html): distinguish mesh simplification from switching whole representations.
- [Spatial shader reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html): deformation/material inputs. These APIs support the implementation; they do not establish art quality or measured cost.

## 2026-10-07: Pixel JRPG pack product brief (M5-M9, proposed)

### User-confirmed objective

Start a separate rapid-output product: a cohesive Japanese-style pixel RPG game-art collection with a 2.5D overhead view, broad character/prop/item/environment coverage, multidirectional character movement, and a single viewing angle for non-character assets. High completion and practical game coverage matter more than file counts. Earlier screenshot examples establish the product category, not permission to copy recognizable characters or artwork. Existing Godot 3D deliverables remain intact. The older pre-rendered-3D-to-2D experiment remains deferred; this request does not require that production method.

### Proposed first edition (scope awaiting approval)

An original small fantasy-adventure world supporting village -> wilderness -> dungeon -> return/reward. It is an asset pack with a Godot demonstration, not a full commercial RPG. Local asset production/inference remains the default constraint. No cloud image generation or new model downloads are implied. User confirmed square-grid orthographic three-quarter top-down (not diamond isometric) and eight-direction character movement on 2026-10-07. Native tiles 32 x 32 pixels; humanoid frame canvas 48 x 64 pixels; icons 32 x 32; pixel-perfect nearest sampling and consistent feet anchors. Larger objects span tile multiples with specified pivots/occlusion regions.

Proposed distinct designs (animation frames, mirrored exports, recolors and tile edge combinations do not count as extra designs):
- 12 humanoids: four adventurer roles (fighter, mage, ranger, healer) and eight villagers (merchant, blacksmith, innkeeper, farmer, guard, elder, child, scholar). Designs are original and share scale/style.
- Eight enemies across woodland/cave/ruin themes; four ambient animals. All 24 characters are proposed to have eight-direction idle (4 frames) and walk (6 frames): 1,920 frame slots before extra actions. Eight directions are user-confirmed; character and frame counts remain proposed. These are planning counts, not produced assets.
- For a small turn-based demonstration: the four adventurers and eight enemies also receive a single battle-facing attack/cast, hurt and defeat set. No universal directional real-time combat or equip-every-item animation system is included in this first edition.
- Five environment kits: village exterior, building interior, meadow/forest, cave, ancient ruins. Supply functional tile transitions, corners, collision/occlusion annotations, doors and entry links. Water/shore belongs to outdoor coverage.
- 64 placeable props covering buildings/architectural components, furniture/workstations, containers/signage, vegetation/rocks and dungeon mechanisms. Building modules and small props are cataloged separately; recolors are optional extras.
- 96 inventory icons: 24 equipment, 16 consumables, 24 crafting/gathering materials, 16 quest/key objects and 16 currency/loot/food objects.
- 32 reusable UI elements: panels, dialogue/name boxes, buttons/states, cursor, slots, tabs, bars, status symbols and prompts, sufficient for inventory/shop/dialogue/basic combat screens. Do not count every sliced panel piece as a separate design.
- 12 short effects (hit, slash, heal, cast, fire, ice, poison, pickup, level-up, smoke, sparkle, teleport).
- 12 simple matching humanoid dialogue portraits.
- Three connected showcase maps: village/interior, forest approach and cave/ruin dungeon, demonstrating the five environment kits and the typical exploration/interaction/reward loop.

Non-character assets use a single camera angle. Static objects receive one finished image rather than arbitrary motion; only interactive/living elements need short single-angle animations (doors/chests opening, torch/fire, water, flags, mechanisms, effects). Clarify if the user literally requires animation on every object.

### Delivery and acceptance

- Transparent PNGs, character sheets and separate frames, tilesets, icon/UI sheets, effects, editable authoring sources and a machine-readable catalog with stable asset IDs, dimensions, pivots, animation clips/FPS, tags and provenance.
- Portable Godot 4 resources: configured SpriteFrames, terrain/tile setup, collision and Y-sorting examples, plus a runnable demonstration and source. Universal images remain engine-independent; Unity-specific implementation remains deferred.
- Consistent palette, light direction, pixel density and outline treatment across all categories; no blurred downscaled illustrations passed off as finished pixel art.
- Character directions preserve identity, clothing and equipment; asymmetric details cannot be blindly mirrored. Animated limbs change poses; translating/rotating a static picture is not accepted as a walking cycle.
- Verify loops and foot sliding in motion, frame clipping/anchors/transparency, terrain transitions and prop sorting, scene links/interactions, UI readability, fresh-project import and Windows runtime.
- A coverage matrix links every promised category to catalog entries and a visible demo use. Report missing categories explicitly; hundreds of exported frames do not establish broad game coverage.
- Art approval of the first representative slice precedes batch expansion. Existing sprite/3D prototypes are technical references only, not automatic visual baselines for this pack.
- Generated assets/builds/screenshots remain local, with source/docs-only commits and no automatic push. Working locations proposed: pixel-rpg-demo/, art-source/pixel-rpg/, production/pixel-rpg/, validation/pixel-rpg/, builds/pixel-rpg-*.

### Ordered plan, not yet implementation approval

M5 locks the art/technical contract through one protagonist, eight-direction movement, a small grass/path tile sample, 12 props and one Godot room. M6 expands and validates characters/portraits/action loops. M7 builds terrain/environment kits, remaining props and map connections. M8 completes inventory/UI/effects and cross-category coverage. M9 performs integrated art/animation/import/runtime review, packaging, installation instructions and truthful showcase capture. No completion-time promise is made before measuring the first slice.
