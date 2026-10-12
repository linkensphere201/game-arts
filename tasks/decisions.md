# Decisions

## Decision Log

### 2026-10-02

- Decision [`M1.1.1`]: Use `E:\projects\project-manager\project-template` as the documentation baseline.
- Reason: The user requested the source project's conventions and document skeleton for a new project.
- Impact: Retain the 12-document structure and adapt project identity, safety rules, and initialization status.

- Decision [`M1.1.1`]: Initialize directly in `E:\projects\game-arts`.
- Reason: The user explicitly requested the current directory; the repeated source path was interpreted as `E:\projects\project-manager`.
- Impact: No dated wrapper directory or unrelated source workspace content is copied.

- Decision [`M1`]: Defer product scope and architecture until requirements are provided.
- Reason: Only documentation initialization has been specified.
- Impact: `M1` represents initialization only; later milestones will follow scope definition.

- Decision [`M1.1.2`]: Initialize Git with `main` and set `origin` to `git@github.com:linkensphere201/game-arts.git`.
- Reason: The user requested repository initialization and supplied the remote address.
- Impact: Local version control is enabled. Remote publication requires a separate push request.

- Decision [`M2.1.2`]: Prioritize validating a small custom game-art delivery offer before investing in workflow templates or an online tool.
- Reason: The user explicitly agreed with this initial judgment after the workflow and monetization discussion.
- Impact: Select a concrete buyer and output, then validate paid demand, repeatable quality, and delivery economics. This is a strategic direction, not proof of product-market fit or authorization to contact customers.

- Decision [`M2.1.3`]: Keep the icon-set example and independent-developer segment as candidates; preserve uncertainty about pricing, tooling, budget, and schedule.
- Reason: Those details were illustrative and have not been selected by the user.
- Impact: Record them as planning questions rather than implementation requirements. Official service listings establish that commercial services exist, not an income forecast.

- Decision [`M2.1.4`]: Require local GPU execution for the AI production workflow.
- Reason: The user explicitly stated that the workflow must run on a local GPU.
- Impact: Filter models and tools for a complete local inference path; do not make hosted inference APIs or cloud GPUs mandatory. Establish the target hardware and validate an actual local run before claiming compatibility. Fully offline operation was not requested.

- Decision [`M2.1.5`]: Follow the user's two-stage sequence: first produce a finished asset on a local GPU; then, if results are effective, formalize the process into a workflow.
- Reason: The user explicitly clarified the stage order after adding the local GPU requirement.
- Impact: This supersedes the immediate paid-pilot ordering in `M2.1.2`. Prioritize local production feasibility and finished-output quality. Keep customer trials and monetization as later topics; no generalized workflow implementation is required in Stage 1.

### 2026-10-03

- Requirement [`M2.2.1`]: Validate both Godot and Unity. Neither engine alone satisfies the requested environment.
- Requirement [`M2.2.2`]: Target text-described, engine-usable pixel-art characters such as a demon. This supersedes the icon example as the current asset direction.
- Scope [`M2.2.3`]: Research and record technical options only; do not begin setup or asset production.
- Recommendation [`M2.2.2`]: Begin with local SDXL/Pixel Art XL concept generation plus pixel editing and short manual animations. Direct sheets, guided frames and video are alternatives with unmeasured costs/quality.
- Proposal [`M2.2.3`]: One side-view 64x64 character, 4-frame idle and 6-frame walk; first validate engines with calibration sprites, then import the same generated source into both. These defaults are not user-approved specifications.
- Planning [`M3`]: Classify future dual-engine production validation as complex; M1-M4 remain the known milestone sequence. Proposed M3 acceptance and decomposition are documented, but implementation is deferred as expressly requested.

## 2026-10-04: Godot MVP Execution Authorized

- `M3`: The user now requests execution of the full sprite creation-to-import flow, with a reusable Godot asset and an actual Godot demonstration project. This supersedes the earlier research-only boundary.
- `M3.1.3`: Unity validation is deferred from this MVP, not removed from the longer-term direction.
- `M3.2`: Adopt the proposed demon, 64x64 cells, idle/walk scope as an implementation default. Preserve local GPU inference and record any deviations.
- `M3.3`: MVP acceptance is a reusable character scene/SpriteFrames/PNG package, an importing demo, successful engine checks and visual evidence. M4 remains conditional.

## 2026-10-04: Delivered MVP Findings

- Decision [`M3.1.1`]: Use DreamShaper 8 for the working MVP after SDXL allocation/loading failures. Do not change system virtual memory. Preserve model hashes and unsuccessful trials.
- Decision [`M3.2.1`, `M3.2.2`]: Select locally generated seed 420052; use art-directed pixel edits and cutout/hand-authored leg poses. Do not describe these as AI-generated animation frames.
- Result [`M3.3.1`]: Deliver the Godot scene/SpriteFrames/PNG resource independently from the importing demo; relocated fresh import and a 60-second Windows run passed.
- Finding [`M3.3.2`]: Technical path works for one character. The current upper-body motion is limited; a distinct tail was not retained; visual/commercial acceptance and full labor cost are unproven. M4 remains conditional.

## 2026-10-05: AI-Assisted Production Route Confirmed

- Decision [`M2.3.3`]: The user confirms AI-assisted asset production as the project route. AI supports concepts, reference/texture candidates and production scripts; Blender provides editable geometry, materials, rigs and animation; Godot verifies actual use; human review accepts visual and motion quality.
- Principle: Preserve inspectable, editable intermediate outputs. Evaluate each stage separately and repair locally. Direct AI 3D generation may later supply a rough mesh or another bounded input when measured quality and effort justify it; it is not the default end-to-end production route.
- Constraints: Preserve local GPU execution for generative art inference, Godot-first validation, deferred Unity, and workflow productization only after useful output is demonstrated. Coding-assistant help is distinct from local generative-art inference; no local language-model deployment is implied.
- Scope: This confirms the route, not the illustrative room/chest/demon scope, art style, or installation schedule. Choose the first 3D deliverable and its acceptance criteria before production. No software installation or asset generation is part of this decision-recording task.

## 2026-10-05: Manual Environments Before Characters

- Decision [`M2.3.4`]: The user requests a Godot-focused manual 3D environment production plan, with environment work preceding character work. This supersedes the interleaved character/scene prototype ordering in M2.3.2. AI-assisted production remains the accepted overall route; the first environment process must be understandable and executable manually. Current scope is research and documentation, not installation or production.

## Sunny coastal meadow (M3.4, 2026-10-05)

The user authorized scene implementation, selected outdoor vegetation/lawn/sunlight/coast, then requested a small scene. Final terrain bounds are 40 x 36 m; the ocean is a backdrop. The user also requested Blender installation: official Blender 4.5.14 LTS portable was downloaded, SHA-256 checked and started successfully under `.local/blender/`.

M3.4.1/M3.4.2 source and scene integration are complete: two editable .blend sources, six GLBs, an editable Godot environment and a free-camera demo. Offline scripts assist explicit mesh construction and scatter; this does not claim mouse-only manual production. M3.4.3 packaging and fresh-copy/runtime validation follow. The original indoor example and larger first draft are superseded. Characters remain deferred.


## 2026-10-05: Source-only remote publication (M3.4.4)

The user requested commit/push without resources or build products. Publish code, shaders, configuration, authored specifications and documentation only. Keep all asset binaries, generated native resources/scenes, images, captures, runtime logs/data, tools, models and packages local. Use a new source-only commit based directly on the prior remote main; preserve original local commits and files rather than rewriting history. Never merge the resource-bearing local lineage into the publication branch. Visual delivery remains local, and a fresh clone requires asset generation before running the demo.

## 2026-10-06: Coastal candidate boundaries (M3.5)

Expand the reusable kit to 16 props plus terrain, preserving the 40 x 36 m scene. Use linked GLB wrappers for prop/terrain reimport, but retain batched grass/flower mesh snapshots for the existing scatter pipeline and disclose that update boundary. Expose environment tuning in Godot so normal use does not require Blender. Distribute a local 0.2.0-rc1 candidate with engine notices and pending asset-license terms; do not represent technical tests as commercial art acceptance. Keep the source-only remote lineage policy.

## 2026-10-06: Two art routes and surface-detail requirement (M3.6.4)

The user explicitly requests two future routes: realistic and cartoon. Both must include more refined textures/material detail; neither is satisfied by a coarse mesh and plain colors. This supersedes treating the current low-poly flat-color appearance as the final quality target. Record the direction now; no immediate two-pack production or default conversion of the existing scene is implied. Model silhouette, texture/material detail and lighting must be evaluated together.

## Independent stone asset authorized (2026-10-06, M3.7)

The user approves the stone as a standalone asset and clarifies that cartoon is a styling treatment. Share detailed geometry and surface maps across realistic/cartoon materials; do not equate cartoon with lower modeling completeness. Keep stone_asset independent of the coast and place comparison lights/camera/reference in a separate demo. Use a geometry-only GLB plus external maps to avoid Blender packed-texture exporter temporary-directory failures. The finished source .blend embeds its maps.

## 2026-10-06: Independent nature sample implementation (M3.8.2-M3.8.5)

Use explicit ground layer weights rather than reinterpreting palette colors. Grass UV0 is for texture and UV2.x for root-to-tip bending; variable blade height is stored separately. Initial grass is opaque geometry; disable demo grass shadows after inspecting dense-root artifacts. Tree uses distinct bark/leaf nodes/materials, alpha-cutout leaf cards, isolated per-instance wind and separate near/far models. Retain local procedural generation and independent folders, with representative tests. Do not describe these first material treatments as final realism/cartoon acceptance or infer speedup from a single run.

## 2026-10-06: Grass style review (M3.8.6)

The user accepts the current cartoon grass direction. Preserve it while refining the realistic route independently. Realistic grass remains below the requested visual target; prioritize blade silhouette, mixed growth patterns and ground transitions before simply increasing mesh density or texture resolution. Reference comparison is recorded in context/research-notes.md. This acceptance concerns cartoon grass, not all nature assets or commercial readiness.

## 2026-10-06: Pre-rendered 3D-to-2D assets deferred (M3.8.10 follow-up)

The user clarified that the pictured marketplace pack contains 3D-rendered 2D assets. Keep this delivery route as a future alternative only. The current main line remains the Godot 3D environment and reusable 3D assets. The proposed parallel 3D-versus-pre-rendered-2D sample is not approved and must not be started automatically. Revisit only when the user chooses to evaluate this alternative.

## 2026-10-07: New pixel RPG product goal (M5.1.1)

The user explicitly requests a separate rapid-output pixel JRPG collection covering multidirectional animated characters and broad single-view non-character content. Establish the goal and plan now. The request supersedes the earlier 3D-only active-focus statement for this new work, without cancelling/deleting the 3D project or requiring a 3D-to-2D production method. Proposed edition counts, camera interpretation and animation specifications are not yet approved. Local production and source-only publication rules continue.

M5.1.1 confirmed specifications: orthographic three-quarter top-down on square tiles; eight-direction character movement. Do not reduce to four directions to save production effort.

## 2026-10-07: M5-M9 execution approved

The user explicitly approved the proposed plan ("按此方案开工"). M5.1.1 is complete. Start M5.1.2/M5.2 with the original Mosslight Journey art slice: orthographic square-grid top-down, eight directions, local production. M6-M9 scope remains approved; batch expansion follows the M5 visual gate. Earlier pending-approval statements are historical.

## 2026-10-07: M5.2.3 unified original art direction

User selected original designs inspired by Re:Zero character temperaments/professions, then requested unified items and world aesthetics and authorized proceeding. Set working humanoid roster to 16 (previous 12 superseded), with 16 matching portrait targets. Eight-direction requirements remain. See context/pixel-rpg-art-direction.md. No direct anime-character replication or artwork incorporation. Complete four cross-category style studies before bulk expansion; current sample is not final art acceptance.

## 2026-10-07: M5.2.4 character composition contract

Use separate species, build, face, hair, headgear, profession outfit and color indices. The user's latest corrections take precedence over earlier role/appearance sketches. Normal, strong, slender, frail and heavy are body shapes, not classes; species does not dictate occupation. Provide an explicit run pose set in all eight directions and a separately anchored shadow. Twelve options per appearance category and sixteen curated recipes are the first implementation, not an inflated combinatorial asset count. Monster coverage is currently goblin-type only; broader bestiary remains future scope.

## 2026-10-07: M5.2.5 model-generated art takes precedence

User explicitly says the logic works but the art is unattractive and asks to use the prior local model to generate character illustrations before sprites. Use DreamShaper 8 locally for this bounded trial. Preserve the component/race/build/class specification and engine code, but replace the procedural raster style. User subsequently praises the model generation quality; retain it as the visual direction. No implicit approval of mechanically downsampled sprites, eight-direction consistency or final commercial quality.

## 2026-10-07: M5.2.6 cross-category style acceptance

User requires unified art across the full pack. The praised local character illustration direction anchors drawing/materials; it does not approve mismatched buildings/items, incorrect species/builds or downsampled sprites. Require a common-scale character/building/prop/item pilot before further batch expansion. Current generation is candidate inventory only; no new batch art is delivery-approved. See context/pixel-rpg-art-direction.md and authoring/model-wave-01-review.json.

## 2026-10-07: M5.2.8 shared-rig 3D-to-sprite direction

The user requests recording a future shift toward modular 3D characters, reusable skeletal animation and batch-rendered 2D sprites. This promotes 3D-to-2D from a general alternative to the preferred next character-production validation route. This turn authorizes documentation only; implementation has not started.

Reason: M5.2.7 per-character image generation and frame repairs accumulate character-specific pixels, not transferable motion. AI variation repeatedly changes clothing, proportions and anatomy; completing one character does not establish efficient production of the next.

Target pipeline: local AI concept/design assistance -> editable Blender body and interchangeable hair/clothing/species parts -> compatible shared skeleton and walk action -> fixed orthographic top-down camera, lighting and eight 45-degree headings -> transparent sprite frames/atlases -> Godot SpriteFrames and importing demo. Keep motion separate from appearance. Materials handle color/pattern changes; silhouette changes require geometry. Body proportions, long garments and tails can require corrective weights, poses or auxiliary bones; one action does not mean zero adaptation. Non-humanoid monsters need separate rig families.

Walking is the immediate animation scope; running is deferred. Stop expanding the old per-frame AI animation approach as the default production strategy. Preserve all existing images, scripts and walk/run studies. No demo behavior or existing package was changed by this decision.

Proposed validation: one approved base character and walk cycle, then three appearances (short-outfit swordsman, long-robed mage, humanoid beast with ears/tail) sharing the same action. Compare eight-direction output in Godot and record per-variant adaptation effort. Accept only if later characters reuse the action without individual frame regeneration, retain consistent clothing/proportions, avoid material clipping/sliding, and meet the target sprite art quality. Low-resolution 3D renders are not automatically polished pixel art. Expand to the 16-character roster only after the pilot succeeds. Exact base design, pixel rendering settings and implementation details remain to be settled.

Research basis: [Factorio production workflow](https://www.factorio.com/blog/post/fff-146), [player rendering](https://www.factorio.com/blog/post/fff-218), [Blender Rigify](https://developer.blender.org/docs/features/animation/rigify/), and [Godot retargeting limitations](https://docs.godotengine.org/en/4.7/tutorials/assets_pipeline/retargeting_3d_skeletons.html). These establish existing techniques, not measured quality or throughput for our pack.

## 2026-10-07: poster-cover/M1 side-task research scope

User requests an independent poster/cover task with reference-image editing, separately generated text layers and futureAPI, prioritizing local deployment. Created [the side-task documents](../../dist-poster-pool-projects/projects/poster-cover/README.md) within game-arts; parent game-asset direction remains unchanged. Research recommendation (not an approved implementation): reuse installed RealVisXL/Animagine for visual layers, deterministic SVG/JSON typography for exact editable copy, and compositor exports. New editing/decomposition models are candidates, not automatic downloads. Z-Image remains removed.

## 2026-10-08 — poster-cover/M2.3

User approved download and validation of quantized FLUX.2 Klein4B. FP8 transformer and FP4 text encoder passed local generation/reference-edit tests. Use576x768 as initial default; higher-resolution success did not provide adequate commit margin. Existing-model reuse is no longer a prerequisite. Full poster layer generation/API remain separate work. See side task for source provenance and evidence.

## 2026-10-08 — poster-cover transferred; original route retained

User explicitly requests marking the poster side task as transferred to dist-poster-pool-projects and continuing game-arts' original direction. This is an ownership/status update, not cancellation of the destination project or implementation of new game assets. All poster-cover IDs remain intact but cease to be active/local backlog items. The destination owns current poster records; poster-harness retains code and its Git remote. Historical poster decisions above are retained for provenance and superseded for current ownership/status.

game-arts remains AI-assisted, Godot-first game-art production. Retain scene/asset refinement, realistic/cartoon directions, original M5-M9 scope and the latest M5.2.8 modular 3D/shared-walk/eight-direction sprite plan. Running remains deferred. Sharing model/tool storage does not merge project responsibilities.

## 2026-10-11 — M5.2.8.1 non-destructive Ivara trial

Use the user-supplied Tripo GLB as an inspection and deformation-test source. Keep it unchanged and create trial copies under ignored .local/ivara-rig-study. Automatic decimation is a feasibility aid, not animation retopology. Automatic skinning and approximate anatomical landmarks require pose-based visual acceptance before producing a reusable walk. Do not infer anatomical adhesion from a single mesh object or raw connected-component count.

## 2026-10-11 — M5.2.8.1.1-M5.2.8.1.3 debug elements

The user wants a lower-polygon model with separate clothing and white-body elements, and a covered breathing preview with fixed feet. Preserve high-resolution and 60k references. Use an approximately 20k surface copy for debugging. Explicitly distinguish extracted garment surfaces from newly constructed body proxies: missing underlying anatomy cannot be recovered by simply hiding outerwear. The initial segmentation/proxy is not a finished modular character; boundary cleanup and anatomical fit remain required. Use localized shape keys for this limited breathing check; this does not supersede the shared skeleton/walk production direction.

## 2026-10-11 — M5.2.9 reset to a body-first foundation

User explicitly requests starting over: anatomical base body first, separate clothing/equipment second, then textures, skeleton and movement. The Tripo mesh, rough surface splits and primitive mannequin remain preserved study/reference files only. They are not the new production body. User then narrows the immediate step to researching open human/clothing resources. No installation or production modeling in that research slice. Prefer clear asset-level CC0 candidates, and distinguish software openness from permission to redistribute model assets. Resource selection remains open pending visual/geometry review; see M5.2.9.1 research.

## 2026-10-11 — M5.2.9.2 one standard body before variation

User requests recording that ONE standard body must be made to work first. Preferred foundation is Blender + MPFB/MakeHuman, with a simple independent-game workflow. Review the body first; only then fit one simple outfit, use basic materials, adapt an existing rig and validate idle/walk and engine/sprite output. Do not treat primitive proxy anatomy as the accepted standard body.

Do not require high-poly sculpting, complex baking, cloth simulation, facial animation or a general wardrobe system for this first slice. Texture/UV work should be limited to what the chosen assets need. Parameterized height/build/face/appearance and later species/accessory variation are retained as future possibilities. The previously suggested three-body validation and five-preset expansion are deferred until the one-character baseline is accepted. No software installation, model download or production work is authorized by this documentation-only turn.

## 2026-10-12 — M5.2.9.2 accepted; M5.2.9.5 body-only rig review

User explicitly accepts the white-body proportions and authorizes the next stage. Current sequence is approved body -> skeleton/weights/joint checks -> clothing -> formal animation. Preserve task IDs: execute M5.2.9.5 now; do not renumber to match the changed order. Previous dressed/walk pilot is a reference experiment, not acceptance of wardrobe or animation. No new clothing or walk production in this slice.

Rebuilt the supplied 53-bone game_engine rig directly on the complete approved body, with MPFB weights and preserve-volume deformation. All 13,380 visible vertices have nonzero deform weights (sums 0.999900-1.000000). Static shoulder, elbow, hip/knee and wrist/ankle checks saved at frames 1/10/20/30/40. Upper-body checks leave foot bone positions unchanged. Inspected elbow and hip/knee side renders; full extreme-pose, hand and engine linear-skinning validation remains pending. Skeleton projection is a 2D annotation of actual bone coordinates, not extra geometry. See .local/mpfb-pilot/body-rig-review/standard-body-rig-review.blend and rig-review-overview.png. M5.2.9.5 initial technical binding completed; visual acceptance pending. Original body file preserved.

## 2026-10-12 — M5.2.9.6.7 record animation methodology

User requests preserving the reference/key-pose/timing/whole-body coordination/contact/visual-review methodology and investigating a cheaper central motion source such as video. Record motion acquisition -> solve/cleanup -> standard-body retarget -> artistic correction -> bake/export/reuse as the pipeline framework. Technical rig/export checks remain separate from artistic acceptance.

The proposed combination is licensed library motions for common actions plus video capture for custom gaps. This is a recommendation, not approval of a specific capture product or a full motion-library replacement. Single-camera and multi-camera methods must be distinguished. GVHMR is research-only for current selection because its published license restricts commercial use. Preserve the approved body and all prior trials.
