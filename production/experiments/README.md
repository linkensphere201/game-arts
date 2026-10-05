# Failed SDXL Environment Experiments

Date: 2026-10-04. These are failure records, not supported setup steps.

- Seed 420041: SDXL 1024, ComfyUI dynamic VRAM, default pinned memory: CUDA allocation failure before sampling.
- Seed 420043: SDXL 768, traditional low-VRAM mode: Windows error 1455 while mapping weights. psutil reported no pagefile/swap configured.
- Seed 420045: dynamic VRAM without pinned memory/async offload: CUDA allocation failure remained.
- Seed 420047: attempted reuse of the internal aimdo loader without aimdo initialization; failed before generation.
- Seed 420049: custom read-only file mapping with traditional loader caused a process-level access violation because model construction was incompatible with read-only backing. No character image was produced.

The experimental loader source is retained in `failed-readonly-loader.py` solely for auditing; do not execute it. The original ComfyUI `utils.py` was restored and its hash verified equal to the retained original. The normal startup script no longer applies this patch. No system pagefile setting was changed.

Next trial uses the smaller SD 1.5-family `Lykon/DreamShaper` DreamShaper 8 pruned checkpoint, 512x512, without the incompatible SDXL LoRA. This is a technical feasibility fallback; quality and commercial suitability still need evaluation.
