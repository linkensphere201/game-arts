# Decisions

## 2026-10-07 — poster-cover/M1.1.1 confirmed scope

User requested a new poster/cover side task supporting reference-image editing, separately generated text layers and a future API; prioritize locally deployable models. Research and documentation are authorized. Keep it inside game-arts with an independent milestone namespace. This does not authorize model downloads or implementation yet.

## 2026-10-07 — poster-cover/M1.1.2 proposed technical direction

Recommendation, pending implementation approval: visual-model generation/editing plus independent deterministic typography/composition. Editable SVG/JSON and transparent text PNGs satisfy different needs; preserve both. Generative lettering and RGBA decomposition do not by themselves supply font-editable text.

## 2026-10-07 — poster-cover/M1.1.3 resource priority

Reuse installed SDXL models first. Existing portrait tests are not poster validation. New-model priority is a bounded klein4B quantized/offload experiment only if baseline editing is insufficient; official13GBVRAM guidance does not prove8GB operation. AnyText2 and segmentation are optional helpers. Defer20B Qwen candidates and do not reinstall cancelled Z-Image. No final model or serving-license approval is inferred from this research.

## 2026-10-08 — M2.3 implementation boundary

User authorizes installing and testing FLUX.2 Klein 4B, explicitly preferring quantization first. Choose official BFL FP8 distilled weights and Comfy-Org Qwen3 4B FP4 encoder plus Flux2 VAE. Preserve other models and user workflows. The first two test cases use an original beverage poster prompt and a color/fruit reference edit; they do not establish commercial poster quality or automatic layout capability. Use existing memory gate and idle Comfy queue; no system virtual-memory change.

## 2026-10-08 — M2.3 validation and default

Keep transformer FP8 + encoder FP4, with 576x768 as the tested default. Generation took 20.9s and the separate reference edit 22.9s in a live existing runtime; these are not cold-start or general latency guarantees. The first 768x1024 generation completed in70.2s but approached Windows commit exhaustion. An attempted operator interruption raced with successful completion; history confirms success, not an aborted image. Add own-job memory interruption polling for subsequent runs. Keep standard text as a future deterministic layer and do not claim automatic layout, alpha extraction or finished-poster delivery from this model validation.
