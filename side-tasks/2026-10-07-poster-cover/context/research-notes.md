# Model Research — poster-cover/M1.1.1-M1.1.3

Checked2026-10-07 against primary model cards and official repositories. Separate evidence from local measurements and recommendations. No new models were installed or benchmarked in this research.

## Recommended order

1. Existing SDXL-family background generation/editing plus deterministic text rendering: lowest incremental download burden, known basic local inference.
2. Add one proven gap-filling component at a time: reference conditioning, structure control or foreground segmentation.
3. Trial FLUX.2 klein4B for instruction/multi-reference editing only after full-package size and quantized local feasibility are established.
4. Treat AnyText2 as optional lettering research; defer20B Qwen generation/editing/decomposition models on this8GB machine.

## Candidate matrix

| Candidate | Evidence and useful role | Local feasibility / limits | Decision |
|---|---|---|---|
| RealVisXL V5.0 (SDXL) | Official card targets photorealism; installed FP16 checkpoint is6.94GB. Useful for photographic backgrounds and subjects [S1]. | Prior local portrait success. Inpainting/reference extensions require separate tests. No guarantee of exact Chinese lettering or product identity. Card lists OpenRAIL++. | First photographic baseline; no new base checkpoint needed. |
| Animagine XL4.0 Opt (SDXL) | Official anime-focused generation/editing model; installed checkpoint6.94GB [S2]. | Prior local generation and ordinary masked edit succeeded. Poster layout and reference consistency remain untested. OpenRAIL++ card. | First illustrated-cover baseline. |
| Realistic Vision V6.0 B1 / existing DreamShaper8 | Already installed SD1.5 options; earlier local tests succeeded. | Lower-resolution fallback; not assumed superior to SDXL for final typography or composition. | Reuse for draft/low-resource comparison; no new download. |
| FLUX.2 klein4B | Official open weights unify generation, editing and multiple references; Apache2.0; card gives approximately13GB VRAM for the stated setup [S3]. |8GB is below that published figure. Quantization/offload is an experiment, not a proven local fit.4B describes the transformer, not total package size including encoder/VAE. | Most relevant new editing candidate, conditional on complete disk/RAM/VRAM estimate and one local trial. |
| AnyText2 | Official implementation supports multilingual visual text editing and per-line font/color control; README recommends at least8GB GPU [S4]. | At the machine's VRAM ceiling; current Comfy/Python compatibility untested. Use isolated dependencies. Generates visual text pixels, not inherently editable vector text. Repository Apache2.0; verify distributed checkpoint/dependency terms before API use. | Optional artistic lettering test, not mandatory for the first MVP. |
| Qwen-Image-Edit-2511 | Official20B, Apache2.0 image-editing model; reference consistency/material/light editing are relevant [S5]. | Full-precision raw transformer parameter estimate alone is approximately40GB (20B x2bytes), excluding encoder/VAE and overhead; not a measured package/VRAM requirement. Quantization still adds substantial storage and offload demands. | Defer for current8GB device; retain as higher-resource quality candidate. |
| Qwen-Image-2512 | Official generation model emphasizes text rendering and natural imagery [S6]. | Local-open-weight option, but not a lightweight default. In-image typography remains flattened pixels. | Future whole-poster quality benchmark, not the editable-text source of truth. |
| Qwen-Image-Layered | Official20B Apache2.0 model decomposes an image into multiple RGBA layers; example recommends640 bucket [S7]. | High resource cost and decomposition quality must be tested. Raster text pixels in a layer do not recover Unicode/font/kerning or native PSD text. | Relevant for imported flattened artwork later; not required when authoring layers separately from the start. |
| FLUX.1 Kontext dev | Official12B instruction-editing model [S8]. | Larger model; non-commercial weight license makes a future commercial self-hosted API a separate licensing decision. Do not conflate output rights with model-serving rights. | Lower priority than klein4B for this branch. |
| BiRefNet | Official local foreground segmentation/background removal weights; MIT card [S9]. | Helps produce alpha masks; not a generator or text editor. Fine hair/glass and device memory need testing. | Optional helper after a manual-mask baseline. |
| LayerDiffuse | Official transparency-generation project [S10]. | Transparent raster generation is different from an editable poster document. Integration and artifact edges remain to be checked. | Optional; avoid another dependency in the first slice. |

Z-Image stays excluded following the user's explicit size-based cancellation. Qwen-Image2.0 is announced in the project README, but the inspected announcement alone is not evidence of a downloadable local checkpoint; do not select an API-only announcement as a local deployment candidate [S11].

## What reference editing means

- Image-to-image: start from a supplied image; denoise strength trades preservation for change.
- Masked inpainting/outpainting: change a region or extend the canvas. Explicit compositing can preserve pixels outside the editable mask, except the declared feather boundary.
- IP-Adapter: appearance/style guidance from an image; it is not a pixel lock or a guarantee of identity.
- ControlNet: guide geometry/layout through edges/depth/pose. SD1.5 adapters cannot be assumed compatible with SDXL; match model family and encoder. Diffusers documents reference adapters combined with structural conditioning [S12].
- Instruction editors such as klein/Qwen: useful semantic editing, but repeated edits can still drift. For exact product packaging, brand marks or an approved portrait, keep the supplied foreground and regenerate only the background/shadow as separate layers.

## Separate text: preferred engineering route

Treat user copy as canonical UTF-8 strings. Generate layout parameters separately; render title/subtitle/callouts using approved local fonts, SVG text, and a pinned renderer. Export editable SVG+layout JSON and one transparent PNG per text layer. Ordinary text updates should require no GPU image generation and must preserve the underlying image hash. SVG supports actual text elements [S13].

Use AnyText2 only where textured/physical lettering is worth raster output and additional review. It cannot replace exact small-print/date/price rendering. A generative raster title should be labeled as such; preserve its underlying literal string as metadata and verify it visually/OCR. Do not describe an outlined SVG path or transparent PNG as editable font text.

## Hardware and commercial-readiness interpretation

Local deployment is not the same as fitting this GPU. Check all weight files, text encoders, VAE, adapters, cache/staging duplication, peak committed memory and latency. No promise of13GB-model operation in8GB based solely on4-bit parameter arithmetic. Start with a singleGPU job, use the established memory preflight, and measure cold/warm behavior. Do not reinstall Z-Image or download every listed candidate.

Model cards identify license families; production must pin exact versions and inspect checkpoint, adapter and font terms. In particular, an open code repository is not proof that every dependency/weight permits paid API serving. This is a technical shortlist, not a completed licensing clearance.

## Sources

- S1: [RealVisXL V5.0 official card](https://huggingface.co/SG161222/RealVisXL_V5.0)
- S2: [Animagine XL4.0 official card](https://huggingface.co/cagliostrolab/animagine-xl-4.0)
- S3: [FLUX.2 klein4B official card](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B)
- S4: [AnyText2 official implementation](https://github.com/tyxsspa/AnyText2), [environment specification](https://github.com/tyxsspa/AnyText2/blob/main/environment.yaml)
- S5: [Qwen-Image-Edit-2511 official card](https://huggingface.co/Qwen/Qwen-Image-Edit-2511)
- S6: [Qwen-Image-2512 official card](https://huggingface.co/Qwen/Qwen-Image-2512)
- S7: [Qwen-Image-Layered official card](https://huggingface.co/Qwen/Qwen-Image-Layered)
- S8: [Kontext official card](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev), [current license](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev/blob/main/LICENSE.md)
- S9: [BiRefNet official model card](https://huggingface.co/ZhengPeng7/BiRefNet)
- S10: [LayerDiffuse official project](https://github.com/lllyasviel/LayerDiffuse)
- S11: [Qwen-Image official release index](https://github.com/QwenLM/Qwen-Image)
- S12: [Diffusers IP-Adapter documentation](https://huggingface.co/docs/diffusers/main/using-diffusers/ip_adapter)
- S13: [SVG text documentation](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/text)
- S14: [ComfyUI HTTP/WebSocket routes](https://docs.comfy.org/development/comfyui-server/comms_routes)

Unknowns to resolve in the pilot: accepted visual style, reference fidelity, font coverage/export fidelity, current Windows integration for any new component, exact complete download budgets and measured peak resource usage. No timing from a vendor's differentGPU setup is adopted as a local estimate.

## 2026-10-08 — M2.3 local validation

User authorized downloading/testing Klein and explicitly preferred quantization. This supersedes the historical existing-model-first priority above. Official BFL FP8 distilled transformer plus Comfy-Org FP4 text encoder and VAE (8.26GB total) passed pinned SHA256 checks. Local 576x768 generation and reference editing passed; first768x1024 run also completed but approached commit exhaustion. See README for reports and visual assessment. Successful image generation does not establish automatic layout or layer extraction.

Sources: https://docs.comfy.org/tutorials/flux/flux-2-klein ; https://huggingface.co/black-forest-labs/FLUX.2-klein-4b-fp8 ; https://huggingface.co/Comfy-Org/vae-text-encorder-for-flux-klein-4b . Exact revisions/hashes are in tools/klein-models.json at repository root. The Comfy VAE file is336MB rather than the168MB Diffusers serialization discussed earlier.
