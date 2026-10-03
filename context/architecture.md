# Architecture and Minimum Validation Proposal

Research date: 2026-10-03. Tasks: `M2.2.1`-`M2.2.3`. Status: researched proposal, not implemented or benchmarked. Defaults below are recommendations, not approved asset specifications.

## Confirmed Requirements

- Generate game art using a local GPU; mandatory hosted inference is excluded (`M2.1.4`).
- Stage 1 produces a usable finished asset; Stage 2 formalizes a workflow only after effectiveness is demonstrated (`M2.1.5`).
- Target pixel-art characters such as a demon, with assets usable in both Godot and Unity. Both engines are required; one does not substitute for the other.
- This request authorizes research and documentation only. No installation, model download, asset generation, or engine project creation is part of this slice.

## Recommended Minimum Experiment

Produce one original side-view demon with two looping animations, and import the same PNG content into two independent engine fixtures. First validate the fixtures with a simple calibration sprite, so generation failures can be distinguished from import/rendering failures.

| Proposed specification | Value |
|---|---|
| Character/view | One demon, right-facing side view; perspective still requires selection |
| Final cell | 64 x 64 pixels, transparent RGBA PNG |
| Animation | Idle: 4 frames; walk: 6 frames; 8 FPS, looping |
| Sheets | idle.png: 256 x 64; walk.png: 384 x 64; no spacing or trimming |
| Timing | 125 ms per frame; idle loop 0.5 s, walk loop 0.75 s |
| Anchor | Fixed canvas coordinate (32, 56), measured from top-left; keep all frames on this canvas |
| Pixel style | Proposed maximum 32 opaque colors across the character; binary alpha; manually cleaned edges |
| Presentation | Native scale and integer 4x scale, nearest-neighbor filtering |
| Deferred | Attack, death, eight directions, combat logic, automatic rigging, training, marketplace publication |

The anchor is a shared origin, not a requirement that every foot stays motionless. Deliberate animation motion must be distinguished from accidental frame displacement. Mirroring is optional and only acceptable if asymmetric equipment and anatomy permit it.

## Local Tool and Model Candidates

Previously observed during the conversation: NVIDIA GeForce RTX 5060 Laptop GPU, 8151 MiB VRAM, driver 592.27. This is hardware inventory evidence, not a successful model run. Available RAM, disk capacity, installed engines, Python/PyTorch environment, and licenses remain unverified.

Proposed baseline: ComfyUI Windows Portable, SDXL base 1.0 plus Pixel Art XL LoRA, and Pixelorama for frame editing. Aseprite is an alternative if already available or separately selected. ComfyUI can be used as a local generation interface during Stage 1 without making a reusable workflow product the deliverable. Its portable package isolates its Python environment [T5].

Use batch size 1, initially without Refiner, ControlNet, or video modules. Test suitable generation resolutions such as 512 and 1024 separately; final cell resolution is a different property. CPU offloading may make a model fit but needs RAM and may reduce throughput. No exact VRAM fit or seconds-per-image claim is made for this laptop.

RTX 50-series compatibility must be checked against the actual packaged PyTorch/CUDA build. A new driver alone does not prove support. Do not blindly reuse older CUDA installation recipes; first verify device detection, a real CUDA tensor operation, and a small inference. Pin the successful environment rather than upgrading components independently [T6].

| Route | Local candidate/process | Strength | Main uncertainty | Recommendation |
|---|---|---|---|---|
| A: draft then pixel animation | SDXL + nerijs/pixel-art-xl; select one character, clean it, manually author short animations | Small dependency set; direct control over final pixels | Manual art effort and quality on this GPU are unknown | First baseline |
| B: direct sprite-sheet generation | Onodofthenorth/SD_PixelArt_SpriteSheet_Generator; repair and slice output | Specialized sprite-sheet candidate | Author still describes img2img adjustments, consistency work, background removal and resizing; does not establish reliable action cycles | Bounded comparison, not assumed automation |
| C: guided frame generation | Approved reference + img2img/inpaint; optional compatible ControlNet pose/silhouette guides | More control over composition and pose | Nonhuman horns/tails and small limbs may drift; added memory/dependencies | Try if baseline manual effort is excessive |
| D: video to sprites | AnimateDiff, extract frames, remove background and clean | Can explore motion | Temporal artifacts, camera motion, inconsistent pixel grid, resource use and cleanup | Defer from minimum experiment |

Sources: model cards [T7-T9], Comfy tutorials [T10-T11], AnimateDiff repository [T12]. Route rankings are project judgments, not measured comparisons. A fixed seed helps controlled comparisons but does not guarantee character identity across poses. ControlNet and LoRA must match the base-model family.

## Text to Deliverable Process

1. Convert the user's description into a short explicit brief: silhouette, horns/tail, clothing, palette, viewpoint, final cell size, animation list, timing and intended engine versions. A local language model is unnecessary for this first trial; a human can structure the brief.
2. Generate a bounded set of static concepts locally. Save prompt, negative prompt, seed, sampler, steps, guidance, resolution, model/LoRA/VAE identifiers and hashes. Select for readability at final pixel size, not just appearance when enlarged.
3. Establish one canonical character frame. Remove background locally or manually, clean alpha, reduce/repair colors and pixel clusters, and align the fixed canvas. An AI-rendered checkerboard is not transparency. Nearest-neighbor reduction alone does not guarantee good pixel art.
4. Build idle and walk frames from the canonical design. Baseline uses manual pixel editing; optional local guided generation supplies rough poses. Check anatomy, accessories, outline, lighting and color consistency frame by frame. Record all manual time.
5. Export untrimmed PNG strips and individual frames, plus a manifest containing frame rectangles, animation names, frame order, durations, loop flags and anchor convention. Aseprite can export PNG and JSON; editor export schemas need mapping to the agreed manifest [T13].
6. Configure engine-native animation resources from this common source. The manifest is a proposed interchange contract; neither engine is assumed to consume it automatically. Manual setup is acceptable in Stage 1.
7. Validate editor playback, independent Windows builds, and import into fresh projects of the pinned engine versions. Save screenshots/short recordings and build/import logs.

## Verifiable Engine Environments

| Concern | Godot fixture | Unity fixture |
|---|---|---|
| Proposed baseline | Stable Godot 4.x Windows standard edition, GDScript, Compatibility renderer; pin exact patch at setup | Unity 6.3 LTS via Hub, pin exact patch; 2D Built-in Render Pipeline project [T3] |
| Required setup | Matching export templates for Windows desktop | Editor, usable license/account state, and required Windows build support for selected scripting backend |
| Animation representation | AnimatedSprite2D with SpriteFrames; atlas regions or individual frames [T1] | SpriteRenderer with AnimationClips and Animator; reusable prefab |
| Import | Nearest texture filtering; fixed frame rectangles; consistent anchor [T2] | Sprite (2D and UI), Multiple, fixed-cell slicing; Point filter, no compression/mipmaps, Full Rect mesh; proposed 64 pixels per unit [T4] |
| Pixel display | Integer viewport scaling and stable camera | Integer orthographic display; optional compatible 2D Pixel Perfect package for Built-in pipeline |
| Anchor mapping | Preserve frame canvas and set sprite offset so common anchor is node origin | Convert top-left pixel anchor to Unity normalized bottom-left pivot: (0.5, 0.125), under the stated coordinate convention |
| Deliverable | Small source project and reusable character scene/resources; Windows export | Small source project and character prefab/clips/controller; Windows standalone build |
| Reproducibility | Engine patch, renderer, project settings, export preset, source assets and hashes | ProjectVersion.txt, Packages manifest/lock, ProjectSettings, Assets and .meta files |

Do not mix Built-in and URP Pixel Perfect setup instructions: Unity documents different package arrangements [T14]. Native engine resources differ even though their source PNG hashes should match. GPU inference and engine testing can run sequentially to reduce competition for laptop VRAM.

Each fixture should show the same character, a ground/anchor marker, current animation and FPS, idle/walk switching, native/4x views, and black/white/checker backgrounds. A calibration strip with numbered frames and known transparent edges should establish frame order, timing, pivot and filtering before the generated art is used. Input or buttons can switch animation; a full game or combat controller is unnecessary.

The verification package is more than a screenshot: retain editable projects, engine-native reusable resources, source PNGs, import instructions, and a runnable build. Exclude generated engine caches, large model weights and local build outputs from normal source commits when implementation begins.

## Planned Gates and Evidence

All rows below are NOT RUN. They define future checks, not results.

| Gate / task | Check | Evidence required to pass |
|---|---|---|
| E0 / M3.1.1 | Local hardware/runtime and exact versions | Device and CUDA checks, small inference, versions, memory and disk inventory; no hosted inference |
| E1 / M3.1.2 | Godot calibration | Correct frames, timing, alpha and integer rendering in editor and Windows export; no relevant errors |
| E1 / M3.1.3 | Unity calibration | Same checks in editor and Windows build; required packages/license state verified |
| E2 / M3.2.1 | Static character approval | Readable final-size silhouette, complete anatomy, clean transparency and agreed palette |
| E3 / M3.2.2 | Animation and packaging | 4 idle + 6 walk frames, correct order/durations, stable identity and anchor, no unintended clipping or visible loop jump |
| E4 / M3.3.1 | Both-engine fresh import | Matching common-source hashes, reusable native resources import into fresh projects, both builds run and switch animation for at least 60 seconds |
| E5 / M3.3.2 | Effectiveness review | Human quality judgment plus generation/cleanup/integration effort and reproducibility evidence; explicit go/revise/stop finding |

Machine checks can verify dimensions, RGBA, frame counts, bounds, timings and file integrity. Human review must judge design readability, anatomy, motion and consistency. Neither layer alone establishes usable quality.

Record cold load separately from warm inference, peak VRAM, generation parameters, attempted/accepted candidates, failures, generation time, manual cleanup/animation time, engine-integration time and reviewer findings. Performance thresholds remain open; do not claim profitability or market demand from this technical experiment.

Suggested bounded trial: up to 8 initial concepts for route A; if necessary compare up to 8 for route B. Review after two correction rounds instead of generating indefinitely. This is a proposed effort cap, not a measured success rate. If a static character fails, pause before animation. If engines pass but art fails, revise art; if both pass but effort is excessive, evaluate route C before Stage 2.

## Delivery Contract and Remaining Decisions

Proposed output package: brief, canonical frame, idle/walk PNG strips, individual frames, manifest, editable pixel source, generation provenance, Godot scene/resources, Unity prefab/animations, demo projects, validation record and import README. Technical usability here covers sprite animation integration, not combat behavior, collision design or universal engine-version compatibility.

Before execution select perspective, final cell size, acceptable manual work, time budget, exact engine patches and editor. Retain model/LoRA/base-model license records and input provenance; model-card tags alone are not a completed commercial-rights review. No commercial clearance is asserted in this research.

Proceed to M4 only after M3 produces an accepted asset in both engines with acceptable measured effort. M4 can then automate the steps that proved useful; generalized UI, batch production and model training are outside this proposal.

Sources and evidence limits: [Research notes](research-notes.md#technical-research-2026-10-03).
