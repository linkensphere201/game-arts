# Godot MVP Execution Record

Date: 2026-10-04. Tasks: M3.1.1, M3.1.2, M3.2.1, M3.2.2, M3.3.1, M3.3.2.

## Plan

Follow the six ordered steps in [active tasks](../tasks/active.md). The user's current request authorizes implementation and prioritizes Godot; the 2026-10-03 research-only and simultaneous dual-engine requirements no longer gate this MVP. Unity remains deferred.

## Inputs and Output Layout

- Text and sprite contract: [brief.json](brief.json).
- Reusable Godot resource source: `assets/ember-imp/`.
- Demo project: `demo/` (pending creation).
- Validation evidence: `validation/`.
- Local tools/models/logs: ignored `.local/`; Windows builds: ignored `builds/`.

## Current Evidence

- NVIDIA query: RTX 5060 Laptop GPU, 8151 MiB VRAM, driver 592.27.
- E: volume had approximately 120 GiB free at setup start.
- Portable Godot 4.7.2 and ComfyUI v0.38.0 are being downloaded from official GitHub releases.
- SDXL checkpoint and Pixel Art XL LoRA are being downloaded from author repositories at pinned revisions; checksums will be verified.
- No successful inference, finished character, or Godot playback has been claimed at this checkpoint.

## Local Resource Locations

Recorded on 2026-10-04 for `M3.1.1` / `M3.1.2`. All project-managed tool and model downloads are stored inside `E:\projects\game-arts\.local\`; they are not system-wide installations.

| Content | Absolute location | Purpose / status at recording |
|---|---|---|
| Downloaded archives and checksum metadata | `E:\projects\game-arts\.local\downloads\` | Godot ZIP, ComfyUI 7z, Godot export-template TPZ and checksums; completed and verified |
| Godot executable | `E:\projects\game-arts\.local\godot\Godot_v4.7.2-stable_win64.exe` | Extracted and verified; console companion used for automated checks |
| ComfyUI portable environment | `E:\projects\game-arts\.local\comfy\ComfyUI_windows_portable\` | Extraction destination; includes its own Python environment |
| Model weights and pinned source metadata | `E:\projects\game-arts\.local\models\` | Verified SDXL/Pixel Art XL retained from unsuccessful trials; verified DreamShaper 8 is the working model |
| Windows export templates | `E:\projects\game-arts\.local\export-templates\templates\` | Extraction destination for matching Windows debug/release templates |
| Background task metadata and logs | `E:\projects\game-arts\.local\runs\` | `setup`, `models`, and `templates` task JSON plus stdout/stderr logs |
| Temporary engine calibration | `E:\projects\game-arts\.local\calibration\` | Known test image and actual Godot-rendered calibration capture; not final character art |
| Final reusable character assets | `E:\projects\game-arts\assets\ember-imp\` | Delivered reusable asset source folder |
| Godot demonstration project | `E:\projects\game-arts\demo\` | Delivered project that imports the character asset |
| Standalone exported builds | `E:\projects\game-arts\builds\` | Windows executable and delivery ZIPs, completed and checked |

The root `.gitignore` excludes `.local/`, `builds/`, Godot import caches and Python bytecode. Large archives, weights and portable runtimes are not staged or pushed. Tracked `tools/` scripts describe setup, and `production/` records the brief and provenance. Git source assets and documentation are separate from local runtime/download storage.

Keep completed archives until explicitly authorized to remove them. Download completion must be followed by checksum validation; a file or directory existing does not mean the environment is ready. No project-managed downloads have been placed in Windows or Program Files directories.

## Environment Checkpoint

- Godot 4.7.2 executable and matching Windows templates verified against official SHA-512 sums.
- ComfyUI v0.38.0 NVIDIA archive verified against official release SHA-256: `8f137eac345707fd7e42bcf8e29377415243011ca15522a86aed6c77331fbd56`.
- Embedded Python 3.13.14, PyTorch 2.14.0+cu130, CUDA 13.0. A CUDA matrix multiplication completed with finite results on capability 12.0; system RAM is approximately 31.64 GiB.
- ComfyUI listens only on `127.0.0.1:8188`, with low-VRAM mode, FP32 VAE and custom nodes disabled. Large models have not yet finished downloading at this checkpoint.
- Godot imported the two calibration strips, visited all ten animation frames, rendered a capture, exported a Windows executable and passed playback checks in that executable.
- The demo currently displays `CALIBRATION ONLY`; it is an environment fixture, not the finished asset. Preview evidence is in ignored `.local/calibration/`.
- Background scripts initially used Windows PowerShell and failed at unavailable `Get-FileHash`. Completed downloads were preserved and checked with PowerShell 7; setup scripts now explicitly require version 7. No assets were inferred from unchecked weights.

## Finished Character and Reproduction

The working route is DreamShaper 8 at 512x512, traditional ComfyUI low-VRAM mode, no SDXL LoRA. SDXL attempts failed on this configuration; see [failure record](experiments/README.md). All eight successful candidate PNGs are retained in `candidates/`, and their exact prompts, seeds, runtime flags and elapsed times are in `runs/`.

Selected seed: **420052**. Original image: `candidates/ember_imp_420052_00001_.png`. Final character: `../assets/ember-imp/`. The draft was chosen for a readable two-legged demon silhouette. The final version has large shaded ivory horns, a three-quarter ready stance and no distinct tail detail at 64x64; it does not match every initial descriptive default.

Local postprocessing removes the background and floor, downsamples to the final grid, reduces the palette and fixes the canvas. Art-directed edits highlight horns/eyes and redraw legs; manually specified poses produce idle/walk strips. These are human-designed edits expressed in scripts, not generated animation frames. This distinction is essential to the feasibility result.

### Replay This Specific Asset

Use PowerShell 7 for setup scripts. Commands below are relative to the repository root. The `.local` runtime must already be present; setup scripts retain downloaded archives and verify hashes.

```powershell
& tools/setup-local.ps1
& tools/download-models.ps1
& tools/download-templates.ps1
& tools/start-local.ps1
python tools/generate-character.py --seed 420052 --count 1
```

`generate-character.py` reads `production/brief.json`; `--prompt "description"` can override its positive prompt. Default model is the smaller DreamShaper checkpoint. `download-models.ps1 -IncludeSDXL` also fetches the unsuccessful SDXL trial's weights, which are not necessary for the working MVP. Repeated seed records get unique filenames.

For the retained selected draft, the local embedded Python can reproduce the exact postprocessing and packaging:

```powershell
$assetPython = '.local/comfy/ComfyUI_windows_portable/python_embeded/python.exe'
& $assetPython -s tools/prepare-sprite.py production/candidates/ember_imp_420052_00001_.png production/selected
& $assetPython -s tools/animate-sprite.py
& $assetPython -s tools/package_asset.py assets/ember-imp
Copy-Item assets/ember-imp/idle.png,assets/ember-imp/walk.png,assets/ember-imp/ember_imp.tscn,assets/ember-imp/ember_imp_frames.tres,assets/ember-imp/character.json demo/ember_imp/ -Force
& $assetPython -s tools/validate-assets.py
```

A different generated character needs fresh selection, segmentation review and pose/art adjustments; the scripts are a documented single-asset MVP, not a proven general text-to-animation product. The authoring pose data is also recorded in `animation-poses.json`.

### Measured Generation Result

- Eight successful 512x512 candidates: first approximately 8.12 seconds; remaining approximately 4.06-4.18 seconds each, as measured by the local client including queue/poll overhead.
- Sampled peak total GPU memory usage reached 3248 MiB. This is device-wide `nvidia-smi` sampling including other GPU use, not isolated model allocation or guaranteed peak capture.
- Model loading, prompt iteration, rejected candidates and manual/scripted art work are additional costs. Full end-to-end labor time has not been instrumented, so these generation times are not delivery-time or profitability estimates.
- Five unsuccessful SDXL setup attempts preceded the working route. The experimental loader was restored; the working configuration uses the original portable loader and disables dynamic VRAM, asynchronous offload and pinned memory.

The new model's pinned source metadata is `DreamShaper_8_pruned.safetensors.source.json`; author repository: https://huggingface.co/Lykon/DreamShaper . Upstream licensing and marketplace acceptance were not cleared by this MVP. No model weights are redistributed in the asset package.

## Session Finish

The generation server was stopped after validation to release local GPU/RAM. Restart it with `tools/start-local.ps1` when generating again; the finished Godot asset/demo does not depend on it. The final Windows demo was opened for user review. No Git push was performed.

## Browser Workflow / Missing Models (M3.3.3)

The MVP uses **DreamShaper_8_pruned.safetensors**. A ComfyUI template requesting `qwen_3_4b.safetensors` and `z_image_turbo_bf16.safetensors` is a different Z-Image workflow. Do not download those approximately 18.96 GB of weights to reproduce this MVP. Replacing just one loader field is insufficient because the architectures use different nodes.

1. In PowerShell 7, run `& E:\projects\game-arts\tools\start-local.ps1`.
2. Open `http://127.0.0.1:8188` in a browser.
3. Select **Workflows / 工作流**, click **Refresh / 刷新**, then open **Ember Imp - DreamShaper 8**.
4. Click **Run / 运行**. This generates a 512x512 character draft, not the finished animated Godot asset. Pixel cleanup and animation remain the separate recorded steps above.

The portable UI workflow is [workflows/ember-imp-dreamshaper.json](workflows/ember-imp-dreamshaper.json). It can also be opened through ComfyUI's workflow file menu. The launcher installs it under `.local/comfy/ComfyUI_windows_portable/ComfyUI/user/default/workflows/` if absent, preserving existing user edits. The model stays in `.local/models/` via `extra_model_paths.yaml`; output drafts are in `.local/comfy/ComfyUI_windows_portable/ComfyUI/output/`.

A missing-model dialog identifies dependencies of the currently opened workflow; it does not mean the delivered Godot executable needs models. The original MVP supplied an API generation script but omitted a matching browser workflow; this follow-up closes that handoff gap.

## 2026-10-04 M3.3.3: Memory Failure Diagnosis

Windows Resource-Exhaustion-Detector event 2004 coincided with all five retained failed inference attempts (21:13-21:18 local time). At 21:18:47, system commit was 33,768,124,416 / 33,970,786,304 bytes (99.40%), although physical memory usage was only 23,936,012,288 bytes. No active page file was reported. See [sanitized counters](../validation/memory-diagnosis.json). Full local events and experiment stderr logs are retained under `.local/runs/`.

This establishes system commit exhaustion during failed loading. It does not establish that every access violation or Chrome software exception has the same cause; no matching Chrome crash record or exact exception code was obtained. The checkpoint SHA-256 still matches the pinned source. Changing mmap mode, forcing FP16 and testing safetensors pread did not resolve the failures. Those experimental defaults have been withdrawn; third-party packages are unchanged.

The launcher now checks Windows available commit before importing PyTorch. It stops with actionable guidance below a conservative 10 GiB launch budget (observed Python commit around 7 GiB plus headroom). This budget is not a universal minimum or a guarantee against later allocation failure. Closing unused apps after saving work, or enabling a Windows system-managed page file, can provide more commit headroom. No user applications were closed and no Windows settings were changed. Current generation remains blocked pending adequate headroom; no successful repaired inference is claimed.

Reference: [Microsoft guidance on event 2004 and commit exhaustion](https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/troubleshoot-application-service-memory-leaks).

## 2026-10-04 M3.3.3 Recovery Verified

After the user's page-file change and restart, `C:/pagefile.sys` was active with 2048 MiB allocated. Available commit before launch was 21.87 GiB; reduced background usage also contributed, so the result is not attributed solely to the page file. Original ComfyUI entry point, model and precision settings were retained. The preflight is a separate check; no package monkeypatch is active.

Cold seed 420052 generation completed in 8.1 seconds including client polling. Its 512x512 RGB pixels exactly match the selected original. The browser restored the named DreamShaper workflow without a missing-model dialog; clicking Run also completed successfully using cached computation. See [recovery evidence](../validation/memory-recovery.json), [browser history](../validation/browser-recovery.json), and [page screenshot](../validation/comfy-recovered.png). Startup memory-gate boundary checks (6.5/10/21 GiB), Python compilation and PowerShell parsing passed. The server is left running for user review. Chrome-specific recovery has not been independently verified; the browser check used the in-app browser.
