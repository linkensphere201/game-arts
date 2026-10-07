# Work Log

## 2026-10-02

- [`M1.1.1`] Initialized 12 Markdown documents from `E:\projects\project-manager\project-template` in `E:\projects\game-arts`.
- [`M1.1.1`] Adapted project identity, reading order, safety and commit rules, milestone register, current status, decisions, and architecture placeholders.
- [`M1.1.1`] Retained the reusable prompt, glossary, and research-note skeletons for future use.
- [`M1.1.1`] Verification: checked the 12-file inventory, local Markdown references, source-template preservation, and consistent completed status for `M1` / `M1.1` / `M1.1.1`.
- [`M1.1.1`] Git checkpoint: unavailable because this directory is not a Git repository; no repository was initialized as part of this documentation-only step.
- [`M1`] Remaining input: product goals, scope, constraints, and acceptance criteria. No implementation or asset production has begun.

- [`M1.1.2`] Initialized Git on `main` and configured `origin` as `git@github.com:linkensphere201/game-arts.git`. This resolves the earlier absence of a local repository.
- [`M1.1.2`] Located the global dangerous-command list and corrected its reference in `AGENTS.md`.
- [`M1.1.2`] Prepared the initial documentation checkpoint under the standing automatic-commit authorization; no push performed.

- [`M2.1.1`] Completed initial official-source research on AI workflow concepts, node-based execution, agents, and human review during the conversation.
- [`M2.1.2`] Discussed five monetization models. The user accepted prioritizing samples and a small custom-delivery pilot before workflow productization.
- [`M2.1.3`] Updated README, overview, research notes, milestones, active status, backlog, and decisions; recorded source links and separated evidence from unvalidated hypotheses.
- [`M2.1.3`] Verification scope: documentation diff, local references, task-ID/status consistency, and Git whitespace checks. No implementation tests apply to this documentation-only slice.
- [`M2.1.3`] Remaining questions: customer segment, asset category, acceptance criteria, budget, tools, pricing, and pilot design. No customer outreach, asset production, paid order, or revenue validation has occurred.

- [`M2.1.4`] Recorded the user's hard requirement for local GPU execution in the overview, architecture, research, decisions, and planning records.
- [`M2.1.4`] Kept hardware specifications and model/tool selection pending; no local runtime installation, model download, GPU inspection, or benchmark was performed.
- [`M2.1.4`] Verification: reviewed the documentation diff, requirement/task consistency, and Git whitespace checks; this slice changes documentation only.
- [`M2.1.5`] Incorporated the user's follow-up: Stage 1 produces a finished asset on a local GPU; Stage 2 creates a reusable workflow only if the result is effective.
- [`M2.1.5`] Updated the project entry point and planning records; reserved `M3` and `M4` for the confirmed forward sequence without claiming detailed acceptance approval or implementation progress.
- [`M2.1.5`] Earlier paid-pilot prioritization is retained as history and explicitly superseded for immediate work. Validation: documentation diff and whitespace checks; no runtime changes.

## 2026-10-03

- [`M2.2.1`] Researched official Godot/Unity sprite, import and runtime documentation; proposed independent calibration scenes plus Windows builds.
- [`M2.2.2`] Compared local SDXL/Pixel Art XL, direct sprite-sheet generation, guided frame generation and AnimateDiff alternatives. Recommended a small local-generation plus manual pixel-animation baseline, subject to actual testing.
- [`M2.2.3`] Recorded sources, uncertainty, proposed one-character contract, dual-engine acceptance gates and M3 decomposition. Updated current scope from the earlier icon example to pixel characters.
- [`M2.2.3`] Preserved research-only boundary: no installation, model download, asset generation or engine project creation. Runtime checks are all NOT RUN.
- [`M2.2.3`] Documentation verification: diff/whitespace, local Markdown links and task-status consistency. Normal documentation checkpoint follows under standing authorization; no push.

## 2026-10-04

- [`M3.1.1`, `M3.1.2`] User authorized a Godot-first MVP, then requested ordered steps before execution. Recorded a six-step plan and character brief; Unity is deferred.
- [`M3.1.1`] Started official portable environment and pinned model downloads under project-local `.local/`, with background PID metadata and stdout/stderr logs. Downloads are not evidence of successful local inference.
- [`M3.1.2`] Verified Godot 4.7.2 archive checksum and executable version. Headless calibration passed; an elevated graphical calibration run used NVIDIA OpenGL and passed with a saved render. The initial sandboxed run emitted a certificate-store warning; the graphical run did not.
- [`M3.1.1`, `M3.1.2`] At the user's request, documented exact archive, tool, model, export-template, log and output locations in `production/README.md`, linked from the project README. Large downloads and local runtime directories are ignored by Git.
- [`M3.1.1`] Verified portable runtime/model hashes. SDXL failed under several memory configurations; archived experiment was disabled and original loader restored. DreamShaper 8 succeeded at 512x512 on the local GPU; eight candidates plus one selected-seed replay were completed.
- [`M3.2.1`, `M3.2.2`] Selected seed 420052, removed background/floor, reduced to 64x64, applied art-directed horn/eye and leg edits, and authored 4 idle / 6 walk frames. The animations are cutout/hand-authored motion, not AI-generated action sequences.
- [`M3.3.1`] Packaged relative-path Godot resources and replaced calibration art in the demo. Structural checks, fresh relocated import, pause/animation timing, demo controls, actual rendering and a 60-second Windows run passed.
- [`M3.3.2`] Recorded 23 shared colors, sampled GPU usage up to 3248 MiB, approximately 8.12 s initial / 4.06-4.18 s subsequent candidate generation, and pixel-identical selected-seed replay in the same runtime. No complete labor-time, commercial-quality or market-demand claim.
- [`M3.3.1`] Created local asset/demo ZIPs and Windows executable with integrity manifest. Updated entry point, progress, decisions and validation evidence. Unity and M4 remain deferred; no push performed.
- [`M3.3.1`] Opened the finished Windows demo for user review and stopped the task-owned ComfyUI server after its queue was empty. Downloads and logs remain at the recorded paths; no files were deleted.

## 2026-10-04 — M3.3.3 browser handoff and memory guard

- Added a named DreamShaper browser workflow; it avoids the unrelated Z-Image/Qwen missing-model template. UI loading removed the dependency warning and backend accepted the graph.
- Diagnosed repeated load failures using Windows event 2004; system commit reached 99.40% with no active page file. Preserved sanitized counters and local failure logs.
- Rejected unsuccessful mmap/FP16/pread experiments; restored original model precision and library loading. Added a pre-PyTorch commit-memory gate; current 6.57 GiB headroom is safely rejected against the conservative 10 GiB project budget.
- No third-party package files, system settings, or user apps were changed. Repaired inference is not yet validated; requires more available commit. Godot delivered assets remain independent of this inference runtime.

## 2026-10-04 — M3.3.3 recovery completion

- Verified active 2048 MiB page file and 21.87 GiB available commit after the user's restart.
- Original-entry-point cold generation passed in 8.1 seconds; output RGB pixels exactly match the selected seed. Browser Run passed with cached computation and no missing-model dialog.
- Memory preflight rejection/acceptance boundaries passed; retained direct original ComfyUI startup. Third-party libraries remain unmodified. Chrome-specific behavior was not tested.

## 2026-10-04 — M2.3.1 incremental 3D discussion

Recorded hardware-based feasibility estimates, conventional 3D game-asset stages, optional branches and AI assistance opportunities. Preserved the distinction between upstream model requirements and local validation. The user requested documentation only; the proposed chest/Blender/Godot experiment is not started. No hardware upgrade, software install or new asset production was selected.

## 2026-10-05 - M2.3.2 implementable 3D routes

Researched modular environments, prop modeling, rigged placeholders, editable humanoid bases, skinning/animation and Godot delivery. Recorded primary sources, tool responsibilities, proposed gates/budgets and evidence limits. No installation or production was started.

## 2026-10-05 - M2.3.3 route confirmation

Recorded the user's approval of AI-assisted production: AI concepts/material candidates/scripts, Blender editable authoring, Godot validation and human quality review. Preserve local inference and conditional later workflow formalization. Direct AI 3D generation remains optional for bounded stages. No installation or production started; illustrative first-scene scope remains unselected.

## 2026-10-05 - M2.3.4 manual Godot environment plan

Recorded the user-confirmed environment-before-character sequence and an 11-step editor workflow in context/architecture.md. Compared GLB vs .blend, instances vs GridMap, whitebox CSG, collision shapes, material ownership and optional UV2/light baking. Defined portability, reimport, collision and runtime acceptance. No tools installed or assets produced.

## 2026-10-05 - M3.4.1 / M3.4.2 coastal scene

Authorized outdoor scene, then reduced by user to a small scope. Installed and SHA-256 verified official Blender 4.5.14 LTS portable; no global installation or PATH changes. Authored editable terrain/component Blender sources and six GLBs, then integrated native Godot scenes with 10,147 grass tufts, 212 flower instances and five trees. Final terrain is 40 x 36 m; sea is background. Initial visual checks exposed missing vertex-color use and unsaved headless MultiMesh buffers; corrected with an explicit material override and GPU-backed offline scene construction. Forward+ reduced Compatibility preview clipping and is the final target. Ground ray samples and a 14 m capsule traversal pass. Fresh-copy and exported-runtime checks are the remaining M3.4.3 work.

## 2026-10-05 - M3.4.3 delivery validation

Reopened both Blender sources successfully. Imported the complete source into a new directory without .godot cache, then repeated ray/capsule/camera checks without errors. Exported Windows build ran for 60 seconds, exited 0 and retained three actual screenshots; runtime stderr is empty. Forward+ at 1600 x 900 averaged 4.191 ms over 13,125 post-warmup frames, with presentation capping, not a general benchmark. Corrected a missing export include_filter; the clean re-export SHA-256 matches the executable tested for 60 seconds. Scene uses native snapshots of imported meshes, so later GLB changes need explicit replace/rebuild. User visual acceptance and character production remain pending.


## 2026-10-05 - M3.4.4 source-only publication

The pending local history contains asset binaries and cannot be pushed as-is. Created `.local/source-publish` on `codex/source-only` from remote main `faa1cf2`, copied only 53 approved source/document paths, and excluded 104 tracked asset/output paths. Added resource/output ignore rules and documented that remote clones require asset generation. Original files and commit history remain intact. Audit the entire outgoing lineage before normal fast-forward publication to origin/main.

## 2026-10-07: poster-cover/M1.1.1-M1.1.3 side-task research

Applied create-task template/builder to side-tasks/2026-10-07-poster-cover, with12 English documents and scoped M1-M4 plan. Compared primary-source local models, reference editing approaches, native text versus raster layers, hardware/complete-package constraints and futureAPI boundaries. Existing portrait measurements were labeled historical, not new poster tests. Recommended existing-model layered composition first; klein4B is a conditional editing challenger, AnyText2 optional lettering, Qwen20B alternatives deferred. No weights, inference, service implementation or deletion. Updated parent indexes; checked local document links, placeholders and Git whitespace. Local documentation checkpoints only; no push.

## 2026-10-08 — poster-cover/M2.3

User-authorized quantized Klein install and validation completed. Three pinned weights verified, three local generation/edit runs inspected;576x768 default saved. Source-only checkpoints include reusable workflows and memory-aware runner. Weights/results stay under ignored.local; no push. See side task README for evidence and limitations.
