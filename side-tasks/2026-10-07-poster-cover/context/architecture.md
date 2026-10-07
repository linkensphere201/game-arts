# Proposed Architecture — poster-cover/M1.1.2

Status: research proposal, not implemented. Start with a local callable workflow; package as a service only after output quality and layer editing are accepted.

## Pipeline

Brief + exact copy + optional reference/mask -> layout plan -> image generation/editing -> protected foreground composition -> independent text rendering -> compositing -> review -> export bundle.

Separate visual generation from layout and typography. No layoutLLM is required initially: use explicit templates/coordinates with user copy. Add model-proposed layout/copy later only if useful, with exact text still supplied to the renderer as data.

## Intermediate contract

- `background.png`: generated/edited visual background without planned title text.
- `subject.png`: optional supplied/extracted subject with alpha; preserve original separately.
- `text/title.svg`, `text/subtitle.svg`, `text/callout-N.svg`: editable text with font identifiers, size, position, wrapping/alignment, color/stroke/shadow data; transparent PNG previews for each.
- `layout.json`: schema_version, canvas size/color space, ordered stable layer IDs, type, asset reference, transform, opacity, bounds, literal Unicode copy, font hash, effects, safe regions and source revision.
- `poster.png`: flattened delivery preview; optional JPG for platforms.
- `manifest.json`: input hashes, model/adapter revisions, prompt/seed/settings, layer provenance, timings and export settings.

Files are illustrative future artifacts, not present deliverables. No native PSD text-layer support is promised yet. SVG font resolution must be pinned and tested. Preserve text strings alongside any optional outlined export.

## Editing behavior

Changing text/content/font/layout rerenders only text/composition; background/source image hashes remain unchanged. Background-only edits use the selected mask; hard-preserved regions are copied from the original after generation, with a documented feather band. Reference style transfer may change pixels and identity; expose it as a different operation from preservation. A decorative raster-lettering layer remains distinguishable from editable text.

## Local implementation proposal

Reuse the existing ComfyUI backend on8189 with versioned API-format workflow templates, loading one model at a time. The official server exposes image upload, queued prompt submission, history and WebSocket progress [research S14]. UI workflow JSON is not itself the API prompt graph. Test the conversion and persist prompt IDs.

Use a local CPU renderer (SVG-capable renderer or headless browser with installed licensed fonts) for text and final layout. Decide renderer after checking CJK glyph coverage, line breaking, SVG/PNG parity and alpha edges. Begin with manual masks; optional BiRefNet later. Protect logos via supplied assets rather than asking diffusion to redraw them.

## Future API contract — proposal only

| Endpoint | Role |
|---|---|
| POST /v1/assets | Upload/reference an input image or mask; return asset_id |
| POST /v1/jobs | Submit generation/edit/compose request; return job_id with202 |
| GET /v1/jobs/{id} | State, progress, errors and artifact references |
| PATCH /v1/designs/{id}/layers/{layer_id} | Revise text/layout using revision checks; no implicit background regeneration |
| POST /v1/designs/{id}/exports | Export requested dimensions/formats |

Job request: template_id, mode, canvas, prompt, reference_asset_ids, optional mask_asset_id, exact text blocks, style preset and seed. Versioned responses expose queued/running/succeeded/failed/cancelled states. Use oneGPU worker initially, CPU text jobs independently, per-job isolation, idempotency keys and structured retryable/nonretryable failures. Avoid a parallel/multimodel serving promise on8GB. Keep ComfyUI as an internal backend and expose stable business fields rather than arbitrary node graphs. Network authentication/access controls belong to M4 deployment, not this research implementation.
