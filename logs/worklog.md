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

## 2026-10-06 - M3.4.5 visual iteration

Inspected the actual overview and prioritized repeated water highlights/parallel foam and uniform grass scatter. Replaced the water shader with noise-warped waves, distance detail fade and a broken moving shore front; added spatial meadow density/tint and soft path/beach verges. Regenerated local scenes (6,202 grass tufts, 184 flowers, five trees), retained the 40 x 36 m bounds and cameras. Same-view screenshots are retained in validation/coast-polish; initial render and 20-ray/14 m capsule/camera checks pass. Resource outputs are deliberately not staged under the source-only policy.

Final M3.4.5 export ran for 30 seconds, exited 0, stderr empty. Mean sampled frame time 4.248 ms at 1600 x 900 with presentation capping. Windows executable and local source ZIP refreshed. No remote push.

## M3.5.1-M3.5.2 implementation checkpoint (2026-10-06)

Created 16 distinct prop meshes plus closed terrain, editable Blender sources, linked GLB wrappers, ground/water/grass shaders, an isolated sunward_coast package, gallery and per-instance controls. Added wet sand, blue flowers, reeds, driftwood, pebble clusters and a timber bench. A fresh folder-only project passes 17-wrapper and two-instance isolation checks. A copied tree GLB widened by 20% updates through reimport without changing wrapper/collider configuration; geometry-dependent colliders still require review after mesh edits. Final visual/performance/package checks continue under M3.5.3/M3.5.4.

## 2026-10-06 - M3.5.3/M3.5.4 candidate verification and packaging

Inspected actual gallery, overview, meadow, beach and bilingual-panel captures. Exported High/Low/panel runs exited cleanly. High mean frame time 6.13 ms vs Low 6.01 ms, p95 both 8.33 ms; short differing-duration runs do not demonstrate a material optimization speedup. Added buyer quickstart, source/reimport/collision limits, 17-model catalog, provenance and pending commercial terms. Exported engine/third-party notices from the engine itself. Created four local ZIPs with file hashes and CRC checks; audited pack resource references for self-containment. Extracted demo imported and ran independently; sandbox certificate-store error resolved by normal-host validation and retained in logs. Technical RC delivered; owner art approval, independent buyer trial and final commercial terms remain open. Resource/binary changes remain unstaged; no remote push.

## 2026-10-06 - M3.6.1/M3.6.4 feedback

Confirmed actual GLB root UV.y=1; replaced UV-based grass wind/color height with local Y/0.55. Production-shader capture at two fixed times passes with 14 zero-weight root vertices and visible moving tips. Host validation/import/export clean; initial sandbox user-log/certificate errors retained. Windows exe refreshed; prior candidate ZIPs unchanged. Rock trial map bake ran, but export failed with a temp-directory access error; preserved original GLB and redirected draft recipe to isolated rock-study output after user scope clarification. No complete realistic asset claim. Recorded realistic/cartoon routes with required surface detail in overview, architecture, decisions and backlog.

## 2026-10-06 - M3.7 independent stone

Delivered one independent stone with 1,282 source vertices / 2,560 triangles, three 1K baked maps and two Godot material styles. Blender packed-texture GLB export failed on temporary-file permissions; geometry-only export plus explicit external texture bindings succeeded. Fixed demo construction order so camera exists when runtime script readies. Inspected comparison and individual rendered views, reduced excessive normal strength and improved closeup framing. Four local archives pass CRC/per-file hash checks; asset-only ZIP imported independently and passed mesh/texture/collision checks. Windows demo completed scripted captures without reported errors. First material study remains open to art review; no photogrammetry claim or coast replacement.

## 2026-10-06 - M3.8.1 vegetation and ground inspection

Inspected actual GLB texture/material/UV channels and authoring/runtime shaders. All three examined assets have zero embedded images; grass UV U is constant zero. Current tree uses opaque crown lobes; terrain uses palette colors/noise. Recorded distinct modeling/UV/material/wind requirements, per-surface tree override constraint, two-style art treatment, independent package boundaries and a ground-first sample sequence. Consulted official Godot foliage/material, MultiMesh and LOD documentation, retaining its 4.7 caveat. No asset regeneration or coast modification in this planning slice.

## M3.8.2/M3.8.3 checkpoint (2026-10-06)

Generated three tiled 1K ground material layers in realistic/cartoon treatments, normalized layer-weight terrain, three fully UV-mapped segmented grass clumps and independent UV2 root weights. Actual renders inspected; corrected excessive darkness and sand variation. Grass near shadows disabled after heavy root self-shadowing. Godot checks pass: 260 root vertices across six variants remain zero-weight, full U range, valid positive blade heights, normalized ground weights and ground collision. Tree and portable-pack validation follow. First import logged the not-yet-built demo; later build/render and sample checks pass.

## M3.8.4 tree checkpoint (2026-10-06)

Created independent near/far tree (5,974/3,070 triangles), bark and cutout leaf map sets in two treatments, separate material roles, instance-isolated wind and tapered trunk colliders. Actual rendering revealed weak bark repetition and sparse far coverage; revised cellular bark and broader distant cards. Root QA caught the tilted first ring: flattened it to exact ground height, now 58 imported root vertices across two LODs per tree validate. Same-camera LOD captures inspected; hard switching can still change canopy appearance. Added practical package/source/limitation documentation. Source-only checkpoint before final packaging and fresh-copy tests.

## M3.8.5 package/runtime verification (2026-10-06)

Created separate ground/grass/tree ZIPs plus demo, sources and Windows bundle. Each asset archive independently imported into an empty project and passed its structural checks; demo import/load passed. Final runtime 30.00 s, mean 5.73 ms / p95 8.33 ms after warmup, empty stderr, six 1440 x 810 PNGs verified. Found and fixed release-mode assert-side-effect screenshot omission; historical logs retained and delivery/ used as final evidence. All binaries, maps and archives remain local. Formal comparative optimization testing and art/buyer acceptance remain open.

## 2026-10-06 - M3.8.6 grass reference review

Compared the actual nature-3 Windows capture with a browser screenshot of VGR's published RDR2 gameplay image. Recorded visible gaps, comparison limits, and realistic-only refinement priorities. Preserved accepted cartoon grass and all existing assets. Browser accessibility binding timed out; documented browser screenshot API succeeded. Reference screenshot remains local; documentation only is committed.

## M3.8.7 realistic grass v2 (2026-10-06)

Generated independent 476/350/266-triangle short/medium/dry realistic meshes and a separate editable Blender source. Retained original cartoon meshes/maps/materials (before/after hashes match). Realistic scattering uses variable verge height/density and patch variation. Fixed the first headless-saved demo by rebuilding with the actual renderer: headless MultiMesh buffers rendered empty, so the first capture is invalid evidence and retained only for diagnosis. Final evidence is validation/nature/realistic-v2/rendered and delivery. Three frozen phase/relit PNGs inspected; 286 rooted vertices validated across both styles. Fresh 0.1.1 grass/demo ZIP imports pass; versioned Windows runtime result recorded below. Metrics cover mixed views, not controlled performance improvement. Updated source-only recipes/docs; outputs remain local. Known art limitations: fine distant noise, grazing highlights, simplistic ground, no seed-head/broadleaf variety yet.

## 2026-10-06 - M3.8.8 mixed grass profiles

User rejected uniformly curved grass and requested screenshot-led parameterized styles. Added three authoring presets and explicit upright/gentle/arched populations with independently shuffled widths/heights. Default short clump 17/12/5, medium 12/9/4, dry 9/7/3 by profile. Every clump contains all three width classes and more than 2x height variation; rooted UV check passes (286 roots). Reduced realistic wind to 0.35 to retain upright profiles in motion. Cartoon hashes unchanged. Built nature-study-0.1.2.exe, visually inspected its grass capture, packaged sources/assets/demo/Windows and passed fresh grass/demo imports. Presets are generation parameters, not live geometry sliders. No remote push, resource publication, or coast conversion.

## 2026-10-06 - M3.8.9 ground sample

Replaced only realistic ground with unique full-patch 2K maps, granular soil, muted turf and sparse rasterized dry litter. Added 85 geometry pebbles (combined ground 2,643 triangles), separate realistic blend shader and three parameter presets. Preserved the flat base and existing grass to avoid unvalidated terrain/plant mismatch. Cartoon ground hashes unchanged. Exported 0.1.3 views 2/3 visually reviewed: less repeating pattern, visible gravel/litter; surface relief and root-zone detail remain limited. Windows 20 s mean 4.26 ms, p95 4.17 ms, 48 peak draws, 45,876 primitives; no stderr. Ground/demo fresh archive imports and normalized-weight/collision-structure checks pass. Metrics are a smoke run, not a controlled optimization comparison. Outputs remain local, no push.

## 2026-10-06 - M3.8.10 free baseline

Downloaded official Kenney Nature Kit, CRC checked and path-safe extraction completed. Read included CC0 notice; counted 329 GLBs and inspected the author's sample. Six representative models imported and rendered in an isolated Godot Compatibility project (capture_error=0). Files remain under ignored .local/references/free-nature; no product integration or remote push. Recorded Quaternius textured pack as a separate untested candidate and clarified that surpassing a free pack requires a useful stylistically comparable advantage, not merely extra geometry/maps.

## 2026-10-06 - Deferred 3D-to-2D option (M3.8.10 follow-up)

Recorded the user's explicit direction: pre-rendered 3D-to-2D assets are a future alternative only. Updated backlog, decision and active scope; no asset generation or prototype started.

## 2026-10-07 - M5.1.1 pixel JRPG goal and draft scope

Created the user-requested active goal and recorded a concrete first-edition coverage proposal, acceptance criteria and ordered M5-M9 milestones. Asked for projection and directional-animation preferences. Identified the first-slice art approval gate and retained original 3D deliverables. Planning only; no new artwork, installations or model downloads.

User answered: square-grid orthographic top-down and eight directions. Updated the draft to 1,920 proposed idle/walk frame slots for 24 characters, pending total-scope approval.

## 2026-10-07 — M5.1.2 / M5.2 / M5.3.1

Implemented a separate Mosslight Journey pixel RPG sample with original directional character geometry, 12 props and a runnable Godot room. Rejected two local DreamShaper concepts for style mismatch. Fixed duplicate walking poses, frame-rate-dependent chest opening and builder resource cleanup. Asset and runtime checks pass; exported Windows build generated. Art remains below the reference's richness; keep M5 visual review open before scaling. Generated art/executables remain local; preserve unrelated 3D changes.

## 2026-10-07 — M5.2.3 unified style study

Recorded the user's original-character choice and world-wide theme requirement. Defined 16 original roles; authored four silhouette/costume studies, twelve shared item designs, a guild shop and merchant stall. Same item images appear in stall and UI; shared palette/materials and seed-diamond motif connect categories. Built a separate Godot street with four selectable characters. Pixel bounds/pose checks and 32-direction runtime tests, switching/collision/interaction pass. Commercial art quality remains unaccepted; backdrop is a demo image rather than modular terrain. Local images/resources/builds remain excluded from commits.

## 2026-10-07 — M5.2.4 modular character correction

Rebuilt character authorship with independent part recipes, five species and five builds. Added 12 hairstyles/faces/headgear/profession outfits and 12 hair/cloth palettes. Sixteen presets generated with idle/walk/run across eight headings; separate shadow retained in packed Godot scene. Fixed duplicate robe appearance and an idle pose lost to pixel rounding. Geometry/part/bounds checks and 256 runtime movement-clip checks pass. Export and actual screenshots retained locally. Further art quality/secondary-motion refinement remains open.

## 2026-10-07 — M5.2.5 model-first art trial

Reused live local ComfyUI with DreamShaper 8. Four 512x768 illustrations (731201-731204) and two image-to-image refinements (731211-731212) succeeded. User positively assessed illustration quality. Selected a model-drawn small figure for a bounded static conversion, retaining source crop and metadata. Compared three sprite resolutions; 48x64 loses substantial detail, 96x128 preserves more but still requires pixel cleanup. No new animation or replacement of current Godot demo claimed. Sources/provenance local, code/docs only for Git.

## 2026-10-07 — M5.2.6.1/.2 local batch and unified-style audit

Added a 32-asset local DreamShaper manifest, resumable generation/provenance runner and review boards. Generated 32 initial candidates plus six bounded retries. Art audit rejects style, composition and identity failures rather than promoting model success to delivery. Recorded 32 rework entries with no selected output. Added a cross-category pilot gate, consistent drawing/proportion/material/camera rules, and corrected the generation prompt's three-head wording to the 3.5-4-head style contract. Illustrations and run records stay local/ignored. Sprite replacement, motion and Godot art acceptance remain open.

## 2026-10-07 — M5.2.6.3/.4 guided local pilot and Godot review

Previous turn classified as progress: committed style contract and concrete rejected-candidate review. Current turn verified ComfyUI queue idle, generated five guided trials, diagnosed/fixed thumbnail upscaling in the first two, and obtained three better-composed local illustrations. Added bounded provenance runner, shared-palette conversion and isolated Godot static review. Inspected actual viewport, fixed title overlap and reduced edge fringe, rerendered successfully. Camera/pixel-art polish and all new animation remain open; no delivery acceptance or remote push.

## 2026-10-07 — M5.2.7.1 rear clothing correction

Previous goal turn made progress through a real Godot style pilot. Verified local queue idle and generated seven bounded direction studies. High-denoise front-reference outputs lost style/proportions; low-denoise side trial stayed frontal. User corrected the clothing-orientation mistake. Updated illustration-derived rear guide to replace lower garment and boot front silhouettes, then locally redrew two rear variants. Selected 753007 only for comparison; recorded unresolved detail and side-view failures. Kept every source/output, did not overwrite playable art or claim complete directions.

## 2026-10-07 — M5.2.7.2 profile guide and conditioning preparation

Previous turn made progress in rear garment reconstruction. Verified the local queue idle, added portrait-size generation, rendered/inspected four trials, and recorded specific identity/costume failures. Added a side layout guide and prepared an IPAdapter Plus SD1.5 graph from pinned official source/model metadata. Windows TLS inside the restricted shell failed; approved escalation fetched metadata and started a resumable verified download. Inspected node imports/model loader; no third-party node executed yet. Released only idle 8188 model cache; memory preflight still failed. Asked user about freeing memory/commit capacity without changing their system settings or terminating programs. Model-conditioning inference and complete directions remain unverified.

Support download completed: both safetensors files match official SHA256 metadata (2,626,556,736 bytes total). Tested trial launcher correctly stopped before starting a process when available commit was 7.22 GiB. Prepared graph connectivity and 512x768 guide / 512x512 reference dimensions passed; no adapter inference has run.

## 2026-10-07 — M5.2.7.2 local reference adapter inference

Memory recovered above the existing start threshold; no process was stopped. Fixed missing trial custom_nodes directory after a terminal launch failure, then verified IPAdapter nodes on isolated 8189. Three queued local trials completed and were inspected. Reference conditioning improves drawing similarity but does not solve garment occlusion; duplicate head and rear boot-flap failures recorded. Added negative-prompt override and next-launch database isolation configuration. Existing startup database warning remains documented; no new complete direction/animation claim.

## 2026-10-07 — M5.2.7 regional conditioning and rear sprite study

Previous turn produced verified adapter inference and failed-garment evidence. Current turn verified idle server, implemented upper-region reference mask, and ran a controlled same-seed comparison. Rear frontal boot flaps removed; visual subcheck passed without claiming complete direction art. Converted S/N at two sizes, verified binary alpha/foot anchors, and inspected the actual board. Final pixel cleanup, camera consistency, lateral/diagonal directions and all model-derived movement animation remain required.

## 2026-10-07 — M5.2.7.2 torso mask and three-view comparison

Verified idle trial server, ran three side mask trials including an exact-control repeat after fixing an empty prompt separator. Inspected strict profile improvement and remaining identity discrepancies. Six static S/E/N conversions pass binary-alpha and foot-bound checks. No directional animation or final art acceptance claimed.

## 2026-10-07 — M5.2.7.2 localized side identity repair

Previous turn established a strict profile with remaining costume/hair differences. Verified idle server and ran three local masked repairs: plain leather bracer, bob tips and cape tail. Inspected each actual result; saved outputs prove zero outside-mask RGB change. Updated three-view static comparison source. Side movement pose study is next within M5.2.7.3; complete eight-direction animation remains unfulfilled.

### M5.2.7.3 — Model-derived side motion study

Created build_side_motion.py from the corrected side illustration rowan-side-cape-755003. It extracts actual model pixels into body/cape/arm/leg layers, adds a small painted occlusion fill and articulates eight walk and eight run poses. Hidden far limbs reuse shaded near/source pixels; this is an assisted cutout motion study, not new diffusion animation or eight-direction completion. Running adds forward lean, bent elbows, larger stride/lift and flight. Shadows remain separate.

Saved 96x128 RGBA sheets, enlarged GIFs, source poses, contact sheet and source-hashed manifest under production/pixel-rpg/model-wave-01/guided/motion/. check_side_motion.py passes 16 unique bounded binary-alpha frames, grounded walk, run contact/flight and less than 8% maximum leg stretch (observed 7.53%). These checks do not establish gait realism. preview_side_motion.gd plays both sheets in an isolated Godot review with nearest filtering and fixed ground shadows. Actual renderer capture succeeded; fixed preview viewport sizing after an initial cropped capture. Environment log/certificate/shader-cache write warnings persist, without blocking the capture.

Visual review: distinct walk/run poses and forward elbow bend are present. Cutout joints, sleeve/skirt seams, rigid foot orientation, slight leg stretching and pixel-cluster polish remain visible limitations. Camera consistency and all remaining directions are open. Do not promote these sheets as a sale-ready character; default playable scene remains unchanged. Next: clean joints and gait before extrapolating directions or additional cast.

### M5.2.7.3 — Forward gait and garment silhouette correction

Inspected the actual v1 contact sheet and source anatomy. Found a motion error beyond pixel seams: airborne feet traveled front-to-back, and the near arm moved with the near leg. Corrected recovery to travel back-to-front, made stance travel backward at constant speed, and reversed arm phase. Added ankle pitch during recovery while keeping support feet flat. Restored the skirt hem/panel hidden by the original hand, tightened arm extraction and removed disconnected alpha fragments. Original v1 outputs were preserved locally before regeneration.

Revision 2 remains a model-pixel articulated study. It produces 16 unique connected, uncropped frames; walk stays at the ground anchor, run includes flight. Export hashes bind QA to actual sheets. Stance-coordinate checks cancel body travel at 41.4 px/s walk and 93.6 px/s run (native sprite scale); these are kinematic checks, not proof of perceptually slip-free gameplay. Maximum bone stretch remains below 8%. Godot actual viewport captured and inspected: floating garment pixels are gone and both actors remain fully visible. Environment log/certificate/cache warnings still occur.

Open art issues: flat reconstructed skirt panel, limited knee/ankle deformation, far-limb reconstruction, soft pixel clusters and side-view camera mismatch. Current state is E-only; no expansion or final art acceptance is implied. Next: resolve camera/proportions and diagonal clothing views alongside local pose cleanup before extending to the approved cast.

### M5.2.7.2 — Rear-quarter garment study

Added prepare_diagonal_guide.py for NE: asymmetric rear cape/shoulder, exposed near arm, rear/side skirt, staggered ground-plane heels and short rightward toes. The layout reuses hair pixels from the local N model drawing; it is explicitly a construction guide, not finished art. Confirmed the live 8189 queue idle before generation. Three local DreamShaper + torso IPAdapter trials completed (756001-756003). Visual review rejects all three as final art: invented topknot, overly preserved guide/neck fragment, or changed hair/sleeve/cape markings respectively.

Added --part ne-hair to the existing bounded repair script and generated rowan-NE-hair-756004 from 756001. Local hair-region img2img and compositing remove the topknot; 35,134 pixels changed, outside-mask RGB difference is exactly zero. This is the current NE static study. It retains readable rear-quarter clothing/footwear, but hair yaw is too close to N and the neck join, bracer details, cape design and overhead camera remain unresolved.

Extended the shared-palette review to S/E/NE/N at 64x96 and 96x128. All eight alpha/foot-bound checks passed and the actual comparison board was visually inspected. This exposes proportion/silhouette differences rather than hiding them with technical checks. No gameplay direction has been approved and no diagonal animation is claimed. Source guide, prompts, masks, histories, rejected candidates and outputs remain local under production/pixel-rpg/model-wave-01/guided/. The review ledger records each status; selected_gameplay_directions stays empty.

### M5.2.7.2 — NE cape projection and head alignment refinement

Reviewed current source and idle 8189 queue. Added bounded ne-cape, ne-heading and ne-nape modes to repair_side_bracer.py. ne-cape widens the actual teal cloth pixels around the near shoulder without scaling the legs/arm, then redraws only that region locally. 756005 has a broader rear-quarter drape; old cape-edge residue and neck gap remain. 756006 is rejected: the head mask yielded a face looking back and invented white collar. Do not use it in sprite conversion.

756007 starts from 756005, limits repair to the small right ear/nape, and uses denoise 0.24. It avoids the invented face and reconnects the neck. It is the current NE study source. Independently checked saved source/output hashes and actual pixels for all three: changes 51,680 / 7,317 / 3,066 respectively; every zero-mask pixel is exactly unchanged. Four-view conversion rerun passes eight binary-alpha/foot-bound checks; actual board inspected.

Art limitations remain explicit: collar/old-edge remnants, cross-view body proportions, consistent overhead projection and finished pixel clusters. These are static NE refinements, not accepted eight-direction art. Prior generated files are preserved and source review ledger records rejection/study status. No service stopped, no extra models installed, no default game scene changed.

During actual board inspection, the largest-component-only segmentation silently discarded the disconnected far calf beneath the NE cape. Updated static review segmentation to retain significant components (at least 64 source pixels and 0.5% of the largest component); erosion and binary alpha remain. Re-rendered and visually verified both NE legs survive at both target resolutions. This fixes conversion loss, not the underlying cape/occlusion drawing quality.

### M5.2.7.2 — Cross-view landmark normalization study

Added rowan-proportion-study.json with explicit, manually inspected crown/chin-or-nape/shoulder/waist/tunic-hem/knee-or-boot-top/sole landmarks for S/E/NE/N. normalize_direction_proportions.py preserves local model drawing pixels while applying a continuous piecewise vertical mapping and one fixed horizontal scale into 96x128 cells. Premultiplied sampling avoids white edge contamination; significant disconnected foreground components remain retained. This is a proportion study, not camera reprojection, redrawing or proof of accurate anatomy.

Generated four separate aligned textures, source/output-hashed manifest, before/after board and labelled direction-switch GIF under production/pixel-rpg/model-wave-01/guided/proportions/. Source illustrations, unaligned comparisons and side movement sheets are unchanged. Verified monotonic landmark mappings, binary alpha, unclipped bounds and aligned crown/sole limits for all four outputs. Actual before/after board inspected: rear hem height now agrees more closely, while garment construction differences are more obvious.

Art gate remains open: frontal off-shoulder wrap differs from covered shoulders in other views, NE collar/cape residue remains, pixel clusters are soft, and overhead perspective is not established. These issues require local garment/anatomy redrawing rather than further global scaling. No direction-switch study is counted as walk/run animation or as completed eight directions. Next priority is shoulder/neckline costume consistency before expanding the cast.

### M5.2.7.2/.3 — Side off-shoulder costume repair and motion update

Added bounded shoulder repair (755004) from the previous side cape source. Local DreamShaper inpainting at denoise 0.32 replaces the covered cap shoulder with exposed skin above a narrow teal upper-arm wrap. Actual output inspected against front costume. 3,622 pixels changed; independently verified zero difference outside the mask and exact preservation of the head and lower costume. This passes the narrow shoulder-design subcheck, not overall art acceptance.

Updated side static conversion, proportion-study source and articulated motion source. Motion revision 2 was archived locally before generating revision 3. All 16 walk/run cells remain distinct, connected and bounded; grounded walk, run flight and forward-recovery/planted-stance checks pass. Four-view static and proportion checks also pass. Actual motion contact sheet and Godot viewport inspected: exposed shoulder/wrap remain readable during arm swings. Remaining cutout joints and unfinished pixel clusters are still present. Godot rendered successfully with the same environment log/certificate/cache warnings.

No new movement direction is claimed; default playable scene and original images remain preserved. The next missing direction is the front-quarter SE view, which must retain the newly clarified off-shoulder design rather than inventing sleeves. Broader camera/garment consistency and the approved M6-M9 inventory remain incomplete.

### M5.2.7.2 — Front-quarter direction study

Generated three local DreamShaper + IPAdapter trials on the existing idle 8189 service. prepare_front_quarter_guide.py uses owned front pixels as a foreshortened layout only; 757001 and 757002 remain essentially frontal and are rejected for SE. Increasing denoise alone did not solve directional construction.

Added prepare_se_construction.py with explicit nose/eye asymmetry, near/far shoulder positions, oblique waist and hem, staggered boots and diagonally right-facing toes. This procedural drawing is an inference guide only. Local model redraw 757003 yields readable right-front head/torso/foot direction and retains the off-shoulder teal wrap / white tunic / brown leather theme. It is the current SE study, not accepted art: the model invents a belt pendant and roughens cape edges; garment details and overhead camera remain open.

Extended both source-size and landmark-aligned comparisons to five views S/SE/E/NE/N, making palette/board/GIF sizing dynamic. Ten static cell alpha/foot checks and five aligned-cell bounds checks pass; actual comparison board inspected. Per-run histories and output hashes verified. Direction-switch GIF now traverses these five views and returns in reverse order. This remains static review, not five-direction movement animation; only E has walk/run studies. No asset counts or broader M5-M9 completion claims changed.

### M5.2.7.2 — Front-quarter accessory and cape cleanup

Extended bounded local repair with se-belt (757004, denoise 0.32) and se-cape (757005, denoise 0.36). First removes the invented hanging hook below the belt; second replaces the ragged left cape edge and extraneous long brown strip with intact teal fabric. Actual full-resolution outputs inspected. The cape's upper patch join and a small inner-edge residue between the legs are still visible and remain art follow-ups, not hidden acceptance.

Independently verified saved source/output hashes, exact outside-mask RGB preservation, and unchanged head/feet. Changed pixels: 1,392 and 8,431. Updated the current SE source in both static and landmark-aligned comparison workflows. Ten static alpha/foot checks and five aligned bounds checks pass; actual latest board inspected. These repairs preserve the established SE orientation; no additional animation or direction has been completed. All previous images and per-run workflows remain local and preserved.

### M5.2.7.3 — Front/back projected motion studies

Added build_axial_motion.py using the original front model illustration and corrected rear model illustration. Produces S/N walk8 and run8 (32 cells) by separating original thigh/shin/foot pixels, projecting alternating depth/recovery, adding run flight and small torso shifts. Front arms currently use foreshortened cutout motion; N arms remain hidden under the actual cape. This is assisted model-pixel motion, not newly generated coherent animation or final pose drawing.

Generated sheets/GIFs/source poses/contact sheet and hashed manifest in production/pixel-rpg/model-wave-01/guided/axial-motion/. Corrected a cutout bug found during actual inspection: thigh pieces included white tunic-hem pixels, producing moving white stripes. Tightened the extraction start and eroded source foreground edges by two pixels to reduce white fringe. Source illustrations remain untouched.

check_axial_motion.py passes 32 unique bounded binary-alpha cells, actual source/sheet hashes, alternating recovery and run-flight presence. preview_axial_motion.gd loads all four sheets in an isolated Godot scene with independent shadows. Actual renderer captured and inspected after the final update. Existing sandbox log/certificate/cache warnings do not prevent rendering. Reproduce with bundled Python build_axial_motion.py then check_axial_motion.py; Godot --path pixel-rpg-demo --script res://authoring/preview_axial_motion.gd, optionally -- --capture=<absolute PNG path>.

Remaining: understated motion, stiff front arm/elbow reconstruction, joint/cloth polish, overhead camera and integration across directions. Axial anchor is [48,112] to reserve depth-step margin, unlike the older E anchor [48,122]; these cannot yet be merged without normalization. Available movement studies now cover S/E/N only; diagonals and leftward motion, unified idle and full eight-way controller integration are not done. Default playable demo unchanged, no final character acceptance.

### M5.2.7.3 — Shared motion resource and width-preserving limb projection

Inspected enlarged N-run leg crops. Uniform segment scaling narrowed/widened ankles when changing projected length, creating mismatched rigid feet. Changed axial bone transform to preserve transverse width while scaling longitudinal length. Rebuilt S/N and passed the existing 32-cell source/hash/alpha/bounds/pose checks. Joint pixel polish is still needed; no full anatomy acceptance claim.

Added export_model_motion.py: reads the actual high-resolution S/E/N pose outputs, applies each direction's explicit landmark mapping, extrapolates beyond crown/sole to preserve animation excursions, and exports one shared 96x144 cell / [48,122] anchor / 128-color palette. Removes only detached 1-2 pixel alpha residue. All 48 native cells are unique, binary-alpha and inside the cell. Generated six sheets and rowan_study.tres under pixel-rpg-demo/mosslight/model_motion/; outputs remain ignored/local. Per-pose provenance, sheet hashes, resource hash and review board are in production/pixel-rpg/model-wave-01/guided/unified-motion/.

The SpriteFrames contains walk_S, run_S, walk_E, run_E, walk_N, run_N, eight frames each at 10 / 13.333 fps. For a centered AnimatedSprite2D, assign this resource, set offset to Vector2(0,-50), use nearest texture filtering and keep shadow separate at the node position. Copy the generated mosslight/model_motion folder with its res:// hierarchy for use in another Godot project. This is a usable study resource, not the final buyer package.

preview_unified_motion.gd loads the native .tres and imported PNGs, validates all six animations and 48 AtlasTexture regions, then renders all of them via AnimatedSprite2D. Editor import and actual viewport capture passed and final screenshot inspected. Existing environment log/certificate/cache warnings remain. Reproduce after pose builders: bundled Python authoring/export_model_motion.py; Godot --headless --editor --path pixel-rpg-demo --quit; then --path pixel-rpg-demo --script res://authoring/preview_unified_motion.gd with optional -- --capture=<absolute PNG path>.

This resolves anchor mismatch in the new unified export only; original E and axial study sheets remain distinct historical formats. Remaining full goal work includes idle, other movement directions, consistent overhead camera, joint/cloth and pixel-cluster art cleanup, playable controller integration and the approved broader character/environment/item inventory. Default project scene unchanged.

### M5.2.7.3 — Right diagonal motion and five-direction resource

Extended the existing projected-motion builder with SE/NE model sources, direction-specific leg/arm extraction and diagonal ground-plane stride vectors. Preserved each illustration's front/rear clothing and foot orientation; no image rotation or E-sheet substitution is counted as a new direction. Added stronger forward torso lean for diagonal runs, with arm attachment points following the same torso transform. Front/diagonal arms still use cutout foreshortening and need better elbow poses.

Generated SE/NE walk8/run8, 32 additional study frames. The projected builder now exports S/SE/NE/N (64 cells), while the side builder provides E (16 cells). Updated tests cover all four projected directions, actual hashes, 64 unique bounded binary-alpha cells and alternating recovery/flight. Actual diagonal contact sheet inspected. Motion remains restrained and joints/cloth need art cleanup; this is not final animation acceptance.

Unified exporter and native Godot preview now cover S/SE/E/NE/N: ten animations, 80 frames, shared 96x144 cells, [48,122] anchor, separate shadow. Dynamic palette/board/resource sizing replaces the earlier fixed three-direction counts. Export checks pass for all 80 cells. Godot editor import, native SpriteFrames/AtlasTexture checks and actual AnimatedSprite2D capture pass; latest five-column render inspected after the run-lean update. Existing environment log/certificate/cache warnings persist without blocking rendering.

Leftward directions, idle, final pose/camera/style consistency and playable controller integration are still missing. Full approved asset-pack scope remains unchanged. Generated sheets/resources stay local and ignored; no default scene change or remote push.

### 2026-10-07 — M5.2.7.3 / M5.3.1 playable integration

Exported eight-way technical SpriteFrames using five model-derived source directions plus three disclosed mirrored directions. Added eight static idle poses: 24 clips / 136 cells total. Added the reusable model character controller, isolated review room and a PackedScene-based integration check. Verified eight headings, normalized walk/run speeds, preserved idle facing, wall/chest collision and live arrow/Shift input. Actual viewport inspected; existing sandbox log/certificate/cache warnings remain. Generated assets stay local. Art acceptance and full pack completion remain open.

### 2026-10-07 — M5.2.7.2 rear shoulder costume correction

Compared actual front and rear illustrations: the front exposes both shoulder caps, while the previous N cape covers them. Added n-shoulders (seed 758001, denoise 0.30) to the existing local masked repair script. Generated on the verified idle 8189 DreamShaper service; prompt/history/source/mask/output hashes retained. The new source exposes shoulders above the teal wrap while retaining the central nape attachment and actual rear-facing cape.

Inspected the full-resolution result and final Godot render. Independently verified pixel-exact preservation outside the mask, edits bounded by x172..343/y239..321, and unchanged image regions y<235 and y>=330. The initial overly strict y<240 head-region assertion caught the blurred mask reaching y239; no source was promoted until the actual change bounds were inspected. No claim that the entire head including its bottom edge is pixel-identical.

Promoted rowan-N-shoulders-758001.png only as the current N study in static comparison, landmark normalization and projected animation. Rebuilt motion and native resources. Checks pass: 64 projected motion cells, five static/aligned views, 136 unified cells, 24 native clips, and actual playable scene input/collision behavior. Existing environment log/certificate/cache warnings persist. The lower cape silhouette, NE shoulder/neckline, elbow articulation and pixel cleanup remain art work; full-pack completion and visual approval remain open. Generated outputs remain local.

### 2026-10-07 — M5.2.7.2 oblique rear shoulder correction

Continued the preceding N costume repair with local DreamShaper masked trial ne-shoulder / 758002 / denoise 0.30. Inspected the existing NE source: a white collar strip and high shoulder wrap contradicted the original off-shoulder design. The new study exposes the near shoulder above a lowered teal band and removes the targeted white collar segment. Actual source and Godot playable capture inspected. Far shoulder remains mostly occluded; cape contours and pixel cleanup still require art review.

Both Comfy queues were verified idle before inference. Verified output hash and exact preservation outside the mask; 5,039 pixels changed, bounded by x237..335/y244..321. Regions y<240 and y>=325 remain unchanged. Updated NE selection in static comparison, proportion configuration and motion builder; NW inherits the disclosed mirror. Rebuilt and checked 64 projected motion cells, five static/aligned views and 136 unified cells. Godot import and actual scene movement/collision/input checks pass, with existing environment log/certificate/cache warnings. Generated media and run records remain local. No full-pack or final-art acceptance claim.

### 2026-10-07 — M5.2.7.3 segmented elbow motion

Replaced whole-arm scaling in S/SE/NE with overlapping upper-arm and forearm model-pixel pieces sharing an articulated elbow. Run uses a stronger forearm bend than walk; arm attachment follows torso lean. N arms remain hidden under the cape. No new illustration inference or completed anatomy claim: depth occlusion, joint seams and clean pixel clusters remain open.

Inspected S/SE/NE run and NE walk contact rows, then the actual native Godot render. Rebuilt projected sheets and unified resources. Added geometric checks using actual shoulder/elbow/wrist coordinates: finite nondegenerate segments and greater average run bend than walk in each affected heading. Existing 64-cell provenance/alpha/bounds/gait checks, 136-cell unified export, native 24-clip checks and playable movement/collision tests pass. Environment log/certificate/cache warnings persist. Current art remains a study; full asset inventory and visual acceptance remain incomplete.

### 2026-10-07 — M5.2.7.3 breathing idle

Replaced single static idle cells with four-frame / two-second breathing loops in all eight headings. Three distinct poses per direction use rise values [0,0.5,1,0.5] pixels; the returning midpoint is deliberately reused. A smooth vertical displacement tapers to zero by row 82, preserving lower-body and foot pixels exactly. This is model-image deformation, not newly inferred animation, blink or independent cloth motion. Mirrored-left limitations remain.

Export now contains 160 timeline cells / 152 distinct cells in 24 clips. check_idle_motion.py verifies each sheet hash, duration, three unique poses, matching return frame and pixel-exact lower-body preservation. Inspected the eight-direction idle board. Godot imports and native resource validation pass; the actual playable test now waits during idle and confirms frames advance while velocity remains zero. Movement/collision tests pass. Existing environment log/certificate/cache warnings remain. Full art acceptance and broader asset inventory remain open.

### 2026-10-07 — M5.3.1 model courtyard assembly

Added model_courtyard.gd with a generated model_courtyard.tscn entry (recreated by export_model_motion.py). Open this scene and press F6; WASD/arrows and Shift use the existing model controller. Places the existing local-model guild, chest and animated character together in a 1200x900 review area. Guild scale 1.5 makes its doorway comparable to the character. This fractional scale is a composition study, not final native pixel-density acceptance. Ground remains an explicitly labeled placeholder; no new terrain, building interior or expanded inventory is claimed.

Added ground-footprint collisions and shared Y sorting. Actual front/back captures exposed an incorrect sorting pivot at the outer paving edge: the character disappeared at the front wall. Moved the sorting pivot to the wall contact line while compensating sprite offset so the building image stays in place. Re-ran the actual scene: front/back collision and relative sorting checks pass, and inspected captures confirm the character is visible in front and occluded behind. Existing environment log/certificate/cache warnings persist. Local captures are under guided/unified-motion/courtyard*.png. Scene/resource outputs remain ignored. Cross-category projection, building pixel cleanup, modular ground and final art approval remain open.

### 2026-10-07 — M5.2.6.3 / M5.3.1 local-model paving study

Added generate_ground_study.py and export_ground_study.py. Both local Comfy queues were checked idle. Text-only DreamShaper trial 759001 produced triangular ceramic-like slabs with excessive realism; retained and rejected. Guided img2img trial 759002 (denoise 0.48) uses a staggered rectangular layout and yields restrained warm paving. Workflows, prompt IDs, histories and output hashes retained under production/pixel-rpg/model-wave-01/ground/. No external/cloud art used.

Converted the second source to a 128x128, <=24-color repeat pattern and inspected a 4x4 repeat board. Added tiled paving beneath the existing courtyard sprites. Actual Godot capture inspected and front/back building collision/sorting tests pass; existing environment warnings remain. Reproduction: run generate_ground_study.py --guided only when its run does not already exist, then export_ground_study.py, Godot editor import, and model_courtyard.tscn. This is one repeat-pattern study, not arbitrary connectable 32px terrain cells. Grass, boundary/corner transitions, irregular variants and final surface-art approval remain missing. Current slabs still look too regular. Generated art stays local and ignored.

### 2026-10-07 — M5.2.6.3 / M5.3.1 local-model grass ground

Extended ground generation with --grass (759003) and --grass --guided (759004). Queues verified idle before generation. Text-only trial invented an unrelated ring graphic and is rejected. The guided sparse tuft layout produced a low-contrast sage/olive ground sample; inspected source and actual Godot courtyard. Converted to a 128px repeat pattern with <=16 colors, retained hashes and a 4x4 repeat board. Export_ground_study.py now exports paving and grass; it requires the selected local sources. The courtyard uses the grass instead of the plain grid background.

Godot import and actual front/back collision/sorting checks pass; existing environment warnings remain. Surface is still visibly repetitive across large areas. Irregular variants, road/grass boundary transitions, dirt and other terrain types remain missing; this is not a complete terrain atlas or final art acceptance. Local source/output/history artifacts retained; no remote media publication.

### 2026-10-07 — M5.2.6.3 / M5.3.1 corner-connected paving

Added build_ground_corners.py: derives sixteen 32x32 alpha overlays from the selected local-model paving texture using TL/TR/BL/BR occupancy bits. Bilinear corner coverage creates outer corners, inner corners, straight boundaries and diagonal cases. A narrow darker paving rim defines the boundary. This is authored compositing of model pixels, not new inference or sixteen independent material designs. Exhaustive checks pass for all 128 compatible horizontal/vertical edge pairs; empty and filled masks checked.

Added reusable mosslight/paving_layer.gd using native TileMapLayer/TileSetAtlasSource. paint_vertices accepts shared corner occupancy and a cell rectangle; grass is supplied underneath. Replaced the courtyard's rectangular paving TextureRect with a 260-cell tile layer and short branch to expose inner/outer joins. Actual Godot screenshot inspected and collision/sorting scene checks pass; environment warnings remain. Reproduce after export_ground_study.py with build_ground_corners.py and Godot import. The atlas is local mosslight/model_ground/paving-corners.png. This is programmatic corner painting, not editor terrain-autotile configuration. Surface variation, dirt/grass edge details and full terrain inventory remain incomplete; current edges are visibly regular.

### 2026-10-07 — M5.3.1 native paving terrain resource

Added authoring/export_paving_tileset.gd to save mosslight/model_ground/paving.tres with 16 atlas cells, one Paving terrain and Match Corners mode. Configuration follows the official TileSet terrain documentation: https://github.com/godotengine/godot-docs/blob/master/tutorials/2d/using_tilesets.rst . Replaced the paving layer's runtime-only TileSet construction with loading this saved resource.

Verification: saved/reloaded resource retains all 64 corner bits; set_cells_terrain_connect paints an L-shaped layout and passes 104 shared-corner checks. The courtyard loads the saved resource and its actual scene collision/sorting test passes. Existing environment log/certificate/cache warnings remain. This verifies the terrain API/resource configuration; no manual editor-brush session is claimed.

Reproduction order: export_ground_study.py -> build_ground_corners.py -> Godot editor import -> Godot --headless --path pixel-rpg-demo --script res://authoring/export_paving_tileset.gd. In the editor, add a TileMapLayer, assign mosslight/model_ground/paving.tres, select Terrains > Paving, and paint above a grass layer; use nearest filtering. Keep the mosslight/model_ground folder hierarchy when copying to another project. Generated resource and atlas stay local. This adds engine usability, not art acceptance or complete terrain coverage.

### 2026-10-07 — M5.2.6.2-4 barrel rework

Reworked the existing rejected prop_barrel (earlier model output was a wheel/logo). Added prepare_barrel_guide.py for an owned structural guide, then generated barrel-760001 with the existing generate_guided_pilot.py on idle local 8189, denoise 0.6. Retained workflow/history/source. Actual output reads as an upright closed wooden barrel with two muted metal bands, visible lid and wooden staves. This is one replacement study, not bulk visual acceptance.

Added convert_barrel_study.py: white-background segmentation, 48x64 binary-alpha sprite, anchor [24,60], quantization against existing guild/chest/book/rowan palette colors. Verified reference sprite hashes remain unchanged. Added two instances of this one design to the courtyard with ground collision. Initial placement intersected the building's decorative paving; moved both barrels outside it. Actual render inspected and barrel/front/back collision checks pass, with existing environment warnings. No barrel animation or second unique design is claimed. Camera consistency and final pixel finish remain review items. Generated source/sprite remain local.

### 2026-10-07 — M5.2.6.2-4 crate rework

Reworked rejected prop_crate using prepare_crate_guide.py and existing guided local-model generation (crate-760002, denoise 0.58, idle 8189 verified). Actual result has top/front/right faces, planks and diagonal front brace rather than the previous abstract emblem. Extended the existing prop conversion command with --prop crate, creating a 56x56 binary-alpha image with anchor [28,52] using the existing pilot colors. Reference sprite hashes remain unchanged.

Placed one crate in the courtyard, added its footprint and an actual collision check. Source and final renderer screenshot inspected; engine scene tests pass with existing environment warnings. Updated the authoritative replacement-study review entry; final visual approval remains pending. Only a static closed crate is delivered in this study, not open/broken animation states. Generated source, workflow, conversion hashes and sprite remain local.

### 2026-10-07 — M5.2.6.2-4 potion and crystal inventory studies

Added prepare_inventory_guides.py and generated two bounded local redraws with the existing guided pilot: potion-760003 and crystal-760004, denoise 0.58. Queues were idle before sequential inference. Retained guides/workflows/history/originals. Inspected actual sources: recognizable round teal potion with cork and brass diamond, and a faceted teal crystal. Added both choices to the existing palette-preserving conversion command; outputs are 32x32 binary-alpha icons with fixed anchors. Existing palette-reference sprite hashes remain unchanged.

Added native-size potion/crystal/book slots to the courtyard header. Texture-size assertions and actual scene render/collision checks pass, with existing environment warnings. Inspected gameplay-size screenshot; icons have distinguishable silhouettes, but final pixel finish remains unapproved. These are static art previews, not working inventory, pickup, use or animated item states. Updated replacement-study records without marking the full pack accepted. Generated media remain local.

### 2026-10-07 — M5.3.1 independent review snapshot

Added package_model_review.py with an explicit 45-file allowlist, dependency checks, per-file SHA256 manifest, ZIP CRC and byte/hash verification. Creates builds/mosslight-review-01.zip and a matching directory, refusing to replace an existing snapshot. Includes runtime-only model character/ground/prop/item studies and two scenes; excludes model weights, Python/ComfyUI, authoring caches and unrelated work. README explicitly marks incomplete art/catalog, mirrored headings, static items and no interior. This is not a release or full-pack completion.

Extracted the actual ZIP to production/pixel-rpg/model-wave-01/package-validation/review-01, verified all 45 hashes, imported from scratch with Godot, then ran its configured courtyard and its actual eight-way character test. Both pass, including barrel/crate/building collision, Y-sort checks, live inputs and advancing breathing idle. Inspected the independent renderer capture. User-directory/log/cache/certificate warnings persist in the sandbox; no zero-warning claim. Runtime references resolve within the extracted project. No automatic remote push. New art work remains prioritized; this snapshot is a portability checkpoint only.

### 2026-10-07 — M5.2.6.2-3 Sylva elf replacement study

Reworked ch_sylva using prepare_sylva_guide.py and local DreamShaper guided generation (sylva-front-761001, denoise 0.42). Golden hair, pointed ears and teal/cream scholar clothing replace the mismatched original. The first output omitted the crystal and duplicated the staff shaft. repair_sylva_staff.py performs a bounded local masked repair (761002, denoise 0.28); actual inference succeeded and outside-mask maximum pixel difference is zero. Both queues were idle before the repair. Sources, masks, workflow and history remain local.

convert_sylva_study.py produces a proportion-preserving static 96x144 study with sole anchor [48,122], binary alpha, existing Rowan palette plus six muted gold shades. The first exact-palette conversion made blonde hair pink, so it was revised after visual inspection. Compared the actual output against Rowan at 3x nearest scaling in production/pixel-rpg/model-wave-01/guided/sylva-scale-review.png. Ear and robe silhouettes read, but the thin staff remains fragmented at sprite scale, clothing detail is busy, and the camera is not validated as overhead. This remains a rework study, not approved character delivery; no Sylva directional clothing views or walk/run animation are claimed. Existing courtyard and review ZIP are unchanged. Next: simplify staff/pixel clusters, then author consistent rear and side garment views before animation.

### 2026-10-07 — M5.2.7.1 Sylva rear garment study

Added prepare_sylva_back.py: explicitly closed rear bodice/skirt, plain belt back, covered nape and heel layout instead of reusing front neckline/buckle. Local guided trial sylva-back-761003 produced a rear robe but changed the hair to twin tails. Extended repair_sylva_staff.py with recorded seed/denoise and bounded rear hair/staff masks. Trials 761004/761006 preserve direction but look stiff; stronger 761005 invented pale bands and is rejected. Rear staff trial 761007 restores a teal crystal. All masked trials preserve outside-mask pixels exactly. These are inspected studies, not art approval.

Extended convert_sylva_study.py --direction back to output a 96x144 rear study alongside the existing front, with the same sole anchor and palette extension. Added preview_sylva.gd and imported/rendered both images in actual Godot at integer 3x nearest scale. Capture: production/pixel-rpg/model-wave-01/guided/sylva-godot-review.png. Static texture checks and render exit 0; sandbox log/certificate warnings persist. The rear no longer displays the frontal neckline/buckle, but hair is too flat, a head-side artifact remains, sleeve lining/heel treatment differ and the staff is fragile at pixel scale. Do not animate or count this as an accepted second character. Next corrective work must resolve these visible identity mismatches, rather than multiplying directions from this source. Existing playable courtyard/package unchanged.

### 2026-10-07 — M5.2.7.1 Sylva rear identity corrections

Rejected three further candidates after direct visual inspection: full-image img2img 761008 altered head/garment structure; fresh text-only 761009 lost chibi proportions, framing and closed costume; curved-lock masked trial 761010 created striped hair. These failures establish that neither higher denoise nor dense line guides reliably repairs this rear identity. Preserved originals/history; none replaces runtime art.

Adopted bounded repair 761011 for two concrete corrections only: removed the invented head-side spike and replaced the broad white sleeve patch with teal cloth and a narrow cream cuff. Outside-mask maximum difference remains zero. Updated rear conversion to this source and reran binary-alpha/96x144/sole-anchor checks plus actual Godot import/render. Latest sylva-godot-review.png inspected; run exits 0 with existing sandbox log/certificate warnings. Hair mass remains flat and cuff/staff pixel detail needs cleanup. This is still an unapproved static study, not a second animated character. Runtime courtyard/package unchanged; full M5-M9 goal remains incomplete.

### 2026-10-07 — M5.2.6.2-4 interactive model-derived chest

Added generate_chest_open.py for local masked half/open lid artwork, preserving the original box pixels outside the upper mask. Trials 762001 (half) and 762003 (open) are study sources; 762002 was rejected for a floating lid gap. export_chest_motion.py applies one transform/palette to closed/half/open 64x64 cells at [32,60], verifies binary alpha and identical lower-body rows 39-63, and produces a three-pose preview. This is a short three-pose animation study, not a smooth physically reconstructed hinge or final camera approval.

Added reusable mosslight/model_chest.gd with nonlooping opening/closing clips, fixed footprint, busy-state guard and a first_opened signal fired once per instance. Courtyard now offers nearby E interaction and a demonstration potion counter. Holding E does not retrigger; distant input is ignored; closing/reopening does not duplicate the reward. No persistent inventory/save or full item-use system is claimed.

Actual Godot tests cover box collision, live injected E input, busy gate, opening, closing, reopening, one reward and distance gating alongside existing building/barrel/crate sorting/collision checks. Initial event-handler input assertion failed; edge-triggered polling with explicit press/release physics ticks passes. A short frame-count cutoff initially ended before test completion; final validation required the COURTYARD_QA_OK marker, not merely exit 0. Actual frames and source art inspected. Existing sandbox log/cache/certificate warnings remain.

Updated runtime packaging dependencies and created builds/mosslight-review-02.zip (49 hashed files). Extracted the actual archive into production/pixel-rpg/model-wave-01/package-validation/review-02, verified all hashes, imported from scratch and passed the same interaction/scene checks there. Prior snapshots remain untouched. Generated art/packages remain local; no automatic push. Wider roster/environment/UI/effect coverage and Sylva identity cleanup remain incomplete.

### 2026-10-07 — M5.2.6.2-4 equipment and gathering icon studies

Added owned sword/shield/herb/coin guides and generated four sequential local DreamShaper studies (763001-763004, denoise 0.55) after verifying idle queues. Reviewed actual model images. Sword is broad and stylized; shield has teal/brass design; herb reads as leafy stems but lost the requested twine; coin uses the shared diamond motif. This expands a review sample, not accepted M8 inventory completion.

Extended palette-preserving conversion to 32x32 icons. Fixed anchor placement after alpha reduction by cropping surviving pixels. For herb only, remove enclosed white gaps between stems and avoid erosion/use a lower binary-alpha threshold to preserve thin stems. Inspected revised pixel output, including the intermediate failed white patch/disconnected-stem results; these were corrected before integration. Existing palette-reference images remain hash-identical.

Added preview_inventory.py and seven native-size slots in the actual courtyard. Reimported final textures and reran Godot scene tests through COURTYARD_QA_OK; actual screenshot inspected. Existing log/cache/certificate warnings persist. Packaging allowlist now includes four new icons, but review-02.zip remains the previous immutable snapshot and does not include this round. No equipment switching, herb use or persistent inventory is claimed. Broader assets and character quality remain incomplete.

### 2026-10-07 — M5.2.6.2-4 outdoor tree and rock studies

Added prepare_nature_guides.py and sequential local DreamShaper tree-764001 / rock-764002 redraws (denoise 0.58), after checking both queues idle. Actual sources inspected: recognizable rounded-crown deciduous tree and angular weathered stone. Tree branch exposure/canopy shading and rock planes remain simplified; these are static art studies, not a completed forest kit or approved final assets.

Extended conversion for a 160x192 tree and 64x64 rock, binary alpha, common bottom anchors, unchanged palette-reference files. Declared five muted foliage colors and five additional stone shades in conversion provenance rather than forcing stone into blue/brass ramps. Added one of each to the courtyard at native scale, trunk-only and rock-footprint collision, shared root-based Y-sort. New actual physics checks cover tree front/back and rock collision. Saved and visually inspected tree-front/tree-back renderer captures: character renders in front when below the root and is occluded behind the canopy when above it. All existing interaction/scene checks pass through COURTYARD_QA_OK; sandbox log/cache/certificate warnings remain.

Packaging allowlist includes both runtime PNGs; previous review-02 ZIP is unchanged. No wind animation, canopy transparency feature, alternate tree species or natural ground-shadow pass is claimed. Full pack scope and remaining character/environment/UI/effect quality work stay active.

### 2026-10-07 — M5.2.6.4 environment contact-shadow pass

Added reusable mosslight/contact_shadow.gd, drawing three nested pixel-stepped ellipses with adjustable footprint/opacity. Courtyard places six shadows under the tree, rock, chest, two barrels and crate in a dedicated ground layer after terrain and before Y-sorted objects. No source artwork is overwritten. These are stylized contact shadows, not directional cast shadows or simulated lighting; the building's existing painted foundation remains unchanged.

Actual Godot scene tests pass, including ground-layer ordering/count and existing collision, tree front/back sorting and chest input/reward checks. Inspected the final renderer capture: roots and prop bases now have visible ground contact without darkening sprites. Existing sandbox log/cache/certificate warnings persist. Packaging allowlist includes the reusable script; previous ZIP snapshots are unchanged. Remaining art consistency, character roster/directions and wider content coverage are not completed by this pass.

### 2026-10-07 — M5.2.6.2-4 furniture and interior scale study

Added prepare_furniture_guides.py and generated table-765001 / bookshelf-765002 sequentially on idle local DreamShaper (denoise 0.58). Inspected actual sources: plank tabletop, four legs and a three-tier bookcase in teal/cream/brown. Table rear legs have a teal cast and remain an art-review issue. Extended common conversion to table 128x112 and bookshelf 144x176, binary alpha, bottom anchors and unchanged palette references.

Added authoring/preview_interior.gd as a separate interactive Godot furniture room. Run Godot --path pixel-rpg-demo --script res://authoring/preview_interior.gd; WASD/arrows move and Shift runs. It uses the existing model character, reusable paving floor and temporary wall blocks. Furniture dimensions, ground footprints and common Y-sort are exercised by --self-test. Actual import/render and front/back table plus shelf collision checks pass through FURNITURE_ROOM_QA_OK. Inspected production/pixel-rpg/model-wave-01/guided/interior-study.png. Existing sandbox log/cache/certificate warnings remain.

This is a furniture scale study, not a finished interior environment: dedicated wood floor/wall/door art, furnishing variety, interactions and exterior-room transitions remain missing. The existing courtyard and immutable ZIP snapshots were not replaced. Full M5-M9 scope and pending character art quality remain active.

### 2026-10-07 — M5.2.6.2-4 model-derived interior wood floor

Extended generate_ground_study.py with a bounded --wood trial (765003). Local DreamShaper redraws an owned staggered-plank layout at denoise 0.48; source inspected and workflow/history retained. Added export_wood_floor.py: 128x128, at most 24 colors, reconciled four-pixel outer bands and exact opposite-edge RGB equality. Retains a 4x4 repeat preview and provenance. This supports full-pattern repetition, not arbitrary 32px tile connectivity.

Replaced the interior scale room's borrowed exterior paving with wood.png. Imported and rendered in Godot; texture dimensions and existing actual furniture collision checks pass through FURNITURE_ROOM_QA_OK. Final scene capture inspected. Existing sandbox log/cache/certificate warnings persist. Pattern repetition remains noticeable; board variants, wall/skirting/door assets and room transitions are still missing. No complete interior-kit or commercial-art approval claim. Existing ZIP snapshots are unchanged.

### 2026-10-07 — M5.2.6.4 linked exterior/interior demonstration

Moved the reusable interior room into model_interior.gd; preview_interior.gd remains a thin standalone entry. Added model_world.gd and authoring/preview_world.gd. Run Godot --path pixel-rpg-demo --script res://authoring/preview_world.gd, or open local model_world.tscn. Near the guild front door press E to enter; near the room bottom center press E to leave. Rooms retain their instances, including the courtyard's claimed chest/reward state; inactive rooms leave the tree and physics world. Interior content is centered in the shared 1200x900 viewport. Formal door/portal art remains missing.

Real-input tests cover distance rejection, two enter/leave cycles, safe spawn and movement, unchanged return coordinates, inactive-room detachment and preserved single chest reward. Initial return-position failure traced to the migrated room being attached to the window root instead of its owning interior node; corrected parenting and verified again. A guarded two-physics-frame handoff prevents overlapping transition execution. Both WORLD_LINK_QA_OK and the independent FURNITURE_ROOM_QA_OK pass. Captured and inspected actual linked room rendering; existing sandbox log/cache/certificate warnings persist. State retention is within the current session only, not disk save/load.

The previous review ZIP is unchanged and does not include this linked example. Temporary walls, door animation, broader maps, roster and art acceptance remain incomplete. No goal-completion claim.

### 2026-10-07 — M5.2.6.2-4 timber wall and linked review package

Added --wall local ground-material trial 765004: 512x256 cream plaster/timber-post panel with upper beam and skirting, denoise 0.45. Inspected generated source. Extended export_wood_floor.py --wall to create a 128x64/24-color horizontal repeat with a four-pixel edge reconciliation band and equal left/right RGB edges; top and bottom are intentionally different. The interior now uses this straight wall instead of a flat placeholder. Corners, side-wall treatment, doors and architectural variation remain missing.

Updated package_model_review.py to include linked runtime rooms, furniture, wall/wood floor, nature, contact shadows and seven icons, and generate the linked main .tscn directly. Created builds/mosslight-review-03.zip with 65 hashed files. Extracted the actual ZIP to production/pixel-rpg/model-wave-01/package-validation/review-03; all hashes pass, fresh Godot import succeeds, and both WORLD_LINK_QA_OK and FURNITURE_ROOM_QA_OK pass in the independent folder. Actual local linked interior rendering inspected. Existing sandbox log/cache/certificate warnings remain. Runtime needs no model server; the package explicitly remains an incomplete art review rather than a finished commercial pack. Prior ZIPs are preserved; no push.

### 2026-10-07 — M5.2.6.2-4 visible interior exit door

Added owned door guide and generated local door-765005 (denoise 0.52): plain timber frame, vertical planks, braces and dark handle details. Converted to 96x144 binary-alpha sprite using the existing palette; source and actual renderer inspected. Raised the straight back wall using integer 2x display scale, keeping the wood floor native-sized, so the door fits the room elevation. Final per-category pixel-density approval remains pending.

Placed the door on the rear wall and moved the linked interior exit from its earlier invisible bottom-center trigger to the visible door at [736,268], with entry spawn [736,304]. Updated interaction hint, packaging dependencies and future package instructions. Actual WORLD_LINK_QA_OK confirms two round trips, safe spawn/movement and reward retention; independent FURNITURE_ROOM_QA_OK confirms existing furniture collisions. Existing sandbox log/cache/certificate warnings persist. Door remains static: pressing E transitions rooms, without an opening animation or walk-through aperture. Previous review-03 ZIP is unchanged and still has its earlier exit layout; current project source has the new door. Wider pack/art completion remains pending.

### 2026-10-07 — M5.2.7.1 rear footwear orientation

Following the user's confirmation of directional clothing correction, inspected Sylva's actual front/rear render. Rear bodice no longer repeats the frontal neckline/buckle, but the feet still displayed front-facing sandal/toe details. Added bounded back-heels repair using local DreamShaper seed 761012, denoise 0.24, closed leather heel-cup guides and rear-seam prompts. Both queues were idle before submission. Recorded graph/history/source hashes and confirmed zero pixel difference outside the feathered repair mask. Prior source trials remain preserved.

Updated the rear conversion source to sylva-back-heels-761012.png. Binary alpha, 96x144 cell and sole anchor at y=122 pass. Actual Godot import/render returns SYLVA_STATIC_RENDER_OK; visually inspected guided/sylva-heels-godot-review.png. Existing sandbox log/certificate errors persist, without preventing the render. The rear now has solid heel cups rather than visible front toe straps. Hair remains flat, sleeve/camera consistency and further directional animation remain unresolved. This is a static correction study, not art approval or completion of the character collection. Existing review ZIPs remain unchanged; no push.

### 2026-10-07 — M5.2.7.1 rear hair lock study

Added bounded back-volume local DreamShaper repair using the heel-corrected source 761012. Unlike the rejected dense curved-stripe guide, this pass uses the existing image with an interior-only hair mask and explicit tapered-lock/cel-shading prompts. Trial 761013 at denoise 0.52 removes the dashed cloth-like bands and yields flowing separated lower locks. Adopted it as the current static conversion study. Stronger trial 761014 at 0.65 creates white holes and excessive contrast inside the hair; rejected, preserved and not exported. Both runs verify zero pixel difference outside their repair mask, preserving clothing, staff and heels.

Inspected both model images, converted sprite and actual Godot render at guided/sylva-volume-godot-review.png. Binary alpha/96x144/sole-y122 checks and SYLVA_STATIC_RENDER_OK pass; sandbox log/certificate errors persist. Native-scale hair now has readable lock divisions but limited highlight depth; sleeve identity, camera and silhouette remain review issues. No new animation or accepted roster completion. Previous review ZIPs remain unchanged. This turn is concrete art/source progress; full M5-M9 objective remains active.

### 2026-10-07 — M5.2.6.4 interior door animation and review-04

Added reusable mosslight/model_door.gd. It retains the model-derived 96x144 door frame and projects the cropped leaf around the left hinge through six widths over 0.6 seconds, revealing a dark aperture. This is a stylized 2D cutout projection, not new model-generated poses or a physically reconstructed 3D door. The exterior entrance remains static; room transfer does not simulate walking through an opened collision aperture.

Linked interior exit now freezes movement while opening and waits for the final open pose before room transfer. Busy/input guards reject repeated E, reset the door on entry and synchronize held input after transitions. Tests exercise two cycles, intermediate fixed-frame/leaf states, frozen/restored movement, repeated input, one transfer per opening, safe spawn and preserved chest reward. WORLD_LINK_QA_OK and FURNITURE_ROOM_QA_OK pass; inspected guided/door-world-door-opening.png. Existing sandbox user-log/cache/certificate errors persist.

Built builds/mosslight-review-04.zip with 67 hashed files, including the current visible door and animation. Extracted the actual ZIP into package-validation/review-04, checked all hashes, imported from scratch and passed both runtime tests there. The archive runs without model services/Python. Previous snapshots preserved. It is still an incomplete art review: roster, character art/directions, broader environments/items/UI/effects and final quality acceptance remain outstanding. No generated artifacts are committed or pushed.

### 2026-10-07 — M5.2.7.2 Sylva side identity study

Made generate_guided_pilot.py accept --reference-source instead of always conditioning on Rowan. Each run retains its own reference input and hashes, including white-background crop for opaque illustrations. Default transparent Rowan reference remains supported. Added prepare_sylva_side.py with an explicit right-facing profile, side torso/belt, near bell sleeve, staff and profile shoes. Layout is only a local-model guide, not delivery artwork.

Local DreamShaper/IPAdapter trial 761015 (0.57 denoise, 0.45 reference weight) is rejected for tall proportions and invented head ornaments. Revised guide enlarges the head and shortens the body; trial 761016 (0.50 denoise, 0.30 reference weight) is a usable side study but invents a bare shoulder and loses the crystal. Bounded 761017 repair covers the shoulder and restores the staff crystal, with exactly unchanged outside-mask pixels. All source trials remain preserved. This is local inference using Sylva's own front illustration, not a cloud route or cross-character reference.

Extended static conversion and actual Godot review to front/back/side. Binary alpha, 96x144 cells and sole-y122 pass; SYLVA_STATIC_RENDER_OK confirms three loaded textures. Inspected guided/sylva-three-views.png: side head is larger than front, sleeve narrower, footwear/socks and shoulder seam differ; hair lighting/pixel detail also remains inconsistent. These are unresolved art issues, not an accepted turnaround or second animated character. Existing package and playable character are unchanged. Sandbox log/certificate errors remain; full M5-M9 goal remains active.

### 2026-10-07 — M5.2.7.2 side cuff and ankle correction

Added bounded side-costume local DreamShaper repair (761018, denoise 0.23) on the existing side study. Replaced invented white sock fill with ankle skin and changed brass-colored cuff edging to cream fabric, retaining the crossing staff through a protected region. Outside-mask difference is zero. Source review still shows a light outline at the former sock boundary; this is not claimed as fully cleaned anatomy.

Updated side conversion and inspected the actual three-view Godot capture guided/sylva-costume-review.png. The prominent white ankle block is removed at sprite scale and cream cuff reads more consistently. Binary alpha, 96x144 cell, y122 sole and SYLVA_STATIC_RENDER_OK pass. Side head/body proportions, narrow sleeve silhouette, shoulder patch and shoe shape remain inconsistent with the front. Static study only, not approved turnaround or animation. Existing log/certificate errors persist. Original sources and review-04 package are preserved; broader M5-M9 work remains incomplete.

### 2026-10-07 — M5.2.6.2-4 matching wooden chair study

Added prepare_chair_guide.py and generated chair-765006 with local DreamShaper (denoise 0.52) after checking both queues idle. Inspected the source: plain frontal raised-view wooden chair with two backrest rails and visible seat top, matching the table's brown palette. Added 64x96 conversion, bottom anchor [32,92], binary alpha, unchanged shared palette references. Enclosed backrest gaps are explicitly transparent and isolated model speckles removed by connected-component selection.

Integrated two placements of this one design in the interior: behind the table and an unobstructed spare. Added footprint collisions and actual front/back chair checks alongside existing table/shelf validation. FURNITURE_ROOM_QA_OK and linked WORLD_LINK_QA_OK pass; inspected guided/chair-interior.png, with visible background through rail gaps and table occlusion of the rear chair. Existing sandbox log/cache/certificate errors persist. No sitting animation or interaction is claimed. Future package allowlist/docs include chair; immutable review-04 remains unchanged. This is one additional model-derived furnishing study, not completed environment coverage or final art acceptance.

### 2026-10-07 — M5.2.6.2-4 inn bed furnishing study

Added prepare_bed_guide.py and local DreamShaper bed-765007 (0.52 denoise), after idle-queue checks. Inspected source: square-grid raised frontal bed, brown frame, cream pillow and muted teal blanket. Converted to 128x176 with binary alpha and [64,172] anchor. Initial shared palette introduced peach-colored pillow speckles; added four declared cream/neutral material shades and inspected the corrected actual render. Existing palette-reference files remain unchanged.

Integrated bed in the interior with a full floor footprint and added front/back/side collision checks. FURNITURE_ROOM_QA_OK passes after final recoloring; linked WORLD_LINK_QA_OK also passes. Inspected guided/bed-interior.png. Existing sandbox log/cache/certificate errors persist. This is static furniture with no sleep animation or interaction, not a finished inn map. Future package dependencies include it; review-04 ZIP remains unchanged. Broad character/environment/UI/effect coverage and art acceptance remain outstanding.

### 2026-10-07 — M5.2.6.4 portable native furniture resources

Added export_furniture_scenes.py for four native scenes: table, bookshelf, chair and bed. Each contains nearest-filtered sprite, bottom-center root anchor and editable StaticBody2D floor footprint. Relative sibling texture references allow a renamed parent folder. Added furniture/README.md with drag-and-drop, Y-sort, dependencies and limitations. Migrated interior placement to instantiate these resources; removed duplicate room-level furniture bodies so collision has one owner.

Added check_furniture_import.gd and verified actual point intersections against each instantiated body, plus clear space below its feet. Created a fresh isolated project at model-wave-01/furniture-import-validation containing only four TSCNs, four PNGs and the check script, nested under assets/renamed-kit; fresh import and FURNITURE_IMPORT_QA_OK pass there. Original project furniture and linked-room tests also pass after migration, and inspected guided/native-furniture.png. Existing sandbox log/cache/certificate errors persist. Future packaging dependencies include the resources/check/docs; old review ZIPs remain unchanged. This improves reuse but does not prove artistic acceptance or complete the broader asset catalog.

### 2026-10-07 — M5.2.6.4 native wall pixel density and review-05

Changed wall conversion from 128x64 displayed at 2x to 256x128 displayed at 1x, using the original 512x256 model source. Visible wall extent remains 768x128 and room collision/layout are unchanged. The repeat board now derives its size from the output dimensions rather than cropping a wider texture. Verified <=24 colors, matching left/right edge RGB, actual native-wall.png render and FURNITURE_ROOM_QA_OK. This fixes the interior's explicit 2x wall pixel scaling; it does not establish pack-wide camera/style acceptance or resolve the courtyard guild's different scale.

Created builds/mosslight-review-05.zip (75 hashed files) including bed/chair, four portable native furniture scenes, their import check and the new wall. Extracted actual archive to package-validation/review-05; all hashes match, fresh import succeeds, FURNITURE_IMPORT_QA_OK and WORLD_LINK_QA_OK pass there. Existing sandbox user-log/cache/certificate errors persist. Older packages preserved. This remains an incomplete art review, with character identity/animation polish, wider roster/maps/items/UI/effects and final acceptance outstanding.

### 2026-10-07 — M5.2.6.2-4 common inventory expansion

Added original key/scroll/bread/pouch composition guides and four sequential local DreamShaper studies (766001-766004, denoise 0.50), after idle-queue verification. Inspected each source. Converted all four to 32x32 binary-alpha sprites with existing palette; scroll shares the four declared neutral cloth/paper shades. Key's enclosed bow is explicitly transparent. The pouch retains a subtle model-invented greenish surface mark and the bread silhouette is rather flat; these remain art-review points, not accepted final catalog entries.

Updated the comparison board to eleven distinct icons and courtyard to a two-row native-32px display. Inspected inventory-eleven-review.png and actual eleven-items-courtyard.png. Conversion dimensions/alpha/anchors/reference hashes pass; actual COURTYARD_QA_OK passes with all eleven textures loaded. Existing sandbox log/cache/certificate errors persist. No key/scroll/food/pouch usage mechanic is claimed. Future package allowlist and count updated; review-05 ZIP remains the older seven-icon snapshot. Full 96-icon/UI/effects target and broader pack remain incomplete.

### 2026-10-07 — M5.2.6.2-4 model-derived nine-patch UI panel

Added original panel layout and local DreamShaper panel-767001 (0.40 denoise), inspected actual model output: restrained brass frame, small diamond corners and empty dark teal center. export_panel_style.py produces a 96x96/24-color binary-alpha PNG and native StyleBoxTexture with relative texture path, 12px corner/content margins and tiled stretch axes. Assign mosslight/model_ui/panel.tres to a Panel's panel style override and use nearest filtering; copy PNG/TRES together for reuse. This is one UI element, not completion of the 32-element interface target.

Added actual rendered check at 120x80, 320x144 and 600x200. All four 12x12 corners are pixel-identical across sizes (PANEL_STYLE_QA_OK); inspected panel-sizes.png for seams/distortion. Integrated the style behind courtyard's eleven-icon display with explicit inner spacing. Actual COURTYARD_QA_OK passes and panel-courtyard.png inspected. Existing sandbox log/cache/certificate errors persist. Future package allowlist includes style/texture/check; review-05 ZIP unchanged. Buttons, selection states, dialogue/shop/inventory interactions, broader assets and artistic acceptance remain outstanding.

### 2026-10-07 — M5.2.6.4 native button theme states

Added export_ui_theme.gd: reusable Theme for Panel/PanelContainer and Button normal/hover/pressed/disabled styles derived from the existing model panel, with a visible two-pixel keyboard-focus outline and cream text. These are modulated states of one artwork, not separately generated assets. ResourceSaver uses relative paths; inspected exported references to panel.png and panel.tres. Added model_ui/README.md covering three-file reuse, margins, nearest filtering, rebuilding and limitations.

Added check_ui_theme.gd using actual injected mouse clicks, motion and keyboard Space: enabled toggle activates once, disabled click is rejected, keyboard activation/focus and mouse hover pass. Inspected actual ui-buttons.png with hover/selected/disabled/focus states. UI_THEME_QA_OK passes; existing sandbox log/cache/certificate errors persist. Future package allowlist includes Theme/docs/test, old ZIPs unchanged. This supplies one reusable control treatment; menus, inventory/shop/dialogue flows, additional controls, accessibility review and full pack/art acceptance remain incomplete.

Follow-up verification: this Godot build retained res:// references despite FLAG_RELATIVE_PATHS. Added explicit same-folder dependency normalization and rejection of remaining res:// references after saving. Rebuilt and inspected actual relative panel.png/panel.tres references; UI_THEME_QA_OK passes again. The initial flag-only export was insufficient.
### 2026-10-07 — M5.2.6.4 interactive item selection example

Added reusable model_inventory.gd PanelContainer using the native theme and eleven 32px icons. Mouse/keyboard selection maintains one selected item, emits its ID and updates readable name/description text. Replaced the courtyard's decorative slots with this panel. This is an asset collection browser, not a quantities/equipment/consumable or saved-inventory implementation.

Added check_inventory.gd with real mouse and Space input, detail-text checks, exclusive selection and panel-bound checks. Character movement is suppressed while a BaseButton owns GUI focus; Escape inside the collection releases focus. Verified that held Right cannot move the character during UI navigation and resumes after Escape. INVENTORY_QA_OK and existing COURTYARD_QA_OK pass. Inspected interactive-inventory.png; existing sandbox log/cache/certificate errors persist. Future package allowlist includes the component/check; old ZIPs unchanged. Full catalog, gameplay inventory/shop/dialogue flows and art acceptance remain outstanding.
### 2026-10-07 — M5.2.7.2 independent left-facing Rowan source

Inspected the current exporter: W/NW/SW gameplay clips remain horizontal reflections, including asymmetric straps/hair. Added prepare_rowan_left.py using a mirrored pose scaffold with a camera-facing utility sheath based on the front design's left hip. Local DreamShaper/IPAdapter rowan-left-768001 (denoise 0.34, reference 0.25) redraws the left view using Rowan's own illustration reference; it is not a final mirrored E image. Inspected original output: bob, bare shoulder band, bracer, tunic, boots and visible hip attachment retained, with drawing/proportion drift still requiring review.

Added independent static conversion with explicit vertical landmarks, existing motion palette and 96x144 cell. Initial strict sole check failed by one pixel; corrected anchoring before saving, then passed binary-alpha/sole-y122 checks and actual LEFT_STUDY_RENDER_OK. Inspected rowan-left-comparison.png against the existing mirrored idle. Hair part, sheath occlusion, joint locations and cloth silhouette still need review. Existing gameplay W sheets are unchanged; no walk/run conversion or reduction of the three mirrored directions is claimed. Existing sandbox log/certificate errors persist. Full goal remains incomplete.
### 2026-10-07 — M5.2.7.2 isolated independent-W motion study

Added prepare_left_motion.py to map the independently model-redrawn rowan-left-768001 illustration into the existing side rig's landmark coordinates. Its temporary right-facing orientation is reversed in the final W export; no E illustration pixels are used. Alignment/source hashes are recorded. build_side_motion.py now accepts optional source/output paths while preserving its defaults. Existing rig masks and small occlusion fills are reused, so this remains a cutout study rather than newly model-generated animation poses.

export_left_motion.py creates isolated 96x144 W walk/run sheets (eight frames each), GIFs and a contact board with the existing idle-W palette. It removes only detached one/two-pixel resampling residue. check_left_motion.py passes 16 distinct connected bounded binary-alpha frames, grounded walk and run flight/contact, and source hashes. preview_left_motion.gd actually plays both clips in Godot and verifies all frames are visited: LEFT_MOTION_QA_OK and LEFT_MOTION_RENDER_OK. Inspected godot-left-motion.png; existing sandbox log/certificate errors remain.

Outputs: production/pixel-rpg/model-wave-01/guided/left-motion/. Skirt rigidity, elbow transitions, restrained cape movement and accessory readability still need refinement. Gameplay sheets, mirrored-direction count and previous packages are unchanged. This is a reproducible isolated motion slice, not art acceptance or full goal completion. Next: improve W garment/joint motion, compare all direction transitions, then integrate only after review.
### 2026-10-07 — M5.2.7.3 integrate independent W into the playable study

Preserved prior runtime motion files under guided/before-independent-w before rebuilding. export_model_motion.py now constructs W idle/walk/run from the independent left illustration's canonical alignment and cutout poses, then restores W orientation. All directions share the rebuilt 128-color palette; native SpriteFrames retains 24 clips/160 timeline cells/152 distinct cells. NW and SW remain explicit mirrors. Model hashes/alignment and per-pose provenance are included. Future review-package wording now reflects two mirrored headings; existing ZIP snapshots remain unchanged.

check_direction_sources.py verifies every sheet hash, W source hashes and independent pixels, and actual per-cell equality for declared mirrors. Its initial slash-string path assertion failed on Windows separators; replaced with Path.parts and reran successfully. IDLE_QA_OK, DIRECTION_SOURCE_QA_OK, MODEL_PLAYABLE_QA_OK and NATIVE_SPRITEFRAMES_QA_OK pass after actual Godot reimport. Playback checks cover eight headings, walk/run/idle, live Shift, speed and collisions. Inspected integrated-eight-directions.png and idle-review.png. Existing sandbox log/cache/certificate warnings persist.

This is integrated technical-study progress, not final art acceptance. Front/side hem detail and hair silhouettes still drift; cutout elbow/cloth movement remains stiff. NW/SW need independent garment views. Next work should address those directional consistency issues before roster expansion. Full M5-M9 scope remains incomplete.
### 2026-10-07 — M5.2.7.2 independent NW garment illustration

Verified both Comfy queues idle, then used prepare_rowan_nw.py to add the near left-hip sheath to a mirrored NE composition scaffold. Local DreamShaper/IPAdapter rowan-NW-769001 (denoise 0.34, reference 0.22 to the independent W illustration) redraws the rear-left view. Inspected original output: rear cape folds, exposed left shoulder band, bob back and visible hip attachment; an invented long white lining wedge remained.

repair_rowan_nw.py performs a masked local-model correction (769002, denoise 0.25) to continue teal lining across that wedge. Original/output images and graph hashes retained; maximum difference outside the mask is zero. Inspected repaired source. convert_rowan_left.py now supports NW with explicit landmarks, shared palette, 96x144 cell and sole y122. Initial conversion removed white sleeve pixels: replaced global white exclusion with edge-connected white-background removal. Actual Godot comparison then shows the sleeve intact. LEFT_STATIC_OK and LEFT_STUDY_RENDER_OK pass; inspected rowan-NW-comparison.png. Existing sandbox log/certificate warnings persist.

This is a static independent NW candidate only. Gameplay NW/SW remain mirrors; W remains independently integrated. NW cutout masks/animation, cape-tail motion, cross-view hair/hem continuity and final art review are outstanding. Source output: guided/rowan-NW-cloth-769002.png; sprite: mosslight/model_review/rowan-NW.png. Full M5-M9 scope remains incomplete.
### 2026-10-07 — M5.2.7.3 independent NW motion integration

Extended the projected axial rig with an explicitly selected NW source, leftward travel vector, source-specific leg bounds/joints and near-arm masks. The default original four-direction build remains unchanged; NW requires an isolated output directory. Built guided/nw-motion with eight walk and eight run poses from rowan-NW-cloth-769002, retaining teal cape pixels in front of the legs. No NE sprite pixels are reflected into this animation. Cape still follows the torso and needs independent cloth refinement.

Preserved prior runtime sheets in guided/before-independent-nw. Unified exporter now normalizes NW using its own landmarks/0.256 horizontal scale and creates independent idle/walk/run in the shared palette. Only SW remains a declared mirror. Updated provenance checks and future package wording; existing ZIPs unchanged. PROJECTED_EXPORT_QA_OK and PROJECTED_ELBOW_QA_OK pass for NW, including distinct bounded cells, source hashes, alternating leg recovery, run flight and greater run elbow bend. DIRECTION_SOURCE_QA_OK and IDLE_QA_OK pass.

After actual Godot reimport, MODEL_PLAYABLE_QA_OK verifies all headings/actions, normalized speeds, collisions and live Shift. NATIVE_SPRITEFRAMES_QA_OK verifies 24 clips/160 timeline cells. Inspected nw-motion/integrated-eight-directions.png: NW rear garment orientation is coherent, but stiffness, cape swing and gait consistency remain visible review issues. Existing sandbox log/cache/certificate errors persist. Next: independent SW source/animation and cross-direction garment/gait cleanup. Full M5-M9 scope and artistic acceptance remain incomplete.
### 2026-10-07 — M5.2.7.2-3 independent SW source and isolated motion

Verified both Comfy queues idle. prepare_rowan_sw.py creates a front-left composition scaffold with the near left-hip utility sheath. Local DreamShaper/IPAdapter rowan-SW-770001 (denoise 0.34, reference 0.25 to independent W) redraws the view. Inspected original model output: frontal throat clasp/buckle, bare shoulder bands, short white tunic, hip sheath and rear teal cape remain readable; hair/hem consistency still needs art review.

Extended static conversion with explicit SW landmarks and shared palette. Actual Godot rowan-SW-comparison.png inspected; LEFT_STATIC_OK and LEFT_STUDY_RENDER_OK pass with binary alpha/sole y122. Extended the axial rig with SW-specific limbs and arm masks, negative-X/positive-Y travel vector and isolated sw-motion output. Original default four-direction build is preserved; left diagonal builds require explicit output directories. Produced eight walk and eight run cutout frames. PROJECTED_EXPORT_QA_OK and PROJECTED_ELBOW_QA_OK pass with source/sheet hashes, distinct bounded frames, alternating recovery/run flight and articulated arms.

SW movement remains an isolated study; gameplay still mirrors SE for SW. No claim that all eight runtime views are independent yet. Motion-contact.png inspected; projected movement and torso-driven cape remain stiff. Next: normalize/integrate SW and verify live direction changes, then cross-direction clothing/gait cleanup. Existing static Godot sandbox log/certificate errors persist. Full M5-M9 scope and art acceptance remain incomplete.
### 2026-10-07 — M5.2.7.3 all eight independent runtime views

Preserved previous sheets in guided/before-independent-sw. Unified exporter now uses SW source-specific landmarks and 0.256 horizontal scale for idle/walk/run. Runtime mirror_sources is empty: all eight headings have independently model-redrawn illustration sources. They still use cutout/image-warp motion, not independently generated model animation frames. Source checks verify eight distinct idle-source hashes, all recorded source/sheet hashes and W/NW/SW pixels differing from opposite-heading reflections. Future package wording updated; existing ZIP snapshots unchanged.

DIRECTION_SOURCE_QA_OK and IDLE_QA_OK pass. Actual reimport, MODEL_PLAYABLE_QA_OK and NATIVE_SPRITEFRAMES_QA_OK pass for all directions/actions, movement speeds, collision and Shift input. Inspected sw-motion/integrated-eight-directions.png. Existing sandbox log/cache/certificate errors persist. Hair silhouette, tunic/shorts/shoulder details and cape stiffness still differ across views; this is not art acceptance or full pack completion.

New gait finding from authoritative rig/export/controller parameters: SW walking stance has source stride 18 and forward X magnitude 0.707, normalized by 0.256 at 10 fps. Over four stance intervals this cancels only 2*18*0.707*0.256/0.4 = 16.29 screen pixels/s horizontally, while the controller moves diagonally at 65/sqrt(2) = 45.96 pixels/s horizontally. Thus existing normalized-speed and alternating-leg tests do not prove foot locking; substantial residual sliding is expected. E likewise has 46 pixels/s stance travel at final 0.2 scale against 65 controller pixels/s. Next priority is world-space foot-contact verification and consistent stride/timing, followed by cloth/identity cleanup before roster expansion. Full M5-M9 remains incomplete.
### 2026-10-07 — M5.2.7.3 side gait calibrated to runtime speed

build_side_motion.py revision 4 computes half-stride from final horizontal scale, actual walk/run targets (65/115 pixels/s), four stance intervals and 0.1/0.075-second frames. Previous revision 3 outputs are preserved in each rig folder's v3 directory. The first larger run stride exceeded the existing stretch ceiling (1.0942); lowering the running hip by four source pixels restored the original <8% stretch bound without weakening the check. Both E and independent W rigs rebuilt, followed by unified runtime and isolated W exports.

Added check_runtime_side_gait.py. It reads controller speed literals, exported clip FPS and rig ankle trajectories, and checks only consecutive grounded stance samples (excluding swing/flight). SIDE_RUNTIME_GAIT_OK passes 20 intervals with numerical world-X residual below 1e-6 pixel. This is sampled horizontal contact verification, not a raster/sub-frame, vertical contact, collision or diagonal foot-lock claim. Existing side/left distinct-frame/contact/stretch checks and eight-direction source checks pass.

Godot reimport, MODEL_PLAYABLE_QA_OK and LEFT_MOTION_RENDER_OK pass; inspected updated godot-left-motion.png. Existing sandbox log/cache/certificate errors persist. An unrelated mistyped Python --version command failed after both builds completed; corrected interpreter path was used for subsequent successful checks. Remaining priority: calibrate six axial/diagonal headings with source-specific X/Y projection, then verify visible foot placement and direction-change phase, cloth and identity continuity. Full pack remains incomplete.
### 2026-10-07 — M5.2.7.3 isolated axial/diagonal gait calibration

Added explicit --runtime-stride to build_axial_motion.py; it requires an isolated output directory. Converts intended final-pixel foot displacement back through each view's independent X scale and piecewise Y mapping, using actual boot-patch sole bounds. Normalized direction vectors remove the approximate 0.707 scaling error. Experimental raw canvas is padded to 512x832 so extended feet are not silently clipped; legacy preview remains 96x128 with a declared smaller 0.15 sampling scale. Default runtime generation remains unchanged.

First trial retained 10/13.333 fps and produced visibly elongated legs. Preserved it in each calibrated folder's long-stride-rejected directory. Second trial uses 16/20 fps, reducing displacement per stance interval while preserving 65/115 movement targets. Generated calibrated-axial, calibrated-nw and calibrated-sw (96 movement frames). check_projected_gait.py verifies six headings/60 grounded intervals in final XY coordinates against controller speeds, finite source bounds and source hashes; PROJECTED_GAIT_OK passes below 1e-6 numerical error. This verifies sampled trajectories only, not raster contact or artistic pose quality.

Actual Godot calibrated S/N preview captured and inspected (calibrated-axial/godot-cadence.png). MODEL_AXIAL_MOTION_CAPTURE_OK passes; existing sandbox log/cache/certificate errors persist. Legs still deform stiffly and cadence differs from the integrated side animations. These candidates are NOT integrated or accepted; current gameplay's six axial/diagonal clips still retain the earlier sliding limitation. Next: improve knee/hip/boot pose construction and unify cadence across directions, then verify real rendered contact before integration. Full M5-M9 scope remains incomplete.
### 2026-10-07 — M5.2.7.3 bounded-leg experiment and pose limitation

Added optional --bounded-legs (requires isolated --runtime-stride). Two-pass leg targets first calculate one shared pelvis drop to keep maximum hip/ankle reach near source length, then place the knee proportionally with a small recovery bend. Boot patches remain rigid; planted soles are unchanged. Source hip/knee/ankle coordinates and segment ratios are recorded. Generated bounded-axial/nw/sw separately; previous trials and runtime assets preserved.

Extended check_projected_gait.py --bounded: six headings/60 grounded XY intervals still pass; maximum segment ratio 1.0187 remains below 1.04. However minimum projected ratio is 0.1683, and shared pelvis drop reaches 57.17 source pixels. These are significant compression/bobbing concerns, not proof of anatomically correct motion. Actual Godot S/N preview inspected at bounded-axial/godot-bounded-legs.png; MODEL_AXIAL_MOTION_CAPTURE_OK passes with existing sandbox log/cache/certificate errors.

Decision: do not integrate this candidate. Pure affine standing-pose segments cannot supply convincing depth-facing bent-leg/boot silhouettes. Next production step is local-model-assisted authored key poses (contact, passing/recovery), retaining reference costume and rigid boot design, then interpolate/clean up and revalidate contact. Numerical trajectory checks remain useful but must not substitute for art quality. Full goal remains incomplete.
### 2026-10-07 — M5.2.7.3 local-model raised-knee key pose

Added generate_rowan_keypose.py: source-preserving masked local DreamShaper redraw of the screen-right leg, with an explicit raised-knee/foreshortened-thigh/bent-boot guide. Both queues verified idle before each sequential trial. 771001 at denoise 0.42 preserves every pixel outside its mask and produces a distinct raised-knee silhouette, but invents a dark boot cuff and changes toe/cuff design. 771002 at 0.25 also preserves unmasked pixels but yields a stiff straight boot with a poor toe; rejected as a replacement for the first study. Original source, guides, masks, graphs, hashes and outputs retained.

convert_rowan_keypose.py applies exactly the same coordinate mapping and existing idle-S palette to the original and 771001. KEYPOSE_CONVERSION_OK passes binary alpha and identical upper 75 pixel rows. Inspected rowan-keypose-comparison.png at 3x nearest. The silhouette is model-authored rather than an affine stretch of the standing boot; this does not prove anatomical or costume acceptance. Output mosslight/model_review/rowan-front-knee.png is one isolated lower-body study. No runtime animation or complete sequence was replaced.

Next: improve the explicit bent-boot/cuff/toe guide while retaining the original folded cuff design, then author complementary contact/passing poses with mask-preserved identity. Do not batch-generate full animations until the key-pose design is coherent. Existing axial/diagonal runtime sliding and broader M5-M9 scope remain incomplete.
### 2026-10-07 — M5.2.7.3 reference-boot key-pose pair

Extended generate_rowan_keypose.py with --reference-boot. It uses the original boot's folded cuff and rounded toe as a resized/rotated composition reference before masked local inference, rather than asking the model to invent those costume details from a flat guide. Trial 771003 (denoise 0.22) visibly retains the cuff/toe better than 771001/771002. Added --screen-leg left: reflect only the editable pose scaffold, composite over the unchanged original, then locally redraw. Trial 771004 creates the complementary raised-leg candidate; the character's upper body is never mirrored. Both runs verify empty queues and zero pixel difference outside the mask.

Converter accepts explicit trial seed and writes separate variant outputs, preserving earlier comparisons. Both 771003/771004 pass identical-upper-75-rows and binary-alpha checks at 96x144 using the same source transform/palette. Added actual Godot preview_rowan_keyposes.gd; KEYPOSE_PAIR_RENDER_OK passes and rowan-keypose-pair.png inspected. Existing sandbox log/certificate errors persist. Cuffs/toes are more consistent, but knee/shorts transitions and leg silhouettes remain review items.

These are two static passing-pose candidates, not a finished walk/run loop or runtime replacement. Next: complementary contact/transition poses plus coordinated arm/weight motion, followed by sequencing and foot-contact verification. Current demo and full-pack acceptance remain incomplete.
### 2026-10-07 — M5.2.7.3 model-authored half-lift transitions and pose loop

Added bounded --lift control to the reference-boot guide. Generated 771005/771006 at lift 0.5, denoise 0.22 for screen-right/left respectively; queues checked before each local run and outside-mask pixel difference remains zero. Inspected model outputs and converted both using the same source transform/palette. Neutral conversion is now saved explicitly. Upper 75 rows remain identical across all candidates.

Added export_rowan_pose_cycle.py: neutral/half-right/right/half-right/neutral/half-left/left/half-left, eight timeline frames and five unique model-derived poses. Binary alpha, bounds, unchanged upper rows and source hashes verified. Outputs guided/keypose-cycle/leg-poses.png, leg-poses.gif and manifest. This is an in-place leg-pose comparison, not a walking/running animation or evidence of foot locking.

Added actual Godot preview_rowan_pose_cycle.gd; KEYPOSE_CYCLE_RENDER_OK observes all eight timeline frames during playback. Inspected sheet and godot-cycle.png; existing sandbox log/certificate errors persist. Arm motion, weight shift, supporting-foot trajectory, contact poses and cloth remain absent, so the gameplay animations are unchanged. Next: coordinate these authored lower-leg silhouettes with body/arm motion and grounded stance before considering integration. Full M5-M9 scope remains incomplete.
### 2026-10-07 — M5.2.7.3 contralateral arm key-pose studies

Extended local key-pose generator with --swing-arm. It starts from the authored 771003/771004 raised-leg sources, masks only the opposite arm and exposed cape behind it, then locally redraws the elbow, leather bracer and hand. Right-arm guide coordinates account for the original asymmetric arm placement (reflection around x271, not the canvas center). Trials 771007/771008 at denoise 0.30 preserve every pixel outside their masks; inspected originals for silhouette, costume and occlusion.

Converter reads generation provenance to choose its protected region: leg-only trials still require identical upper 75 rows; arm-edit trials require identical upper 54 rows because their authorized edit crosses the lower torso. Both arm candidates pass binary-alpha and protected-pixel checks. Godot preview_rowan_keyposes.gd --arms captures rowan-arm-keypose-pair.png; KEYPOSE_PAIR_RENDER_OK passes and actual image inspected. Existing sandbox log/certificate errors persist.

Opposite-arm/leg coordination is now represented in two static candidates. Hands/elbows are angular, and cape fill behind the removed standing arms is too flat; these remain art defects, not accepted final poses. Existing leg-only loop and runtime animations unchanged. Next: arm transition poses, improved exposed cape/hand contours, then coordinated sequencing and supporting-foot/weight transfer. Full M5-M9 goal remains incomplete.
### 2026-10-07 — M5.2.7.3 coordinated arm/leg transition loop

Extended arm guide rotation for half/full swing, selecting matching authored half/full leg sources. Added restrained cape shadow/highlight guides behind removed standing arms. Sequential local trials 771009/771010 produce half-swing transitions; 771011/771012 refresh full-swing poses. Each run checks idle queues, records source/graph/output provenance and verifies zero outside-mask pixel differences. Inspected all four model sources; hands/elbows and cape fill remain simplified art-review areas.

Converted all four with identical upper 54 rows and the shared 96x144 mapping/palette. export_rowan_pose_cycle.py --arms creates a separate coordinated-cycle folder, preserving the earlier leg-only comparison. The new eight-cell cycle contains five distinct poses with contralateral arm/leg pairing. Alpha/bounds/identity/source checks pass. Actual preview_rowan_pose_cycle.gd --arms plays all eight timeline cells (KEYPOSE_CYCLE_RENDER_OK); inspected godot-cycle.png. Existing sandbox log/certificate errors persist.

Outputs: guided/coordinated-cycle/leg-poses.png and leg-poses.gif. This is still an in-place coordination study, not final walking/running: torso/weight remain fixed, stance does not compensate world movement, return uses repeated transition poses, and cloth motion is absent. Runtime remains unchanged. Next: supporting-foot/contact and weight-transfer authoring with rendered gait checks. Full M5-M9 scope remains incomplete.
### 2026-10-07 — M5.2.7.3 authored contact pair and raster drift evidence

Added --contact to the local key-pose generator. Each original leg supplies its own boot/cuff reference; the guide puts one foot forward and the other behind, preserving teal cape regions. Local trials 771013/771014 at denoise 0.28 produce opposing contact candidates. Both runs verified idle queues and zero outside-mask changes. Inspected originals; costume retained with small cuff speckles/contour roughness still present. Converted both with identical upper 75 rows and common palette/coordinates.

Added --contact pose-cycle variant, preserving earlier loops. Contact-left/right replace the two neutral cells, yielding six distinct poses over eight timeline cells. Actual Godot playback visits all cells; KEYPOSE_CYCLE_RENDER_OK passes and contact-cycle/godot-cycle.png inspected. Existing sandbox log/certificate errors persist. Contact arms remain neutral and transfer timing is not final.

New raster diagnostic extracts boot sole Y from explicit left/right boot ROIs in the final sprites. At 65 px/s and 120 ms/frame, intended stance intervals drift 2.8 px for contact-to-half-lift and 7.8 px for subsequent transitions, for both feet. This is measured failure evidence, not a foot-lock pass. Runtime stays unchanged. Next: author/retarget the support-foot sequence and timing against these pixel measurements, preserving boot shape and coordinated arm poses. Full M5-M9 remains incomplete.

### 2026-10-07 — M5.2.7.3 rigid-boot sampled stance experiment

Added export_rowan_support_cycle.py, deriving an isolated support-cycle from the authored contact cycle. At 16 fps and 65 px/s, translated each supporting boot without changing its raster pixels; only the exposed thigh above the cuff is resampled. Source hashes, unchanged upper 85 rows, binary alpha and exact boot pixel preservation pass. Final-raster sole measurements give 0.0625 px residual per sampled stance interval (six intervals), versus 2.8/7.8 px in the earlier 120 ms contact study. This does not establish continuous foot lock or stance transfer between halves.

Actual Godot preview with --support plays all eight cells at 16 fps; KEYPOSE_CYCLE_RENDER_OK and exit 0. Inspected review-sheet.png and godot-cycle.png. Existing sandbox log/certificate errors remain. Thigh compression/cuff transitions are visibly abrupt; fixed torso, neutral contact arms and absent cloth motion still prevent final acceptance. Keep this experiment separate from gameplay. Next: authored support-leg foreshortening and body-weight/contact transition refinement, then moving-ground visual verification before integration. Full M5-M9 goal remains incomplete. Generated previews stay local and ignored.

### 2026-10-07 — M5.2.7.3 actual moving-position comparison

Added preview_rowan_travel.gd: render the original contact cycle and rigid-boot candidate side by side against a fixed grid with actual node translation at 65 px/s. Captured 64 deterministic time samples spanning one second, retaining exact positions/frame indices. TRAVEL_CAPTURE_OK passes with exit 0; sandbox log/certificate warnings remain. review_rowan_travel.py assembles actual engine captures into comparison.gif and comparison.png and records held-frame stance traces. Inspected the four-time contact sheet.

The candidate has 3.234375 px sole variation within each sampled stance window despite 0.0625 px differences at frame changes. The latter was never a continuous-lock proof. This held-frame effect is distinct from accumulated gait drift; do not chase a zero-subframe-error target by arbitrarily increasing frame count or hiding it with camera motion. More material visible defects are the fixed upper-body weight and compressed thigh/cuff transitions. Next priority remains authored weight transfer/support-leg silhouettes, followed by the same moving comparison. These previews are diagnostic studies, not accepted walking/running assets, and gameplay is unchanged. Full approved M5-M9 scope remains active.

### 2026-10-07 — M5.2.7.3 restrained weight-transfer candidate

Added export_rowan_weight_cycle.py, deriving weight-cycle from the hash-verified support sheet. Authored eight torso offsets: (-1,1), (-1,2), (-1,0), (0,-1), (1,1), (1,2), (1,0), (0,-1). Head/upper torso through row 74 translate rigidly; rows 75-87 form the connecting tunic/thigh band. All pixels from row 88 down are byte-identical to the previous candidate, retaining boot design and sole trajectories. WEIGHT_CYCLE_OK verifies binary alpha, rigid upper art and unchanged lower raster across all eight cells. This is compositing of existing model-authored artwork, not a new model inference.

Extended actual Godot travel preview and capture packaging with --weight. Both compared loops run at the same 16 fps and 65 px/s, so the comparison isolates body motion. TRAVEL_CAPTURE_OK and TRAVEL_REVIEW_OK pass; inspected the four-time comparison image. Existing log/certificate sandbox errors remain. Outputs weight-cycle/leg-poses.gif and weight-cycle/travel/comparison.gif stay ignored/local. The torso now has limited lateral support shift and vertical recoil/rise, but compressed thigh/cuff transitions and neutral contact arms remain visible limitations. Held-frame sole span stays 3.234375 px as expected because lower-body pixels are unchanged.

Do not replace gameplay or claim final walk/run acceptance yet. Next: improve authored contact-arm and leg-to-tunic transitions, review the full loop including recoil frames, then integrate only a visually coherent candidate. Full approved M5-M9 inventory and acceptance remain incomplete.

### 2026-10-07 — M5.2.7.3 contact-arm authoring and phase correction

Extended generate_rowan_keypose.py with --contact-arm, using authored contact 771014/771013 as immutable source outside the arm mask. Sequential local DreamShaper trials 771015 (left leg forward/right arm forward) and 771016 (right leg forward/left arm forward), denoise 0.32, both verify idle queues and zero outside-mask differences. Inspected both source images and converted with the common palette/coordinates; upper 54 rows remain identical. Bracer/hand anatomy is still simplified.

Inspection also found a timing defect: the previous full/half/full arm ordering repeated its extreme before the next contact. Added --phased-arms to weight exporter: right-full, right-half, neutral, left-half, left-full, left-half, neutral, right-half. Upper-arm donors are recorded with hashes, composed above row 81 before the existing restrained weight shift; supporting legs/boots below row 88 remain unchanged. This composes existing locally authored poses and does not mirror the character. Output is separate phased-cycle, preserving previous candidates.

Actual Godot comparison --phased-arms compares both candidates at 16 fps/65 px/s; 64 rendered samples captured. WEIGHT_CYCLE_OK, TRAVEL_CAPTURE_OK and TRAVEL_REVIEW_OK pass, with the known sandbox log/certificate warnings. Inspected all eight new cells and moving comparison contact sheet. No neutral-arm reset at the two contacts; the passing poses now have neutral arms. Existing thigh compression, limited hand silhouettes and absent independent cloth motion remain unresolved; no gameplay replacement or final acceptance. Next: lower-body/tunic transition cleanup and loop review before integrating this front-walk candidate. Full M5-M9 scope remains incomplete.

### 2026-10-07 — M5.2.7.3 playable front-walk candidate

Added authoring/front_walk_review.gd: loads the existing collision review room, duplicates SpriteFrames in memory and overrides only walk_S with phased-cycle at 16 fps. WASD/arrows and Shift use the existing controller; F6 toggles candidate/baseline. Shared resources remain unchanged. Documented the exact launch command in pixel-rpg-demo/README.md. Hid duplicate header labels in this view and corrected the obsolete mirrored-left warning in model_playable.gd to reflect the current independent sources.

Actual Godot --check passes live downward input, all eight frames, idle on release, stationary stop, restart, actual F6 input, baseline FPS preservation and west-wall collision. FRONT_WALK_PLAYABLE_OK, exit 0; inspected phased-cycle/playable.png after header cleanup. Existing sandbox log/certificate/shader-cache warnings persist. This is a controllable integration candidate, not a replacement for the shared final animations. Other directions and run remain existing studies; lower-body transitions and broader art acceptance still need work. Full M5-M9 goal remains active.

### 2026-10-07 — M5.2.6.2–M5.2.6.4 equipment and ingredient coverage

Expanded the model-first item collection from eleven to fourteen entries: hand axe, teal-gem brass ring and woodland mushroom. Added owned composition guides and ran sequential local DreamShaper img2img on idle queues. Axe 772001 was rejected for stone-like cracks; 772004 at denoise 0.60 removes those cracks and supplies a decorated teal/brass blade. Ring 772002 and mushroom 772003 at 0.48 retained their basic silhouettes. All model sources and generation records remain local; no cloud inference used.

Extended the existing converter: shared palette, 32x32 canvas, binary alpha and bottom anchor y28; ring inner hole explicitly transparent. Reference asset hashes remain unchanged. Inspected inventory-fourteen-review.png and actual inventory-fourteen-godot.png. Added the three entries to the reusable Godot item browser, made the review board three rows and updated the future package allowlist/description (no new ZIP created). Mushroom volume and ring contour still need art polish; automatic conversion is not final pixel-art acceptance.

Fresh Godot import succeeds. INVENTORY_QA_OK verifies fourteen buttons, actual mouse selection/descriptions for all three new entries, keyboard selection, exclusive toggle state, panel/window bounds, UI movement lock and Escape release. Existing sandbox log/certificate/shader-cache warnings persist. This completes a concrete item expansion under the existing approved scope while character contact/thigh refinement remains open. Full M5-M9 coverage and final acceptance remain incomplete.

### 2026-10-07 — M5.2.6.3–M5.2.6.4 modular timber room

Added export_timber_kit.py and timber_room.gd. Six native modules derive from the existing locally generated timber-wall material: back, side cutaway rail, front rail, left/right back corner and front corner. Each has a relative PNG reference and its own collision rectangle; no new model inference or external art. The room builder exposes bays (256 px each) and depth (32 px rows), preserving floor tiling and consistent 1:1 texel scale. This covers rectangular rooms only, not arbitrary concave/T-junction layouts or full-height side walls.

Replaced the interior's monolithic wall/floor and invisible boundary colliders with this modular shell. Furniture, hero and door remain shared. Existing floor depth grows from 432 to 448 px to align the 32px grid. Inspected actual ground/modular-room.png: back-to-side corners and front boundary now visible. Added module files/builder to future package allowlist; no new delivery ZIP generated.

TIMBER_KIT_QA_OK passes for 1x6 and 3x14 rooms, probing actual physics at seams/corners and open floor. FURNITURE_ROOM_QA_OK passes all existing furniture collision checks after integration. WORLD_LINK_QA_OK passes live E, repeated-input guard, two doorway round trips and retained reward. All exit 0 with existing sandbox log/certificate/cache warnings. The art remains a simple material study; richer trim, wall decor, junctions and final polish are still pending. Full M5-M9 goal remains incomplete.

### 2026-10-07 — M5.2.6.4 independent review snapshot 06

Created builds/mosslight-review-06.zip: 106 hash-listed project files plus manifest, 776531 bytes, SHA256 c23327c270da6fa7e5bd80102ab8098ba6754680ca5e81c9ef1db14627cbfcda. Includes current eight-source runtime character, fourteen inventory icons/browser/theme, linked courtyard/interior, modular timber room, furniture and optional phased front-walk comparison. The comparison script now supports an in-project candidate sheet and optional capture path. Packaged copy removes the authoring-directory fallback; its shared runtime animation remains unchanged. No model weights, cache or production directory included. Previous snapshots preserved.

Extracted the actual ZIP to validation/pixel-rpg/review-06-relocated and performed fresh Godot import. WORLD_LINK_QA_OK, FRONT_WALK_PLAYABLE_OK, TIMBER_KIT_QA_OK, MODEL_PLAYABLE_QA_OK/LIVE_IDLE_QA_OK and INVENTORY_QA_OK all pass with exit 0 in that independent project. Inspected the relocated inventory screenshot. ZIP contents/each hash rechecked after validation. Known sandbox user-directory/log/cache/certificate errors remain; no missing asset/script failure observed. Added relocated validation directories to .gitignore to keep generated project copies out of commits.

This is a portable review snapshot, not final commercial delivery. Broader roster/catalog, animation/art polish and full M5-M9 acceptance remain incomplete. Local run requires Godot 4.7.2, not ComfyUI/Python/network. Open the extracted project.godot and F5; optional front-walk launch is documented in its README.

### 2026-10-07 — M5.2.6.2–M5.2.6.4 Bren dragonborn rework

Returned to roster coverage using the existing CH03 specification. Added an owned broad dragonborn guide: grey reptilian head, paired ivory horns, steel shoulders, teal split tabard, leather boots/bracers and a visible scaled tail. Local DreamShaper 773001 at denoise 0.58, with both queues verified idle, preserves these distinguishing features better than the old human-faced horned youth. Model output inspected; no external character art or cloud inference used.

Converted to 96x144 with foot anchor [48,122], binary alpha and the existing Rowan palette plus six grey/steel and six gold shades. Preserved source aspect ratio and tail. BREN_STATIC_OK passes. Actual Godot three-character static comparison BREN_RENDER_OK passes; inspected bren-godot.png alongside Rowan/Sylva. Existing sandbox log/certificate warnings remain. The front-facing camera and scale/gauntlet fine detail still need cleanup. Updated the existing review registry with this replacement study while keeping delivery_approved false and selected_source null.

This adds a usable static review sprite and original illustration, not a completed character: no Bren rear/side views or idle/walk/run animation yet. Next: reconstruct rear armor/tabard/tail and side profile from this source while retaining species/build and shared style. The review-06 ZIP is unchanged and does not include this new study. Full M5-M9 goal remains incomplete.

### 2026-10-07 — M5.2.7.1 Bren rear garment study

Added prepare_bren_back.py from the owned front illustration: explicit rear skull/neck, armor shells, closed back tabard/seam, plain belt back, rear boot shafts/heels and tail root. Local 773002 at denoise 0.40 retained side-face traces and a neck white patch because the guide did not cover the entire old face. Revised the head/neck coverage and generated 773003 at 0.45. Inspected both; selected 773003 for static review, retaining the rejected trial. Back no longer shows frontal eyes/muzzle, chest buttons or belt buckle. Rear armor lighting, boot volume and flank accessory consistency still require refinement.

Extended the existing Bren converter/actual Godot preview with --back, preserving the front sprite. Shared palette and 96x144 cell/sole122 tests pass; BREN_STATIC_OK and BREN_RENDER_OK exit 0. Inspected bren-back-godot.png. Existing sandbox log/certificate warnings remain. This is independent local-model rear artwork, not a reflected frontal sprite. Side/diagonal views and all Bren animations remain unbuilt; neither view is final art acceptance. Review-06 remains unchanged. Next: profile garment/anatomy study, then consistency cleanup before any motion batch.

### 2026-10-07 — M5.2.7.2 Bren side-profile study

Added prepare_bren_side.py with original profile anatomy, pauldron depth, side-split tabard, boot toes and trailing tail. Local 773004 (0.53) incorrectly produced a hood/human facial patch; rejected. 773005 (0.38, front identity reference 0.35) restored bare anatomy but interpreted horns as ears and flattened armor; rejected. Added actual owned front horn/metal surface crops to the guide, then 773006 (0.48, front reference 0.55) produced a clearer dragon profile and metal shoulder. Inspected all outputs. Existing queued sessions were polled to completion; no duplicate submission after a timeout.

Extended converter with mutually exclusive --back/--side, preserving front/rear files. Converted 773006 into the common 96x144/sole122/shared palette and declared material ramps. Actual preview_bren.gd --turnaround shows front, rear and side together; BREN_STATIC_OK and BREN_RENDER_OK pass, known sandbox warnings remain. Inspected bren-turnaround-godot.png. This is an independent local-model side study, not a reflected/deformed frontal output.

The new side invents a central horn ornament, extra cheek spikes and differing boot/bracer details. These are explicitly unaccepted design drift; do not animate or ship them as a coherent completed character yet. Next: remove those additions and reconcile rear/side armor and boots to the front before diagonal/motion work. Review-06 is unchanged; full M5-M9 remains incomplete.

### 2026-10-07 — M5.2.7.2 Bren side ornament repair

Added repair_bren_side.py: local masked redraw with explicit source/guide/mask/graph/output hashes and zero outside-mask pixel-difference verification. Trials 773007-773010 attempted simultaneous cheek-spike removal; inspected all and rejected them for white crescents/seams or an excessively flat, squared skull. Expanded masking alone did not solve the anatomy/volume problem. Preserve these trials; do not promote them on numerical mask checks.

773011 limits the repair to the invented central horn ornament, retaining original cheek/head/body pixels. Inspected output: ornament removed; original two horns and the unmasked design retained. Updated the side converter to this source only. BREN_STATIC_OK and actual BREN_RENDER_OK pass; inspected refreshed three-view Godot image. Existing log/certificate warnings remain. Cheek spikes, armor/boot consistency and all diagonal/motion work remain unfinished; no final character acceptance or update to review-06. Next cheek correction needs a better volume/contour guide instead of a flat polygon fill.

### 2026-10-07 — M5.2.7.2 targeted Bren cheek-frill correction

Extended repair_bren_side.py with mutually exclusive --trim-spikes, starting from ornament-clean 773011. Unlike rejected whole-skull fills, this retains the main ear and central head shading, masking only the upper/lower extra frills. Trial 773012 left small guide seams; expanded the painted overlap within the narrow masks for 773013. Inspected both; selected 773013 for the side study. Local inference verifies zero outside-mask pixel differences, so body/tail/equipment remain unchanged. All guides/masks/source/outputs and generation history retained.

Converted the new side at the existing shared palette and 96x144/sole122 contract; BREN_STATIC_OK and actual BREN_RENDER_OK pass with known sandbox warnings. Inspected the updated Godot three-view image. Updated the existing review registry to reference current rear/side sources and explicit unresolved ear/armor/boot/proportion differences. The main pointed ear remains intentionally visible, matching the front's ear concept, but its shape is not yet reconciled. No diagonal views, animation, final character acceptance or review-06 replacement claimed. Next: material/boot consistency and side body depth before movement authoring.

### 2026-10-07 — M5.2.7.2 Bren side boot consistency

Added mutually exclusive --boots masked repair mode starting from head-clean 773013. Replaced the invented near-boot lacing with a plain closed leather shaft, retaining original shoe/toe/sole and all pixels outside the narrow edit mask. Local trial 773014 exposed white guide gaps at the cuff/ankle; rejected. 773015 paints continuous leather through the mask boundaries and clears only the exterior silhouette. Inspected the source result; zero outside-mask difference passes.

Updated the side converter and review registry to 773015. BREN_STATIC_OK (shared palette, binary alpha, 96x144, sole122) and BREN_RENDER_OK pass; inspected the three-view Godot screenshot. Known sandbox log/certificate warnings persist. Side boots now lose the unsupported lacing, but boot volume, pauldron finish, bracer decoration and proportions remain inconsistent across views. This is continued static refinement, not full character completion; all diagonals and animations remain pending. Review-06 unchanged.

### 2026-10-07 — M5.2.6.2–M5.2.6.4 Mira beastfolk healer rework

Added an owned Mira guide from the approved CH05 role/species brief and generated local DreamShaper 774001 at denoise 0.56 after checking both queues idle. Inspected the illustration: copper ponytail, paired furry ears, cream-tipped tail, practical apron/rolled sleeves and ankle boots replace the old teal-haired weapon-bearing study. The model shifted the dress to muted sage/olive and omitted visible herbs; bag/hand readability and role detail remain open. Original body/role design, not a copied anime character.

Added roster-static-studies.json and convert_roster_static.py to record this source and its seven sage/linen palette extensions against Rowan. Output is binary-alpha 96x144 with sole122, preserving proportions. ROSTER_STATIC_OK passes; actual Godot --mira review passes and mira-godot.png inspected with Rowan/Bren. Existing sandbox log/certificate warnings persist. Warm copper/linen/leather harmonize with the set, but softer source contour, front-facing camera and omitted herb detail still need art review. Updated the existing review registry without approving delivery.

Mira is a static front candidate only: all rear/side/diagonal views and idle/walk/run remain pending. Review-06 unchanged. Full approved M5-M9 scope remains incomplete; continue character role/details and garment reconstruction alongside the existing unresolved Bren/Rowan work.

### 2026-10-07 — M5.2.6.2 Mira herb-pouch profession detail

Added repair_mira_herbs.py for a bounded local-model edit of the belt pouch opening. The owned guide adds a tied broad-leaf herb sprig; DreamShaper 774002 retains the face, ears, ponytail, clothing and tail outside the mask exactly (maximum outside-mask pixel difference zero). Both queues checked idle, source/guide/mask/graph/history/output hashes recorded, and final illustration inspected.

Updated the static registry/review source to mira-herbs-774002.png and rebuilt the same 96x144/sole122/shared-palette sprite. The leaf cluster remains visible at game scale; detailed leaf anatomy is naturally limited at this size. ROSTER_STATIC_OK and actual Godot roster render pass, with the existing sandbox log/certificate warnings. Inspected refreshed mira-godot.png. Hand clarity, contour style and gameplay camera remain art-review items; rear/side/diagonals and all animations are still pending. Review-06 unchanged. Next: rear apron ties, ponytail and tail-root construction before further directional work; full M5-M9 scope stays incomplete.

### 2026-10-07 — M5.2.7.1 Mira rear garment reconstruction

Added prepare_mira_back.py and locally redrew the owned rear layout with DreamShaper (774003, denoise 0.42). The rear reconstructs hair/ponytail, crossed apron straps, waist ties, tail attachment and boot heels rather than retaining a frontal apron bib. Source, guide and generation history remain local. Added the rear to the static registry and configurable front comparison to convert_roster_static.py.

Converted to the shared palette plus declared sage/linen ramp, binary-alpha 96x144, anchor (48,122). Actual Godot --mira-back capture inspected; BREN_RENDER_OK and exit 0 confirmed, with existing sandbox log/certificate warnings. Rear shoulder sleeves and cream tail-tip shape still differ from the front and require reconciliation before animation. This is an unapproved static study, not a completed eight-direction character. Review-06 unchanged; full M5-M9 remains incomplete.

### 2026-10-07 — M5.2.7.1 Mira rear sleeve consistency

Added repair_mira_sleeves.py for local masked DreamShaper redraw (774004). Restored a sage blouse sleeve with rolled cuff over the previously exposed near upper arm and a far cuff beneath the ponytail. Both Comfy queues were idle before generation. Source/guide/mask/graph/history and output hash retained locally; outside-mask maximum pixel difference is zero. Inspected full-resolution result before promoting it to the rear static registry.

ROSTER_STATIC_OK and actual BREN_RENDER_OK pass with exit 0; inspected the refreshed Godot front/rear comparison at shared 96x144/sole122 scale. Sleeve color remains readable. Existing sandbox log/certificate warnings persist. Tail-tip shape, garment volume/proportions and overall camera consistency remain unresolved. Side/diagonal views and animation are still pending; no character completion or delivery approval. Review-06 unchanged.

### 2026-10-07 — M5.2.7.2 Mira side-view trials, none accepted

Added prepare_mira_side.py: owned profile layout with single eye/nose silhouette, copper ponytail, furry ears, sage rolled sleeve, vest/skirt, narrow forward apron edge, herb pouch, boots and cream-tipped tail. Checked both queues idle, then ran three sequential local DreamShaper trials. Source, guide, graph, prompt IDs and output provenance are retained. Inspected all full-resolution images.

774005 (denoise .48, reference .4) drifts into a three-quarter face, elongated proportions and invented collar/extra pouch. 774006 (.36, no adapter) retains profile but looks flat and guide-like with crude face/hand. 774007 (.55, no adapter) gains shading but changes sleeves to white, loses the pouch and alters belt/boots/body proportions. All rejected in the existing review registry. No sprite conversion, engine replacement or completion claim for these candidates. Next: stronger shaded profile guide and correct body ratio, not additional blind parameter sampling. Existing front/rear studies and review-06 remain unchanged; full M5-M9 remains active.

### 2026-10-07 — M5.2.7.2 Mira profile reconstruction from retained model source

Added repair_mira_profile.py. Reused the clear profile face from rejected 774007, normalized body height below y235 from 533 to 384 pixels, and locally redrew a shaded sage rolled sleeve, leather belt and herb pouch (774008). This explicitly changes source proportions; the upstream hash and normalization are recorded. Local generation checks both queues; zero outside-mask differences are measured against the normalized source, not the original unscaled illustration. Inspected the resulting image.

Registered the result as an unapproved side static study and added --mira-turnaround engine comparison. ROSTER_STATIC_OK and BREN_RENDER_OK pass with existing sandbox log/certificate warnings. Inspected actual three-view capture: sleeve/belt/herbs now match the intended role, but white collar/socks, visible human ear, head depth and pouch position differ. The tail/background cutout also needs cleanup. These remain blockers to character art acceptance, not reasons to declare this direction complete. No animation integration or review-06 update. Next: remove unsupported garment/anatomy details and reconcile silhouette at native sprite scale; full M5-M9 remains incomplete.

### 2026-10-07 — M5.2.7.2 Mira profile cuff correction and cutout diagnosis

Local detail trial 774009 tried hair-over-ear, collar and cuff repairs together; rejected after inspection for blocky hair and a cuff mask extending into background. Added repair_mira_details.py for the retained narrower 774010 trial: constrain the sock recolor to neutral light pixels inside the ankle region, then local-model composite. Zero outside-mask difference passes. White sock fill is reduced; outlines remain and should not be reported as fully corrected anatomy. Ear/collar unchanged.

Converted 774010 and inspected actual Godot three-view capture; ROSTER_STATIC_OK and BREN_RENDER_OK pass with existing sandbox log/certificate warnings. Investigated suspected tail background: sample points (220,480), (218,490), (230,493), (225,500) all belong to the same white component as the outer background, which the converter removes. Do not expand the cutout into the cream fur to address a tail-shape mismatch. White collar, human ear, cuff outlines, silhouette/pouch and tail-tip consistency remain pending; no completed character or animation claimed. Full M5-M9 and review-06 status unchanged.

### 2026-10-07 — M5.2.7.2 Mira sage collar and side-lock repair

Extended repair_mira_details.py with explicit cuffs/collar/hair modes and fixed source/seed chains. 774011 recolors the existing collar shading to sage instead of replacing it with a flat fill. 774012 borrows actual shaded hair for the guide and locally redraws it over the unsupported human ear. Both local model runs checked idle queues, recorded provenance, and verified zero changes outside their masks. Inspected full-resolution outputs; the ear is covered, but the side-lock join remains somewhat angular and is not final hair acceptance.

Promoted 774012 only as the current static side study, preserving earlier files. Shared-palette/binary-alpha/sole122 conversion and actual Godot three-view render pass; capture inspected. Existing sandbox log/certificate warnings remain. Side neck bow, cuff outlines, head depth, pouch position and tail-tip shape still differ from the front/rear design. No completed direction set, movement integration or release claim. Review-06 unchanged; full approved M5-M9 scope remains active.

### 2026-10-07 — M5.2.7.2 Mira profile neck bow and boot trim

Added trim mode to repair_mira_details.py, starting from 774012. Removed the invented neck bow and boot buckle, and replaced light cuff bands with plain leather. 774013 left a notch between collar and chest; rejected. Extended the shaded blouse guide through that boundary for 774014, inspected full source, and retained it as the current side study. Both local runs preserve all pixels outside their masks and retain original files/provenance.

ROSTER_STATIC_OK and actual Godot BREN_RENDER_OK pass; inspected refreshed three-view capture with known sandbox log/certificate warnings. Small unsupported ornaments are now removed, but larger differences remain: side head depth/hair silhouette, boot shaft thickness, pouch position and tail-tip shape. These are the next meaningful consistency targets; removing ornaments alone does not establish a coherent finished character. Side study stays unapproved, no movement clips added, review-06 unchanged. Full M5-M9 remains active.

### 2026-10-07 — M5.2.7.2 Mira profile head-depth normalization

Extended repair_mira_details.py with proportion mode (774015), using the retained 774014 source. The owned guide expands head depth by 1.22 around fixed nose x330, fading to unchanged geometry from y220 to y255. Local masked redraw at denoise .18 harmonizes the changed head; the original costume/lower body remain outside the edit. Both queues checked idle, generation/provenance retained, outside-mask maximum difference zero. Inspected the illustration and shared 96x144 conversion.

Actual Godot three-view comparison passes BREN_RENDER_OK; existing log/certificate warnings persist. The profile reads less narrow beside the front/rear, but ponytail transition now has a visible bulge. Keep this as an unapproved proportion study, not a completed direction. Boot volume, pouch position and tail-tip shape remain inconsistent. Further work must resolve silhouette continuity before diagonal views or movement integration. Full approved scope remains active and review-06 unchanged.

### 2026-10-07 — M5.2.7.2 Mira ponytail continuity and pouch occlusion trials

Added ponytail mode (774016) to repair_mira_details.py: a smooth local taper around y224 uses existing strand shading, followed by local redraw. Inspected source and Godot sprite comparison; the mid-ponytail bulge is reduced. Promoted only 774016 as the current static side study. ROSTER_STATIC_OK and BREN_RENDER_OK pass with existing sandbox log/certificate warnings; all masked runs verify zero outside-mask differences.

Added experimental pouch mode and retained two rejected trials: 774017 moves the pouch toward the near hip but turns the hand into a buckle; 774018 restores cloth texture and protects selected skin pixels but reveals a duplicate hand contour from the restoration source. Neither is selected or used by the engine. This establishes that relocation needs explicit arm/pouch occlusion layers, not a skin-color threshold or a broad patch from the old source. Existing pouch position, boot volume and tail shape remain unresolved. No completed character or animation claimed; full M5-M9 remains active, review-06 unchanged.

### 2026-10-07 — M5.2.7.2 Mira arm/pouch occlusion reconstruction

Enlarged inspection of 774016 revealed that the source hand is inside a clothing pocket and its belt crosses the forearm; preserving that silhouette caused the previous relocation failures. Reworked pouch mode into explicit dress -> pouch/herbs -> hanging arm layers. The source for restored cloth is a clean lower-skirt region, avoiding the old hand. Locally redrew a relaxed closed hand in front of a near-hip pouch and kept the belt behind the arm.

774019 produced a flared forearm at the mask boundary; rejected. Extended the transition upward for 774020. Inspected full source and actual Godot three-view sprite: hand/pouch layering now reads correctly, but an upper-arm horizontal seam and lighter pouch color remain. Both runs verify zero outside-mask change; ROSTER_STATIC_OK/BREN_RENDER_OK pass with known sandbox log/certificate warnings. Selected 774020 only as an unapproved static study. Boot volume/tail silhouette and remaining directions/movement remain incomplete; review-06 unchanged. Full approved M5-M9 stays active.

### 2026-10-07 — M5.2.7.2 Mira arm-seam and pouch-color finish

Added finish mode (774021) to repair_mira_details.py. Rebuilt only the internal arm seam from neighboring skin values and warmed the visible pouch surface while preserving the hand silhouette. Local masked redraw retains the corrected belt/arm/pouch ordering. Both queues checked idle; zero outside-mask difference confirmed; original and guide/mask/history/output hashes remain local. Inspected full source: the horizontal arm join is removed and the pouch reads as brown leather again.

Reconverted with the shared palette/96x144/sole122 contract and inspected actual Godot three-view capture. ROSTER_STATIC_OK/BREN_RENDER_OK pass with existing sandbox log/certificate warnings. The main remaining issues are boot volume, tail contour and the side source's finer rendering compared with front/rear. Technical validation is not art approval. No directional animation or release update; full M5-M9 remains active and review-06 unchanged.

### 2026-10-07 — M5.2.6.3 Mira shared-palette style comparison

Added study_mira_palette.py for a non-destructive three-direction comparison. Median-cut palettes are derived jointly from visible sprite pixels, then snapped to existing source swatches; unused palette entries repeat a real swatch rather than adding black. Requested 24/40 colors produce 23/38 shared swatches. Both variants preserve exact alpha masks and bounds, record input/output hashes, and leave current engine sprites untouched.

Inspected both two-row comparison boards. The 23-color candidate loses eye and sleeve separation, while the 38-color candidate remains close to the original finer profile rendering. Neither resolves the directional shadow/line-style discrepancy; neither promoted. This narrows the next action to source shadow masses and contour design instead of further palette-size tuning. No engine test is needed for these unselected diagnostic images; existing current study and review-06 remain unchanged. Full M5-M9 remains active.

### 2026-10-07 — M5.2.7.2 Mira hair-shadow simplification trials

Added experimental hair-style mode to repair_mira_details.py, limiting changes to head hair and ponytail. The guide median-filters small details and maps hair brightness to a copper ramp. Local 774022 at denoise .25 produces flat blotches and region boundaries. 774023 blends 65% ramp with 35% existing shading and raises denoise to .42; some locks return, but horizontal ponytail bands and ear-root boundary artifacts remain. Inspected both full-resolution images; both rejected, current source stays 774021.

Both queues checked idle, generation completed with zero outside-mask changes, and guide/mask/history/output evidence retained. This disproves brightness-bin shapes as sufficient art guidance for this source. Next style work must draw continuous shadows following locks instead of preserving quantization boundaries. No sprite/engine replacement or acceptance claim from these trials. Existing current Godot study and review-06 remain unchanged; full M5-M9 remains active.

### 2026-10-07 — M5.2.7.2 Mira continuous-lock shadow candidate

Added hair-locks mode (774024): explicitly authored continuous shadow/highlight shapes follow the scalp and ponytail, with feathered boundaries and a local DreamShaper redraw at .42. This replaces brightness-bin guidance from the rejected trials. Source inspection shows coherent broad locks and warmer copper hair; forehead shadow planes remain angular. Queue/provenance/outside-mask checks pass.

Added an isolated mira-side-locks registry entry and --mira-hair engine comparison, preserving the current mira-side baseline (774021). ROSTER_STATIC_OK and BREN_RENDER_OK pass with existing sandbox warnings. Inspected front/baseline/candidate capture: the candidate is warmer and less speckled at game size, without the prior horizontal ponytail bands. Retain it as a style candidate, not delivery approval or an automatic baseline replacement. Next refinement must address the source forehead planes while retaining sprite readability. Full M5-M9 remains active; no movement or review-06 update.

### 2026-10-07 — M5.2.7.2 Mira curved shadow trial and roster continuation

774025 replaces two hard polygon shapes with sampled cubic curves, retaining the previous local redraw settings. Generation succeeds with zero outside-mask difference, but inspected output has patchy scalp/ponytail spots. Rejected; 774024 remains the style candidate and 774021 the static side baseline. No resource replacement. Further Mira style work remains open. Continue the approved roster batch with Osric's elderly/frail swordsman rework rather than spending the entire batch on one character's local shading; this does not cancel Mira or narrow M5-M9.

### 2026-10-07 — M5.2.6.2–M5.2.6.4 Osric elderly swordsman rework

Read the original Osric brief (elderly human male, lean/frail, grey swept hair/short beard, weathered brown cloak, cream shirt, sword belt and worn boots). Added prepare_osric_guide.py with owned original face/beard/clothing/equipment geometry and generated 775001 locally with DreamShaper at .55 after checking both queues idle. Inspected actual illustration: age, beard, narrow build and worn cloak now present, unlike the rejected young/female studies. Sword/scabbard is visually conflated with the cloak edge; not a resolved equipment design.

Registered the front study with five grey material swatches extending the shared palette. ROSTER_STATIC_OK (96x144, binary alpha, sole122) and actual Godot --osric render pass with known sandbox log/certificate warnings. Inspected Rowan/Bren/Osric comparison: older face/beard remain readable at game size. Hands, camera, sword separation and all additional directions/animations remain pending. No final character approval or review-06 replacement; full M5-M9 remains active, Mira issues retained.

### 2026-10-07 — M5.2.6.2 Osric sheathed-sword separation

Added repair_osric_sword.py for bounded local edits. 775002 replaces the merged long cloak strip with a separate wrapped grip, brass guard/tip and narrow leather scabbard. Inspection found it floating beside the figure plus a small old cloth sliver. --attach (775003) adds a visible suspension strap emerging behind the hand and clears the residual sliver. Both runs check idle queues, record provenance and verify zero outside-mask pixel difference. Face, beard and other clothing remain unchanged.

Selected 775003 as the current unapproved front study. Shared-palette 96x144/sole122 conversion passes ROSTER_STATIC_OK; actual Godot --osric capture passes and was inspected. Sword survives segmentation and is visible beside the character at gameplay scale. Known sandbox log/certificate warnings remain. Carry angle, hands/camera, other directions and all animations remain pending; no final character or release approval. Full M5-M9 remains active and review-06 unchanged.

### 2026-10-07 — M5.2.7.1 Osric rear cloak study

Added prepare_osric_back.py: mirrors the owned front only to place asymmetric equipment, then independently reconstructs back hair/nape, a fully closed cloak with rear collar/folds, and heel panels. Local DreamShaper 775004 (.40) generated after both queue checks. Inspected actual illustration: no frontal face/beard/shirt/buckle remains on the back; sword appears on the opposite screen side. Hilt ornament and cloak/shading proportions drift from front and remain review items.

Added osric-back registry/conversion and --osric-back engine comparison. ROSTER_STATIC_OK (shared palette plus declared greys, binary alpha, 96x144, sole122) and actual BREN_RENDER_OK pass with known sandbox log/certificate warnings. Inspected Rowan/front/rear capture. This establishes a rear static candidate, not a finished character; side/diagonal views and all animations remain pending. Review-06 unchanged; full M5-M9 remains active.

### 2026-10-07 — M5.2.7.2 Osric side-view reconstruction

Added owned prepare_osric_side.py. Whole-image local trials 775005/775007 generate duplicate heads; 775006 retains a flat crude face. None accepted directly. Added repair_osric_side.py to retain the usable lower elderly profile from 775007 and remove the extra head. 775008 leaves boundary remnants, 775009 a white gap, 775010 a cap-like seam. Extending the mask into the existing hair transition at denoise .42 produces 775011 with a connected single head. Inspected every source; masked edits preserve all outside pixels.

Added explicit optional body_scale conversion metadata, applied only to osric-side (split y260, lower-canvas height factor .60) to correct the overly long body while retaining head detail. Source remains unchanged. ROSTER_STATIC_OK and actual --osric-turnaround Godot render pass with known sandbox log/certificate warnings; inspected three-view capture. Elderly identity is readable, but sleeves, sword, boots and camera still differ. This is an unapproved static side study; no directional animation or package update. Full M5-M9 remains active.

### 2026-10-07 — M5.2.7.2 Osric side rolled-sleeve consistency

Extended repair_osric_side.py with --sleeve (775012), starting from head-clean 775011. An owned sleeve/skin guide and local .30 redraw replace the long sleeve with rolled cream fabric and a bare forearm, preserving the original hand/head/cloak outside the mask. Queue and zero outside-mask difference checks pass. Source inspection finds sleeve length corrected, with extra dark elbow marks still needing cleanup.

Updated only the current side source; retained explicit body normalization and shared palette. ROSTER_STATIC_OK and actual Godot three-view render pass with known sandbox log/certificate warnings. Inspected the capture. Sword, boot design, elbow marks and camera remain unapproved; no motion or package update. Full M5-M9 remains active.

### 2026-10-07 — M5.2.7.2 Osric side detail cleanup

Added mutually exclusive --details mode to repair_osric_side.py (775013), using selected 775012 as source. Interior-only guides remove the unsupported elbow marks and vertical boot laces while preserving the sleeve edge, hand, sword and outer silhouette. Local DreamShaper redraw at .25 completed after idle queue checks; recorded zero outside-mask difference. Inspected full source and actual Godot three-view capture before selecting it as the current static study.

ROSTER_STATIC_OK (96x144, binary alpha, shared palette, sole122) and BREN_RENDER_OK pass; known sandbox log/certificate warnings remain. Sword design, boot silhouette and directional camera consistency remain unresolved. This is not a finished character or animation. Full M5-M9 stays active; review-06 package unchanged. Generated media/provenance remain local and excluded from commits.
### 2026-10-07 — M5.2.7.2 Osric side sword candidate

Added --sword local redraw mode and retained three provenance-backed trials. 775014 replaces the transverse black hilt with a vertical wrapped grip, brass guard and narrow leather scabbard but leaves a flat cloak patch. 775015 borrows neighboring cloth texture but leaves old hilt pixels. 775016 extends the removal mask and clears the old hilt; hip cloth transitions and belt suspension remain unsatisfactory. All three runs check idle queues and zero outside-mask differences.

Registered 775016 separately as osric-side-sword, leaving selected osric-side 775013 unchanged. Added --osric-sword actual engine front/baseline/candidate comparison. Conversion and Godot render pass (ROSTER_STATIC_OK/BREN_RENDER_OK, known sandbox log/certificate warnings). Inspected source and capture: equipment materials better match front, but the candidate is not approved or promoted. Next work needs explicit belt/arm/scabbard occlusion reconstruction. No animation or review-06 package update; full M5-M9 remains active.
### 2026-10-07 — M5.2.7.2 Osric hip continuity and sword selection

Added --hip mode (775017), starting from retained sword candidate 775016. Authored continuous cloak/trouser boundaries and folds instead of copying a rectangular texture patch; added a short leather suspension strap beside the existing hand/guard. Local DreamShaper .38 redraw completes with zero outside-mask difference, preserving head, sleeve and hand outside the mask. Inspected full source: the transverse flat patch is gone; lower cloak transition and camera still need review.

Converted and compared front/old-side/candidate in Godot, then selected 775017 as the current unapproved side study. Reconverted current side and inspected actual three-view render. ROSTER_STATIC_OK and BREN_RENDER_OK pass with known sandbox log/certificate warnings. All original trials retained locally. Equipment is closer to the front brown/brass design; boots, proportions, projection and all directional animation remain incomplete. No review-06 release update; full M5-M9 stays active.
### 2026-10-07 — M5.2.6.2–M5.2.6.4 Tovin goblin merchant study

Continued the approved roster with Tovin (short heavy goblin merchant), preserving unresolved Osric/Mira directional work. Added owned prepare_tovin_guide.py with green projecting ears, round torso, ochre waistcoat, cream shirt and leather ledger satchel. Local DreamShaper 776001 at .55 restores species/outfit/accessory identity but face reads young and belly needs more weight. 776002 at .62 with stronger adult/rotund instructions loses bag and boots, adds a tie and remains juvenile; rejected. Both outputs retained with provenance.

Added optional figure_height to the existing converter (default114 unchanged, Tovin100, bounded32..114) so short species do not automatically become human height. Shared 96x144 cell, binary alpha and sole122 remain. Initial Godot capture exposed pink waistcoat mapping; extended the declared material ramp with ochre swatches and rechecked actual render. ROSTER_STATIC_OK/BREN_RENDER_OK pass, with known sandbox log/certificate warnings. Source and final Rowan/Osric/Tovin capture inspected. Adult face, belly, eye readability and top-down camera remain pending. No finished character, animation or review-06 update. Full M5-M9 remains active.
### 2026-10-07 — M5.2.6.2 Tovin body and adult-face refinement

Added refine_tovin.py for local masked revision of 776001. A smooth horizontal torso warp peaks at +19% width and returns to original coordinates at neck/lower legs. Face guide strengthens lowered brows, eyelids, nose and smile folds. 776003 leaves duplicate original eyebrows; 776004 clears them incompletely; both rejected. 776005 expands the original-brow clearing regions and produces a single brow pair, broader belly, retained ledger bag and boots. Each trial checks both queues and verifies zero pixel difference outside its mask, with source/guide/history hashes retained locally.

Selected 776005 as the unapproved front study after full-source inspection and actual Godot roster capture. Conversion retains figure_height100, shared material ramps, binary alpha, 96x144 cell and sole122. ROSTER_STATIC_OK and BREN_RENDER_OK pass with known sandbox log/certificate warnings. Mature features and heavy build are stronger; small-scale eyes and elevated camera remain review items. No rear/side/diagonal animation or release update. Full M5-M9 remains active.
### 2026-10-07 — M5.2.7.1 Tovin rear garment reconstruction

Added prepare_tovin_back.py from current front 776005. Mirroring only places asymmetric equipment; rear hair/nape/ears, closed waistcoat back and adjustment belt, rear satchel panel/strap and heel panels are independently redrawn. Local DreamShaper 776006 at .40 completed after checking both queues idle. Inspected full source: no front face, placket/lapels or satchel flap remains; hairstyle is longer than front and an unsupported strap persists at right hip.

Registered tovin-back with matching 100px figure height and declared green/ochre material ramps. Added --tovin-back engine comparison. ROSTER_STATIC_OK and actual BREN_RENDER_OK pass with known sandbox log/certificate warnings. Inspected front/rear Godot capture: round silhouette, outfit color and bag side are coherent enough for an unapproved static study. Hair length, stray strap, camera and all remaining directions/animations are unresolved. No release package update; full M5-M9 remains active.
### 2026-10-07 — M5.2.7.1 Tovin rear strap cleanup and rejected hair trials

Added repair_tovin_back.py. Local 776007/776008 shorten the hair but leave horizontal patch seams/remnants; rejected. 776009 expands the redraw to the whole back of the head and removes the seam, but shifts brown hair toward olive and introduces a pale collar; rejected. All runs retain provenance and verify zero outside-mask changes. Hair length remains open rather than accepting a different design.

Added --strap-only (776010), restoring the entire original head region in guide/mask and limiting local .30 redraw to the unsupported right hip strap. Inspected original-scale output and actual Godot front/rear comparison: stray strap removed, hand/waistcoat boundary retained, left satchel untouched. Selected 776010 as current unapproved rear study. ROSTER_STATIC_OK/BREN_RENDER_OK pass with known sandbox log/certificate warnings. No completed directional set or animation; review-06 unchanged and full M5-M9 active.
### 2026-10-07 — M5.2.7.2 Tovin side profile and satchel restoration

Added owned prepare_tovin_side.py with one profile eye/nose/ear, round belly, short legs and layered hand/satchel. 776011 (.50, no adapter) gives a coherent profile but omits the bag. 776012 (.50, reference weight .40 to front) changes waistcoat to long coat and shoes to high boots; rejected. Added repair_tovin_side.py (776013, local .30), drawing only the visible satchel/flap/clasp and strap behind the hanging hand. Queue checks and zero outside-mask difference pass; all source/provenance retained.

Inspected actual source and registered only repaired 776013 as an unapproved static side study. Added --tovin-turnaround to compare front/rear/profile in Godot with shared 100px figure height, palette and sole122. ROSTER_STATIC_OK/BREN_RENDER_OK pass with known sandbox log/certificate warnings. Direction and round abdomen read, but face age, collar, shoe cuffs, strap continuity and camera still differ. Side artwork is not an accepted animation source yet. No release update; all M5-M9 requirements remain active.
### 2026-10-07 — M5.2.7.2 Tovin side garment-detail cleanup

Added --details to repair_tovin_side.py, starting from bag-restored 776013. 776014 replaces the orange cheek with a visible green patch and retains cuff outlines; rejected. 776015 samples adjacent cheek skin successfully but rectangular lower-leg reconstruction creates disconnected trouser edges; rejected. 776016 uses source foreground pixels and existing silhouette for trouser material continuation, removes the green neck clasp, and retains the sampled cheek repair. All local .30 runs record zero outside-mask change and preserve sources.

Selected 776016 after full source and actual Godot three-view inspection. ROSTER_STATIC_OK/BREN_RENDER_OK pass with known sandbox log/certificate warnings. Cheek/clasp mismatch is resolved and ankle material matches trousers, but the wide cuff silhouette still remains; low-shoe redesign is not complete. Face age, collar shape, strap continuity and camera also remain pending. No animation or package update; full M5-M9 stays active.
### 2026-10-07 — M5.2.7.2 Tovin side cuff silhouette correction

Read actual foreground runs at y580..670 before editing: y610 trouser edges are x199..245 and x264..308, while y627 expands into unsupported boot cuffs. Added --ankles (776017) to repair_tovin_side.py. Guided contour reconstruction joins those measured upper-leg edges to low shoes, rather than recoloring the existing wide cuffs. Local .40 redraw completes with zero outside-mask difference; head, torso, bag and hand unchanged.

Inspected source and actual Godot three-view capture, then selected 776017 as the current unapproved side study. The flared cuff silhouette is removed and legs remain connected; source hem/shading transitions still need polish. Conversion and render markers pass with known sandbox log/certificate warnings. Face age, collar, strap continuity, projection and full directional motion remain unfinished. Review-06 unchanged; full M5-M9 active.
### 2026-10-07 — M5.2.7.2 Tovin collar and shoulder-strap consistency

Added --collar and --clean-neck to repair_tovin_side.py. 776018/776019 retain hard neck-band boundaries and are rejected. 776020 expands redraw into lower jaw/nape at .60, producing a folded linen collar and exposed neck; it also creates a dangling blue line below the chin. 776021 removes that exterior artifact with a small white-background mask at .20. Collar mode replaces unsupported back gold trim and draws the near-shoulder leather strap. All runs verify zero outside-mask differences and retain local provenance.

Inspected each full source and selected 776021 as the current unapproved side study. Actual Godot three-view capture and conversion pass (ROSTER_STATIC_OK/BREN_RENDER_OK) with known sandbox log/certificate warnings. Face age, complete strap continuity, trouser shading and projection remain unresolved; this does not finish directional animation. Full M5-M9 remains active, review-06 unchanged.
### 2026-10-07 — M5.2.7.2 Tovin mature profile-eye study

Added --face mode to repair_tovin_side.py using selected 776021. Guide narrows the profile eye and adds brow/cheek creases without touching hair, clothing or body. 776022 leaves the old higher eyebrow, rejected. 776023 expands the removal region but produces an overly white eye, rejected. 776024 strengthens pupil/upper lid and lowers local denoise to .22; one narrower eye with brown brow and mature cheek folds results. All three verify zero outside-mask difference and preserve provenance.

Selected 776024 as current unapproved static side after original-scale and actual Godot three-view inspection. Narrow eye remains visible at the 100px figure height, though its angular shape needs art review. Conversion and render markers pass with known sandbox log/certificate warnings. Source age mismatch is reduced, not a completed character approval. Rear hair, strap continuity, trouser shading, camera and remaining directions/animations are still open. Full M5-M9 active; review-06 unchanged.
### 2026-10-07 — M5.2.6.4 Interactive roster review

Added roster_review.gd for side-by-side front/rear/right-profile inspection of Bren, Mira, Osric and Tovin. Shared foot baseline, 1x/2x/3x nearest-neighbor display, light/dark background, mouse buttons and keyboard cycling make proportion/color/directional mismatches directly reviewable. Labels explicitly identify static studies and incomplete movement. Local PNGs load directly; missing/wrong-sized assets fail with a path. Existing game runtime and review-06 remain unchanged.

Initial live-input check exposed that SceneTree itself did not receive node _input callbacks and reused one InputEvent object. Fixed by a dedicated input Node and distinct press/release events. Re-ran checks: all twelve texture sizes and actual used-alpha bottom anchors122, character cycle/wrap, all zoom levels, background toggle and button signal paths pass with ROSTER_REVIEW_OK/exit0. Inspected saved real-engine screenshot. Known sandbox log/certificate warnings and shader-cache write warning remain; no art acceptance inferred. Initial failed review process subsequently exited normally. README documents launch/controls. Full M5-M9 remains active.
### 2026-10-07 — M5.2.6.2–M5.2.6.4 Neris elven steward front study

Continued approved roster with Neris, preserving all existing unresolved character work. Added owned prepare_neris_guide.py for pointed elf ears, black low buns, slender build, burgundy long tailoring, cream cuffs and belt keys. Local DreamShaper 777001 (.55) has correct species/hair/color but omits keys and adds a prominent chest ornament. Added repair_neris_keys.py (777002, local .30): keys hang from a belt tab clear of the hand. Idle queues and zero outside-mask difference verified; actual source inspected. Key teeth are not yet crisp and chest ornament remains excessive.

Registered current front with declared burgundy/charcoal swatches, shared 96x144/binary-alpha/sole122 conversion. Added --neris Godot comparison with Rowan/Mira; conversion and render markers pass, known sandbox log/certificate warnings remain. Inspected real-engine image: distinct black hair/burgundy profession silhouette retained. This is an unapproved static study, with camera/details and all rear/side/diagonal animation still missing. Existing interactive four-character viewer and review-06 remain unchanged; full M5-M9 active.
### 2026-10-07 — M5.2.6.2 Neris restrained coat tailoring

Extended repair_neris_keys.py with mutually exclusive --coat/--placket modes. 777003 replaces the oversized chest medallion/gold plate with burgundy cloth and small brass buttons. 777004 removes lower gold strip/tassel but leaves a rectangular brown patch; rejected. 777005 borrows lower coat-opening texture but includes a white gap from the donor's bottom; rejected. Restricting the donor to y520..550 yields 777006 with continuous dark underlayer, matching lower placket and retained belt keys. Every masked run records zero outside-mask difference and preserves trials.

Selected 777006 after full-source and actual Rowan/Mira/Neris Godot inspection. ROSTER_STATIC_OK/BREN_RENDER_OK pass with known sandbox log/certificate warnings. Neris now has restrained tailoring rather than a prominent breast ornament. Key teeth, camera and all additional directions/animation remain incomplete; no final art approval or release update. Full M5-M9 remains active.
### 2026-10-07 — M5.2.7.1 Neris rear clothing study

Added prepare_neris_back.py from selected front 777006. Mirroring places asymmetric keys; rear ear surfaces, back hair with low buns, nape/collar, closed burgundy panel/vent, rear belt and heel panels are independently reconstructed. Local DreamShaper 777007 (.40) generated after both idle queue checks. Source inspection confirms no front face, buttons, medallion or key-front design remains. The model lengthens cream cuffs and obscures the left hand; these remain explicit correction items.

Added neris-back registry and --neris-back actual Godot comparison. Shared palette, 96x144/binary-alpha/sole122 conversion and BREN_RENDER_OK pass with known sandbox log/certificate warnings. Inspected front/rear capture; cuff/hand and camera/proportion issues prevent acceptance as a finished character. Side/diagonal movement remains missing; review-06 and interactive four-character viewer unchanged. Full M5-M9 remains active.
### 2026-10-07 — M5.2.7.1 Neris rear cuffs and hand correction

Added repair_neris_back.py (777008) from 777007. Owned local guides extend burgundy sleeves to short cream wrist cuffs and reconstruct the left hand; right hand position remains. Local .30 redraw completes after both idle queue checks, records source/guide/mask/history hashes and verifies zero outside-mask difference. Inspected full source: long white gauntlet-like regions are removed and the left hand is visible; minor sleeve-edge artifacts remain.

Selected 777008 as current unapproved rear, reconverted and inspected actual Godot front/rear capture. ROSTER_STATIC_OK/BREN_RENDER_OK pass with known sandbox log/certificate warnings. Cuff lengths now better match front. Camera/proportion polish, key clarity, side/diagonal views and all Neris motion remain unfinished. No package update or final art acceptance; full M5-M9 active.
### 2026-10-07 — M5.2.7.2 Neris profile clothing study

Added prepare_neris_side.py for independently constructed right-profile anatomy, low bun, long coat, short cuffs and belt keys. Local DreamShaper 777009 (.50) turns the garment but introduces a far eye and substitutes a belt loop for keys. Added repair_neris_side.py; trial 777010 leaves a far-eye fragment, while 777011 (.20) removes it and restores hanging key stems. Both local masked trials verify zero change outside the mask; source/graph/history/output provenance retained locally.

Registered 777011 as an unapproved static study and added --neris-turnaround to the engine comparison. ROSTER_STATIC_OK and BREN_RENDER_OK/exit0 pass; inspected actual front/rear/side screenshot. Known sandbox log/certificate warnings remain. Closed near eye, added ear ornament, tall collar, profile geometry and body proportions still differ from front/rear and need correction. No animation, art approval, release update or full-character completion; M5-M9 remains active.

### 2026-10-07 — M5.2.7.2 Neris profile eye and ear identity

Extended repair_neris_side.py with --identity from 777011. Trials 777012-14 open the brown eye/remove jewelry but expose bun and neck/collar seams; do not select them. Current 777015 keeps the source collar, opens the near eye, removes the generated earring and reconnects the bun behind the ear. All masked trials finish with zero outside-mask difference. Full-source inspection confirms the local changes; fine hair/eye contours remain uneven.

Selected 777015 only as an unapproved static study. Shared 96x144 binary-alpha sole122 conversion and actual Godot three-view render pass; inspected engine screenshot. Known sandbox log/certificate warnings remain. Tall collar, head/profile proportions and projection need a coherent head/neck revision rather than further small patches. Eight directions and walk/run remain incomplete; no release or art acceptance. M5-M9 scope remains active.

### 2026-10-07 — M5.2.7.2 / M5.2.6.4 Neris coherent profile reconstruction

Added rebuild_neris_profile.py: independently redraw the complete head/neck region from current side 777015 while preserving all clothing below the collar. Broad rounded head, forward single eye, plain elf ear and low bun replace the narrow, patch-repaired profile. Trial 777016 (.48) introduces a high white collar; 777017 (.32) has a short collar but flat/jagged face. Selected 777018 (.40) as the current unapproved study: broader profile, exposed neck and short collar. All trials check both queues and verify zero change outside the reconstruction mask. Face shading, bun detail, collar color and projection remain pending; this is not final art acceptance.

Converted selected source to shared 96x144/binary alpha/sole122. Added Neris to the interactive roster viewer, adjusted button spacing to prevent overlap, and generalized the live-input wrap test to all five characters. Actual Godot check passes for fifteen texture dimensions/anchors, character cycle/wrap, zoom/background and button signals; inspected saved engine screenshot. Known sandbox log/certificate and shader-cache warnings remain. README updated. No additional headings, motion or release package completed; full M5-M9 scope remains active.

### 2026-10-07 — M5.2.7.2 Neris northeast garment study

Added prepare_neris_diagonal.py with asymmetric shoulders/sleeves, closed oblique coat back, offset vent, heel/toe projection and partially occluded far-side keys. Initial source-hair guide trials 777019/20 leave a direct rear head or overlapping ear edges. Replaced the whole head guide with a single constructed skull/ear silhouette. Trial 777021 (.52) turns the outfit but loses near elf ear and compact buns. Selected 777022 (.44) as an unapproved northeast study; neck transition, flat shading, belt panels and bun shapes remain inconsistent.

Generated via local DreamShaper after idle queue checks; per-trial guides/graphs/histories remain local. Registered neris-NE, converted to shared 96x144/binary-alpha/sole122, and added --neris-diagonal for rear/NE/side engine comparison. Conversion and actual render checks pass, and source/engine images inspected. Known sandbox log/certificate warnings persist. This adds one draft heading, not accepted eight-direction coverage or movement. Interactive viewer still reviews three standard views; release unchanged. Full M5-M9 remains active.

### 2026-10-07 — M5.2.7.2 Neris southeast front-garment study

Added prepare_neris_front_diagonal.py: independently constructed three-quarter face, offset front placket, visible keys, asymmetric arms and forward diagonal shoes. Local DreamShaper 777023 (.50) turns face/clothing/shoes coherently but omits keys and substitutes loose hair for the low bun. Added repair_neris_front_diagonal.py: 777024 restores compact bun and hanging keys with .28 local redraw. Initial engine comparison exposes brown coat drift. --coat uses a material-limited wine-color guide and .18 redraw; 777025 leaves brown sleeve bands from an overly broad belt exclusion, rejected. Corrected belt exclusion yields current 777026. All local repair trials verify zero outside-mask difference.

Registered southeast draft and added --neris-front-diagonal engine comparison. Shared 96x144/binary-alpha/sole122 conversion and actual Godot render pass; inspected final source and engine image. Coat now reads wine across torso/sleeves/skirt. Brass button detail, hands, style/shading and camera remain pending. Known sandbox log/certificate warnings persist. Five Neris headings now have static drafts, not accepted directional movement; no release or full-character completion. M5-M9 scope remains active.

### 2026-10-07 — M5.2.7.2 Neris west-side garment study

Added prepare_neris_west.py: reflect the east source as construction input, remove keys now occluded on the far hip, and record source hash/guide-only status. Independently generated west view 777027 (.36) changes pose detail and lighting; not a final mirrored sprite. It invents a pouch and white hand. Added repair_neris_west.py: local 777028/29 leave rectangular patch seams, 777030 rebuilds continuous front cloth but opens a hem gap. Current 777031 preserves original hem-to-trouser junction while removing pouch and restoring bare hand; zero outside-mask difference verified. Source inspection confirms no visible keys on this opposite side.

Registered west study and --neris-west engine comparison. Shared 96x144/binary-alpha/sole122 conversion and actual Godot render pass; source and engine output inspected. Cloth shading, collar/button detail and projection still need consistency work. Known sandbox log/certificate warnings remain. Six headings now have Neris static drafts; NW/SW and all movement are missing. No art acceptance or package release; full M5-M9 active.

### 2026-10-07 — M5.2.7.2 Neris eight-heading static review

Added prepare_neris_opposite_diagonal.py with source-hashed reflected construction guides: SW removes occluded keys; NW adds keys on the near hip. Independent local DreamShaper redraws 777032/33 (.32) preserve the intended front/rear garment direction and equipment visibility. These are not final mirrored sprites. Registered and converted both drafts; expressions, buns, key detail, sleeve proportions and shading remain unapproved.

Added export_neris_direction_studies.py: eight unique individually sourced 96x144 binary-alpha sprites, sole122, source/output hashes, explicit zero animation clips, local 768x144 atlas and manifest. Added preview_neris_directions.gd: compass-layout Godot render, exact atlas-region/source-pixel equality, heading uniqueness and anchor checks. NERIS_STATIC_ATLAS_OK / NERIS_DIRECTIONS_RENDER_OK pass; inspected actual eight-heading screenshot. Known sandbox log/certificate warnings remain. Total-view inspection exposes larger front head, flatter side shading and inconsistent cuffs. Eight static drafts exist; continuity polish and all Neris idle/walk/run motion remain unfinished. No package release or M5-M9 completion.

Local review command: `.local/godot/Godot_v4.7.2-stable_win64_console.exe --path pixel-rpg-demo --script res://authoring/preview_neris_directions.gd --quit-after 600`. Atlas and capture live in `production/pixel-rpg/model-wave-01/guided/`, remain ignored, and are not included in review-06.

### 2026-10-07 — M5.2.7.3 Neris front lifted-leg key poses

Added generate_neris_walk_pose.py for local masked left/right foot lifts. Trials 777034/35 attach flat coat patches and break the shin/boot transition; rejected. Current 777036/37 use compressed original coat-tail painting and transparent-background boot guides before .38 local redraw. Original face, torso, arms and support leg are protected; every trial verifies zero outside-mask difference. Source inspection shows connected trouser/shoe forms and lifted coat tails. Motion arcs, weight transfer and arm swing are not solved.

Added convert_neris_walk_poses.py with one reference crop/scale for neutral and both poses, shared palette and binary alpha. Initial parity check found palette sampling accidentally included every Rowan frame; corrected to the existing converter's first frame. Neutral now matches the current front exactly, upper78 rows are identical in all poses, and each support foot remains pixel-identical. Added --neris-walk-poses Godot comparison; conversion/render checks pass and actual engine capture inspected. Known sandbox log/certificate warnings remain. These are two lifted-foot pose studies, not a walk cycle; contact/passing transitions, arm swing, all directions and running remain unfinished. M5-M9 stays active; no release update.

### 2026-10-07 — M5.2.7.3 Neris intermediate lifts and live motion study

Extended generate_neris_walk_pose.py with --half. Left trial 777038 leaves a shin/boot gap; rejected. Current 777040 extends the trouser guide into the boot and joins correctly. Right 777039 supplies the matching intermediate lift. Extended fixed-coordinate conversion to five total source poses; original front parity, identical upper78 rows and unchanged support-foot regions pass for full and half lifts.

Added preview_neris_leg_motion.gd: real AnimatedSprite2D playback compares direct held lifts against intermediate poses at 8 slots/second, explicitly labelled an in-place leg study. Live capture visits all eight slots; 24 engine screenshots preserve upper-body pixels and contain at least five distinct lower-body poses. Source and sampled engine images inspected; local GIF assembled from actual captures. Known sandbox log/certificate warnings remain. Motion is still a marching/lift experiment: proper contact/passing, forward travel, opposing arm swing and weight transfer are absent. No walk/run acceptance or release; full M5-M9 active.

Reproduce: run `generate_neris_walk_pose.py --swing left --half` / `--swing right --half` only for missing trials (existing-trial guard prevents duplicate jobs), then `convert_neris_walk_poses.py`. Engine command: `.local/godot/Godot_v4.7.2-stable_win64_console.exe --path pixel-rpg-demo --script res://authoring/preview_neris_leg_motion.gd --quit-after 600`. Captures and `neris-leg-motion-godot.gif` are local ignored review outputs.

### 2026-10-07 — M5.2.7.3 Neris opposing arm extremes

Added generate_neris_arm_pose.py on existing full lifted-leg sources. Original sleeve/hand paintings are foreshortened/extended as guides for opposing arm movement and redrawn locally. Trials 777041/42 leave old-contour white seams; corrected erase/underlying-coat regions produce selected 777043/44. Keys stay outside the edit mask. Both current trials verify zero outside-mask difference; shoulder/underarm contour polish and sleeve volume remain pending.

Extended fixed conversion to two arm extremes. Leg-only poses retain upper78/support-foot invariants; arm poses retain head43 rows and their corresponding lower legs pixel-for-pixel. Added --arms to live Godot comparison. All eight playback slots observed; actual captures show arm-state changes with unchanged head. Sources and sampled engine capture inspected, local GIF assembled. Known sandbox log/certificate warnings remain. Extreme poses currently enter abruptly because intermediate poses still have resting arms; arm transitions, contact/passing and weight transfer are not complete. This is not a finished walking clip or release; full M5-M9 remains active.

### 2026-10-07 — M5.2.7.3 Neris intermediate arm comparison

Extended generate_neris_arm_pose.py --half: trials 777045/46 apply half-strength opposing arm guide transforms to existing half-lift legs. Local redraws preserve all unmasked pixels. Source inspection confirms intermediate sleeve/hand positions; edge/shading cleanup remains. Fixed-coordinate converter now handles nine poses and verifies unchanged head43 rows plus corresponding lower-leg pixels for all four arm variants.

Added --arm-transitions live comparison and captured all eight slots in Godot. Actual screenshots retain fixed head and show at least five distinct arm-region states; local comparison GIF generated. Added measure_neris_arm_transitions.py. Measured silhouette peak change falls 58 -> 43 pixels, but upper-body RGBA mean change rises 276 -> 459 (peak 488 -> 476). These are discontinuity proxies, not naturalness tests: smoother geometry does not establish stable rendering. Retain the intermediate poses as unapproved comparison art; model shading variation requires cleanup before promotion. Known sandbox log/certificate warnings remain. Contact, forward travel, weight transfer, remaining directions/run and broader pack scope are unfinished; M5-M9 remains active.

### 2026-10-07 — M5.2.7.3 Neris sleeve color consistency study

Added stabilize_neris_arm_colors.py: retain each locally generated model silhouette and transfer neutral reference texels along the inverse authored arm transform inside its recorded mask. Keep target colors where reference sampling is transparent. Four separate comparison outputs preserve exact alpha, head, lower legs and unmasked colors; source/reference/output hashes recorded. This is model-derived sprite postprocessing, not new procedural character artwork.

Extended transition measurement and added --color-stable live Godot comparison. With identical silhouettes, intermediate-pose upper-body pixel-change mean falls 459 -> 373.25 and peak 476 -> 396; silhouette peak remains 43. These are proxies only and do not establish perceptual acceptance. Actual Godot playback reaches all eight slots; sampled captures inspected and head/leg pixels match across comparison columns. Local GIF assembled from actual captures. Known sandbox log/certificate warnings remain. Keep candidate separate while sleeve edges, contact/passing, forward travel and weight transfer are unfinished; full M5-M9 and all-direction walk/run scope remain active.

### 2026-10-07 — M5.2.7.3 Neris projected contact poses

Added generate_neris_contact.py: local DreamShaper 777047/48 (.32) uses original shoes/trousers to project the rear foot higher while keeping the near foot on its reference baseline. Both lower-leg regions are redrawn, leaving upper body unchanged; zero outside-mask difference verified. Source inspection confirms connected legs/shoes and two distinct projected depths. Small shoe-outline artifacts and actual ground-contact behavior remain review items.

Extended fixed converter to both contact studies. First103 sprite rows match standing exactly, and measured foot-bottom ordering flips correctly between left-forward and right-forward poses. Existing lift/head/support-foot checks continue to pass. Added --neris-contact actual Godot comparison; render marker/exit0 pass and capture inspected. Known sandbox log/certificate warnings persist. These projected contact drawings do not prove non-sliding locomotion: phase timing, arm correspondence, weight transfer, forward travel and ground locking remain to implement/test. No final walk/run acceptance or release; full M5-M9 active.

### 2026-10-07 — M5.2.7.3 Neris forward-travel stance experiment

Added export_neris_stance.py combining contact and existing model-derived lift/arm-color candidates into eight frames at 12fps/24px per second. A comparison atlas translates each support boot rigidly while compressing only the lower-coat/thigh strip above it. Boot pixels and upper100 rows are preserved; alpha remains binary; support soles lock exactly at frame-switch samples. This is an isolated candidate, not the main runtime or an accepted gait.

Added preview_neris_stance.gd with actual forward travel, fixed ground grid, pixel-verified sole markers and per-render runtime traces. Initial uncapped run hit the 600-frame failsafe before finishing captures (no completion marker); reran with --max-fps 60 and obtained NERIS_TRAVEL_CAPTURE_OK. Added validate_neris_stance.py: eight complete live stance intervals, naive maximum drift 7.5998px versus corrected 1.8784px, within the explicit 2.05px held-frame tolerance. Actual captures inspected and comparison GIF generated. Known sandbox log/certificate warnings remain. Residual hold drift, lower-coat/thigh compression, neutral contact arms, weight transfer, other directions and running still require work; no full-pack completion or release.

Reproduce in order: `export_neris_stance.py`; `.local/godot/Godot_v4.7.2-stable_win64_console.exe --path pixel-rpg-demo --max-fps 60 --script res://authoring/preview_neris_stance.gd --quit-after 600`; `validate_neris_stance.py`. Outputs remain local under `production/pixel-rpg/model-wave-01/guided/neris-stance/`.


### 2026-10-07 — M5.2.7.3 Neris torso weight comparison

Added export_neris_weight.py as a separate model-derived sprite candidate. Upper body shifts at most one pixel laterally toward the support side and one pixel vertically; nearest-neighbor displacement fades over rows85-100. All pixels from row100 down remain identical to the locked-foot atlas, with rigid head translation and binary alpha asserted. Source/output hashes and per-frame transforms are recorded locally. This is postprocessing of local-model artwork, not a replacement generation route or biomechanical simulation.

Extended the stance engine preview and validator with --weight while retaining the original comparison. Actual Godot playback/capture completed; eight full stance intervals show identical support trajectories in both columns, maximum held-frame drift1.9393px (limit2.05px). Inspected sampled engine captures and generated weight-comparison.gif. Existing sandbox log/certificate warnings remain. Small torso motion is present, but naturalness is unapproved: waist pixel stepping, neutral contact arms, lower-coat compression and direction consistency remain review items. Other directions, run and the broader M5-M9 pack remain unfinished; no release replacement or push.

Reproduce: export_neris_weight.py after export_neris_stance.py, then preview_neris_stance.gd with --max-fps 60 and user argument --weight, then validate_neris_stance.py --weight. Local outputs: production/pixel-rpg/model-wave-01/guided/neris-stance/weighted.png, weight-study.json, weight-runtime-validation.json and weight-comparison.gif.


### 2026-10-07 — M5.2.7.3 Neris contact-arm coordination

Added export_neris_contact_arms.py: reuse existing model-derived arm extremes on opposite-foot contacts and the corresponding half-arm pose on the first passing frame. Four of eight upper-body frames change; all lower92 rows and head43 rows remain exact. Source hashes and join row recorded. Extended weight exporter, actual Godot travel preview and validator with --contact; previous comparison modes remain available. Candidate is separate from runtime/release art.

Engine capture completed and eight complete stance intervals verified: candidate and previous support trajectories identical, max held-frame drift1.8712px below2.05px. Inspected engine screenshots and produced contact-comparison.gif. Sleeve contour protrusions are still visible: a trial connected-component cleanup removed zero pixels because those shapes remain connected, so the ineffective cleanup was not retained. They need deliberate contour redraw rather than claiming automatic cleanup. Contact arms now change with foot phase, but sleeve/waist transitions and naturalness remain unapproved. Other headings, run and broader M5-M9 scope remain unfinished. Existing sandbox log/certificate warnings remain; no release/push.

Reproduce after locked atlas: export_neris_contact_arms.py; export_neris_weight.py --contact; Godot preview_neris_stance.gd --max-fps 60 with user argument --contact; validate_neris_stance.py --contact. Outputs stay in local guided/neris-stance.


### 2026-10-07 — M5.2.7.3 Neris sleeve contour and playable south-walk review

Extended contact-arm exporter with an explicit sprite-space upper-sleeve corridor: rows57-67, outer boundaries33/62, established coat outline color. It removes connected contour protrusions that component filtering could not address. Assertions protect head, cuffs/hands outside that row interval, torso interior and lower body; eight-frame contact sheet inspected. Updated weighted/contact engine comparison still has identical support trajectories, eight complete stance intervals, max1.8933px held-frame drift. This remains an art candidate; shading/waist, gait naturalness and cross-direction consistency are unapproved.

Added authoring/play_neris_walk.gd as an isolated interactive engine review: holdSpace moves south using the current eight-frame candidate at24px/s; release returns to existing neutral sprite; R resets, Escape exits. Independent translucent ground shadow stays with the root rather than bobbing with the torso. Boundary stops both movement and animation. Actual InputEventKey checks verify start, stop with stable position/idle, restart phase, boundary stop and shadow parenting; NERIS_PLAYABLE_OK and saved engine screenshot inspected. Existing sandbox log/certificate/shader-cache warnings remain. This viewer is local, not included in review-06, and explicitly exposes only south walking; it does not stand in for eight-direction walk/run or the broader pack.

Run interactively: `.local/godot/Godot_v4.7.2-stable_win64_console.exe --path pixel-rpg-demo --max-fps 60 --script res://authoring/play_neris_walk.gd`. For verification append `--quit-after 600 -- --check`. Requires the existing neutral sprite and local coordinated-weighted atlas. No release/push.


### 2026-10-07 — M5.2.7.3 Neris rear lifted-leg model studies

Added generate_neris_rear_walk.py using approved-route local DreamShaper masked redraw on rear source777008. Trials777049/50 use separate hem/leg guides and create white joining gaps; rejected. Current777053/54 transform the contiguous lower garment/trouser/heel guide before .38 redraw; inspected source images show connected legs and rear coat structure. All trials record exact prompt/history/source hashes and verify zero outside-mask differences. Both queues checked idle before each sequential job. Optional half-pose seed slots555/556 are defined but not generated.

Added convert_neris_rear_walk.py with fixed rear reference crop/scale, existing palette and binary alpha. Neutral equals existing rear sprite; upper76 rows remain identical. Initial support-leg check found resampling bleed in right-lift conversion; explicit protected support-region restoration after resizing fixes it, with both support-leg assertions passing. This preserves the reference support region rather than weakening the check.

Added --neris-rear-walk to actual Godot static comparator; BREN_RENDER_OK and engine screenshot inspected. Closed rear coat, belt and vent remain rear-facing. These are two lifted-leg studies, not a north walk cycle: contacts, intermediates, arms, ground locking and direction consistency remain unfinished, alongside all run/pack work. Existing sandbox log/certificate warnings remain. No release/push. Local sources and capture: guided/neris-rear-walk-777053.png, -777054.png and neris-rear-walk-godot.png.


### 2026-10-07 — M5.2.7.3 Neris rear intermediate lift playback

Generated local rear half-lift trials777055/56 using the contiguous lower-body guide. Both record successful local history and zero outside-mask differences. Source images inspected: coat and leg remain connected; inner hem contour still needs refinement. Extended fixed rear converter to five poses, retaining neutral parity, identical upper76 rows and explicit support-region preservation for full/half lifts. These checks pass.

Added --rear to the existing live leg comparator, with a separate output prefix and no replacement of front studies. Actual Godot AnimatedSprite2D playback visits all eight slots. Twenty-four captured frames verify a fixed upper body and at least five distinct lower-body states; screenshot inspected and neris-rear-leg-motion-godot.gif assembled from actual captures. Source555/556 and capture outputs remain ignored/local. Known sandbox log/certificate warnings persist. This is an in-place leg-transition study; rear arms, contacts, weight transfer, actual north travel, other directional movement and running remain unfinished. No package release or M5-M9 completion.

Reproduce: generate_neris_rear_walk.py --swing left/right --half only for missing trial records; convert_neris_rear_walk.py; Godot preview_neris_leg_motion.gd --max-fps 60 --quit-after 600 -- --rear.


### 2026-10-07 — M5.2.7.3 Neris rear opposing arm poses

Added generate_neris_rear_arms.py: rear-specific sleeve masks, opposite arm guide motion (foreshorten away arm, extend near arm), protected coat center and existing rear leg sources. First777057/58 leave rectangular side-cloth protrusions; tapered underlying-coat guide gives selected777061/62 plus half-amplitude777063/64. Each local job checks both queues idle, retains prompt/history/hashes, and verifies zero outside-mask difference. Current full sources inspected; side seam/sleeve shading remains unapproved. No front artwork is mirrored into the rear.

Extended fixed rear converter to nine poses. Head43 rows and lower90 rows match their references; full/half support regions remain protected. Initial lower85 assertion included hands/arm-mask feathering: inspected exact changed coordinates (rows85-88) and corrected anatomical check to90, the actual lower-body region. This does not claim unchanged hand pixels. Rear --arm-transitions playback visits all eight slots; actual screenshots show fixed head and at least five arm-region states. Engine capture inspected and neris-rear-arms-godot.gif assembled. Existing sandbox log/certificate warnings persist. Arms are pose candidates, not a completed gait: contacts, north travel/stance, contour/color consistency, other directions and running remain unfinished. No release or push.

Reproduce: generate_neris_rear_arms.py --leg left/right [--half] only for missing records; convert_neris_rear_walk.py; Godot preview_neris_leg_motion.gd --max-fps 60 --quit-after 600 -- --rear --arm-transitions. Outputs local under guided/ and model_review/.


### 2026-10-07 — M5.2.7.3 Neris rear contact and north-travel experiment

Added generate_neris_rear_contact.py: local DreamShaper777065/66 redraws rear lower-leg guides, shortening the away/leading leg projection while retaining the nearer heel baseline. Both sources inspected, closed back and connected legs retained, zero outside-mask changes verified. Added contact sprites to fixed rear converter; upper103 rows match rear neutral exactly. These projected poses alone do not prove grounded gait.

Added export_neris_rear_stance.py: eight contact/arm-lift frames at12fps and signed speed-24px/s, independently output under guided/neris-rear-stance. Rigid support boot translation plus thigh-strip adjustment locks sampled world sole positions; preserves upper100 rows and binary alpha. Extended actual Godot stance preview/validator with --rear and upward-travel assertion. Eight complete runtime stance intervals: naive maximum drift5.5999px, corrected1.6004px, within2.05px hold tolerance. Engine captures inspected and travel-comparison.gif generated. Known sandbox log/certificate warnings remain.

This is a separate unapproved north gait experiment, not a full walk/run release. Contact arms remain neutral; phase correspondence, upper-body motion, sleeve shading, hem continuity and other directions remain unfinished. Full M5-M9 scope stays active. Reproduce: generate rear contacts only if missing; convert_neris_rear_walk.py; export_neris_rear_stance.py; Godot preview_neris_stance.gd --max-fps 60 --quit-after 600 -- --rear; validate_neris_stance.py --rear. No push; generated outputs remain local.


### 2026-10-07 — M5.2.7.3 Neris coordinated rear and bidirectional control

Extended contact-arm and torso-weight exporters with --rear, a rear-specific join row90 and no application of front-only sleeve contour coordinates. Existing rear model arm poses replace neutral contact arms and first passing arms, then receive the same bounded torso sway/bob candidate. Head/lower-body preservation and binary-alpha checks pass. Actual north travel comparison shows eight complete stances with identical before/after support trajectories (max1.8804px hold drift); source atlas and engine capture remain unapproved artwork.

Extended play_neris_walk.gd to north/south movement on Up/Down (Space retains south), facing-specific stationary textures, independent shadow, bounded movement and opposite-input cancellation. Actual InputEventKey checks pass for south start/stop/restart, both boundaries, north movement/idle, opposing keys and return to south. Sampled rear comparison and bidirectional engine screenshot inspected. Existing sandbox log/certificate/shader-cache warnings persist. This is a local two-direction review, not eight-direction completion or a released character: other six directions, run, contour/shading consistency and broader M5-M9 work remain unfinished.

Reproduce rear candidate after rear stance export: export_neris_contact_arms.py --rear; export_neris_weight.py --rear; export_neris_weight.py --rear --contact; stance preview/validator --rear --contact. Interactive play_neris_walk.gd uses both local coordinated-weighted atlases; --check runs control verification. No release/push.


### 2026-10-07 — M5.2.7.3 Neris east stride contact studies

Added generate_neris_east_stride.py: independent local-model side-view stride guides with separated near/far legs and sheared original coat-tail painting. Trials777067/68 leave an impossible white gap at the hip; rejected. Added continuous underlying trousers and transparent tail strips; selected777069/70 close the gap. Local redraws retain source head/torso and verify zero outside-mask differences. Sources inspected: boot tongue/lace-like detail, hem edge and weak near/far distinction still require polish. These are unapproved contact studies, not a walk cycle.

Added convert_neris_east_stride.py using one expanded source crop150..375 for neutral and both strides, anchored to the original profile center and common sole baseline. Expansion avoids truncating the forward shoe outside the original static bounds. Upper76 rows identical, binary alpha, distinct cells and no horizontal clipping checks pass. Separate neutral study preserves old static side asset. Added --neris-east-stride engine comparator; actual capture inspected and BREN_RENDER_OK passes with known sandbox log/certificate warnings. Passing, arms, contact timing/ground lock, other directions and running remain unfinished; full M5-M9 remains active. No release/push.

Local outputs: guided/neris-east-stride-777069.png, -777070.png, neris-east-stride-keyposes.json, neris-east-stride-godot.png; model_review/neris-walk-east-*.png. Reproduce missing trials with generate_neris_east_stride.py --lead near/far, then converter and preview_bren.gd -- --neris-east-stride.


### 2026-10-07 — M5.2.7.3 Neris east passing pose studies

Added generate_neris_east_passing.py with bent swinging knee, straight support leg, transparent boot placement and reduced coat-tail opening. Local DreamShaper777071/72 preserve head/torso and zero unmasked difference; source images inspected. Foot depth/overlap is visible, but knee is largely hidden under the coat, near/far distinction and shoe consistency remain art-review issues. Extended shared expanded-crop converter to five unique poses; protected upper76 rows, binary alpha and no horizontal clipping pass.

Added preview_neris_east_motion.gd: actual Godot contact-only versus contact/passing playback, eight slots visited. Captured24 frames verify fixed upper body and four distinct lower-body states; sample engine capture inspected and neris-east-leg-motion-godot.gif generated. This rough held-key sequence is not a finished walk: arm movement, down/up transitions, timing, eastward travel and stance lock remain absent. Known sandbox log/certificate warnings remain. Full eight-direction walk/run and M5-M9 scope remain active; no release/push.

Reproduce missing sources with generate_neris_east_passing.py --lead near/far; convert_neris_east_stride.py; Godot preview_neris_east_motion.gd --max-fps 60 --quit-after 600. Sources/captures remain local in guided/ and model_review/.


### 2026-10-07 — M5.2.7.3 Neris east arm extremes

Added generate_neris_east_arms.py: rotate original visible sleeve/hand guide16degrees opposite the near-leg contact, restore underlying coat and protect head/keys. Local trials777073/74 leave shoulder holes/old contour;777075/76 improve underlying coat but retain white arm-background seams. Removing white background from the arm cutout before rotation yields current777077/78. Every trial records local prompt/history/hashes and zero unmasked changes. Front-swing source inspected; seam continuity improved, sleeve shading/shoulder mass and partially occluded hand remain unapproved.

Extended fixed converter to seven poses; arm poses preserve head43 rows and corresponding lower85 rows. Added --arms live Godot comparison, all eight slots visited, actual capture inspected and neris-east-arms-godot.gif generated. Existing sandbox log/certificate warnings remain. Contact extremes now carry opposing visible arm movement, but passing poses still have neutral arms so switching is abrupt. Half-arm transitions, shading consistency, eastward travel/stance and full remaining pack scope remain unfinished. No release/push.

Reproduce missing trials with generate_neris_east_arms.py --lead near/far; convert_neris_east_stride.py; Godot preview_neris_east_motion.gd --max-fps 60 --quit-after 600 -- --arms. Source/capture assets remain local.


### 2026-10-07 — M5.2.7.3 Neris east half-arm phase composition

Extended east arm generator --half with local777079/80 on passing-leg sources and8degree sleeve rotation. Both local jobs succeed with zero outside-mask difference. Extended fixed conversion to nine unique poses; half-arm head and corresponding lower85 rows remain unchanged. Added export_neris_east_phases.py with explicit independent arm/leg assignments, source hashes and join85. Passing legs stay in the correct half-cycle while arm angles progress through extreme/half/neutral/opposite-half states. Binary alpha and unchanged head/lower body assertions pass.

Added --transitions engine comparison against abrupt arm extremes; actual Godot playback reaches all eight slots, sampled capture inspected, neris-east-transitions-godot.gif assembled. Existing sandbox log/certificate warnings remain. Intermediate arm poses exist but perceptual quality is not approved: palette/shading variation, waist join, missing down/up leg transitions, horizontal travel/stance and running remain unfinished. Full M5-M9 objective active, no release/push.

Reproduce missing half sources with generate_neris_east_arms.py --lead near/far --half; convert_neris_east_stride.py; export_neris_east_phases.py; Godot preview_neris_east_motion.gd --max-fps 60 --quit-after 600 -- --transitions. All generated sources/atlas/captures remain local.


### 2026-10-07 — M5.2.7.3 Neris east down/up leg transitions

Added generate_neris_east_intermediate.py with near/far support assignments and separate down/up guide polygons/heel positions. Local777081-84 succeed with zero unmasked differences. Source inspection shows connected hips/legs and intermediate stride widths, but cuff/shoe/hem variants remain unapproved (including lighter ankle-looking detail in down pose). These drafts are not promoted as finished art.

Extended fixed converter to13 distinct poses, protecting intermediate upper76 rows. Extended phase exporter --leg-transitions to replace repeated passing legs with down/passing/up states while retaining independent arm mapping. All eight composed lower-body frames are distinct; binary alpha/head/lower preservation assertions pass. Added live --leg-transitions Godot comparison against held passing legs, observed all eight slots, inspected actual capture and created neris-east-full-transitions-godot.gif. Known sandbox log/certificate warnings remain. Horizontal ground contact, speed synchronization, shading/contour cleanup, other headings and running remain unfinished; full M5-M9 active, no release/push.

Reproduce missing generation with generate_neris_east_intermediate.py --lead near/far --phase down/up; converter; export_neris_east_phases.py --leg-transitions; Godot preview_neris_east_motion.gd --max-fps 60 --quit-after 600 -- --leg-transitions. Local atlas neris-east-complete-phase-study.png means all eight study phases exist, not completed production animation.


### 2026-10-07 — M5.2.7.3 Neris actual east-travel calibration

Added export_neris_east_travel.py: read support heel from actual sprite row120 (leading cluster on contacts), measure sequence59/53/47/43, select48px/s at8fps and at most2px lower-region shift to make six-pixel frame-boundary progression. Upper101 rows remain unchanged and lower114+ texture translates rigidly. Both lower feet move in affected frames; this is explicitly a limited calibration candidate, not anatomically independent leg rigging. Inputs/hashes/transforms recorded; main actor unchanged.

Added preview_neris_east_travel.gd with real horizontal movement, fixed world grid, sprite-verified heel anchors and runtime traces. Added validate_neris_east_travel.py: five complete stances show original24px/s max drift9.6003px, calibrated48px/s max5.6003px. Bound6.05px follows six-pixel movement per held frame; it is intentionally not the prior north/south2.05px bound and does not establish acceptable gait. Actual engine capture inspected; comparison.gif generated. Existing sandbox log/certificate warnings remain.

Speed calibration reduces measured slip but doubles speed, so do not promote it into the shared runtime. Remaining work includes common directional stride/speed, residual held-frame sliding, independently controlled support foot, shading/shoe/hem polish and all unfinished M5-M9 scope. No release/push. Reproduce exporter, Godot preview_neris_east_travel.gd --max-fps 60 --quit-after 600, validator. Outputs local guided/neris-east-travel/.


### 2026-10-07 — M5.2.7.3 Neris compact side-contact redraw

Extended east stride generator --compact to reduce leg separation while preserving shoe size and upper-body identity. Trials777085/86 compress limb widths and produce implausibly thin shins; rejected. Current777087/88 move guide leg centerlines inward while preserving polygon thickness, and use transparent original boot guides. Local redraws verify zero unmasked difference; sources inspected. Short stride is visible, but cuff/ankle coloring and inconsistent coat opening still need polish. These are separate art candidates, not proof of common-speed gait.

Fixed expanded-crop conversion now includes15 unique studies and protects compact upper76 rows. Added --neris-compact Godot comparison against the long contact. Render marker passes and actual screenshot inspected with known sandbox log/certificate warnings. Main movement remains unchanged. Short-contact candidates still need matching intermediate legs, phase assembly and actual24px/s drift measurement before common-speed integration; all other M5-M9 requirements remain active. No release/push.

Reproduce missing compact trials with generate_neris_east_stride.py --lead near/far --compact; converter; preview_bren.gd -- --neris-compact. Local source777087/88 and neris-compact-godot.png remain ignored outputs.


### 2026-10-07 — M5.2.7.3 Neris compact east common-speed verification

Extended intermediate generator --compact to move support/swing endpoints without compressing leg/boot width. Local777089-92 succeed with zero unmasked changes. Fixed converter now contains19 unique studies with unchanged intermediate upper76 rows. Added compact phase assembly using compact contacts/down/up, existing passing legs and independent arm assignments. Generated artwork remains unapproved: shoe/cuff/hem consistency needs polish.

Extended east travel exporter/preview/validator with separate --compact outputs,12fps and24px/s in both comparison lanes. Measured heel targets53/51/49/47 and bounded lower-region correction preserve upper101 rows and rigid bottom114+ pixels. Eight actual live stances: uncorrected max4.6001px, corrected1.6002px, passing2.05px bound. Actual Godot capture inspected, comparison.gif generated. This now matches north/south speed/cadence; it does not assert biomechanical or art acceptance. Both feet move under the bounded lower-region adjustment in affected frames. Existing sandbox log/certificate warnings remain.

Main actor still unchanged pending integration and visual review. Remaining directions, run, outfit/species roster and broader M5-M9 pack remain unfinished. No release/push. Reproduce missing compact intermediate sources with --compact, then converter, export_neris_east_phases.py --compact, export_neris_east_travel.py --compact, actual east travel preview --compact, validator --compact. Outputs local guided/neris-east-compact-travel/.


### 2026-10-07 — M5.2.7.3 Neris three-direction interactive review

Integrated calibrated compact east atlas into the isolated play_neris_walk.gd review alongside existing south/north candidates. All use24px/s and12fps; east manifest settings and atlas size are verified at load. Right-arrow movement uses east animation and its independently converted idle, maintains facing on release, and returns to north/south correctly. Reset now restores both coordinates. Unavailable west and mixed-axis inputs stop rather than playing an incorrect directional asset; UI explicitly labels S/N/E-only scope.

Actual InputEventKey checks pass for previous north/south behavior plus east displacement-versus-elapsed phase, east stationary texture, mixed-axis stop, east boundary, reset, unavailable west, east-to-north turn/idle and independent shadow. NERIS_PLAYABLE_OK and actual three-direction screenshot inspected. Existing sandbox log/certificate/shader-cache warnings remain. This is engine-review integration, not art acceptance: character scale/shading across views, shoes/coat continuity, five remaining headings and all running remain unfinished, as does broader M5-M9 content. No release/push.

Run `.local/godot/Godot_v4.7.2-stable_win64_console.exe --path pixel-rpg-demo --max-fps 60 --script res://authoring/play_neris_walk.gd`; append `--quit-after 600 -- --check` for input validation. Local capture guided/neris-stance/three-direction-playable-godot.png. Review still depends on local generated atlases and is not included in review-06.

### 2026-10-07 — M5.2.7.3 Neris west contact studies

Added independent west short-stride guide/redraw script using west source777031, its own coat strips and shoes, without mirroring east final pixels. Local777093/94 complete successfully with zero unmasked differences. Fixed-coordinate converter creates three96x144 studies (neutral and two contacts), checks distinct frames, binary transparency, protected upper85 rows and horizontal bounds. Actual source images and nearest-neighbor review inspected.

Art review rejects promotion for now: ankle gaps, inconsistent cuffs and weak near/far leg distinction remain. Converted low-resolution preview hides some source defects; this is not acceptance. No playable west integration or new release. Next repair ankle continuity before adding passing, arm swing and measured travel; broader M5-M9 remains unfinished. Generated files stay local. Reproduce generate_neris_west_stride.py --lead near/far then convert_neris_west_stride.py. Preview: production/pixel-rpg/model-wave-01/guided/neris-west-contact-review.png.

### 2026-10-07 — M5.2.7.3 West ankle repair and passing study

Local masked ankle repairs777095/96 close the contact-pose white gaps; upper outfit stays unchanged. Added repair_neris_west_ankles.py with overlapping cloth guides and recorded source/graph/hash/outside-mask checks. Passing trials777097/98 hallucinate coat tails as trousers and are rejected. Updated generator uses shoe-only crops, continuous trouser guides and0.20 denoise;777099/100 restore visible charcoal legs below the coat. Source inspection still shows hem irregularity, shoe-shape variation and weak near/far distinction; not final art acceptance.

Fixed converter now uses repaired contacts and two passing poses, five distinct96x144 cells with unchanged upper85 rows, binary alpha and no horizontal clipping. Added preview_neris_west_motion.gd: actual AnimatedSprite2D comparison of held contacts against contact/passing at8fps, all eight timeline slots observed; NERIS_WEST_PLAYBACK_OK. Actual engine screenshot inspected and neris-west-leg-motion-godot.gif generated from24 captures. Existing sandbox log/certificate warnings remain. This is an in-place lower-body study, not verified locomotion. Arms, full phase transitions, ground locking/common-speed travel, cross-view art consistency and running remain unfinished. No playable-west integration, release or push; full M5-M9 remains active.

### 2026-10-07 — M5.2.7.3 West opposing arm phases

Added generate_neris_west_arms.py using original west sleeve/cuff/hand rotation as guide with local masked redraw, fixed head and legs. Trials777101/102 show white seams;777105/106 repair torso coverage but retain old rear sleeve remnants. Current777109/110 explicitly clear the old rear edge and preserve collar;777111/112 supply half-swing transitions. All four source images inspected and unmasked difference is zero. Sleeve folds, hand shapes, torso shading and shoulder contour still vary; these remain unapproved studies.

Expanded fixed converter to nine distinct cells; leg studies preserve upper85 rows, arm studies preserve head45 and corresponding lower90+ rows. Live Godot --arms compares fixed-arm gait against full/half/neutral opposing phases. NERIS_WEST_PLAYBACK_OK observes all eight timeline slots; actual captures inspected and neris-west-arm-motion-godot.gif generated. Known log/certificate warnings remain. Legs still hold passing poses across phases; full leg transitions and ground-speed calibration are next. No production west integration, release or push; broader M5-M9 remains incomplete.

### 2026-10-07 — M5.2.7.3 West down/up leg phases

Added generate_neris_west_intermediate.py with separate down/up support and swing guides. Local777113-116 succeed with zero outside-mask changes; all source views inspected. Fixed converter now has13 unique cells and protects intermediate upper85 rows. Added export_neris_west_phases.py with explicit eight-frame independent arm/leg assignment, join at90, source hashes and head/lower-body preservation checks. This replaces held passing legs with down/passing/up phases. Shoe and cuff shapes, hem edges and near/far readability remain unapproved.

Extended actual Godot preview --transitions to compare held passing legs with the new phase atlas. NERIS_WEST_PLAYBACK_OK observes all eight slots;24 captures exported to neris-west-transition-motion-godot.gif. Known sandbox log/certificate warnings remain. This validates in-place playback only; no actual west travel or foot-contact measurement yet. Next measure/calibrate at the shared24px/s and12fps before runtime integration. Broader M5-M9 remains unfinished; no release or push.

### 2026-10-07 — M5.2.7.3 West common-speed travel calibration

Measured sprite support heels41/44/47/56 at row120; the last transition jumps9px. Revised up-pose guide support endpoint before calibration: local777117/118 replace115/116 in conversion, with unchanged upper outfit and zero outside-mask differences. Source images inspected; shoe/cuff/hem style is still unapproved.

Added west travel exporter, actual Godot moving comparison and trace validator. Both lanes move left at24px/s,12fps; selected target heels43/45/47/49 require at most2px lower-region translation. Upper101 rows are unchanged; bottom114+ moves rigidly. Both feet shift on affected lower rows, so this is a bounded contact correction, not independent leg rigging. Actual8 complete stances measure uncorrected4.8002px versus corrected1.8002px maximum heel drift, within2.05px held-frame bound. NERIS_WEST_TRAVEL_OK, validator and actual capture inspected; comparison.gif generated under guided/neris-west-travel. Known sandbox log/certificate warnings remain.

Next integrate this candidate into isolated interactive review with idle, turns and boundaries; main release unchanged. Full art acceptance, diagonals, running, roster and broader M5-M9 remain unfinished. No release or push. Reproduce west converter, phase exporter, travel exporter, preview_neris_west_travel.gd --max-fps60 --quit-after600, validator.

### 2026-10-07 — M5.2.7.3 Four-direction interactive Neris review

Integrated calibrated west candidate into play_neris_walk.gd. West uses its independent idle and atlas, verifies12fps/-24px/s manifest and768x144 dimensions, and shares speed magnitude with S/N/E. Signed horizontal direction is distinct from north; mixed axes/opposed keys stop while diagonal animations remain absent. Direction changes restart phase; idle preserves facing.

Actual InputEventKey regression passes existing S/N/E checks plus west displacement-versus-phase, west release idle, opposing horizontal keys, mixed west/down input, left boundary, reset, east-to-west and west-to-north switching, and body-attached shadow. NERIS_PLAYABLE_OK and four-direction-playable-godot.png inspected. Known sandbox log/certificate/shader-cache warnings remain. This is isolated candidate integration only: cross-view proportions/shading, sleeve/shoe/hem cleanup, four diagonal animations, running and full roster/content remain unfinished. No release or push; review-06 unchanged.

Run local Godot with --path pixel-rpg-demo --script res://authoring/play_neris_walk.gd; arrow keys walk, R resets and Escape exits. Add --max-fps 60 --quit-after 600 -- --check for validation. Generated sources remain local dependencies.

### 2026-10-07 — M5.2.7.3 Southeast contact artwork

Started independent SE movement from static777026, preserving head, torso, keys and diagonal camera. Added generate_neris_se_stride.py with near/far leg endpoints, asymmetric shoe sizes/vertical placement, and moving coat panels. Trials777119/120 contain transplanted far-leg fragments and dangling shoe blocks. Current777121/122 use explicit individual shoe masks and cloth-only tail strips, removing those source-guide artifacts. Both succeed with zero outside-mask differences; sources and converted preview inspected. Hem, trouser shading and shoe silhouettes remain unapproved.

Added fixed-coordinate converter: three distinct96x144 cells, upper77 invariant and transparent canvas borders. Shared expanded bounds permit downward contact extent; neutral sole anchor is retained without independently normalizing each pose. Outputs neris-SE-contact-study.png / neris-SE-contact-review.png and hashed keypose metadata. These are contact studies only, not a diagonal walking clip or engine integration. Passing/arm phases and two-axis ground-contact validation remain next; full M5-M9 unfinished. No release/push.

### 2026-10-07 — M5.2.7.3 Southeast passing-leg study

Added generate_neris_se_passing.py with independent support versus bent swing leg and original isolated shoe shapes. Initial777123/124 have a sharp far-knee silhouette and near-shoe height insufficient to read as lifted in diagonal perspective. Current777125/126 reduce knee protrusion and give near/far swing different lift offsets. Both local redraws succeed with zero unmasked differences; source views inspected. Hem-edge noise, trouser/shoe variation and inter-view proportions remain unapproved.

Fixed converter now emits five distinct cells with protected upper77 rows and transparent borders. Added preview_neris_se_motion.gd; live AnimatedSprite2D compares contact-only timing against contact/passing at8fps, all eight slots observed. NERIS_SE_PLAYBACK_OK, actual screenshot inspected,24 captures converted to neris-SE-leg-motion-godot.gif. Known log/certificate warnings remain. This proves in-place leg playback only; arms, intermediate phases and two-axis contact calibration remain next. No diagonal runtime integration, release or push. Full M5-M9 remains unfinished.

### 2026-10-07 — M5.2.7.3 Southeast near-arm phases

Added generate_neris_se_arms.py for near-arm full/half rotations on fixed SE contacts/passing artwork. Protected collar, far hand and key region; local masked redraw leaves all unmasked pixels unchanged. Initial777127/128 have shoulder/body white seams. Current777131-134 extend underlying coat coverage and protect collar, improving continuity; all sources inspected. Thin pale sleeve-edge remnants, blocky underarm fill, variable folds/hand shapes and fixed far arm remain unapproved. This is near-arm development, not completed opposing two-arm motion.

Converter now has nine unique cells; head49 rows and corresponding legs87+ remain identical. Godot --arms compares fixed arm versus near-arm phase changes and observes all eight slots. Actual capture inspected, neris-SE-arm-motion-godot.gif generated; known sandbox log/certificate warnings remain. Next clean underarm contour and add complementary far-arm movement before leg intermediate phases/two-axis ground calibration. No diagonal runtime integration, release or push; full M5-M9 unfinished.

### 2026-10-07 — M5.2.7.3 Southeast sleeve contour cleanup

Revised near-arm guide extraction to remove pale edge pixels above the cuff, explicitly clear the old sleeve silhouette, and narrow underlying coat fill. Local777135-138 replace131-134 in conversion; all four sources inspected. Obvious old sleeve remnants and blocky underarm protrusion improve. Cream cuff is excluded from the stronger pale-edge removal; head, protected equipment and lower legs stay fixed. Sleeve folds/hand shading still vary and far arm remains static, so art is not approved.

Fixed conversion invariants pass (nine distinct cells, head49/lower87 protection, binary alpha and bounds). Actual Godot --arms playback observes all eight slots; capture inspected and neris-SE-arm-clean-motion-godot.gif generated. Known log/certificate warnings remain. Next add complementary far arm, then intermediate legs and diagonal contact calibration. No release/push; broader M5-M9 unfinished.

### 2026-10-07 — M5.2.7.3 Southeast complementary far arm

Added generate_neris_se_far_arm.py using cleaned near-arm sources and opposite smaller far-arm rotation. Protected near side and foreground key region; backward far hand becomes occluded. Initial777139/140 show shoulder pinholes; current777143-146 preserve a larger shoulder region. All four current source images inspected, zero unmasked differences. Far cuff thickness, shoulder contour and occlusion transitions still need polish; these are unapproved candidates.

Converter emits13 distinct cells and checks head49, lower87 and near-side50-column preservation across far-arm edits. Godot --two-arms compares near-arm-only versus complementary arm phases, all eight slots observed. Actual capture inspected; neris-SE-twoarm-motion-godot.gif generated. Known log/certificate warnings remain. Legs still hold passing phases; intermediate legs and two-axis travel/contact calibration remain next. No diagonal runtime integration, release or push; full M5-M9 unfinished.

### 2026-10-07 — M5.2.7.3 Southeast down/up phases

Added local intermediate generator with support near/far, separate down/up endpoints and lifted swing shoes.777147-150 succeed with zero outside-mask changes; source views inspected. Converter now17 unique cells, protected intermediate upper77. Exporter composes eight phases with two-arm art above row87 and independent legs below. SE passing labels denote support leg, so near-contact uses near-down/near-passing/near-up, and far-contact uses far equivalents; do not copy an opposite passing label blindly. Head49 and lower87 preservation checks pass; all eight lower-body phases differ.

Extended Godot --transitions comparison; NERIS_SE_PLAYBACK_OK observes all eight slots. Actual capture inspected, neris-SE-transition-motion-godot.gif generated. Known sandbox log/certificate warnings remain. Hem artifacts, trouser/shoe variation and cross-direction art remain unapproved. Next measure diagonal ground contact in both axes at common speed; no diagonal runtime integration, release or push. Full M5-M9 unfinished.

### 2026-10-07 — M5.2.7.3 Southeast two-axis contact calibration

Added export_neris_se_travel.py with explicit near/far anatomical heel anchors checked against source alpha, normalized24px/s velocity (24/sqrt(2) on each axis),12fps and rounded diagonal phase targets. At most1px correction per axis; upper101 rows stay unchanged and bottom112+ pixels translate rigidly. Both feet move under the lower-region adjustment, not independently rigged. Source hashes, anchors and offsets recorded.

Actual Godot preview moves both lanes diagonally and records two-dimensional marker positions. Validator checks normalized speed, marker positions against runtime time/anchor data, complete four-frame stances, both axis ranges and maximum pairwise Euclidean drift. Eight stances: original4.1253px versus corrected2.4285px maximum distance; each corrected axis about1.7172px. Bound2.9px includes2px held-frame travel plus diagonal target-rounding spread, and is not equivalent to a2.05px Euclidean bound. Actual capture inspected and comparison.gif generated. Known log/certificate warnings remain.

This is local contact calibration, not art acceptance: shoes/cuffs/hem and inter-view proportions remain unapproved. Next integrate SE into isolated interactive review with normalized mixed-axis input, then remaining diagonals/run/roster and broader M5-M9. No release or push.

### 2026-10-07 — M5.2.7.3 Southeast interactive integration

Integrated SE independent idle and calibrated atlas into play_neris_walk.gd. Manifest verifies12fps and normalized24px/s velocity. Right+Down selects SE; release either key returns to the corresponding cardinal direction, release both keeps SE idle. Opposing inputs and unfinished diagonals stop. SE travel stops at the first boundary using distance clipping that preserves the diagonal angle, rather than sliding along the remaining axis with mismatched artwork.

Actual InputEventKey checks pass prior four-direction regressions plus SE displacement length/time and equal axes, SE-to-E/S turns, release idle, contradictory keys, right/bottom boundary stop and approach from(547,400) to(550,403). NERIS_PLAYABLE_OK and five-direction-playable-godot.png inspected. Known sandbox log/certificate/shader-cache warnings remain. This is five-direction candidate review; three diagonals, all running and substantial art/roster/world scope remain unfinished. No release/push; review-06 unchanged.

### 2026-10-07 — M5.2.7.3 Southwest contact and passing legs

Added independent SW stride/passing generators using static777032, explicit SW shoes and cloth-only tail masks. Local777151/152 contacts and777153/154 passing succeed with zero unmasked changes; all sources inspected. Left-facing perspective retains larger/lower near shoe and hidden keys. Pose-dependent hem edges, trouser shading, shoe silhouette and cross-view proportions remain unapproved.

Added fixed-coordinate SW converter with expanded shared bounds and neutral sole anchor: five distinct96x144 cells, upper84 preserved, binary alpha, transparent borders. Added actual Godot contact-versus-passing review; support-leg labels stay consistent between contact and passing. NERIS_SW_PLAYBACK_OK observes all eight held timeline slots. Actual capture inspected and neris-SW-leg-motion-godot.gif generated; known log/certificate warnings remain. These are in-place lower-body studies, not verified diagonal locomotion. Arms, intermediate legs and two-axis travel remain next. No SW runtime integration/release/push; full M5-M9 unfinished.

### 2026-10-07 — M5.2.7.3 Southwest near-arm phases

Added local SW near-arm generator with independent sleeve guide, narrower belt protection and protected far hand. Prequeue array-slice mismatch corrected before generation. Trial777156 clips the forward hand under an oversized protection region; current777159-162 separate belt/far-hand masks and restore whole moving hand. All current source views inspected and unmasked difference is zero. Sleeve volume, hand shape and cloth shading remain unapproved; far arm remains fixed.

Converter now nine distinct cells, unchanged corresponding legs90+. Initial head52 assertion catches one pixel at(53,51) on the shoulder sampling boundary, not head/neck; inspected difference coordinates and corrected anatomical head invariant to49 rows. Conversion then passes. Godot --arms actual playback observes all eight slots; capture inspected and neris-SW-arm-motion-godot.gif generated. Known log/certificate warnings remain. Next complementary far-arm poses, intermediate legs and two-axis contact calibration. No SW runtime integration/release/push; full M5-M9 unfinished.

### 2026-10-07 — M5.2.7.3 Southwest complementary far arm

Added local far-arm generator using existing near-arm poses and opposite smaller rotations.777163-166 succeed with zero outside-mask changes; all source views inspected. Shoulder/belt protection and explicit old-arm clearing preserve near-side artwork. Cuff/hand silhouettes and hand overlap close to the torso still need polish; not approved finished motion.

Converter now13 distinct cells; corresponding legs90+ and near-side columns50+ are preserved, along with head49. Godot --two-arms compares near-arm-only versus complementary phases and observes all eight timeline slots. Actual capture inspected, neris-SW-twoarm-motion-godot.gif generated. Known sandbox log/certificate warnings remain. Next intermediate leg phases and diagonal two-axis contact calibration. No SW interactive integration/release/push; broader M5-M9 unfinished.

### 2026-10-07 — M5.2.7.3 Southwest intermediate legs and phase assembly

Added SW down/up generator with explicit near/far support and swing endpoints.777167-170 succeed with zero unmasked changes; all source views inspected. Hem/pant-cuff edge artifacts and shoe variation remain unapproved. Converter now17 unique cells and protects intermediate upper84. New phase exporter retains support-leg identity across contact/down/passing/up and composes complementary arms above row90 with independent legs below. Head49/lower90 preservation passes, all eight lower-body phases differ.

Godot --transitions compares held passing legs with full leg phases and observes all eight slots. Actual capture inspected and neris-SW-transition-motion-godot.gif generated. Known sandbox log/certificate warnings remain. Next actual SW two-axis contact calibration at normalized24px/s; no SW interactive integration/release/push. Full M5-M9 unfinished.

### 2026-10-07 — M5.2.7.3 Southwest contact calibration and interactive review

Added SW two-axis travel exporter, actual moving Godot preview and trace validator. Explicit heel anchors use opposite horizontal progression; normalized velocity(-24/sqrt(2),24/sqrt(2)),12fps, at most2px lower-region correction. Upper101 unchanged and bottom112+ rigid translation checked. Both feet move in adjusted rows, not independently rigged. Eight actual stances: original4.9765px versus corrected2.4285px Euclidean maximum; axis drift about1.7172px. Same2.9px diagonal held-frame/rounding bound as SE. Actual capture inspected; guided/neris-SW-travel/comparison.gif generated.

Integrated SW idle/calibrated atlas into isolated play_neris_walk.gd. Left+Down normalized motion, release to W/S, full release SW idle and angle-preserving first-boundary stop verified through actual key events, including approach(103,400) to(100,403). Prior five-direction tests pass. A parse typo introduced while adapting SE loading was corrected before passing validation. NERIS_PLAYABLE_OK and six-direction-playable-godot.png inspected; known log/certificate/shader-cache warnings remain. Rear diagonals, run, art consistency and broader M5-M9 remain unfinished. No release or push; review-06 unchanged.

### 2026-10-07 — M5.2.7.3 Northeast contact studies

Added independent NE contact guide/model generator using rear-diagonal source777022. Local trials777171/172 succeeded with zero outside-mask differences. Source images inspected: closed rear coat and protected torso retained; near/far trouser/shoe contacts alternate. Hem edges, pant cuffs and perspective still need polish. These two poses are not a completed walk.

Fixed-coordinate converter produces neutral and two contact sprites at96x144 with common crop/scale/sole reference, shared palette and binary alpha. Upper78 rows identical, three unique poses and unclipped bounds verified. Actual Godot three-pose render passes NERIS_NE_CONTACT_RENDER_OK and guided/neris-NE-contact-godot.png inspected. Known sandbox log/certificate warnings remain. Next NE passing, arms, intermediate phases and diagonal contact calibration, then NW/run and wider pack work. No interactive NE integration, release or push; review-06 unchanged.

### 2026-10-07 — M5.2.7.3 Northeast passing and crop correction

Local NE passing trials777173/174 completed with zero unmasked changes; support leg is explicit in metadata. Inspected both source images and converted five-pose study. Pant/shoe joins and hem edges remain rough, not accepted final art. Found the prior NE crop began atx200 and truncated the source ear/bun; expanded it tox155 and added source silhouette containment assertion. Existing border-only checks had not detected this internal crop error. Five unique sprites share coordinates/palette, protected upper78 and binary alpha.

Actual Godot contact-only versus contact/passing playback observes all eight timeline slots and passes NERIS_NE_PLAYBACK_OK. Captured24 frames, inspected runtime image and saved guided/neris-NE-leg-motion-godot.gif. Four distinct movement drawings held over eight slots, not eight finished phases. Known log/certificate warnings remain. Arms, intermediates, ground calibration, NW/run and broader M5-M9 scope remain incomplete. No new release, interactive NE integration or push.

### 2026-10-07 — M5.2.7.3 Northeast near-arm motion

Added masked local near-arm generator with shoulder rotation opposite the near leg, full and half poses. Initial175/176 contained white background speckles.179/180 fixed edge-connected whites but retained enclosed white pockets near the hand;183-186 removed hand-region pockets but left cuff-adjacent white. Final187-190 use an explicit original cuff polygon to preserve cream cloth while removing background whites, and broader underlying coat fill closes shoulder seams. All selected source images inspected; hand outline/torso overlap and coat edge still require polish. Rejected trials retained locally.

Converter now9 unique poses, protected head49 and corresponding lower91 pixel equality pass. Actual Godot --arms playback compares fixed arm with near-arm phases and observes all8 slots; capture inspected and neris-NE-arm-motion-godot.gif saved. Known log/certificate warnings persist. Far-arm counter-swing, intermediate legs, contact calibration, NW/run and wider M5-M9 remain unfinished. Not final art, no NE interactive integration/release/push.

### 2026-10-07 — M5.2.7.3 Northeast complementary far arm

Added local far-arm generator on selected near-arm sources187-190. Initial191-194 protection boundary atx242 truncated the forward hand; widened to258 and regenerated195-198. All selected jobs succeeded with zero outside-mask changes; all source images inspected. Explicit cream-cuff mask avoids white background contamination. Far hand/coat overlap and angular silhouettes still need polish, not final art acceptance.

Converter now13 unique poses; head49, corresponding lower91 and near-side columns50+ preserved. Godot --two-arms compares near-arm-only versus complementary arms, observes all8 timeline slots and passes NERIS_NE_PLAYBACK_OK. Runtime image inspected; guided/neris-NE-twoarm-motion-godot.gif saved. Known sandbox log/certificate warnings remain. Intermediate leg phases and diagonal contact calibration next; NW/run and broader M5-M9 unfinished. No NE interactive integration/release/push. A mistyped trailing Python version command failed after successful generation; no model job restarted from that shell failure.

### 2026-10-07 — M5.2.7.3 Northeast intermediate legs and phase assembly

Added NE down/up local model guide generation with explicit near/far support legs.199-202 succeeded with zero unmasked differences; all four source images inspected. Rear coat preserved; shoe/hem variation and bent-knee silhouettes still require refinement. Converter now17 unique poses, fixed complete silhouette crop, protected upper78 on intermediates and binary alpha verified.

New phase exporter composes contact/down/passing/up for each support leg with complementary arms above row91. Head49 and lower91 preservation pass; all8 lower-body phases are distinct. Actual Godot --transitions comparison observes all8 timeline slots and passes NERIS_NE_PLAYBACK_OK. Runtime capture inspected; guided/neris-NE-transition-motion-godot.gif saved. Known sandbox log/certificate warnings remain. This is in-place phase coverage, not finished art or verified locomotion. Next NE two-axis stance calibration, then NW/run and broader M5-M9 work. No interactive NE integration, release or push.

### 2026-10-07 — M5.2.7.3 Northeast two-axis contact calibration

Added export, actual Godot travel preview and trace validator for NE at normalized24px/s,12fps. Explicit opaque anatomical heel anchors use negative horizontal and positive vertical local progression to compensate northeast world motion. Maximum lower-region axis correction2px; upper101 unchanged and bottom112+ rigid translation verified. Both feet move within adjusted rows, not independently rigged.

Actual8-stance trace initially reduced maximum Euclidean marker drift4.7713 to2.4285px. Moved preview labels away from sprite lanes and reran:4.7713 to2.5092px, still below2.9px held-frame/rounding bound. Runtime captures inspected and guided/neris-NE-travel/comparison.gif saved. First exporter adaptation accidentally changed the fixed-row threshold; rigid-shoe invariant caught it and the threshold was corrected before passing. Known log/certificate warnings remain. This measures contact markers, not final animation/art acceptance. NE interactive integration, NW/run and wider M5-M9 remain unfinished; no release/push.

### 2026-10-07 — M5.2.7.3 Northeast interactive integration

Integrated NE neutral and calibrated12fps/24px/s atlas into isolated play_neris_walk.gd. Right+Up normalized movement uses the independent rear-diagonal sprites. Updated first-boundary clipping for the upper edge while preserving SE/SW behavior. Actual InputEventKey checks verify NE speed/direction, release to E/N, full release to NE idle, conflicting vertical inputs, and angle-preserving stops at(550,397) from(547,400) and(403,330) from(400,333). Existing six-direction checks also pass.

NERIS_PLAYABLE_OK reports S/N/E/W/SE/SW/NE. Inspected guided/neris-stance/seven-direction-playable-godot.png. Known sandbox log/certificate/shader-cache warnings remain. NW and run are unavailable; art proportions, shading and hand/garment polish remain unapproved. Broader M5-M9 goal unfinished; review-06 unchanged, no release or push.

### 2026-10-07 — M5.2.7.3 Northwest contact studies

Added independent NW contact generator from source777033. Local203/204 succeeded with zero unmasked changes; source images inspected. Rear garment and left-hip ornament remain protected; no mirrored final artwork. Near shoe on image left is larger/lower, and contact alternates with far shoe. Shoe contours, hem edges and cross-view proportions remain unapproved.

Fixed full-silhouette crop(165,source top,345,640), common scale/anchor and shared palette produce three distinct96x144 sprites. Upper81 equality, binary alpha, silhouette containment and unclipped canvas checks pass. Conversion enum typos from adapting the directional template were corrected before success. Actual Godot three-pose render passes NERIS_NW_CONTACT_RENDER_OK; guided/neris-NW-contact-godot.png inspected. Known sandbox log/certificate warnings remain. Next passing/arms/intermediates and travel calibration; no NW interactive integration, release or push. Wider M5-M9 remains unfinished.

### 2026-10-07 — M5.2.7.3 Northwest passing poses

Added local NW passing generator with explicit support-leg metadata.205/206 succeeded with zero unmasked changes; both source images inspected. Raised feet alternate and rear coat remains intact, but ankle/shoe joins and hem contours are still rough. Converter now5 unique cells, common full-silhouette crop, protected upper81 and binary alpha pass.

Actual Godot contact-only versus contact/passing comparison observes all8 timeline slots and passes NERIS_NW_PLAYBACK_OK. Runtime image inspected, guided/neris-NW-leg-motion-godot.gif saved. Four distinct movement drawings held across8 slots, not8 finished phases. Known log/certificate warnings remain. Next arms/intermediates and travel calibration; NW interactive movement, run and broader M5-M9 remain unfinished. No release or push.

### 2026-10-07 — M5.2.7.3 Northwest near-arm studies

Added local NW near-arm generator with full/half opposite-shoulder rotations, explicit cream-cuff region and protected left-hip ornament/belt.207-210 succeeded with zero unmasked differences; four source images inspected. Hand/ornament overlap in the inward pose and hand contours remain visibly rough, not accepted final art. Outward poses retain the independent rear garment.

Converter now9 unique cells; head50 and matching lower93 preserved. Actual Godot --arms comparison observes all8 timeline slots, passes NERIS_NW_PLAYBACK_OK and captures24 frames. Runtime image inspected; guided/neris-NW-arm-motion-godot.gif saved. Known log/certificate warnings remain. Far-arm motion, intermediates, travel calibration, NW integration, run and broader M5-M9 remain unfinished. No release or push.

### 2026-10-07 — M5.2.7.3 Northwest complementary far arm

Added local far-arm generator on207-210 near-arm sources with opposite smaller shoulder rotations and protected near side/belt.211-214 succeeded with zero unmasked differences; all source views inspected. Far cuff/body overlap and hand outlines remain angular; this is motion study coverage, not final art approval.

Converter now13 unique sprites; head50, corresponding lower93 and near-side columns0:45 preserved. Actual Godot --two-arms comparison observes all8 timeline slots and passes NERIS_NW_PLAYBACK_OK. Runtime image inspected; guided/neris-NW-twoarm-motion-godot.gif saved. Known log/certificate warnings remain. Next intermediate legs, two-axis contact calibration and NW interactive integration. Run and broader M5-M9 remain unfinished. No release or push.

### 2026-10-07 — M5.2.7.3 Northwest intermediate legs and phase assembly

Added local NW down/up generator with explicit support legs and preserved rear garment/hip ornament.215-218 succeeded with zero unmasked differences; all source images inspected. Shoe openings and angular knee silhouettes remain rough and unapproved. Converter now17 unique sprites, common crop/scale and protected intermediate upper81 verified.

New phase exporter retains support-leg identity across contact/down/passing/up, composes complementary arms above row93 and preserves head50/lower93. All8 lower-body phases distinct. Actual Godot --transitions observes all8 timeline slots and passes NERIS_NW_PLAYBACK_OK; runtime image inspected and guided/neris-NW-transition-motion-godot.gif saved. Known sandbox log/certificate warnings remain. Next actual NW travel/contact calibration and interactive integration. Run, art polish and wider M5-M9 unfinished; no release or push.

### 2026-10-07 — M5.2.7.3 Northwest two-axis contact calibration

Added NW travel exporter, actual Godot preview and trace validator at normalized24px/s and12fps. Explicit opaque support-heel anchors advance positively in both local axes to compensate northwest world movement. Upper101 unchanged and bottom112+ rigid translation checked; adjustment bound2px per axis. Both feet move within corrected rows, not independently rigged.

Eight complete actual stances reduce maximum Euclidean heel-marker drift4.1253 to2.4284px, within2.9px held-frame/rounding tolerance. Runtime capture inspected and guided/neris-NW-travel/comparison.gif generated. Known sandbox log/certificate warnings remain. Contact calibration is not finished art or biomechanical acceptance. Next NW input integration to complete8-direction walk operation; run, visual refinement and wider M5-M9 unfinished. No release or push.

### 2026-10-07 — M5.2.7.3 Eight-direction interactive walking

Integrated independent NW neutral/calibrated atlas into play_neris_walk.gd. Left+Up uses normalized24px/s movement and12fps animation, with matching idle on release. Extended first-boundary clipping to northwest. Actual InputEventKey tests verify NW direction/speed, release to W/N, full release idle, vertical conflicts, left-edge approach(103,400) to(100,397), top-edge approach(400,333) to(397,330), and already-blocked state. Prior seven-direction tests pass.

NERIS_PLAYABLE_OK now covers S/N/E/W/SE/SW/NE/NW, facing idle, axis conflicts, reset, boundaries and separate shadow. Inspected guided/neris-stance/eight-direction-playable-godot.png. Known sandbox log/certificate/shader-cache warnings remain. This closes Neris eight-direction walking technical coverage only; run, consistent proportions/palette across directions, hand/garment polish and broader M5-M9 assets remain incomplete. Review-06 unchanged; no release or push.

### 2026-10-07 — M5.2.7.3 Common-scale walk art audit and SE crop repair

Added actual Godot eight-heading walking gallery at2x/12fps with common ground guides. All8 headings observed all8 slots; NERIS_WALK_GALLERY_OK passes. Visual audit shows E/W coats noticeably browner than other headings, inconsistent head/body proportions and rough hand overlap. These remain concrete art blockers before acceptance, despite playable mechanics.

Source silhouette audit found SE crop185:370 discarded416 foreground pixels (source bounds169:337); SW/NE/NW checked crops discard0. Expanded SE to155:370 and added source containment assertion. Rebuilt17 poses/phases/calibration. Resampling moves one hand-boundary pixel to(43,87); anatomically this is hand/coat, not legs, so splice/protection boundary updated to88. Far heel anchor now(54,118), max correction2px. Actual8-stance SE trace4.9765 to2.4285px passes2.9 tolerance. Gallery rebuilt and inspected. Known sandbox log/certificate warnings remain. Next unify directional coat palette/proportions, then run and wider assets; no release/push.

### 2026-10-07 — M5.2.7.3 Side-coat palette consistency candidate

Added bounded deterministic E/W coat-ramp conversion on local-model-derived calibrated walk atlases and neutral sprites. Explicit brown fabric colors map into existing burgundy ramp within rows49:69 and75:103. Alpha, head/neck, belt band69:75, lower103+ and all unselected pixels unchanged. Outputs and hashes recorded under guided/neris-coat-palette; original calibrated atlases retained.

Actual Godot gallery --palette passes eight headings/eight slots and inspected capture shows E/W coats substantially closer to the shared wine palette. Fixed protected belt band can retain brown cloth; head/body proportions, noisy shading and hand overlap remain unresolved. This is a separate unapproved art candidate, not promoted into interactive/release assets. Known sandbox log/certificate warnings remain. Next refine material mask and cross-view proportions, then run and broader M5-M9. No push.

### 2026-10-07 — M5.2.7.3 Interactive side-coat candidate review

Added optional --palette mode to play_neris_walk.gd, loading E/W walk and idle candidates while retaining the default original review. Verifies all4 source/output SHA256 values and exact per-pixel alpha before substitution, rejecting stale candidates. Full actual eight-direction key/idle/boundary tests pass with replacements; NERIS_PALETTE_PLAYABLE_OK and NERIS_PLAYABLE_OK emitted. Inspected guided/neris-stance/palette-playable-godot.png. Known log/certificate/shader-cache warnings remain.

Local review command from repository root: `.local/godot/Godot_v4.7.2-stable_win64_console.exe --path pixel-rpg-demo --script res://authoring/play_neris_walk.gd -- --palette`. Omit --palette for original coats; add --check for automated key validation. This is an optional unapproved visual candidate, not a packaged release. Remaining brown fabric around protected waist band, inconsistent proportions and rough hands still need refinement; run and broader M5-M9 remain incomplete. No push.

### 2026-10-07 — M5.2.7.3 Refined side-coat material selection

Inspected enlarged E/W neutral waist regions with row guides. Earlier fixed69:75 protection primarily covered cuff/hand and surrounding cloth, not a reliably identified belt; do not claim a semantic belt mask. Replaced whole-row exclusion with per-frame warm hand-highlight seeds (rows65:88) dilated2px, retaining the explicit fabric-color allowlist. Rebuilt four candidates with unchanged alpha, protected head/lower legs/hand neighborhood and all nonselected colors verified.

Actual Godot --palette gallery passes all headings/slots and inspected capture shows the previous broad brown cloth band reduced. Hand mask is heuristic; does not establish perfect material segmentation or recover missing side-view belt details. Source art still needs garment/detail/proportion work. Candidate remains optional via --palette, not released; run and full M5-M9 remain incomplete. Known log/certificate warnings remain. No push.

### 2026-10-07 — M5.2.7.3 First east running key-pose study

Added local DreamShaper masked run generator with waist-pivot upper-body guide, bent complementary arms, raised rear heel and moving split coat. Trial777219 rejected for disconnected collar and simplified garment. Revised777220 reconnects collar and adds fastening/folds; outside-mask difference is zero relative to the leaned source guide, not the original standing image. Both trials retained locally. Head uses deterministic waist-pivot shear, not a newly drawn turned view.

Converted idle/walk/run comparison at shared source crop and scale to96x144 binary-alpha sprites; silhouette containment passes NERIS_RUN_KEYPOSE_OK. Actual Godot three-pose render passes NERIS_RUN_RENDER_OK, guided/neris-east-run-godot.png inspected. Known sandbox user-log/certificate warnings persist. Running silhouette is distinct from walking, but collar seam, omitted side keys/ornament, rough hands and cross-view proportions remain art blockers. One key pose only: no running cycle, flight phase, travel calibration or interactive promotion. Review-06 unchanged; no push. Next preserve costume details before complementary running poses and eight-direction expansion.

### 2026-10-07 — M5.2.7.3 Running costume-detail repair

Added bounded local-model repair on run220 using the original profile's gold-key silhouette and a closed neckline guide.221 restored keys but left a pale neck/collar gap;222 fills that gap while preserving the running pose. Both retained. Output equals its run220 source everywhere outside the feathered collar/key mask. Source and reference SHA256 recorded. Collar edges and hands remain rough; this is not final art acceptance.

Updated fixed-scale converter and actual Godot comparison to show idle/walk/run-before/run-refined. Four silhouettes fit the common crop; binary alpha, unchanged head rows0:35 and lower85+ between run versions verified. NERIS_RUN_KEYPOSE_OK and NERIS_RUN_RENDER_OK pass; runtime image inspected. Key detail is small but present in the sprite. Known sandbox log/certificate warnings remain. Next complementary run poses/flight phase, followed by actual cycle and travel validation; no run animation or broader pack completion claimed. No release or push.

### 2026-10-07 — M5.2.7.3 Running leg contact/flight studies

Generated far contact and two flight poses from repaired222, preserving the upper body and keys. Trials223-225 rejected: color-only cloth extraction introduced holes.226-228 use solid tail masks with sampled paint and filled hip; images inspected, unmasked pixels unchanged. Hem/boot contours remain crude. Near/far limb distinction is weak and the shared fixed arms are not a correct complete run cycle.

New converter yields four unique96x144 sprites at common crop/scale, binary alpha and at least4px flight clearance. Protected upper81 rows match; an attempted82-row bound caught one resampled boundary pixel at(47,81), so actual protection ends before that boundary. NERIS_RUN_LEGS_OK passes. Actual Godot8fps comparison observes all4 frames, maintains separate fixed shadow and emits NERIS_RUN_LEGS_PLAYBACK_OK; runtime capture inspected and guided/neris-east-run-legs.gif saved. Known sandbox log/certificate/shader-cache warnings remain. This sparse sequence still lacks crossing/passing, landing compression and opposite arm phases; it reads too much like hopping, not finished running. Next add crossing/compression and correct arms before travel validation or multi-direction expansion. No release or push.

### 2026-10-07 — M5.2.7.3 Running crossing/passing poses

Added local generator for near/far support with supporting foot beneath hips and the other foot folded across the shin.229/230 succeeded; source views inspected and unmasked differences zero. Solid coat-tail mask retained. These poses visibly narrow the leg silhouette compared with the repeated extended contact/flight shapes, but ankle intersections and coat seams remain rough and near/far distinction remains weak.

Converter now6 distinct fixed-scale sprites, protected upper81, binary alpha and flight clearance checks pass. Godot --crossing compares original4 poses at8fps with6 poses at12fps (equal0.5s cycle), observes all6 requested slots and passes NERIS_RUN_LEGS_PLAYBACK_OK. Captures inspected and guided/neris-east-run-crossing.gif saved. Known sandbox log/certificate/shader-cache warnings persist. Upper arms remain fixed, compression/push-off incomplete and ground-travel lock absent; this is not finished running or approved art. Next landing compression and opposing arm swing before directional expansion. No release or push.

### 2026-10-07 — M5.2.7.3 Running landing compression

Generated near/far down poses231/232 with bent support knee, shortened leg height and folded recovery leg; source images inspected, unmasked pixels unchanged. Converter now8 unique fixed-scale poses, protected raw upper81 and binary alpha verified. Separate weighted atlas translates down poses2px; resulting sole heights stay within1px of contact floor. Flight clearance remains at least4px. This verifies vertical image placement, not world-space foot lock.

Actual Godot --down compares6 phases/12fps to8 phases/16fps with equal0.5s cycles. Initial83ms capture cadence missed frame slots; after faster42ms requested sampling, all8 observed and NERIS_RUN_LEGS_PLAYBACK_OK passes. Inspected runtime capture; guided/neris-east-run-down.gif is a roughly50ms-per-capture preview, not timing evidence. Known sandbox log/certificate/shader-cache warnings persist. Fixed arms, weak depth distinction, rough shoes/hem and uncalibrated travel remain. Next opposite arm poses and phase coordination. No release or push.

### 2026-10-07 — M5.2.7.3 Opposite running arm endpoint

Local233 rebuilt backward near elbow and forward far arm but introduced a collar discontinuity.234 extends the torso guide and protects source rows before316/from413; masked generation succeeds with zero outside changes. Source inspected: collar retained, but shoulder seam, flat torso and fist/cuff contours remain rough. Rejected233 retained.

New arm exporter uses the common source crop/palette, verifies head49 and lower74 equality, and splices opposite arm endpoints above74 over8 leg poses. Near-leg-leading half uses near-arm-back; far-leg-leading half retains near-arm-forward. Down offsets remain2px. Actual Godot --arms comparison observes all8 slots at16fps and passes NERIS_RUN_LEGS_PLAYBACK_OK; capture inspected and approximate50ms GIF saved. Known sandbox log/certificate/shader-cache warnings remain. This is abrupt two-endpoint switching, not finished coordinated arms: intermediate arm shapes and shoulder/torso repaint needed before travel calibration. No release or push.

### 2026-10-07 — M5.2.7.3 Running arm midpoint

Generated235 with near elbow beneath shoulder and folded forearm, far arm partly occluded by torso. Zero changes outside mask; source inspected. Midpoint retains face/collar/belt/keys/legs, but shoulder boundary and fist/cuff treatment remain rough. There is still a visible torso-shading difference between model-redrawn sleeves and the original endpoint.

Optional export --middle adds a third arm drawing with mapping back/back/middle/front/front/front/middle/back over existing8 leg poses. Same midpoint is reused in both swing directions; this is not8 distinct arm drawings. Head49/lower74 preservation passes. Actual Godot --middle compares two endpoints against midpoint sequence at16fps, observes all8 slots and passes NERIS_RUN_LEGS_PLAYBACK_OK; capture inspected and approximate50ms GIF saved. Known sandbox log/certificate/shader-cache warnings persist. Next shoulder/torso consistency and world-space foot-travel calibration; no art approval, release or push.

### 2026-10-07 — M5.2.7.3 Running upper-garment palette candidate

Enlarged three-arm audit identifies different brown/wine quantization and brighter back-arm torso. Added explicit10-color fabric mapping to existing wine ramp within rows51:73, offset2 for down frames. Warm skin neighborhoods protected with1px dilation.914 pixels across8-frame atlas changed; alpha and every unselected pixel unchanged. The heuristic is not a complete semantic material mask and does not repair shoulder geometry or fold placement.

Actual Godot --material compares original midpoint atlas to optional corrected palette, observes all8 slots and passes NERIS_RUN_LEGS_PLAYBACK_OK. Runtime capture inspected; guided/neris-east-run-material.gif saved at approximate50ms/capture. Brown patches reduced; pose silhouettes, shoulder seams and shading distribution still differ, so no final art acceptance claimed. Known sandbox log/certificate/shader-cache warnings persist. Next world-space foot movement measurement; keep original atlases and this optional candidate separate. No release or push.

### 2026-10-07 — M5.2.7.3 Running world-space heel calibration

Added exporter/actual Godot travel preview/trace validator at48px/s and16fps. Source is optional material candidate. Support phases0/1/2 and4/5/6 use opaque heel markers at row119; airborne3/7 have no planted marker and remain pixel-identical. Target heels step3px backward per frame. Lower-row correction bound3px, upper101 unchanged, bottom114+ rigid translation and pixel-count preservation pass. Both feet in corrected lower rows move together; this is not a skeletal rig.

Actual runtime11 complete three-phase support groups reduce maximum heel-marker drift5.3333 to2.5999px, within3.05px held-frame tolerance. Monotonic trace and improvement assertions pass; inspected travel-16.png and comparison.gif produced under guided/neris-east-run-travel. Known sandbox log/certificate warnings persist. Marker calibration does not establish full-sole grounding, natural biomechanics, shoulder/hand quality or final art acceptance. Next interactive east walk/run switching with this candidate, while wider directional running and full pack remain unfinished. No release or push.

### 2026-10-07 — M5.2.7.3 Interactive east walk/run switching

Integrated calibrated east run candidate into play_neris_walk.gd. Shift+Right selects48px/s at16fps; release Shift returns24px/s walk at12fps. Mode changes reset phase, idle/blocked movement clears running. Other headings explicitly retain walk; no mirrored or accelerated placeholder runs. Startup checks source hash and expected run metadata/dimensions. UI states the single-heading run scope.

Actual InputEventKey checks exercise walk/run/walk speed and texture selection, direction release while Shift held, diagonal walk fallback, opposing keys, right boundary and reset/shadow. Initial same-turn test failed because queued input had not flushed; press helper now flushes buffered events before synchronous test ticks. Full prior eight-heading/palette checks plus NERIS_EAST_RUN_PLAYABLE_OK pass. Screenshot guided/neris-stance/east-run-playable-godot.png inspected. Known sandbox log/certificate/shader-cache warnings remain. Command: `.local/godot/Godot_v4.7.2-stable_win64_console.exe --path pixel-rpg-demo --script res://authoring/play_neris_walk.gd -- --palette`. Add --check for validation. Art transitions/proportions remain unapproved; seven other running headings and broader pack incomplete. No release or push.

### 2026-10-07 — M5.2.7.3 Independent west running key pose

Local236 starts from left-facing source031 with leftward waist-pivot guide, far leg forward/near heel recovering and complementary near arm forward. Uses plain left belt without right-side keys; no mirrored final east artwork. Source inspected and zero unmasked differences relative to leaned guide verified. Far cuff/hand is ambiguous, shoulder contours rough and torso simplified; not accepted final art.

Converter uses fixed left-source crop/scale for idle/run96x144 sprites, confirms full silhouette and binary alpha. Cross-view comparison shows remaining head/body proportion differences against east study. Actual Godot two-pose review passes NERIS_WEST_RUN_RENDER_OK; screenshot inspected. Known sandbox log/certificate warnings persist. This is one west key pose, no west loop, calibration or input integration. East run remains sole playable running direction. Next repair far cuff/hand then west phases while preserving the approved full pack scope. No release or push.

### 2026-10-07 — M5.2.7.3 West running far cuff repair

Added bounded local-model repair of236 far arm.237 separated sleeve/cuff but mask cut the top of the fist.238 expands mask upward, preserves the near side and shows a small skin fist with narrow cream cuff. Both retained; selected238 source inspected and outside-mask difference zero. Far arm shape remains simplified, not art-approved.

Converter retains before/after at common scale; binary alpha/full silhouette and identical head47/lower67 verified. Actual Godot three-pose comparison passes NERIS_WEST_RUN_RENDER_OK and screenshot inspected. Known sandbox log/certificate warnings persist. West remains one run key pose with no loop or interactive integration; next alternating support/contact/flight poses. Full pack remains incomplete; no release or push.

### 2026-10-07 — M5.2.7.3 West eight-phase running legs

Added local west phase generator from repaired238.239-245 cover opposite contact, alternating down/support/flight; all succeed with zero unmasked differences. Seven-source contact sheet inspected: torso stable, leg crossing/flight present, but tail-to-thigh transitions rough and depth distinction weak. No mirrored finished artwork.

Fixed west crop/scale converter yields8 distinct96x144 poses; protected raw upper79, binary alpha, complete silhouette and flight clearance>=4px pass. Down poses translate2px in weighted atlas with sole height within1px of contact floor. Actual Godot16fps observes all8 slots, fixed shadow and emits NERIS_WEST_RUN_PLAYBACK_OK. Runtime capture inspected; guided/neris-west-run-legs.gif saved at approximate50ms/capture. Known sandbox log/certificate/shader-cache warnings remain. Arms are still fixed, no west travel calibration or input integration; next complementary arms and phase assembly. Full pack unfinished, no release or push.

### 2026-10-07 — M5.2.7.3 West running arm assembly

Generated complementary near-back and middle arms.246/247 retained a fragment of the old near hand above the mask; rejected.248/249 expand that region while separately protecting collar. Source images inspected; outside-mask pixels unchanged. Shoulder outline/torso repaint and fists still rough, not final art.

Exporter uses independent west crop/palette, preserves head45/lower72 and composes front/front/middle/back/back/back/middle/front over existing far-leading then near-leading leg phases. One midpoint reused in both swing directions. Actual Godot --arms compares fixed arms against three arm poses at16fps, observes all8 slots and passes NERIS_WEST_RUN_PLAYBACK_OK. Runtime capture inspected and approximate50ms GIF saved. Known sandbox log/certificate/shader-cache warnings remain. West still lacks travel calibration/input integration; art consistency and six other run headings incomplete. No release or push.

### 2026-10-07 — M5.2.7.3 West running travel calibration

Added west exporter/actual Godot preview/trace validator at-48px/s and16fps. Rightmost opaque row119 heel anchors advance3px per support slot; lower correction bound2px, upper101 unchanged, bottom114+ rigid and no pixel loss verified. Airborne frames remain unchanged and are excluded from stance statistics. Eleven complete actual support groups reduce max marker drift5.2000 to2.8002px, below3.05 held-frame tolerance. Runtime capture inspected; comparison.gif saved in guided/neris-west-run-travel. This measures a heel marker, not complete sole/biomechanical correctness. Art remains unapproved; known sandbox log/certificate warnings persist. Next west input integration; no release or push.

### 2026-10-07 — M5.2.7.3 Interactive west running

Integrated independent west calibrated atlas with source hash/dimension/speed checks. Shift+Left/Right now run at48px/s; other headings remain24px/s walking. Added actual key-event checks for west speed, release-to-walk, direct east run turn, northwest fallback, return to west run, idle and left boundary. Generic abs inference caused a parser failure during editing; explicit bool/absi fixed it before successful validation. All east/west run, palette and eight-direction walking markers pass. Inspected guided/neris-stance/west-run-playable-godot.png. Known sandbox log/certificate/shader-cache warnings remain. Two running headings only; art/proportion/garment issues and six other run headings remain incomplete. No release or push.

### 2026-10-07 — M5.2.7.3 Front running high-knee studies

Local250/251 derive from front006 with alternating raised knees and shortened corresponding coat tail. Original ivory trim, center fastening and waist keys retained; upper source rows before479 protected. Both source images inspected, zero unmasked changes. Current straight torso/fixed arms make these read as high stepping, not a finished run. Shoe edges and shortened-tail folds remain rough.

Fixed front crop/scale produces three distinct96x144 sprites; full silhouette/binary alpha/protected upper81 pass. Actual Godot static comparison passes NERIS_FRONT_RUN_RENDER_OK and screenshot inspected. Known sandbox log/certificate warnings persist. No front run loop, airborne/compression phases, world travel calibration or input integration. Next front torso/arm pose work and transitions; full pack remains unfinished. No release or push.

### 2026-10-07 — M5.2.7.3 Front opposite arm endpoints

Generated arms opposite250/251 raised legs.252/253 broad side clearing removed parts of torso/tails, rejected and retained.254/255 restore central jacket before sleeve drawing and tighten lower protection; source views inspected, zero unmasked differences. Faces/buttons/keys preserved. Shoulder seams and thin side remnants remain visible; not final art.

Converter now5 unique common-scale sprites, with head47 and matching lower86 preserved for arm edits plus prior upper81 equality for leg-only poses. Actual Godot five-pose comparison passes NERIS_FRONT_RUN_RENDER_OK; screenshot inspected. Known sandbox log/certificate warnings persist. Two bent-arm high-knee endpoints only: torso still upright, no compression/flight/midpoint sequence, travel calibration or front-run interaction. Next cleanup and transition construction; full pack incomplete. No release or push.

### 2026-10-07 — M5.2.7.3 Front sleeve join cleanup

Local256/257 repair bounded shoulder seams and narrow old-sleeve traces on254/255. Source views inspected: white shoulder gaps filled; small side residues/flat shoulder shading still need polish. Outside masks unchanged; retained original trials. Updated selected arm sprites.

Conversion initially detected one changed opaque pixel at(57,86), brown94/65/56 to wine91/52/63 on lower jacket edge due to cleanup/resampling. Actual leg preservation boundary is now87, head47 remains protected. Corrected converter passes; subsequent actual Godot static render passes NERIS_FRONT_RUN_RENDER_OK. Earlier render after failed conversion was not treated as conversion success. Known sandbox log/certificate warnings persist. Torso still upright and front running transitions absent; next midpoint/compression/flight construction. No release or push.

## 2026-10-07: M5.2.8 route-change record

Recorded the user's intended shift from character-specific AI frame repair toward editable modular 3D characters, shared skeletal walking and eight-direction sprite rendering. Added proposed pilot steps and reuse/visual acceptance criteria; updated current priority and backlog. Explicitly deferred running and preserved prior studies. Documentation only: no generation, modeling, runtime changes, packaging or push. Verified the documentation diff and task-ID consistency.

## 2026-10-07: M5.2.6.2 additional blonde character prototype

User requests one additional long-haired, slender, full-busted blonde character. Generated adult female concept under working name Aurelia using local DreamShaper 8 on port 8189. Teal/cream/brass traveling-mage outfit is an assistant assumption; user has not selected profession or accepted final design. Trial a1 drifted to realistic rendering and unsuitable palette/costume; retained. Trial a2 uses existing Sylva illustration as an img2img style reference and is the current review candidate: long golden hair, slender adult silhouette, full bust under clothing and coherent teal/brass outfit. Face/hand details and roster-scale proportions still need refinement. This is an additional concept, not a finished sprite or animation, and does not resume per-frame animation work or change M5.2.8 direction. Sources and generation graphs retained under production/pixel-rpg/model-wave-01/{originals,runs}/ch_aurelia-a*. No generated images staged.

### 2026-10-07: M5.2.6.2 Aurelia costume studies

User requests bikini-style top, thong bottom, red cape and large-eyed chibi face. Local adult-character trials a3-a6 retained with graphs. Current adult review candidate a6 has blonde hair and red two-piece costume, but cape exterior remains tan, head proportions/eye size do not yet meet requested chibi style, and decorative background persists. A3 has hair/face artifacts; a4 introduces a corset; a5 has inappropriate youthful proportions and is not selected. No trial is final accepted art. Front-only view does not verify rear thong construction. Existing originals retained; shared-rig pilot remains future work.

### 2026-10-07: M5.2.6.2 user-selected Aurelia a8 edit

User selected a8 and requests yellow hair, red cape and a more open neckline. Earlier a7-a10 whole-image style trials are retained, not accepted. Added bounded edit script: recolor hair/cape by region/color selection; locally generate only neckline mask and composite onto recolored a8. Result guided/aurelia-selected-778011.png inspected: gold hair, burgundy cape, lowered white blouse neckline; selected face, pose and proportions retained. Zero pixel difference outside neckline mask relative to recolored base verified. This follows the latest selected image (short tied hairstyle retained), superseding the prior full-costume retry. Neckline edge remains a review candidate; no animation or final sprite acceptance.

## 2026-10-07: M5.2.6.2 Animagine XL 4.0 Opt test

Installed verified official Opt checkpoint under .local/models, retaining the existing DreamShaper. Prepared downloader, resumable same-brief generation script and labeled review-sheet script. At user request, released memory only from verified idle project ComfyUI processes; available commit rose from 1.37 to 15.35 GiB. One low-VRAM server retained on 8189; no page-file changes or unrelated application termination.

16/16 complete at 832x1216; Euler ancestral, normal scheduler, 28 steps, CFG5. First 30.19s, subsequent median26.17s, total421.01s, device-wide peak5393MiB. Original records/seeds retained; new prompts are model-adapted and resolution differs from historical originals. Visual review of complete overview shows promising linework and greater body/species differentiation but inconsistent proportions, pose/background/style artifacts. This proves local inference feasibility for the tested setup, not final sprite quality or strict superiority. Full outputs and paired sheet are in production/pixel-rpg/animagine-comparison. Model freed after testing. Script compile and diff checks passed; resources remain ignored; no push.

### 2026-10-07: M5.2.6.2 interactive Animagine edit workflow

Added production/workflows/animagine-local-edit.json for ordinary masked appearance edits in ComfyUI 8189. Uses verified Opt checkpoint, existing Ivara as local example, VAEEncodeForInpaint, fixed seed/28 steps/CFG5/Euler ancestral and denoise0.45. User paints a mask in LoadImage; final composite preserves pixels outside that mask. Blank mask leaves the image unchanged. Source originals are retained; outputs use animagine_manual_edit prefix in .local/reference-comfy/output. All node types/input names and bidirectional link types validated against running ComfyUI object_info. No image generated or GUI round-trip tested in this slice; user must paint and save a mask before running.

### 2026-10-07: M5.2.6.2 masked edit gray-patch fix

User reran with ordinary blue-clothing prompt. Latest task succeeded but output retained a gray-looking patch. Input RGB exactly matches original; alpha contains a nonempty soft mask (26405 pixels, peak178/255). VAEEncodeForInpaint blanked the masked input, combined with low denoise0.45 and partial final compositing. Replaced blanked encoding with VAEEncode + SetLatentNoiseMask, thresholded painted mask at0.1, raised default denoise to0.65 and added actual mask preview. This changes mask handling; a blank mask still intentionally preserves the whole image.

Executed safe blue-clothing graph with the user's mask: prompt a5675065-0909-45fb-a30d-19deb71039f8 succeeded; output .local/reference-comfy/output/animagine_blue_edit_fixed_00001_.png visually shows blue cloth instead of gray patch. Outside-mask pixels exactly match input. New node/input/link structure validated against running server. UI file must be reimported; changing file does not update an already-open browser workflow. Detail changes inside mask are expected, not a precise recolor guarantee.

### 2026-10-07: M5.2.6.2 photographic model installation and Z-Image cancellation

Installed official pinned RealVisXL V5.0 FP16 and Realistic Vision V6.0 B1 FP16 plus SD1.5 VAE. Full SHA256 checks passed. Actual ordinary denim-jacket portrait tests succeeded: RealVis768x1024 in24.1s, Realistic Vision512x768 in9.1s (client elapsed, different resolutions; not a controlled speed benchmark). Both outputs visually inspected under .local/reference-comfy/output/photo_models. Matching UI workflows copied to .local/reference-comfy/user/default/workflows. Existing user workflows/art retained.

Sequential curl download proved faster than parallel ranges in this connection. Experimental range downloads suffered truncated responses; an official HF client probe also made no useful progress. Probe caches were retained: .local/download-ranges (about6.46GB), .local/hf-photo-download, and one zero-byte default Xet log under C:/Users/hp/.cache/huggingface/xet. No files deleted.

User then cancelled Z-Image as too large. Verified own download parent/curl process identities and stopped them without force. Exact planned deletion scope: its6.201GB main file,2.946GB partial encoder,0.335GB VAE and two associated range-cache directories, totaling13,019,325,282bytes. Paths resolved inside project .local. Deletion awaits the exact CONFIRMED response mandated by AGENTS.md / CODEX_DANGEROUS_COMMANDS.md; do not report them removed yet. Small provenance records and source workflow recipes remain. Default installer now excludes Z-Image; no third-model generation was attempted. No push.

### 2026-10-07: M5.2.6.2 approved Z-Image removal completed

User replied CONFIRMED to the displayed exact Remove-Item command. Revalidated all five absolute targets under project .local and checked for reparse points, then removed only the approved main model, partial text encoder, ae VAE and their two range-cache directories. All five paths verified absent; RealVisXL and Realistic Vision files remain at their expected lengths. Planned logical data removed:13,019,325,282bytes (~12.1GiB). E free space after removal:137,396,404,224bytes (~128GiB); whole-drive free-space delta can include concurrent activity. Small provenance metadata and source recipes remain. No other assets or caches deleted; no push.

## 2026-10-07: poster-cover/M1.1.1-M1.1.3 side-task research

Applied create-task template/builder to side-tasks/2026-10-07-poster-cover, with12 English documents and scoped M1-M4 plan. Compared primary-source local models, reference editing approaches, native text versus raster layers, hardware/complete-package constraints and futureAPI boundaries. Existing portrait measurements were labeled historical, not new poster tests. Recommended existing-model layered composition first; klein4B is a conditional editing challenger, AnyText2 optional lettering, Qwen20B alternatives deferred. No weights, inference, service implementation or deletion. Updated parent indexes; checked local document links, placeholders and Git whitespace. Local documentation checkpoints only; no push.

## 2026-10-08 — poster-cover/M2.3

User-authorized quantized Klein install and validation completed. Three pinned weights verified, three local generation/edit runs inspected;576x768 default saved. Source-only checkpoints include reusable workflows and memory-aware runner. Weights/results stay under ignored.local; no push. See side task README for evidence and limitations.

## 2026-10-08 — task ownership closure for poster-cover

Marked poster-cover as TRANSFERRED to dist-poster-pool-projects in README, overview, active tasks, backlog, milestones and decisions. Historical records and stable IDs remain; poster work is not locally queued. Restored original game-art production as the current focus, including the previously recorded M5.2.8 shared-rig character pilot. Documentation-only update; no scene, asset or runtime changes.

## 2026-10-11 — M5.2.8.1 Ivara inspection and deformation trial

Imported the unchanged Tripo GLB into Blender 4.5.14, measured connectivity and textures, and rendered five views. Created a welded/decimated 59,999-triangle copy, approximate 20-bone rig and automatic weights. All vertices received weights. Saved a rest-stress-rest action and re-imported the exported GLB: 20 bones/action survived and animated displacement was verified. Nine exported-asset preview frames were assembled into a GIF. Visual review found unwanted torso/jacket movement: this is a successful diagnostic experiment, not an accepted rig, finished walk or Godot asset. Original SHA256 unchanged. Full measurements, local paths, export warnings and next gate in production/pixel-rpg/ivara-rig-study.md. Generated files remain ignored; no remote push.

## 2026-10-11 — M5.2.8.1.1-M5.2.8.1.3 low-poly, elements and breathing

User clarified hidden outerwear/equipment, retained inner outfit and fixed-foot gentle breathing, then requested polygon reduction and body/clothing separation. Produced a 19,999-triangle copy, split its surfaces into seven objects and exported those parts independently. Constructed a separate 4,348-triangle eight-object white mannequin proxy; this is approximate new anatomy, not extracted under-clothing surfaces. Hiding original jacket/belt/guards exposed missing surfaces. Corrected torso-center basis for this study; retained failed preliminary drafts locally. Created a covered shape-key breathing study (4 seconds, 0.0018433 model-unit maximum displacement, evaluated feet exactly unchanged). Garment boundaries/fit remain visibly rough and are not accepted. Saved an assembled review Blender file, separate static GLBs, metrics and previews under ignored .local/ivara-rig-study/2026-10-11-elements. Original GLB and 60k trial hashes unchanged. No model/preview files staged, no push.

## 2026-10-11 — M5.2.9.1 reset and open-resource review

Recorded user-directed body-first reset and preserved prior experiments as reference-only. Researched official Blender base-mesh, MPFB/MakeHuman, wardrobe/equipment and Kenney sources. Shortlisted CC0 body/garment routes and identified a conflict between Quaternius pack-page CC0 labels and its current QAL redistribution restrictions. Stored links, scope and selection caveats in context/research-notes.md. No assets downloaded, software installed, models edited, or animation resumed. Documentation-only verification and scoped local checkpoint; no push.

## 2026-10-11 — M5.2.9.2 standard-body-first decision

Recorded the user's request to make one standard body work before parameterized character expansion. Prioritize Blender + MPFB/MakeHuman and the minimal independent-game path: reviewed body, one simple outfit, basic materials, existing rig, then idle/walk and engine/sprite validation. Updated active status, milestone gate, decision and deferred backlog. No download, installation, model edit or animation work; documentation-only checkpoint.

## 2026-10-12 — M5.2.9.2-M5.2.9.6 single-character technical pilot

User expands authorization from body-only testing to one full body/clothing/equipment/rig/movement pilot. MPFB 2.0.18 pinned source loaded locally; one continuous adult male body created and three views inspected. Independent CC0 sweater, trousers, boots and sword fitted with existing UV/materials. Built-in 53-bone game_engine rig and interpolated garment weights; corrected initial waist overlap and knee pole direction. Packed editable stages, 31,418-triangle five-mesh GLB, Idle/Walk and actual Godot demo now exist under ignored .local/mpfb-pilot/character-v1.

M5.2.9.2-.5 have a working technical baseline, with artistic acceptance pending. M5.2.9.6 remains in progress: idle/walk import and sampled foot-motion tests pass; actual Godot viewport capture inspected. Gait/contact polish, eight-direction sprites and cross-character reuse are not complete. White-clay bald anatomy and generic existing wardrobe are intentionally provisional, not final anime game art. Preserve all prior Tripo studies. See production/pixel-rpg/mpfb-character-pilot.md for exact source licenses, commands, outputs and limitations. No resources committed; no push.

## 2026-10-12 — M5.2.9.2 accepted; M5.2.9.5 body-only rig review

User explicitly accepts the white-body proportions and authorizes the next stage. Current sequence is approved body -> skeleton/weights/joint checks -> clothing -> formal animation. Preserve task IDs: execute M5.2.9.5 now; do not renumber to match the changed order. Previous dressed/walk pilot is a reference experiment, not acceptance of wardrobe or animation. No new clothing or walk production in this slice.

Rebuilt the supplied 53-bone game_engine rig directly on the complete approved body, with MPFB weights and preserve-volume deformation. All 13,380 visible vertices have nonzero deform weights (sums 0.999900-1.000000). Static shoulder, elbow, hip/knee and wrist/ankle checks saved at frames 1/10/20/30/40. Upper-body checks leave foot bone positions unchanged. Inspected elbow and hip/knee side renders; full extreme-pose, hand and engine linear-skinning validation remains pending. Skeleton projection is a 2D annotation of actual bone coordinates, not extra geometry. See .local/mpfb-pilot/body-rig-review/standard-body-rig-review.blend and rig-review-overview.png. M5.2.9.5 initial technical binding completed; visual acceptance pending. Original body file preserved.

### 2026-10-12 — M5.2.9.6.1-M5.2.9.6.4 first-pass delivery

Rig audit passes (53 bones, 13,380 weighted visible vertices, mirrored rest joints, no zero-length bones). Created ten white-body clips: Idle, Walk, TurnLeft/Right, Run, Jump, AttackLeft/Right, HitLight and five-step HitHeavy. Corrected unreachable running targets, NLA time origin, Godot optimizer drift, arm bend-plane twisting and bounded shoulder weights. Approved body geometry and original rig source preserved.

All source motion-intent checks and every-frame imported ankle comparisons pass; maximum Godot ankle difference about 0.00000231 m. Actual GPU capture completed with empty error log. Initial sandbox editor/log path warnings remain environmental. Idle markers stay fixed; Walk/Run support markers match configured travel speeds; turn endpoints +/-90 degrees; jump peak root height 0.339 m; light one-step root retreat 0.08 m; heavy five lifts/root retreat 1.08 m.

Deliverables are ignored under .local/mpfb-pilot/action-set-v1: editable Blender source, ten-clip GLB, selectable Godot review, GIFs and phase sheets. See production/pixel-rpg/body-action-set.md. This completes the requested first-pass action coverage and technical preview, not final artistic animation acceptance or the broader sprite milestone. Shoulder silhouette, finger pose, foot roll/pivots, impact strength, transitions and gameplay integration remain refinement items. No clothing expansion, sprite batch, resource commit or push.

## 2026-10-12 — M5.2.9.2.1 proportion candidate

Built a reversible 6.25-head shape-key study from the original MPFB body; preserved source SHA256 and 13,380 visible vertices. Rendered front/side/back/three-quarter/top-down views and original/new comparison. Inspected front and side: lighter waist/torso and enlarged head; facial anatomy still realistic and provisional. New static body is not rigged; original ten-action delivery unaffected. Code and documentation only are eligible for checkpoint; outputs stay ignored. No push.

## 2026-10-12 — M5.2.9.2.2 manga face refinement

Created separate facial shape key and neutral eyeballs on the stylized body. Iterated eye depth and centerline continuity, then applied the user's lower-forehead/short-chin/large-eye/tapered-face direction. Final local candidate stylized-face-v4; prior trials retained. Source preserved, 13,380 body vertices retained; neck-down coordinates unchanged. Rendered matched before/after front, side, three-quarter and full body. Static appearance review pending; existing action set unchanged. Source/docs checkpoint only; no push.

## 2026-10-12 — M5.2.9.2.2 rejected; pre-face appearance restored

User rejected the manga face as unnatural and requested the before appearance. M5.2.9.2.2 is rejected/superseded, not awaiting approval. Current editable body: `.local/mpfb-pilot/restored-body/current-base-body.blend`, with Manga_face=0 and Manga_6_25_heads=1. Neutral test eyes retained to match the before comparison; no new facial deformation active. The original proportion-only file remains `.local/mpfb-pilot/stylized-body-v1/stylized-base-body.blend`. Prior face trials retained as inactive experiments. Do not continue facial stylization without a new user request.

## 2026-10-12 — M5.2.9.6.5 action adaptation delivery

Mapped 13,380 original body vertices exactly, fitted 53 bones to the approved proportion map, joined white eyes with head weights. All 16,360 resulting vertices weighted. Added arm-chain target scaling and reach verification after discovering 1.89 cm unreachable walk targets; corrected v2 passes all ten motion checks. Godot maximum every-frame ankle error 0.000000761 m. Captured 318 frames with success marker and empty stderr; inspected overview and action phases. Current artifact root .local/mpfb-pilot/restored-body-actions-v2; v1 preserved as intermediate only. Source hashes unchanged; rejected face disabled. Shoulder volume, finger grips and foot roll remain first-pass limitations. Source/docs checkpoint only, no push.

## 2026-10-12 — M5.2.9.6.6 Quaternius trial

Downloaded author's free Standard ZIP; bundled CC0 license verified. Actual inventory 43 clips, 65 bones. Compared with our MPFB-based 53-bone rig: complete main-joint mapping, twelve extra terminal bones, T/A rest-pose and proportion differences. Retargeted four clips, preserving seconds and source foot-height trajectory with vertical compensation. Fixed auxiliary render object visibility and Loop-suffix import naming after first failed trial. v2 Godot max ankle error 0.000001456 m; actual GPU capture successful with empty stderr; overview and sword phases inspected. Sprint/sword staging noticeably stronger, target shoulder/waist weights and horizontal contacts still need work. No purchase, full library migration or push.

## 2026-10-12 — M5.2.9.6.7 animation methodology and video research

Recorded user-requested methodology and investigated video-to-motion using official MediaPipe, FreeMoCap and GVHMR sources. Distinguished landmark tracking, monocular motion inference and calibrated multi-camera reconstruction. Identified GVHMR commercial restriction and FreeMoCap minimum two-camera recommendation for reliable 3D. Proposed library-plus-capture acquisition feeding the current standard rig. Documentation only; no installation, benchmark, generated assets or push. Existing unrelated environment edits preserved.

## 2026-10-12 — M5.2.9.6.8 expanded adaptation

Extended existing retarget tool with an optional ten-source-clip mode and preserved four prior turn/hit drafts in one Godot review. Added scrolling controls and multi-row overview generation. Source hashes unchanged; all 14 imported clips pass ankle comparisons, max 0.000001456 m. Actual GPU capture completed with empty stderr; 14 GIFs and phase sheets generated and inspected representative frames. Technical adaptation complete; foot/skin polish, transitions and gameplay jump remain pending. No generated assets staged, no push.

## 2026-10-12 — M5.2.9.6.9 heavy-hit revision

After checkpoint 8a10270 for expanded Quaternius adaptation, implemented user-requested lateral loss of balance and exactly two recovery steps. Separate non-destructive build script, new stagger-v1 output. Source hash unchanged; other 13 clips preserved. Lift/contact/reach assertions and all Godot import checks pass; actual capture and phase review complete. Draft delivered for visual review, no push.

## 2026-10-12 — M5.2.9.6.9 deepen stagger leg flexion

Increased impact/footfall pelvis compression and added a small backward hip shift at user request. Saved stagger-v2 independently, preserving v1. Two-step/contact/reach and Godot import checks pass; unchanged thirteen other clips verified. Actual capture and phase-sheet review complete. No asset staging or push.

### 2026-10-12 — M5.2.9.6.9 standalone Windows preview

Exported the current stagger-v2 Godot review to builds/body-action-review/body-action-review.exe (110,763,784 bytes), using the existing local Windows release template, embedded PCK, actions.json inclusion and capture/report exclusion. Local export preset is retained in stagger-v2/godot-demo/export_presets.cfg. No Godot installation is needed to run the EXE. Actual OpenGL GPU startup smoke test with --quit-after 120 exited 0 with no logged errors. This is a startup test, not a new full visual acceptance. EXE remains local/ignored; no push.

## 2026-10-12 — M5.2.9.6.10 walk shoulder correction

Diagnosed walk shoulder prominence using isolated clavicle/twist comparisons. Reduced walk-only clavicle rotation, preserved mesh, weights and other clips. Godot checks/capture and standalone EXE smoke test pass. Delivered separate shoulder-v1 output and body-action-review-shoulder.exe; earlier files preserved. No push.

## 2026-10-12 — M5.2.9.6.11 walk arm correction

User identifies hand penetration introduced by shoulder-only correction. Re-authored walk arms as natural hanging pendulums, replaced adaptive lateral offsets with constant clearance in arms-v2, retained relaxed clavicles. Sampled hand-envelope separation >=0.023716 m, Godot validation/capture and standalone EXE smoke test pass. Other thirteen clips preserved. Delivered body-action-review-natural-arms.exe; source and previous artifacts preserved. No push.

## 2026-10-12 — M5.2.9.6.11 three walk posture refinements

Implemented soft finger curl, approximately 2-degree torso lean and 35-degree elbows at user request. Preserved side clearance and other thirteen clips. Godot capture/import, posture assertions, closeup review and standalone EXE startup pass. Current output arms-v3 / body-action-review-relaxed-walk.exe. No push.

## 2026-10-13 — M5.2.9.6.12 hand poses and reusable orbit skill

Created independent Relaxed/Fist finger assets and integrated Relaxed with walking. Eight-view inspection exposed the incorrect fixed world-axis curl assumption. The user rejected the procedural thumb; replaced Fist with the existing sword right-hand grip and anatomical mirroring to the left. Current output hands-v13; earlier trials preserved.

Verified exact isolation of other motion, mesh/weights unchanged, 30 channels per pose, sword-reference match, all-frame relaxed pose application, 12.1 mm minimum sampled lateral envelope clearance, 16 Godot clips and actual GPU capture. Inspected both fist hands around 360 degrees, unchanged relaxed hands and two walk extremes. Exported body-action-review-hand-poses.exe and startup exited 0. Visual acceptance remains pending; sword grip is not a tight boxing fist.

Solidified blender-orbit-review (Python rendering, eight angles, contact sheet, manifest, read-only source handling) in E:/projects/skills and installed its matching local copy. Skill validation passed; separate skill commit d9b191c. User requested commits after completion; no push and no generated assets staged.
