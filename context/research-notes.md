# Research Notes

## Research Scope

- Date: 2026-10-02.
- IDs: `M2.1.1` (workflow concepts), `M2.1.2` (monetization and initial direction).
- Method: Initial review of official sources and discussion with the user. No customer interviews, paid orders, production trials, or revenue measurements have been conducted.

## Core Concepts

- An AI workflow organizes models, tools, data, and human review into repeatable steps with defined inputs, outputs, and acceptance checks.
- In Anthropic's engineering terminology, workflows primarily follow predefined paths; agents dynamically choose their process and tools. They can be combined [S1].
- In ComfyUI, a workflow is a connected node graph; its structure can be represented as JSON [S2, S3]. A shared workflow file still depends on its required environment and components.
- Human review can be an explicit workflow step. n8n documents approval or rejection before selected tool executions [S4].

## Evidence and Limits

| Finding | Evidence | What it does not establish |
|---|---|---|
| Commercial workflow implementation and integration services exist. | n8n's official service partner directory [S5]. | Typical provider income, our customer demand, or our profitability. |
| ComfyUI workflows can be deployed as APIs. | Official Comfy API documentation [S6]. | That an online product will attract paying users or retain them. |
| Repeatable orchestration and human review are supported patterns. | [S1-S4]. | Identical generated outputs or consistently acceptable game assets. |

## Monetization Options Considered

| Model | Deliverable | Main challenge to validate |
|---|---|---|
| Finished assets | Usable game-art packs | Quality, consistency, buyer demand. |
| Custom delivery | Assets matching a customer brief | Communication, revision effort, delivery time. |
| Workflow templates | Reusable workflow plus instructions | Reproduction, compatibility, support burden. |
| Team implementation | Integrated production process | Reliability, integration, maintenance. |
| Online tool | Usage-based or subscription access | Acquisition, compute costs, retention. |

These are candidate business models, not measured revenue opportunities.

## Initial Conclusion Accepted by the User

On 2026-10-02, the user agreed with prioritizing a small, concrete custom-delivery offer to validate demand before investing in templates or an online tool.

Proposed progression: sample assets and a paid pilot -> repeatable delivery -> reusable workflow -> consider templates or an online service if evidence supports them.

Value depends on accepted customer outcomes and viable delivery economics. Building a workflow alone does not establish a business.

## Candidate Experiment (Not Yet Selected)

A consistent-style game-item icon set for an independent developer was discussed as an example. Neither this asset category nor this customer segment is confirmed.

Possible process: brief -> references and prompts -> candidate generation -> human selection and correction -> specification checks -> export and archive.

Before a pilot, specify asset count, style, dimensions, background, formats, acceptance criteria, delivery time, and included revisions. No price or delivery commitment has been set.

## Validation Questions

- Demand: Who needs the deliverable enough to pay for a small trial?
- Delivery: Can a second batch meet the same style and quality requirements?
- Economics: What time and cost are required per accepted asset, including failed generations, manual edits, communication, and revisions?
- Constraints: What tools, hardware, input assets, and applicable commercial-use terms need checking for the selected offer?

Track order revenue, model/compute cost, labor and rework, acquisition/platform fees, and ongoing support where applicable. No market price or profit forecast is claimed.

## Sources

Official pages consulted during the initial discussion on 2026-10-02; not re-fetched during this documentation update.

- [S1: Anthropic - Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [S2: Comfy - About Comfy](https://support.comfy.org/articles/9806306061-about-comfy)
- [S3: Comfy workflow JSON specification](https://github.com/Comfy-Org/docs/blob/main/specs/workflow_json.mdx)
- [S4: n8n - Human review for tools](https://docs.n8n.io/advanced-ai/human-in-the-loop-tools/)
- [S5: n8n Service Partner Directory](https://experts.n8n.io/)
- [S6: Comfy API deployment](https://support.comfy.org/articles/2703236295-comfy-api-deploy-your-comfyui-workflow-as-an-api)

## Local GPU Constraint Added After Initial Research

- [`M2.1.4`] The user requires the workflow to run on a local GPU. This is a selection gate for future production tools and models.
- Earlier hosted API examples demonstrate a general monetization option only; they are not a selected implementation or a required dependency for this project.
- Confirm target GPU/VRAM and runtime environment before recommending models. Compare candidates by local compatibility, output quality, peak memory, runtime, repeatability, and applicable commercial-use terms.
- For local delivery economics, record GPU time, electricity and hardware allocation where applicable, plus labor and failed attempts; do not use hosted API pricing as the sole cost model.
- Local inference is not a claim of offline capability or verified performance. These have not been tested.

## Latest User Direction: Two Stages

- [`M2.1.5`] Stage 1: produce a finished asset using the local GPU and judge its effectiveness.
- Stage 2: only if Stage 1 is effective, turn the successful production process into a reusable workflow.
- This supersedes the earlier recommendation to make a paid custom-delivery pilot the immediate next step. Paid demand and business economics remain later research topics.
- The first asset, hardware, and effectiveness criteria are still undefined. No output quality, local performance, or business outcome has been validated.

## Technical Research: 2026-10-03

Tasks: `M2.2.1` (dual-engine validation), `M2.2.2` (production alternatives), `M2.2.3` (proposal and evidence record). Research is complete; runtime validation has not begun.

The user has clarified the asset category as pixel-art game characters, for example a demon, and now explicitly requires both Godot and Unity. This supersedes the earlier unselected icon example. The first character's exact perspective and specifications remain proposed.

The recommended experiment is one character with two short animations, a common PNG/metadata package, and separate Godot/Unity fixtures. Full design, deliverable contract, alternatives, acceptance gates and unresolved choices are in [Architecture and minimum validation proposal](architecture.md).

### Findings and Limits

- Both engines have documented sprite-animation/import mechanisms [T1-T4]. Their existence does not prove our projects, exports or generated assets work.
- Local generation tools and pixel-style model candidates exist [T5, T7-T9]. Pixel-style output is not automatically a transparent, aligned or coherent animation. The sprite-sheet author's instructions themselves include additional processing [T9].
- Recommended baseline is local concept generation followed by manual pixel cleanup and short animation authoring. Guided frame generation is an optional comparison. This recommendation is an inference from integration/consistency risks, not a completed quality benchmark.
- Earlier hardware inspection reported RTX 5060 Laptop GPU, 8151 MiB VRAM, driver 592.27. RAM, available disk, installed engines and actual model/runtime compatibility remain unknown. No production test has been run.
- The latest consulted PyTorch release guidance changes available CUDA builds [T6]. Freeze a working ComfyUI/PyTorch combination after testing rather than assuming older installation recipes apply.
- Local inference is mandatory. Initial downloads and Unity setup may require internet; completely offline installation has not been requested or established.

### Technical Sources

Primary documentation, author repositories and model cards consulted on 2026-10-03. Stable/latest URLs may change; pin exact versions when implementing. Model-card claims are author claims, not independently reproduced results.

| ID | Source | Relevance |
|---|---|---|
| T1 | [Godot 2D sprite animation](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html) | AnimatedSprite2D, SpriteFrames and sheet-based animation |
| T2 | [Godot CanvasItem](https://docs.godotengine.org/en/stable/classes/class_canvasitem.html) | Nearest texture filtering |
| T3 | [Unity 6 releases](https://unity.com/releases/unity-6) | Unity 6.3 LTS listed; candidate engine baseline |
| T4 | [Unity 6.3 Sprite Editor](https://docs.unity3d.com/6000.3/Documentation/Manual/sprite/sprite-editor/use-editor.html) | Sprite rectangles and pivot editing |
| T5 | [ComfyUI Portable for Windows](https://docs.comfy.org/installation/comfyui_portable_windows) | Local portable setup and dependencies |
| T6 | [PyTorch 2.12 release](https://pytorch.org/blog/pytorch-2-12-release-blog/) | Current CUDA build and GPU compatibility considerations |
| T7 | [SDXL base 1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) | Base model candidate; standalone base and offloading options |
| T8 | [Pixel Art XL](https://huggingface.co/nerijs/pixel-art-xl) | SDXL LoRA; author suggests nearest downscaling and no Refiner |
| T9 | [SD PixelArt SpriteSheet Generator](https://huggingface.co/Onodofthenorth/SD_PixelArt_SpriteSheet_Generator) | Specialized candidate; documented consistency/postprocessing caveats |
| T10 | [Comfy ControlNet](https://docs.comfy.org/tutorials/controlnet/controlnet) | Optional spatial conditioning |
| T11 | [Comfy inpainting](https://docs.comfy.org/tutorials/basic/inpaint) | Optional localized repairs |
| T12 | [AnimateDiff](https://github.com/guoyww/AnimateDiff) | Motion-generation alternative, deferred |
| T13 | [Aseprite CLI](https://www.aseprite.org/docs/cli/) | PNG sheet and JSON export |
| T14 | [Unity pixel-perfect sprite preparation](https://docs.unity.com/en-us/engine/6000.6/manual/unity2d/2d-urp/2d-pixelperfect/prep-sprites) | Point filtering and pipeline-specific package distinction; newer manual, verify against chosen patch |
| T15 | [Pixelorama](https://github.com/Orama-Interactive/Pixelorama) | Open-source pixel-art and animation editor candidate |
| T16 | [Godot Windows downloads](https://godotengine.org/download/windows/) | Standard editor versus .NET distribution and export setup entry point |

No source establishes laptop-specific throughput, a guaranteed text-to-animation success rate, or commercial suitability of the eventual output. Those remain validation questions.

## 2026-10-04 Implementation Evidence

`M3.1.1`-`M3.3.2` now have actual Godot-MVP evidence, superseding research-only status for that scope. SDXL + Pixel Art XL did not succeed on the tested no-pagefile configuration. A smaller [DreamShaper 8 checkpoint from the author repository](https://huggingface.co/Lykon/DreamShaper) produced eight candidates locally; seed 420052 was selected. This is our measured result, not a general comparison proving one model superior.

The final path uses local generation plus explicit art-directed cleanup and animation. Fresh Godot import, controls, standalone runtime and selected-seed replay passed. See [validation](../validation/README.md) and [production](../production/README.md) for exact versions, hashes, scripts, limits and failed configurations. Unity and generalized automation remain deferred.

## 2026-10-04: Incremental 3D Asset Production (M2.3.1)

Scope: record the discussion and technical assessment only. The user asked for a more incremental approach than direct end-to-end AI 3D generation. No 3D installation, model download, asset production or new implementation milestone is authorized by this record. The chest example below is a proposal, not a selected deliverable.

### Local Feasibility Assessment

The machine has an RTX 5060 Laptop GPU with 8151 MiB VRAM and approximately 32 GiB RAM. A page file is now active; this improves system commit headroom but does not increase dedicated VRAM. Official TripoSR guidance reports about 6 GB VRAM for default single-image inference; Hunyuan3D-2 reports 6 GB for shape generation and 16 GB for shape plus texture; TRELLIS.2 specifies at least 24 GB. These are upstream requirements, not successful local 3D benchmarks. Smaller single-object trials appear plausible; complete textured/animated character generation is not established. Run image generation and 3D generation sequentially to release model memory between stages. Windows/CUDA extension compatibility remains to be tested if implementation is later approved.

### Conventional Game-Asset Pipeline

A usable asset combines mesh geometry, materials/textures and, when needed, rigging/animation, plus engine configuration. Production is iterative, and not every asset needs every stage.

| Stage | Work | Output |
|---|---|---|
| Requirements | Define use, style, scale, camera distance, animation and performance constraints | Asset specification |
| Visual design | Gather references and design silhouettes, colors and relevant views | Concept/reference images |
| Blockout | Build primitive shapes and test proportions in the game | Rough mesh |
| Modeling | Polygon modeling or sculpting for structure and detail | Detailed geometry |
| Game mesh preparation | Control polygon count and topology; support deformation where necessary | Runtime mesh |
| UV and optional baking | Map surfaces to 2D; transfer selected high-resolution details to textures | UV layout and baked maps |
| Materials/texturing | Create color, roughness, metallic response, normals and wear as needed | Materials and textures |
| Optional rigging/animation | Skeleton, skin weights and motion; rigid parts may use transform animation | Rig and animation clips |
| Engine integration | Import, set scale/pivots/collision, connect animation and inspect appearance/performance | Tested engine asset |

High-poly -> low-poly -> baking is a common route, not a mandatory sequence. Low-poly stylized props can use direct modeling and simple materials. Static props usually need no skeleton; chests/doors can animate separate rigid parts; organic characters require more attention to joints, topology, skinning and motion. Environments often reuse modular pieces. Purchased assets, existing libraries, scanning and procedural construction are alternative inputs to the pipeline.

### Incremental AI Assistance

| Entry point | Candidate assistance | Required review |
|---|---|---|
| Concepts | Generate appearance and color variants | Structural plausibility and cross-view consistency |
| Simple modeling | Assist Blender scripts for geometric props or modular structures | Proportions, connections and mesh quality |
| Surface imagery | Generate patterns, markings and texture candidates | Seams, baked-in lighting and UV suitability |
| Material variants | Assist color, wear and dirt variations | Style consistency and surface response |
| Export/checks | Automate naming, export and missing-resource checks | Actual in-engine rendering and behavior |

A plausible texture image is not automatically a complete PBR material. Likewise, an AI-generated shape is not automatically a game-ready animated character. Script-assisted modeling is most approachable for simple geometric objects; it does not eliminate organic modeling and deformation work.

### Proposed Transition Experiment (Not Started)

Text brief -> locally generated concept image -> simple Blender mesh -> simple materials -> one rigid-part animation -> GLB export -> Godot validation.

Illustrative asset: a chest with separate body/lid, metal trim, a hinge-position pivot and an opening animation. First define dimensions, style and a modest performance budget. Validate silhouette, materials, pivot/motion, scale and collision in Godot. Use this to measure editing effort and decide which steps should later be automated. A generated concept remains a reference; it is not a guaranteed consistent multi-view blueprint. No new software purchase or hardware upgrade is selected.

### Sources Consulted in This Discussion

- [TripoSR official repository](https://github.com/VAST-AI-Research/TripoSR): single-image reconstruction, default VRAM guidance and texture baking option.
- [Hunyuan3D-2 official repository](https://github.com/Tencent-Hunyuan/Hunyuan3D-2): shape/texture resource guidance.
- [TRELLIS.2 official repository](https://github.com/microsoft/TRELLIS.2): official hardware requirement.
- [Adobe Substance Bakers](https://experienceleague.adobe.com/en/docs/substance-3d/bakers/home): baking and texturing role.
- [Substance Painter project creation](https://experienceleague.adobe.com/en/docs/substance-3d-painter/using/getting-started/project-creation): mesh and texturing project inputs.
- [Godot 3D formats](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html): glTF/GLB and Blender import.

The process synthesis and proposed experiment are project judgments informed by these sources, not claims that every studio follows an identical workflow. No local 3D quality, speed or commercial suitability has been measured.

## 2026-10-05: Implementable Scene and Character Routes (M2.3.2)

Scope: technical research and a proposed acceptance plan, not installation or asset production. The user asks how scenes and characters can become usable deliverables. This extends M2.3.1 without starting a new implementation milestone. The recommended style is a small stylized low-poly scene; this is a default proposal, not a user-approved art direction.

### Tool and Responsibility Split

Use Blender for editable meshes, UVs, materials, rigs and animation; use Godot for scene composition, lighting, physics, interaction and runtime checks. Deliver explicit GLB files plus editable sources. Keep imported model data separate from gameplay wrapper scenes so reimport does not overwrite gameplay changes. Bake unsupported procedural material effects into textures or recreate them in the engine; do not assume arbitrary Blender node graphs transfer through GLB.

Local diffusion can provide reference images and texture candidates, but is optional for geometric modeling. Blender Python and Geometry Nodes can assist repetitive construction. Script generation by the coding assistant is distinct from local GPU image inference; no local language model has been installed or benchmarked. Complex organic forms, skin weights and motion quality require visual iteration. Current hardware is a plausible fit for the bounded low-poly proposal, not a measured guarantee for large scenes or high-resolution sculpting. Keep inference and editor workloads sequential when memory is tight. No Blender executable was found in PATH or the standard Program Files/Blender Foundation location during a limited inspection; other installations were not ruled out.

### Environment Route: Build a Kit, Then Assemble a Level

1. Fix the camera, visual style, player dimensions and scale convention (proposed one unit per meter). Block out a single room in Godot with primitives and verify movement before detailing.
2. Define a small reusable kit: floor, straight wall, corner, doorway, pillar, door, crate/chest and a few decorations. Set module dimensions and snapping increments together, with consistent pivots.
3. Model modules in Blender using primitives, extrusion, bevels, duplication and optional scripts. Share a small material palette; add a texture atlas or reusable surface textures only when needed.
4. Export GLB modules and assemble reusable Godot scenes. Ordinary scene instances suit a small room; GridMap/MeshLibrary is an option for grid-based static architecture, not a requirement. Interactive doors/chests should remain independently controlled scenes.
5. Add collision appropriate to use: simple shapes for interactive/dynamic props; more detailed static collision only where necessary. Add navigation only if AI movement is included. Tune lighting in Godot, then measure render/physics cost in an exported build.

Godot documents GridMap as placement of reusable MeshLibrary meshes on a grid, with collision/navigation support. Its export guidance recommends checking transforms, triangulation and asset axes, and generally tuning lighting in Godot. These mechanisms support this proposal; the design and performance of our kit remain untested.

### Character Routes and Recommended Progression

| Route | Purpose | Main limitation |
|---|---|---|
| Existing rigged character with recorded provenance | Validate controller, camera and animation integration first | Does not validate original character authorship; redistribution terms must match delivery |
| Simple rigid-part robot/armored figure | Learn local scripted geometry and transform animation | Does not exercise organic skin deformation |
| Editable low-poly humanoid base | Create an original stylized humanoid/demon by adapting shape, materials and accessories | Requires topology, weight and animation correction |
| Sculpted creature from scratch | Distinct anatomy and close-up detail | Highest manual workload: sculpt, retopology, UV, bake, skin and animate |

For a demon, begin with a simple biped body and add horns/loincloth. Defer wings, independent fingers, facial expressions and a complex tail until the basic rig works. MakeHuman/MPFB is a candidate for human bases, not an automatic demon generator. Rigify assists rig construction; it does not guarantee acceptable skinning. Pin compatible tool/add-on versions before implementation and avoid installing every candidate tool at once.

Character production: approved silhouette and neutral pose -> runtime mesh with bend-friendly joints -> simple UV/materials -> skeleton -> skin weights -> test extreme shoulder/elbow/hip/knee poses -> idle and in-place walk clips -> GLB -> Godot CharacterBody3D wrapper, collision capsule and animation switching. Initially let code move the character and use in-place animation; calibrate walk cycle speed to movement to limit foot sliding. Root motion is a later alternative, not a requirement.

Reusing animations requires more than matching bone names. Godot documents rest-pose differences and BoneMap/SkeletonProfileHumanoid mapping. Retargeting must be checked for proportions, foot contact and accessory motion. Bake Blender control-rig/constraint results into exportable bone animation; keep the editable rig source. Do not promise arbitrary skeleton compatibility.

### Proposed First Playable Slice (Not Approved or Started)

A single small room, one controllable character, one opening door or chest, and a few reusable props. The proposal is deliberately split so visual authoring failures are distinguishable from engine integration failures.

| Gate | Work | Acceptance |
|---|---|---|
| A: graybox integration | Room primitives + placeholder/rigged character + camera | Walk, turn and collide correctly; scale and camera are usable |
| B: original prop | Editable chest or door with pivot and open/close animation | GLB imports in a fresh project; action works without material/pivot errors |
| C: environment kit | Replace room primitives with reusable modules | Modules align without gaps; materials and lighting look coherent; collision is usable |
| D: original character | Adapt/model a low-poly biped, skin and add idle/walk | No severe joint collapse; animation loops and switches; feet reasonably match movement |
| E: delivery | Package sources, resources, provenance and demo | Fresh import, reimport preserving gameplay, and standalone Windows validation |

Optional initial budgets to calibrate after profiling: approximately 2k triangles per simple prop, 10k for the protagonist, shared 1K textures where needed, and one room with a 1080p/60 FPS target on this laptop. These are proposed constraints, not industry limits or measured results. Record frame time, draw calls, memory, import warnings, visual defects and manual revision effort. Prefer smaller scope over unverified optimization tricks. Do not claim 60 FPS from editor screenshots.

Deliver editable .blend sources (or parameter scripts plus editable outputs), GLB exports, textures, independent Godot scenes, named clips, an asset manifest (dimensions, pivots, polygon/material counts), source/license records and a runnable demo. Separate purchased/third-party validation fixtures from original authored assets. The existence of a runnable demo does not establish commercial art quality.

### Sources Checked 2026-10-05

- [Godot model export considerations](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/model_export_considerations.html): axes, transforms, triangulation and lighting.
- [Godot GridMap](https://docs.godotengine.org/en/stable/tutorials/3d/using_gridmaps.html): modular mesh placement and collision/navigation.
- [Godot skeleton retargeting](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/retargeting_3d_skeletons.html): bone mapping and rest-pose compatibility.
- [Blender Geometry Nodes](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/): procedural geometry tools; version must be pinned before implementation.
- [Blender Rigify](https://docs.blender.org/manual/en/5.2/addons/rigify/index.html): rig construction assistance.
- [MPFB export guidance](https://static.makehumancommunity.org/mpfb/docs/exporting.html): game-engine export/material considerations.
- [Kenney support and asset terms](https://kenney.nl/support): candidate fixture assets; retain the selected pack's own license record.

No tools or asset packs were installed or downloaded for this research. No local 3D generation, Blender export or Godot 3D performance benchmark has yet been performed.
