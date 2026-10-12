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

## 2026-10-06: AAA grass visual reference (M3.8.6)

User accepts the cartoon grass direction but requests more believable realistic grass. Inspected the actual local Windows screenshot, validation/nature/delivery/nature-3.png, against a public Red Dead Redemption 2 gameplay image published in [VGR's Yarrow guide](https://www.vgr.com/red-dead-redemption-2-where-to-find-yarrow-plants/). Browser capture saved locally at validation/nature/references/rdr2-grass-browser.jpg. This is a screenshot of a published game image, not a locally running game or an original asset.

Observed in the reference: fine irregular silhouettes, low pale grass mixed with taller darker clumps, muted green/straw color variation, flowers/shrubs, and irregular exposed soil. Observed locally: broad straight strips, conspicuous similar clumps, saturated greens, dark rectangular-looking bases, and abrupt grass/path boundaries. Different camera distance, lighting and image resolution prevent an exact material/performance comparison. A still cannot establish wind quality, polygon counts, texture resolution or the game's rendering implementation.

Recommended realistic-only next pass:
1. Isolate realistic generation/output so rebuilding cannot overwrite the accepted cartoon treatment; the current shared authoring script generates both.
2. Author narrow curved/twisted blades and irregular clumps; mix short ground cover, taller grasses, sparse seed heads and dry bent leaves.
3. Reduce uniform saturation, vary leaf age and local color, and inspect veins/roughness/normal strength at actual gameplay distance.
4. Scatter in uneven patches with shorter sparse path verges, exposed soil and dry litter instead of a sharp wall.
5. Inspect front/back lighting, root contact and shadow behavior. Compare fixed cameras/light at close and gameplay distances; verify root-pinned motion and runtime cost before expanding coverage.

These are production recommendations from visual assessment, not claims about RDR2's internal pipeline. More triangles or higher-resolution textures alone would not correct the observed silhouette and distribution problems. No asset code or output was changed in this comparison.

## 2026-10-06: Free nature asset baseline (M3.8.10)

User requests downloading free resources before deciding how to outperform them. Downloaded Kenney Nature Kit from the official [asset page](https://kenney.nl/assets/nature-kit) to .local/references/free-nature/kenney_nature-kit.zip (10,537,521 bytes; SHA256 FA7974A0D342BFE63C38664BA9F8EC1A4AAB8EA25F099BDC56870E33588C4D9D). CRC passed; extracted to .local/references/free-nature/kenney-nature. License.txt identifies Nature Kit 2.1, CC0 and personal/educational/commercial use. Website says 330 files; actual archive has 329 GLBs plus other model formats and preview images. Do not treat format duplicates as unique assets.

Inspected the author's Sample.png and imported six representative GLBs (two grasses, bush, rock, oak and pine) into a separate Godot 4.7.2 Compatibility project at .local/references/free-nature/kenney-godot. All six rendered and benchmark.png saved without reported errors. This confirms this selection, not all 329 models. The author's sample is assembled promotional art; our six-item render is a simple inspection gallery, not a same-lighting comparative scene.

Observation: simple geometry can still produce a coherent, useful stylized kit through consistent palette, broad catalog and modular scene construction. Kenney is a cartoon/low-poly benchmark, not a realism bar. More triangles, maps or procedural parameters in our current sample do not establish superior product value.

Also found [Quaternius Ultimate Stylized Nature Pack](https://quaternius.com/packs/ultimatestylizednature.html): official page lists 63 models, CC0, textured assets with normal maps and FBX/OBJ/Blend/glTF. Official download points to a Google Drive folder; not downloaded or locally evaluated in this pass.

Recommendation: compare equivalent styles and intended use. Define a testable advantage such as a cohesive ready-to-use Godot coast with rooted wind, usable collision, clear controls, sample layouts and documented performance. Next benchmark should place selected free assets and our assets in equivalent scenes/camera/light, then assess art quality and assembly effort. Slight visual improvement alone is not evidence of purchase demand. No third-party assets merged into our product or pushed remotely.

## 2026-10-07: Reference-conditioned character consistency (M5.2.7.2)

Local evidence: plain DreamShaper img2img can change viewpoint but also invent hair, sleeves, equipment and body proportions. Stronger layout conditioning helped rear garment structure but did not establish production-ready side views. A larger 512x768 rear study improved detail without proving cross-view identity.

Investigate a separate appearance-reference input while retaining pose/layout guides. The official [ComfyUI IPAdapter Plus repository](https://github.com/cubiq/ComfyUI_IPAdapter_plus) documents SD1.5 Plus adapters and the ViT-H image encoder; this is an augmentation to the existing DreamShaper checkpoint, not switching to cloud generation. The repository is maintenance-only, so local compatibility must be tested rather than assumed. Current 8188 object_info has ControlNet/CLIPVision nodes but no IPAdapter, and control/vision weight folders were empty. No guarantee of identity preservation or animation consistency follows from model availability.

Pinned support model repository h94/IP-Adapter revision 018e402774aeeddd60609b4ecdb7e298259dc729; official API metadata provides expected sizes/hashes. Support weights total 2,626,556,736 bytes. Node source pinned to cubiq/ComfyUI_IPAdapter_plus commit a0f451a5113cf9becb0847b92884cb10cbdec0ef; downloaded archive is retained locally for review. The chosen ordinary Plus route does not invoke FaceID/InsightFace. Inspected imports and model loader (safe_load=True); this is a bounded source inspection, not a security audit.

Preparation uses tools/download-reference-models.ps1 and tools/start-reference-trial.ps1. The latter checks exact hashes, refuses duplicate/live trial launches, requires the main queue to be idle, releases only idle model cache, and applies the existing 10 GiB available-commit preflight before starting an isolated loopback trial on 8189. The main service and browser workflow remain available on 8188. Do not run both inference queues concurrently. No new inference was demonstrated merely by downloading weights.

## 2026-10-07: Poster/cover side task — poster-cover/M1.1.1-M1.1.3

Research and model comparisons are maintained in [the side-task research record](../../dist-poster-pool-projects/projects/poster-cover/context/research-notes.md). Recommend existing SDXL-family backgrounds plus separate SVG/JSON typography and transparent text exports. New instruction-editing candidate: FLUX.2 klein4B, whose official approximately13GBVRAM guidance does not establish feasibility on this8GBdevice. AnyText2 is an optional raster-lettering tool; Qwen20B editing/decomposition candidates are deferred. Distinguish reference guidance from exact preservation, and RGBA layers from editable text. No downloads or inference in this research slice.

## 2026-10-08 — poster-cover/M2.3

Klein4B quantized local validation passed. FP8 transformer + FP4 encoder + VAE total8.26GB, hash-verified. Default576x768 generation20.9s and reference edit22.9s;768x1024 succeeded with insufficient commit margin. Full measurements, output paths and limits: [side task](../../dist-poster-pool-projects/projects/poster-cover/README.md). No automatic-layout or final-poster claim.

## 2026-10-11 — M5.2.9.1 open human/clothing source research

Scope: research only, following the user's reset to body -> independent clothing/equipment -> textures -> skeleton -> animation. No assets downloaded, software installed or models edited in this slice. Official pages were checked; published capabilities are not locally validated geometry.

### Primary candidates

1. [Blender Human Base Meshes](https://www.blender.org/download/demo-files/): the official listing identifies v1.4.1, CC0, approximately 49 MB, Blender 4.2+. The [official download index](https://download.blender.org/demo/asset-bundles/human-base-meshes/) lists its ZIP as 50,643,039 bytes. [Developer notes](https://developer.blender.org/docs/release_notes/4.0/asset_bundles/) describe realistic/stylized body/head assets and topology improvements. Good candidate for a directly editable Blender starting point. Choose a proper continuous body rather than a primitive blockout, then inspect joint topology; the whole bundle is not automatically game-ready. The older separate realistic_human_base.blend training download is CC-BY, not the same CC0 bundle.
2. [MPFB Blender extension](https://extensions.blender.org/add-ons/mpfb/): parameterized human creation, clothing/bodypart library, rig options and MakeHuman compatibility. Core graphical assets are CC0 per [MPFB output FAQ](https://static.makehumancommunity.org/mpfb/faq/can_i_sell_models.html) and [MakeHuman license](https://github.com/makehumancommunity/makehuman/blob/master/LICENSE.md). Software and asset licenses are distinct. Third-party assets require their own license check. [Proxy documentation](https://static.makehumancommunity.org/mpfb/docs/assets/concept_proxymeshes.html) describes alternative low-density topologies and refitting after body changes. Recommend this ecosystem when body variants plus compatible clothing are the priority; anime/Q proportions still need deliberate art direction and validation.
3. [MakeHuman asset packs](https://static.makehumancommunity.org/assets/assetpacks.html): official list separates CC0 and CC-BY. Useful CC0 candidates include shirts01, pants01, shoes01, dress01, hats02, gloves01, hair01, bodyparts01 (horns), equipment01 and suits02. Do not treat all community assets as CC0 or assume arbitrary downloaded garments fit a different base mesh.
4. [Kenney Blaster Kit](https://kenney.nl/assets/blaster-kit): 40 files, CC0, stylized weapon supplement; not a complete humanoid/clothing foundation and not a close match to the fantasy wardrobe by itself.

### Concrete clothes/equipment shortlist

- [shirts01](https://static.makehumancommunity.org/assets/assetpacks/shirts01.html): tops/T-shirts/sweaters; listed 23 MB, CC0 entries.
- [dress01](https://static.makehumancommunity.org/assets/assetpacks/dress01.html): dresses, tunic and kimono; listed 44 MB, CC0 entries.
- [suits02](https://static.makehumancommunity.org/assets/assetpacks/suits02.html): fantasy/sci-fi suits including a monk robe and hood; listed 183 MB. The page also contains recognizable franchise-named designs; shortlist generic/original items rather than assuming a CC0 label clears third-party character rights.
- [equipment01](https://static.makehumancommunity.org/assets/assetpacks/equipment01.html): listed 17 MB, CC0 weapons including sword, dagger, bow, hammer and magic sceptre.
- [hats02](https://static.makehumancommunity.org/assets/assetpacks/hats02.html) and [shoes01](https://static.makehumancommunity.org/assets/assetpacks/shoes01.html): helmet and footwear starting points; inspect the exact chosen mesh, license and fit before use.

### Quaternius licensing discrepancy

[Universal Base Characters](https://quaternius.com/packs/universalbasecharacters.html) advertises six body variants, average 13k triangles, 20 hairstyles and CC0. [Fantasy Outfits](https://quaternius.com/packs/modularcharacteroutfitsfantasy.html) advertises 12 outfits/62 modular parts and CC0. These would be technically interesting, but the [current QAL page](https://quaternius.com/license.html), dated 2026-08-28, prohibits standalone redistribution of original or modified assets. Pack pages and the general license conflict. Do not select a newly obtained copy as our resale-asset foundation until its exact applicable grant is established. This research does not relicense older CC0 assets already obtained or assert a blanket ban on all rendered output.

### Recommendation and next gate

Compare MPFB/MakeHuman's body-and-clothing ecosystem with Blender's CC0 base-mesh bundle before choosing one canonical body. Favor MPFB for parameterized body variations and compatible wardrobe; favor the Blender bundle for direct stylized sculpt/edit work. Do not mix incompatible bases/garments without refitting. For initial review, obtain only one suitable body and a simple garment after this research stage, retain source/license/hash, inspect silhouette, continuous anatomy, pose, joint edge flow, UV and density. Then progress through the user-approved order. No new binding or animation before the body/clothing stages are accepted.

## 2026-10-12 — M5.2.9.6.7 low-cost video-to-motion research

Question: can video supply reusable motion more cheaply than manually authoring each joint? Yes, markerless motion capture / human motion recovery is an established approach. Local feasibility and total cleanup cost remain untested on this workstation.

| Candidate | Verified capability | Role and limitation |
| --- | --- | --- |
| MediaPipe Pose Landmarker | Local image/video/live processing; estimates 33 3D landmarks; optimized for on-device real-time use | Lightweight tracking baseline. Not a ready-made full skeletal animation exporter; orientation, twist, root motion and foot contacts require additional solving. |
| FreeMoCap | Open-source markerless capture with ordinary cameras and Blender integration | Practical local multi-camera candidate. Official requirements say one camera does not provide reliable 3D; use at least two, preferably three, with calibration. Setup/synchronization and cleanup add work. |
| GVHMR | Official local video inference, including a static-camera option | Relevant single-camera 3D motion-recovery research. Official license restricts use to educational/research/non-profit purposes; commercial use requires contacting the author. Not selected for the asset-sale pipeline. Windows/RTX 5060 Laptop 8GB performance and dependencies remain unverified. |

Sources checked 2026-10-12:
- MediaPipe capabilities and model variants: https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker
- FreeMoCap hardware/3D requirements: https://docs.freemocap.org/documentation/software-hardware-prerequisites.html
- FreeMoCap capture setup: https://docs.freemocap.org/documentation/single-camera-recording.html
- FreeMoCap source/software license (AGPL-3.0): https://github.com/freemocap/freemocap
- GVHMR inference: https://github.com/zju3dv/GVHMR
- GVHMR installation: https://github.com/zju3dv/GVHMR/blob/main/docs/INSTALL.md
- GVHMR commercial-use restriction: https://github.com/zju3dv/GVHMR/blob/main/LICENSE

Do not infer model/dependency or output-asset rights from a software license alone. Do not treat training GPU counts as inference requirements, or estimated world-coordinate landmarks as exact ground-truth capture.

Recommendation: use the existing licensed action library for common motions; explore video capture for distinctive motions. A single-camera clip has the lowest acquisition barrier but potentially greater reconstruction/cleanup cost. Multi-camera FreeMoCap is the stronger local candidate when reliable 3D matters and camera setup is acceptable. No new package/model installation, capture, benchmark or asset replacement occurred in this research slice. Exact tooling is not yet selected.

Acceptance for a future short pilot: recognizable action on the approved body; stable planted feet; no unexplained flips or large jitter; meaningful torso/hip coordination; inspectable baked animation; Godot playback matching Blender. Record actual human/agent cleanup time, not only inference speed. Keep original video and source motion separate from retargeted clips.
