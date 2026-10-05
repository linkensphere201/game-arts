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
