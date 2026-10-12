# Milestone Register

## Complexity

- Initialization and initial research/documentation slices: Simple.
- Overall project classification: Complex for the proposed local-generation and dual-engine validation scope.
- Planning gate: The user authorized Godot-first implementation on 2026-10-04. The MVP is delivered; Unity is deferred and M4 remains conditional.

For complex work, define the complete known milestone sequence `M1` through `Mn` and approve milestone-level acceptance targets before implementation begins. This register covers completed initialization and initial research/documentation; it is not a complete product implementation plan.

## Numbering Contract

- `M<n>`: milestone.
- `M<n>.<s>`: stable subgoal or work package.
- `M<n>.<s>.<t>`: executable task.
- `M<n>.<s>.<t>.<u>`: optional final decomposition level when required.
- Assign IDs sequentially within their parent.
- Never renumber or reuse an ID after progress reporting or implementation begins.
- Keep cancelled or superseded IDs and mark their final state.
- Reference at least one ID in every active-status, decision, implementation, test, and work-log entry.

## Milestones

| ID | Name | Goal | Acceptance target | Status |
|---|---|---|---|---|
| `M1` | AI documentation initialization | Establish the project documentation skeleton. | All 12 template documents exist, root conventions are adapted, and initial status is consistent. | Complete |
| `M2` | Initial workflow and business research | Establish concepts and a provisional validation direction. | Official sources, evidence limits, user acceptance, and pending questions are recorded. | Complete |

## Decomposition

### M1

- [x] `M1.1` Establish project conventions and working documents.
  - [x] `M1.1.1` Copy and adapt the template; verify file inventory, safety rules, and status consistency.
  - [x] `M1.1.2` Initialize Git on `main`, configure `origin`, and create the initial documentation commit.

### M2

- [x] `M2.1` Establish the initial understanding and business hypothesis.
  - [x] `M2.1.1` Research AI workflows, tools, human review, and agent distinctions.
  - [x] `M2.1.2` Review monetization models and discuss a service-first validation approach.
  - [x] `M2.1.3` Record research sources, user-accepted direction, progress, and next planning questions.
  - [x] `M2.1.4` Record the mandatory local GPU execution constraint and pending hardware validation.
  - [x] `M2.1.5` Record the user-confirmed stage order and supersede immediate paid-pilot prioritization.

`M2` IDs were assigned when recording the completed discussion on 2026-10-02. Completion means the initial research record is complete, not that demand or profitability is proven.

## Future Planning

Define subsequent milestones once the product scope is known. Preserve all completed IDs.

## Confirmed Forward Sequence (Planning)

| ID | Stage | Goal | Acceptance target | Status |
|---|---|---|---|---|
| `M3` | Stage 1: local GPU finished output | Deliver the Godot-first sprite MVP. | Local GPU draft, usable sprite resource, importing demo, fresh import and standalone run verified; visual limitations recorded. | Godot MVP delivered; Unity deferred |
| `M4` | Stage 2: reusable workflow | Formalize the effective production process. | Inputs, dependencies, parameters, human steps, and exports documented; another run confirms usable results. | Conditional on M3 effectiveness |

The user confirmed the order and conditional gate, then authorized the Godot MVP using the documented defaults. Technical delivery is complete; visual acceptance and acceptable overall editing effort remain to be reviewed before M4.

## M2 Technical Research Extension

- [x] `M2.2` Research the minimum local-production and dual-engine experiment.
  - [x] `M2.2.1` Collect Godot and Unity environment/import/build validation options.
  - [x] `M2.2.2` Compare text-to-pixel-character production routes and local candidates.
  - [x] `M2.2.3` Record sources, proposed asset contract, acceptance gates and execution boundaries.

## M3 Decomposition (Updated 2026-10-04)

The known sequence remains M1 initialization -> M2 research -> M3 usable local output -> conditional M4 workflow formalization. The user authorized Godot-first execution on 2026-10-04; the Godot scope is complete. Unity is deferred.

- [x] `M3.1` Establish the local GPU and Godot environments for the first MVP.
  - [x] `M3.1.1` Inventory hardware/software and validate local GPU inference.
  - [x] `M3.1.2` Validate Godot calibration scene and Windows export.
  - Deferred: `M3.1.3` Validate Unity calibration scene and Windows build after the Godot MVP.
- [x] `M3.2` Produce one usable character package.
  - [x] `M3.2.1` Generate and inspect a canonical pixel character; user art acceptance remains separate.
  - [x] `M3.2.2` Author short animations and export the common asset contract.
- [x] `M3.3` Validate delivery and effectiveness.
  - [x] `M3.3.1` Verify fresh import and a runnable Godot build for the authorized MVP; Unity remains deferred.
  - [x] `M3.3.2` Review quality, measured effort and the go/revise/stop decision.

Results: [Validation](../validation/README.md). Godot/local inference checks passed using DreamShaper 8; SDXL failures are recorded separately. M4 remains conditional and no generalized workflow is claimed.

## 2026-10-04 Execution Update

The user authorized M3 execution, prioritizing Godot. M1/M2 remain complete; M3 is in progress; M4 remains conditional. The earlier research-only gate is superseded.

- `M3.1.1`: In progress, RTX 5060 Laptop/8151 MiB/driver 592.27 confirmed. Portable local runtime setup begins.
- `M3.1.2`: In progress, target Godot 4.7.2 stable.
- `M3.1.3`: Deferred; Unity is outside the first MVP.
- `M3.2.1` / `M3.2.2`: Pending; one demon, idle/walk animations.
- `M3.3.1`: Scope adjusted to Godot fresh import/demo validation for this MVP.
- `M3.3.2`: Pending review of actual visual quality and measured effort.

## 2026-10-04 Delivery Update

The six-step Godot MVP is complete. Asset and source demo are tracked; the Windows executable and delivery ZIPs are local ignored outputs. A 60-second standalone run, relocated fresh import, controls and same-runtime selected-seed replay passed. The art is an inspected cutout prototype; user quality acceptance and end-to-end labor economics remain open. The earlier execution-update bullets above describe the start of work, not the current status.

## 2026-10-04 Repair Follow-up

- `M3.3.3`: Supply and verify the DreamShaper ComfyUI browser workflow so the MVP does not route users into an unrelated missing-model template.

M3.3.3 complete: after page-file activation/restart, local generation and browser workflow execution passed. See production recovery record.

## M2.3: Incremental 3D Research

- [x] `M2.3.1` Record local 3D feasibility, the conventional asset pipeline and candidate incremental AI assistance. Documentation complete on 2026-10-04; 3D implementation is not started or authorized. The M3 sprite scope and conditional M4 remain unchanged.

- [x] M2.3.2 Research implementable environment/character routes, tool responsibilities and a gated Godot 3D prototype proposal (2026-10-05). Implementation remains unapproved and not started.

- [x] M2.3.3 Record the user-confirmed AI-assisted production route (2026-10-05). First 3D deliverable remains unselected; no new implementation milestone is started.

- [x] M2.3.4 Research and document the manual Godot environment workflow, acceptance gates and scene-before-character ordering (2026-10-05). Scene production not started.

## M3.4: Sunny Coastal Meadow (2026-10-05)

The user authorized implementation of the environment-first route and selected an outdoor lawn, sunlight and coast. This extends Stage 1 under M3; M4 remains conditional and characters remain deferred. The previous indoor example and exclusion of vegetation/water are superseded for this slice.

- [x] M3.4.1 Author a bounded coastal layout, reusable vegetation/rock resources, terrain, water and sunlight.
- [x] M3.4.2 Integrate editable Godot scenes, camera controls and collision; inspect actual rendered views.
- [x] M3.4.3 Validate fresh import, ground collision and standalone Windows delivery; document controls, source locations and limits.

Acceptance: one self-contained Godot outdoor scene with a broad grassy area, visible vegetation, sunny shadows, beach and sea; working navigation/view controls; actual engine screenshots and error-free representative runtime. Stylized appearance and a 40 x 36 m terrain implement the user request for a small scene, not photorealism. The scene is authored as native editable resources with bounded offline geometry/scatter assistance, not end-to-end generative AI. Blender 4.5.14 is installed with editable source outputs; this slice does not claim mouse-only manual production. No model download or inference is needed.

## Small scene implementation update (2026-10-05)

- [x] M3.4.1: 40 x 36 m coastal terrain and editable Blender/GLB component kit.
- [x] M3.4.2: saved native environment, wind/water, sunlight, free camera and inspected views; final exported screenshots inspected.
- [x] M3.4.3: clean fresh-copy import, physics and 60-second Windows-runtime checks passed; user visual acceptance pending.

Blender is now installed per explicit user request, superseding the earlier not-installed condition. Source-authoring scripts assist Blender modeling and Godot assembly; the result is manually editable but not a mouse-only production demonstration. No characters or M4 automation product started.

- M3.4.4: Prepare and audit source-only remote publication while preserving local resources and history.

## M3.4.5: Coastal visual polish (2026-10-06)

The user requested continued environment polish. First bounded pass: reduce ocean ripple repetition and replace parallel foam lines with broken advancing/receding foam; vary meadow density and soften grass at path/beach edges. Keep the 40 x 36 m terrain, asset shapes and camera views. Save before/after evidence locally, verify shaders in the actual engine, repeat collision checks and refresh the Windows build. Tree/rock silhouette variants and buyer-facing parameter controls remain follow-ups. No remote push or resource staging is authorized by this slice.

M3.4.5 technical pass complete: actual screenshots inspected, collision/control checks passed, and the Windows export ran for 30 seconds without errors. User visual acceptance pending.

## M3.5: Sale-oriented coastal pack candidate (2026-10-06)

User authorized sustained improvement against a sellable-pack standard. This remains Stage 1 under M3, not M4 workflow productization. Known ordered implementation slices:

- M3.5.1: improve silhouettes and ground surfaces; deliver 12 reusable prop variants plus terrain, with Blender source and GLB inventory.
- M3.5.2: self-contained sunward_coast folder, linked GLB wrapper scenes, independent environment controls and asset gallery. No Blender knowledge required for normal placement/tuning.
- M3.5.3: fresh-project copy, source reimport, per-instance settings isolation, physics and representative runtime/quality validation.
- M3.5.4: package candidate archives, provenance, installation/editing guide, scope/limitations, version notes and a sale-readiness checklist. Do not publish listings, select a final commercial license, or claim buyer acceptance without evidence.

Acceptance: usable small 40 x 36 m environment plus reusable props, no external runtime dependencies or project-setting modifications, no original-project path leaks, editable parameters, intact reimport linkage, inspectable screenshots and clean Windows runtime. Keep binaries/resources/output local; commit source and docs only. Existing source-only publication lineage remains separate; no remote push requested.

### M3.5 completion record

- [x] M3.5.1: 16 props plus terrain (expanded from 12), improved vegetation/shore details and ground surfaces.
- [x] M3.5.2: self-contained folder, 17 linked wrappers, independent controls and gallery.
- [x] M3.5.3: fresh import/reimport/isolation/physics/runtime and extracted archive checks; evidence recorded.
- [x] M3.5.4: four local candidate archives, hash inventories, installation/catalog/provenance/terms draft and readiness checklist.

Commercial acceptance gates remain open in RELEASE.md. No characters or M4 productization started.

## M3.6: Root-fixed grass and realistic rock study (2026-10-06)

User requests correction of grass motion and a realism-first rock pass. Continue authorized scene polish in order: M3.6.1 repair root weighting and verify actual rendered motion; M3.6.2 construct one weathered limestone sample with improved silhouette, baked color/normal/roughness and a geometry/material comparison; M3.6.3 integrate the sample, check Godot rendering/import/runtime and record limitations. Preserve small scene, source-only commits and historical candidate ZIPs. Other rock variants follow the evaluated sample; do not claim that subdivision alone produces realism.

M3.6 scope clarification: the user clarified that the second point is primarily a question about the asset pipeline. M3.6.1 remains active. M3.6.2 is exploratory/deferred; a trial bake hit an exporter temporary-directory permission error before GLB/source delivery. The original runtime rock is preserved. M3.6.3 integration is deferred pending a concrete rock-production request; no full realism conversion is authorized by this clarification.

- M3.6.1 complete: imported roots have UV.y=1, causing the old inverted weights. Height-based weighting fixes all 14 root vertices at zero; two deterministic shader renders show different upper-blade positions, and normal-host checks/export pass.
- M3.6.4 complete (direction record): realistic and cartoon routes confirmed; both require detailed texture/material treatment. Future production remains deferred.

## M3.7: Standalone stone asset (2026-10-06)

User approves producing the stone as an independent asset with realistic and cartoon styling. Known authorized sequence: M3.7.1 build one finished silhouette, UVs and baked albedo/normal/roughness; M3.7.2 provide two material styles sharing the same detailed geometry plus original/geometry-only comparison in an independent Godot demo; M3.7.3 validate fresh import/rendering and package asset/source docs. Cartoon is a styling treatment, not reduced completeness. Existing coast remains unchanged. This resumes the deferred rock experiment as standalone delivery rather than coast integration.

M3.7.1 complete: 20,480-triangle bake source reduced to 2,560 triangles, UVs and three 1K maps; packed editable Blender source. M3.7.2 complete: same geometry with realistic/cartoon materials and independent comparison demo. M3.7.3 complete: scoped archives, CRC/hash validation, fresh isolated asset import, actual renders and Windows run. This is a first standalone sample, not a photorealism or sale-readiness claim.

## M3.8: Vegetation/ground continuation

- [x] M3.8.1: inspect current tree/grass/terrain and record concrete production plan and acceptance criteria (2026-10-06).
- [ ] M3.8.2: three-layer 4 x 4 m ground sample, two art routes.
- [ ] M3.8.3: three textured grass clumps, full UVs and independent root weights.
- [ ] M3.8.4: one tree with bark/leaf detail, weighted wind and inspected distant representation.
- [ ] M3.8.5: combined sample/fresh-copy tests, comparable profiling and packaging.

Current turn investigates how to handle these categories; new assets are not yet generated. Detailed plan is in context/architecture.md. Prior stone/coast remain intact.

### M3.8 first-sample delivery (2026-10-06)

- [x] M3.8.2: two ground treatments, three 1K material layers, 4 x 4 m patch with normalized weights and collision.
- [x] M3.8.3: three textured clumps, independent root weights, batch placement and inspected rendering.
- [x] M3.8.4: textured near/far tree, separate bark/leaves, rooted wind, trunk collision, two surface treatments.
- M3.8.5: independent archive imports, package audits, visual inspection and final 30-second Windows run complete. Controlled comparative performance profiling and external art acceptance remain follow-ups; no measured optimization speedup is asserted.

These are first review samples. No coast-wide replacement, finalized commercial acceptance or new M4 workflow productization.

- [x] M3.8.6: capture and inspect an AAA grass reference against the current realistic sample; record cartoon acceptance and realistic-only refinement priorities (2026-10-06). Asset refinement itself remains follow-up.

## M3.8.7: Realistic grass refinement (2026-10-06)

User authorized implementing the M3.8.6 reference findings. Sequence: isolate realistic meshes/maps from accepted cartoon assets; improve blade shape and mixed clumps; soften placement transitions; inspect same-camera Godot captures and rooted wind, then validate standalone import/runtime. Keep the 4 x 4 m sample scope and local-only generated assets.

M3.8.7 first refinement delivered: isolated geometry/maps and improved scatter; same-camera captures and phase/relit views inspected; standalone grass/demo imports and exported Windows run pass. Cartoon resource hashes unchanged. Seed heads, additional species, distant aliasing and ground-contact polish remain open art follow-ups.

## M3.8.8: Mixed grass silhouettes (2026-10-06)

User requests upright and curved leaves with visibly varied widths/heights instead of uniformly arched grass. Implement approximately 50% upright, 35% gently curved and 15% strongly curved blades within each clump, independently mix three width classes and heights. Preserve cartoon assets. Verify geometry distribution, roots, same-camera screenshot and exported runtime.

M3.8.8 complete for this iteration: reference_meadow / upright_meadow / wind_swept authoring presets, independently mixed bend/width/height, validated roots and unchanged cartoon hashes, same-camera exported capture, standalone package imports. User art acceptance remains open.

## M3.8.9: Realistic ground refinement (2026-10-06)

User authorized the 4 x 4 m ground/grass sample pass: irregular soil/turf/sand blending, fine surface detail, sparse gravel and dry litter, parameterized ground styles. Keep cartoon resources unchanged. Validate standalone ground import/collision and actual Godot views. Prioritize material/contact before terrain displacement; keep the ground plane flat so existing grass remains planted.

M3.8.9 first pass complete: separate realistic geometry/shader/maps and ground presets, inspected exported ground/grass views, unchanged cartoon hashes, normalized weights/collision structure and fresh ground/demo import checks. Technical sample delivery, not final art acceptance.

- [x] M3.8.10: download and inspect a free nature-kit baseline; verify representative Godot imports and record product comparison criteria (2026-10-06).

## New pixel JRPG product (2026-10-07, M5-M9)

Classification: complex. User authorized establishing a new rapid-output product goal. The concrete sequence below is proposed for approval before implementation, per the project planning gate. M1-M4 remain historical/conditional and are not renumbered. The current active planning focus is the new pixel JRPG pack; existing 3D work is preserved. See context/architecture.md for counts, assumptions and acceptance.

| ID | Milestone | Acceptance | Status |
|---|---|---|---|
| M5 | Art and engine contract | Representative protagonist eight-direction movement, tile sample, 12 props and one Godot room; camera/scale/palette and motion quality reviewed before expansion | Proposed |
| M6 | Character collection | 12 humanoids, 8 enemies, 4 animals, multidirectional idle/walk; limited battle actions and 12 portraits, consistent anchors/identity | Proposed |
| M7 | Environments and scene assembly | Five environment kits, 64 total props including M5 samples, connected showcase areas, verified transitions/collision/sorting | Proposed |
| M8 | Items, UI and effects | 96 icons, 32 UI elements and 12 animated effects, demonstrated in inventory/shop/dialogue/combat examples | Proposed |
| M9 | Complete delivery | Coverage audit, art/motion review, fresh import, Windows run, PNG/source/Godot packages and buyer instructions | Proposed |

Executable entry tasks:
- M5.1.1: settle projection, direction count and first-edition scope; record approval.
- M5.1.2: define original visual guide, palette, naming/catalog and pixel/anchor contract.
- M5.2.1: author the first character directional idle/walk set and review moving previews.
- M5.2.2: author representative terrain/props and integrate the single-room sample.
- M5.3.1: validate and review the first slice before scaling M6-M8 production.

No batch asset generation starts on an unapproved plan. Counts are proposals, not completed inventory or guaranteed turnaround.

M5.1.1 clarification: user confirmed orthographic square-grid top-down and eight movement directions. Edition counts and M5-M9 acceptance sequence still await scope approval.

## 2026-10-07: M5-M9 execution approved

The user explicitly approved the proposed plan ("按此方案开工"). M5.1.1 is complete. Start M5.1.2/M5.2 with the original Mosslight Journey art slice: orthographic square-grid top-down, eight directions, local production. M6-M9 scope remains approved; batch expansion follows the M5 visual gate. Earlier pending-approval statements are historical.

### M5 implementation checkpoint (2026-10-07)

M5.1.2 complete. M5.2.1/M5.2.2 initial samples implemented; M5.3.1 technical validation passes, visual review pending. See pixel-rpg-demo/README.md for exact inventory, reproduction and limitations. M6-M9 remain approved future scope, not completed assets.

### M5.2.3 — Unified character/item/street art study

Authorized 2026-10-07. Produce four original character studies, representative equipment/items and one town street scene under a shared art direction, then review before batch expansion. Initial assets and technical integration complete; art acceptance pending. M6 humanoids/portraits target revised from 12 to 16 within the user's requested 10-20 range. Original M5-M9 sequence remains in force; other inventory counts remain unchanged.

### M5.2.4 — Modular character redesign

User explicitly rejected insufficient character differentiation and authorized a component-based redesign: 12 options in each requested appearance category, profession outfits, five body builds, human/beastfolk/elf/monster/dragonborn archetypes, separate shadows, eight-direction idle/walk/run. Technical implementation and sixteen preset studies completed; detailed art acceptance pending. Walk/run now use eight frames each for these characters; previous humanoid animation counts are historical. This is a replacement character foundation, not evidence that M6 portraits/battle actions or all M7-M9 scope is done.

### M5.2.5 — Model-first illustration and sprite study

Authorized by user after rejecting M5.2.4 art quality while accepting its logic. Sequence: local-model illustration -> select/retain character design -> transparent sprite/pixel cleanup -> review perspective/scale -> directional idle/walk/run -> Godot replacement. Four illustrations and two refinements generated; user accepted their illustration quality. Initial static resolution comparison produced. Final sprite quality and directional animation remain incomplete; previous procedural character art is not the accepted visual foundation.

### M5.2.6 — Apply model-first route across asset categories

User authorizes replacement work across characters, clothing, buildings, props and items. Ordered execution: M5.2.6.1 audit and explicit batch/provenance manifest; M5.2.6.2 local original-art generation and targeted retries; M5.2.6.3 reviewed segmentation/sprite conversion; M5.2.6.4 isolated Godot static-art review. This creates a first replacement batch, not completion of the wider M6-M9 inventory or directional animation. Maintain original images and per-asset status. Do not regenerate accepted mechanics solely to change appearance.

### M5.2.7 — Directional garment and identity study

Continue the approved character replacement work: reconstruct rear/side/diagonal clothing and anatomy from the same design before eight-direction animation. User explicitly rejects changing body direction without clothing direction. M5.2.7.1: rear clothing guide and local-model study; M5.2.7.2: side/diagonal views and identity review; M5.2.7.3: coherent walk/run pose construction and engine verification. These are execution subdivisions of existing scope, not new or reduced product goals.

### M5.2.8 — Shared-rig 3D-to-sprite pilot (planned)

2026-10-07: User confirms recording this as the future production direction; implementation not started. Preserve M5.2.7 results as studies; per-frame AI animation is superseded as the default expansion strategy, and running is deferred.

- M5.2.8.1: Define and review one modular base character with consistent front/side/back rendered appearance.
- M5.2.8.2: Bind a compatible skeleton and author one reusable walk cycle.
- M5.2.8.3: Validate three appearances (short outfit, long robe, beast accessories) with the shared action; measure adaptation effort.
- M5.2.8.4: Batch-render eight headings with stable canvas/foot anchor and import into Godot; review visual quality, clipping, grounding and repeatability before roster expansion.

These are proposed execution steps within the existing M5-M9 product scope, not completed tasks. See the M5.2.8 decision for limits and acceptance criteria.

## Transferred milestone namespace — poster-cover (2026-10-08)

Status: TRANSFERRED to dist-poster-pool-projects. The following dated entry is historical; its pending approvals and statuses are not current game-arts tasks. Consult the destination register for current status. Preserve poster-cover/M1-M4 without renumbering; game-arts M1-M9 and the M5.2.8 character direction continue unchanged.

### Historical registration (2026-10-07)

Complex side task with its own qualified namespace, `poster-cover/M1` through `poster-cover/M4`; these do not renumber or replace parent M1-M9. [Local register](../../dist-poster-pool-projects/projects/poster-cover/tasks/milestones.md): M1 research and scope (research completed), M2 layered-poster validation (proposed), M3 reusable local workflow (proposed), M4API (proposed). User authorized task creation and research. M2-M4 execution targets await review before implementation; no new model downloaded.

- 2026-10-08: independent `poster-cover/M2.3.1-M2.3.3` completed (pinned quantized Klein installation, local generation/edit measurements and workflow handoff). This is a bounded feasibility slice, not completion of full layered-poster M2 or API M4.

## 2026-10-11 — M5.2.8.1 Ivara local inspection trial

User authorized trying the inspection/animation-preparation route on production/pixel-rpg/tripo-3d-dl/ch_ivara.glb. Preserve that source byte-for-byte. M5.2.8.1 is now in progress: inspect anatomy using multiple views, measure mesh structure, and test a reduced copy with automatic weights and diagnostic poses. This bounded experiment does not mark the shared walk, three-appearance reuse or Godot acceptance complete.

M5.2.8.1 trial result (2026-10-11): inspection and automatic-rig feasibility experiment completed; original preserved. Reduced copy and exported diagnostic motion verified, but chest/jacket deformation prevents visual rig acceptance. M5.2.8.1 review and M5.2.8.2 reusable walk are not complete. See production/pixel-rpg/ivara-rig-study.md.

### 2026-10-11 — M5.2.8.1 refinement scope

User requests hidden outerwear/equipment with retained inner clothing and fixed-foot gentle breathing, then a lower-polygon debugging copy and separate clothing/body objects. New execution subdivisions:

- M5.2.8.1.1: 20k-triangle debugging copy, preserving the original and 60k trial.
- M5.2.8.1.2: Separate visible clothing/equipment surfaces and construct an explicitly labeled independent white mannequin where underlying anatomy is absent; review boundaries and fit.
- M5.2.8.1.3: Restrained covered breathing study, fixed feet, with measured vertex displacement. This supersedes the arm/leg stress action as the requested immediate preview, not the long-term shared-walk goal.

## 2026-10-11 — M5.2.9 body-first character rebuild

User explicitly rejects continued repair of the generated clothed mesh as the production foundation. Preserve M5.2.8.1 and its children as superseded reference experiments, not accepted production body/garments. Do not renumber those IDs. The body-first order below is user-directed; current authorization is narrowed to resource research before further implementation.

- M5.2.9.1: Research reusable open human/clothing/equipment resources and exact licenses. Completed as a source review; no downloads or local geometry validation.
- M5.2.9.2: Select/adapt a continuous anatomical base body and review front/side/back, proportions and topology. Not started.
- M5.2.9.3: Independently model/adapt clothing and equipment around the accepted body. Not started.
- M5.2.9.4: Finalize detail/low-poly topology as needed, UVs, baking and textures. Not started.
- M5.2.9.5: Skeleton, skinning and deformation checks. Not started; dependent on preceding model stages.
- M5.2.9.6: Animation, shared-action validation, eight-direction renders and Godot review. Not started. Preserve the original shared-rig/reuse objective; running remains deferred.

### 2026-10-11 — simplified single-standard-body gate

Current M5.2.9.2 scope: one standard MPFB/MakeHuman-based body, editable and anatomically complete, with reviewed proportions and front/side/back views. Not started; no installation or body acceptance claimed. M5.2.9.3-M5.2.9.6 follow sequentially for one outfit and one character only. For M5.2.9.4, prefer existing UVs and simple materials; high-poly sculpting and elaborate baking are optional, not required deliverables. Reuse an existing rig at M5.2.9.5, then validate idle/walk at M5.2.9.6. Parameterized multi-body production and cross-character action reuse are deferred until the single-character baseline works. Preserve existing IDs and historical scope, but apply this narrower current gate.

## 2026-10-12 — M5.2.9.2-M5.2.9.6 single-character technical pilot

User expands authorization from body-only testing to one full body/clothing/equipment/rig/movement pilot. MPFB 2.0.18 pinned source loaded locally; one continuous adult male body created and three views inspected. Independent CC0 sweater, trousers, boots and sword fitted with existing UV/materials. Built-in 53-bone game_engine rig and interpolated garment weights; corrected initial waist overlap and knee pole direction. Packed editable stages, 31,418-triangle five-mesh GLB, Idle/Walk and actual Godot demo now exist under ignored .local/mpfb-pilot/character-v1.

M5.2.9.2-.5 have a working technical baseline, with artistic acceptance pending. M5.2.9.6 remains in progress: idle/walk import and sampled foot-motion tests pass; actual Godot viewport capture inspected. Gait/contact polish, eight-direction sprites and cross-character reuse are not complete. White-clay bald anatomy and generic existing wardrobe are intentionally provisional, not final anime game art. Preserve all prior Tripo studies. See production/pixel-rpg/mpfb-character-pilot.md for exact source licenses, commands, outputs and limitations. No resources committed; no push.

## 2026-10-12 — M5.2.9.2 accepted; M5.2.9.5 body-only rig review

User explicitly accepts the white-body proportions and authorizes the next stage. Current sequence is approved body -> skeleton/weights/joint checks -> clothing -> formal animation. Preserve task IDs: execute M5.2.9.5 now; do not renumber to match the changed order. Previous dressed/walk pilot is a reference experiment, not acceptance of wardrobe or animation. No new clothing or walk production in this slice.

Rebuilt the supplied 53-bone game_engine rig directly on the complete approved body, with MPFB weights and preserve-volume deformation. All 13,380 visible vertices have nonzero deform weights (sums 0.999900-1.000000). Static shoulder, elbow, hip/knee and wrist/ankle checks saved at frames 1/10/20/30/40. Upper-body checks leave foot bone positions unchanged. Inspected elbow and hip/knee side renders; full extreme-pose, hand and engine linear-skinning validation remains pending. Skeleton projection is a 2D annotation of actual bone coordinates, not extra geometry. See .local/mpfb-pilot/body-rig-review/standard-body-rig-review.blend and rig-review-overview.png. M5.2.9.5 initial technical binding completed; visual acceptance pending. Original body file preserved.

## 2026-10-12 — M5.2.9.6 first action set authorized

User asks the agent to audit the rig and proceed if usable. Scope: white-body Idle/Breath, Walk, Turn, Run, Jump, separate left/right hand attacks, light-hit half-step retreat and heavy-hit 4-5-step retreat. Running is explicitly re-authorized for this slice. Deliver 90-degree left/right turns and five-step heavy retreat as concrete first-pass interpretations. No wardrobe expansion.

- M5.2.9.6.1: Audit binding, hierarchy, symmetry and representative linear-skinning poses before action production.
- M5.2.9.6.2: Idle, Walk, TurnLeft/TurnRight, Run and Jump; contact and loop checks.
- M5.2.9.6.3: AttackLeft/AttackRight, HitLight and five-step HitHeavy; readable timings and displacement checks.
- M5.2.9.6.4: Bake reusable clips, import into a selectable Godot preview, capture actual playback and document limitations.

These extend the previously accepted milestone without renumbering. Agent may resolve routine technical issues and iterate without asking for each pose; final artistic quality must be reported separately from structural test success.

### 2026-10-12 — M5.2.9.6.1-M5.2.9.6.4 first-pass delivery

Rig audit passes (53 bones, 13,380 weighted visible vertices, mirrored rest joints, no zero-length bones). Created ten white-body clips: Idle, Walk, TurnLeft/Right, Run, Jump, AttackLeft/Right, HitLight and five-step HitHeavy. Corrected unreachable running targets, NLA time origin, Godot optimizer drift, arm bend-plane twisting and bounded shoulder weights. Approved body geometry and original rig source preserved.

All source motion-intent checks and every-frame imported ankle comparisons pass; maximum Godot ankle difference about 0.00000231 m. Actual GPU capture completed with empty error log. Initial sandbox editor/log path warnings remain environmental. Idle markers stay fixed; Walk/Run support markers match configured travel speeds; turn endpoints +/-90 degrees; jump peak root height 0.339 m; light one-step root retreat 0.08 m; heavy five lifts/root retreat 1.08 m.

Deliverables are ignored under .local/mpfb-pilot/action-set-v1: editable Blender source, ten-clip GLB, selectable Godot review, GIFs and phase sheets. See production/pixel-rpg/body-action-set.md. This completes the requested first-pass action coverage and technical preview, not final artistic animation acceptance or the broader sprite milestone. Shoulder silhouette, finger pose, foot roll/pivots, impact strength, transitions and gameplay integration remain refinement items. No clothing expansion, sprite batch, resource commit or push.

## 2026-10-12 — M5.2.9.2.1 approved stylized proportion branch

Extend M5.2.9.2 with a separate manga proportion study authorized by the user: approximately 6-6.5 heads, lighter torso and longer limbs, informed by Breath of the Wild / Tears of the Kingdom. Preserve the previously accepted base and action set. Static editable candidate and comparison renders delivered; visual acceptance pending. Bone refitting and contact recalibration follow body review, not included in this static slice.

## 2026-10-12 — M5.2.9.2.2 facial geometry study

Authorized refinement of the proportion variant: lower forehead, short chin, large eyes, tapered oval face. Independent reversible face shape key and neutral eyeballs, matched multi-view renders and source-preservation/symmetry checks. Static candidate delivered for visual review; no expression or animation completion claim. Earlier M5.2.9.2.1 preserved.

## 2026-10-12 — M5.2.9.2.2 rejected; pre-face appearance restored

User rejected the manga face as unnatural and requested the before appearance. M5.2.9.2.2 is rejected/superseded, not awaiting approval. Current editable body: `.local/mpfb-pilot/restored-body/current-base-body.blend`, with Manga_face=0 and Manga_6_25_heads=1. Neutral test eyes retained to match the before comparison; no new facial deformation active. The original proportion-only file remains `.local/mpfb-pilot/stylized-body-v1/stylized-base-body.blend`. Prior face trials retained as inactive experiments. Do not continue facial stylization without a new user request.

## 2026-10-12 — M5.2.9.6.5 adapt first action set to restored body

Authorized and technically completed: fit existing rig/weights to the restored proportion variant, rebuild the ten action clips, verify source contacts/reach and Godot import, and deliver actual playback previews. Current output restored-body-actions-v2. Facial stylization remains rejected. Artistic motion polish, wardrobe and broader sprite milestone remain separate; do not mark those complete.

## 2026-10-12 — M5.2.9.6.6 four Quaternius samples

Authorized limited trial: inspect the free Standard library/license, compare skeleton structures, retarget four representative actions and preview in Godot. Technical experiment delivered under .local/quaternius-pilot/retarget-v2; user visual review pending. Preserve prior action set. Full library import, weapon props, final contact/skin cleanup and commercial acceptance are outside this slice.

## 2026-10-12 — M5.2.9.6.7 methodology and video-motion feasibility

Documentation/research completed: record animation authoring methodology, evaluate MediaPipe, FreeMoCap and GVHMR using official sources, and outline a short video-to-current-body pilot. Local installation, capture, performance testing and production tool selection remain unstarted. No full-library or body replacement.

## 2026-10-12 — M5.2.9.6.8 expanded Quaternius adaptation

User approves replacing available motion categories with Quaternius and retaining custom turn/hit work. Execute ten source clips (idle, walk, jog, sprint, three jump phases, jab, cross, sword) on the approved current body, retaining four previous turn/hit drafts in the same review project. Verify Godot import and actual playback, report quality limitations separately. This slice does not implement gameplay jump physics, animation state transitions or final contact/skin polish. Video capture stays deferred; existing motions are sufficient for the current prototype.

### M5.2.9.6.8 technical adaptation completed

Delivered .local/quaternius-pilot/expanded-v1: ten Quaternius clips plus four previous turn/hit drafts, editable Blender/GLB, scrolling Godot preview and 14 actual-playback GIFs. Left Jab/right Cross confirmed from source movement and phase review. All 14 Godot sampled ankle comparisons pass (max 0.000001456 m), capture completes with empty stderr. Jump remains three separate phases. Final contacts, skin polish, transitions and gameplay integration remain pending. See production/pixel-rpg/body-action-set.md. Existing motions suffice; video capture remains deferred.

## 2026-10-12 — M5.2.9.6.9 two-step off-balance heavy hit

User requests lateral upper-body imbalance during backward movement and exactly two retreat steps. Replace only the heavy-hit draft in a new copy of the expanded review; preserve light hit and all Quaternius clips. Stage impact/side lean, two recovery steps, and settling. Verify step count, planted-foot stability, reachable leg targets and actual Godot playback. Do not alter the approved body or prior deliverables.

### M5.2.9.6.9 revised heavy-hit draft delivered

Current review is .local/quaternius-pilot/stagger-v1. Heavy hit now leans laterally, retreats exactly two steps and settles in 1.9 s; previous five-step heavy-hit requirement is superseded. Light hit and thirteen other clips unchanged. Lift count, support-ankle stability, leg reach, Godot import and actual playback checks pass. New GIF: HitHeavy_Stagger2.gif. Visual acceptance and gameplay transitions remain pending.

## 2026-10-12 — M5.2.9.6.10 walk shoulder correction

User reports shoulders protruding backward during walk. Close rear/side comparisons isolate excessive retargeted clavicle rotation; upper-arm twist attenuation alone does not resolve the silhouette. Apply a walk-only clavicle rotation correction, preserve mesh/weights and other actions, verify actual playback and rebuild the standalone EXE.

## 2026-10-12 — M5.2.9.6.11 natural walk arms and hand clearance

User rejects the shoulder-only walk correction because hands intersect the body and do not hang naturally beside the legs. Preserve the relaxed clavicles, but re-author walk upper limbs with nearly extended elbows, relaxed hand/finger rest poses and small opposite-leg pendulum motion. Inspect the full cycle and preserve every other clip.

## 2026-10-12 — M5.2.9.6.12 reusable hand poses and orbit review

User authorizes only Relaxed and Fist hand poses, applies Relaxed to walk, and requires multi-angle full-circle inspection before showing results. Build finger-only reusable poses plus closeup review clips, preserve other motion, inspect both hands at eight azimuths and walking in context. User also requests a reusable Blender orbit screenshot skill canonically in E:/projects/skills, installed locally and committed after completion. Keep skill and game-art repository commits separate; do not push.

### M5.2.9.6.12 implementation complete; user visual review pending

Delivered two reusable hand poses, relaxed-hand walk, sword-grip-derived Fist (correcting the rejected thumb), 16-clip Godot review and standalone EXE. Both hands inspected at eight azimuths; walk contact phases checked around the body. Transform isolation, mesh/weight preservation, pose-reference matching, sampled lateral clearance, Godot import and actual startup pass. Orbit skill committed separately in E:/projects/skills. See tasks/active.md for exact artifacts and limitations.
