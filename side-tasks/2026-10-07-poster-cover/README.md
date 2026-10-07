# Poster and Cover Generation

Created 2026-10-07 inside game-arts. Namespace: `poster-cover`. Current scope: local Klein validation delivered on 2026-10-08; full layered poster implementation and API remain deferred.

## Verified local installation — M2.3

- FLUX.2 Klein 4B distilled FP8 transformer: 4,070,624,520 bytes.
- Comfy-Org Qwen3 4B FP4 text encoder: 3,848,213,998 bytes.
- Flux2 Comfy VAE: 336,211,292 bytes.
- Total: 8,255,049,810 bytes (8.26 GB / 7.69 GiB), excluding existing runtime and outputs. All three SHA256 values match pinned upstream LFS metadata.
- Runtime: existing ComfyUI 0.38.0 at http://127.0.0.1:8189, PyTorch 2.14.0+cu130, RTX 5060 Laptop (8151 MiB). No new Python packages or ComfyUI updates were needed.

| Test | Size | Wall time | Sampled device VRAM peak | Minimum available Windows commit | Result |
|---|---|---|---|---|---|
| First generation, orange lemonade | 768x1024 | 70.2 s | 7859 MiB | 0.36 GiB | Completed; insufficient operating margin for a default |
| Reference edit, strawberry lemonade | 576x768 | 22.9 s | 4659 MiB | 4.53 GiB | Completed, substantial scene/layout preservation |
| Lower-resolution generation | 576x768 | 20.9 s | 4405 MiB | 2.40 GiB | Completed; saved as default |

All cases used 4 Euler steps, Flux2Scheduler, seed 20261008, batch 1, guidance 1 equivalent via BasicGuider, and tiled VAE decode. Reported wall time starts at queue submission; excludes file hashing. GPU/commit readings were sampled approximately every 2 seconds and are not guaranteed exact peaks. Later runs share a live runtime and warm filesystem; these are not controlled cold-vs-warm benchmarks. No full-precision quality comparison was run.

Visual inspection: both generation outputs contain a clear glass/product, coastal background and large clean upper-left headline space, without visible lettering. The edit changes orange slices/juice to strawberries/pink juice while broadly preserving the pedestal, horizon and glass placement. Pink saturation is strong, and scene pixels are not locked. This demonstrates generation and semantic editing for one brief, not commercial acceptance or automatic layout.

## Files and use

All absolute locations start at `E:/projects/game-arts/`:

- Transformer: `.local/reference-comfy/models/diffusion_models/flux-2-klein-4b-fp8.safetensors`
- Text encoder: `.local/reference-comfy/models/text_encoders/qwen_3_4b_fp4_flux2.safetensors`
- VAE: `.local/reference-comfy/models/vae/flux2-vae.safetensors`
- Default browser workflow: `production/workflows/klein-poster-generate.json`
- Reference-edit workflow: `production/workflows/klein-poster-edit.json`
- Both workflows also copied to `.local/reference-comfy/user/default/workflows/`.
- Initial 768x1024 output / edit source: `.local/reference-comfy/output/poster_klein/base_00001_.png`
- Reference edit: `.local/reference-comfy/output/poster_klein/edit_00001_.png`
- Default-size generation: `.local/reference-comfy/output/poster_klein/base_00002_.png`
- Copied edit input: `.local/reference-comfy/input/klein-reference-<content hash>.png`; exact filename stored in edit workflow.
- Test reports: `.local/runs/klein-poster-*-20261008-*.json`; API graphs: `.local/runs/klein-poster-*-api.json`.
- Pinned download provenance: `tools/klein-models.json`; component-adjacent `.source.json` files.

Open ComfyUI and load the workflow JSON. Edit the CLIPTextEncode prompt; in the edit workflow, select a reference in LoadImage. Default is 576x768. Other aspect ratios, large images and multi-reference jobs remain untested. ImageScale in the edit workflow fits to the target dimensions; choose matching aspect ratios to avoid stretching.

Reproduce using the project portable Python:

```powershell
& .local/comfy/ComfyUI_windows_portable/python_embeded/python.exe tools/test-klein-model.py generate
& .local/comfy/ComfyUI_windows_portable/python_embeded/python.exe tools/test-klein-model.py edit --input .local/reference-comfy/output/poster_klein/base_00001_.png
```

The runner verifies all weights, requires an idle queue, frees idle cached models and checks the existing 10 GiB available-commit gate before loading. It requests interruption of its own job if available commit falls below 0.75 GiB; that is a best-effort guard, not a guarantee against OOM. It unloads models after completion. Direct browser execution does not invoke this external memory guard. No user processes were closed and no system page-file settings were changed.

## Scope and next stage

The user approved quantized download and validation, superseding the earlier existing-model-first research recommendation. No Z-Image weights were reinstalled. Model weights, reference PNGs and outputs stay local/ignored; only scripts, workflow recipes and documentation are versioned. No push was performed.

The four-stage proposal remains: visual composition -> background/core-element generation -> independent accurate text -> layer composition. Current outputs are flattened backgrounds; editable text, extracted subject layers and final poster composition are not implemented. Qwen3-4B is not a finalized layout choice. AnyText2 remains optional artistic-text research.

## Documents

- [Research](context/research-notes.md)
- [Architecture proposal](context/architecture.md)
- [Milestones](tasks/milestones.md)
- [Active status](tasks/active.md)
- [Decisions](tasks/decisions.md)

## 2026-10-08 — M2.4 SVG demo delivered

The user requested the next typography/composition demo. [Demo source and instructions](../../production/poster-demo/README.md): six editable SVG text layers and transparent PNGs over the unchanged Klein background; final PNG/SVG, layout and manifest. Local exports took approximately0.49s and0.24s, without GPU generation. Price29->19 changed1066 pixels inside the price masks only; other5 layers remained hash-identical. Chinese wrapping, overflow rejection and exact recomposition passed. Full SVG export visually inspected. This supersedes the earlier statement that text/composition are entirely unimplemented, but remains a manually laid-out demo, not full automation or API delivery.
