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

## Independent poster/cover side task (2026-10-07)

Complex side task with its own qualified namespace, `poster-cover/M1` through `poster-cover/M4`; these do not renumber or replace parent M1-M9. [Local register](../side-tasks/2026-10-07-poster-cover/tasks/milestones.md): M1 research and scope (research completed), M2 layered-poster validation (proposed), M3 reusable local workflow (proposed), M4API (proposed). User authorized task creation and research. M2-M4 execution targets await review before implementation; no new model downloaded.

- 2026-10-08: independent `poster-cover/M2.3.1-M2.3.3` completed (pinned quantized Klein installation, local generation/edit measurements and workflow handoff). This is a bounded feasibility slice, not completion of full layered-poster M2 or API M4.
