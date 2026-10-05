# MVP Validation Record

Date: 2026-10-04. Task IDs: M3.1.1, M3.1.2, M3.2.1, M3.2.2, M3.3.1, M3.3.2.

| Check | Result | Evidence |
|---|---|---|
| Actual local GPU inference | PASS using DreamShaper 8; SDXL failed | Production run JSON and model metadata; `working-environment.json` |
| Asset structure | PASS | `asset-checks.json`: dimensions, alpha, frame counts, palette, copy identity |
| Fresh project / relocated resource folder | PASS | `fresh-import.log`: both animations, timing, anchor, playback and pause |
| Demo behavior | PASS | `demo-controls.log`: buttons, pause, background, speed, movement, facing |
| Actual engine rendering | PASS, visually inspected | `godot-demo.png` |
| Windows standalone export/runtime | PASS, 60 seconds | `windows-runtime.log`; task metadata retained under `.local/runs/final-build.json` |
| Replaying selected text/seed in same local runtime | PASS, RGB pixels identical | `replay.json`; original and replay production records |
| Delivery archive integrity | PASS | `delivery-manifest.json`, CRC checked during packaging |

## Visual Assessment

The character is recognizable as a horned demon at native scale, has a stable silhouette and transparent background, and displays cleanly at integer scale. Idle has breathing/blink changes; walk uses six distinct hand-authored leg poses. This is a cutout prototype with restrained upper-body motion, not a fully redrawn professional walk cycle. A distinct tail was not retained at the final scale. User art-direction approval and commercial-readiness judgment remain pending.

The engine screenshot is actual Godot output. The GIF is generated from the delivered PNG strips, not a recording of the engine. Structural and timing checks do not prove aesthetic quality. The same-runtime replay does not establish determinism across machines or software versions.

## Environment Findings

Successful configuration: Godot 4.7.2 standard / OpenGL Compatibility; RTX 5060 Laptop 8151 MiB, driver 592.27; ComfyUI 0.38.0, embedded Python 3.13.14, PyTorch 2.14.0+cu130; DreamShaper 8 checkpoint at the recorded revision; traditional low-VRAM mode, dynamic VRAM/async offload/pinned memory disabled, FP32 VAE. No system pagefile change was made.

Eight successful candidate generations took approximately 8.12 seconds for the first and 4.06-4.18 seconds thereafter. Highest sampled total device memory was 3248 MiB; sampling includes other GPU activity and can miss shorter peaks. End-to-end labor time is not instrumented. See [production details](../production/README.md) and [failed SDXL experiments](../production/experiments/README.md).

Sandboxed early Godot runs logged certificate/cache access warnings. Final fresh-import, controls and standalone graphical checks ran with required local access and no such errors in the retained pass logs.
