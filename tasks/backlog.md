# Backlog

## Delivered Godot MVP

M3.1.1, M3.1.2, M3.2.1, M3.2.2, M3.3.1 and the technical results of M3.3.2 are complete for the Godot-first scope. See [active status](active.md).

## Follow-up Candidates (Not Started)

- M3.3.2: Collect user feedback on silhouette, colors, stance and cutout motion; decide what quality improvements matter.
- M3.1.3: Add Unity validation when requested; reuse the common PNG contract.
- M4: Only after the asset is useful with acceptable editing effort, validate a second character and formalize reusable steps. Segmentation and pose authoring currently contain character-specific choices.
- M4: Consider extra views, attack/death animations, packaging standards or tooling after the first asset is reviewed.
- Later commercial work: check model/input/output terms, marketplace requirements, target buyers and pricing independently of technical success.

Do not automatically reopen SDXL compatibility work, alter system virtual memory, purchase tools, publish assets or push commits. Retain existing downloads until file removal is explicitly authorized.

## Incremental 3D Candidate (Not Started)

- Follow-up to `M2.3.1`: consider a simple geometric prop through concept -> Blender mesh/material -> rigid-part animation -> GLB -> Godot. A chest is illustrative, not confirmed. Select scope and acceptance criteria before implementation; do not automatically install 3D tooling or download weights. See [research record](../context/research-notes.md#2026-10-04-incremental-3d-asset-production-m231).

- M2.3.2 follow-up: select style/camera, asset ownership approach and first playable slice. Proposed order: graybox -> original interactive prop -> environment kit -> original biped -> fresh-import/export validation. See the 2026-10-05 research record; this is not an implementation commitment.

- M2.3.4 supersedes the earlier interleaved prototype order: select a bounded environment and manually validate whitebox -> one Blender/GLB module -> reusable kit -> Godot composition/collision/lighting -> fresh import and export. Character production follows environment acceptance.

- M3.4 follow-up: review the small coastal scene with the user before character work. If iterative source changes become frequent, replace native mesh snapshots with linked GLB wrappers; do not start workflow productization solely because this scene runs.

- M3.4.5 follow-up: improve tree/shrub silhouettes and introduce a few coherent variants; add ground-surface detail and then approachable Godot controls. Keep the first scene compact and defer characters until the environment is accepted.

- M3.6.2/M3.6.3: Deferred rock study and integration. When production resumes, validate a surfaced sample before broad replacement; retain separate realistic/cartoon evaluation under M3.6.4.
- M3.6.4: Future asset art must follow either the realistic or cartoon route with finished surface detail. Decide sample/reference, camera distance and texture budget at implementation time; both full asset sets are not started.

- M3.8.2-M3.8.5: follow the vegetation/ground sample sequence and acceptance criteria in context/architecture.md; prioritize grounded surface/grass blending before full tree production and coast replacement.

## Alternative delivery route: 3D-rendered 2D assets (2026-10-06)

- M3.8.10 follow-up, deferred/not started: potentially reuse Blender assets to render consistent fixed-view transparent images for Godot 2D scene assembly. Consider camera/projection, scale, tile transitions, shadows and sorting when revisited. This is an optional future product direction, not a change to the current Godot 3D scope; no comparison prototype is authorized.

## 2026-10-07: M5.2.8 future character production pilot

Prioritize the shared-rig modular 3D-to-sprite pilot described in decisions.md and milestones.md. Validate one walk action across three appearances before expanding to 16. Determine base proportions, module/rig compatibility, pixel rendering treatment and measured adaptation cost. Running remains deferred. Preserve all prior studies; no implementation, downloads or asset replacement in this documentation slice.

- TRANSFERRED (2026-10-08): poster-cover/M1.2.1 and later poster scope belong to [dist-poster-pool-projects](../../dist-poster-pool-projects/projects/poster-cover/tasks/milestones.md); no game-arts follow-up is queued.

- TRANSFERRED (2026-10-08): poster-cover/M2.3/M2.4/M4.1 results and remaining work are maintained in the destination. These IDs are historical references, not local backlog.

## 2026-10-11 — M5.2.9 deferred parameterized character expansion

After acceptance of one standard body and the simple single-character production path, evaluate bounded body/face/appearance parameters and shared outfit/action reuse. Normal, strong, slim, frail and heavy presets, species accessories and batch generation remain deferred ideas. Do not start with a three-body comparison or build a general character/wardrobe system before the baseline works.
