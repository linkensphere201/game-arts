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

## 2026-10-07: poster-cover/M1 side-task research scope

User requests an independent poster/cover task with reference-image editing, separately generated text layers and futureAPI, prioritizing local deployment. Created [the side-task documents](../side-tasks/2026-10-07-poster-cover/README.md) within game-arts; parent game-asset direction remains unchanged. Research recommendation (not an approved implementation): reuse installed RealVisXL/Animagine for visual layers, deterministic SVG/JSON typography for exact editable copy, and compositor exports. New editing/decomposition models are candidates, not automatic downloads. Z-Image remains removed.

## 2026-10-08 — poster-cover/M2.3

User approved download and validation of quantized FLUX.2 Klein4B. FP8 transformer and FP4 text encoder passed local generation/reference-edit tests. Use576x768 as initial default; higher-resolution success did not provide adequate commit margin. Existing-model reuse is no longer a prerequisite. Full poster layer generation/API remain separate work. See side task for source provenance and evidence.
