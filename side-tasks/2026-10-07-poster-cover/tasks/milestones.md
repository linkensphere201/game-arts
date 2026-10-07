# Milestone Register

Classification: complex. Local namespace: poster-cover. Known sequence M1-M4 is proposed below. User authorized creation and research on2026-10-07. M2-M4 implementation acceptance targets are not yet approved; do not start implementation/downloads on the strength of this research alone.

| ID | Goal | Acceptance | State |
|---|---|---|---|
| M1 | Requirements, evidence and technical shortlist | Distinguish reference editing/text layers, source-backed local candidates, device limits, proposed API and pilot criteria | Research complete; plan awaiting review |
| M2 | One layered poster, then bounded local comparison | Reference input edited; protected subject retained; title/subtitle independently editable/exportable; visual acceptance and measured resource use | Proposed |
| M3 | Reusable local poster/cover workflow | Three aspect presets, repeatable layer edits, structured errors, reproducible exports and provenance | Proposed; depends on M2 |
| M4 | API package | Async job lifecycle, stable layer updates/exports, queue/resource limits, deploy/restart/error handling and client example | Proposed; depends on M3 and serving-license review |

## Current research tasks

- M1.1.1 complete: identify requirements, reuse local test evidence, inspect primary model sources.
- M1.1.2 complete: define separate text/visual layer contracts and candidate API boundaries.
- M1.1.3 complete: rank models by incremental resource burden and define a falsifiable pilot.
- M1.2.1 pending: confirm first visual use case, deliverable format and M2-M4 acceptance with user before implementation.

## Proposed M2 entry slice

- M2.1.1: one reference input/mask and approved copy/layout; pin baseline model/fonts/settings.
- M2.1.2: produce background/subject/title/subtitle/flattened output; demonstrate text-only edit with identical background hash.
- M2.1.3: inspect subject boundaries and text readability; record cold/warm latency, peak device VRAM, RAM/commit and disk additions; receive art review.
- M2.2.1: after the first slice succeeds, compare four themes x three aspect ratios x two seeds (24 cases) using the selected baseline, plus matched cases for one justified challenger only.

## Proposed acceptance measurements

- Preserve every requested title, date, price and punctuation exactly; missing glyphs or incorrect copy fail. OCR is a secondary check, not a replacement for inspecting source strings and rendered glyphs.
- No clipping/overflow; inspect output at intended viewing size as well as100%.
- Text layers export independently with valid alpha; typography changes do not alter visual-base hashes or trigger diffusion.
- Hard-preserved regions are pixel-identical at working resolution outside the explicit feather boundary; inspect masked joins, hands/hair/product edges separately.
- Cover reflow uses a new layout, not destructive stretching. All three ratios keep focal subject and text safe areas.
- Record failures and chosen retries, not just cherry-picked images. Report latency/memory rather than promising a preset runtime; formal latency target still needs agreement.
- On this8GBGPU use batch1 and oneGPU job; check commit headroom before loading. Document complete additional weights/caches before any new download. No new bulk-model installation in M1.

## Dependencies

First style/use case and PSD requirement affect deliverables. New ControlNet/IP-Adapter architecture and currentWindows runtime compatibility need validation. M4 depends on pinned model/adapter/font terms for the actual serving use, not just a model-card license label. Do not renumber existing tasks; qualify IDs in parent records.

## 2026-10-08 — M2.3 bounded Klein validation authorized

User explicitly requests download and validation, then confirms quantization first. This supersedes the research-only boundary for this slice, without approving the full M2.1 layered-poster implementation or M3/M4. M2.3 sequence: component installation, generation/edit validation, evidence and reproducible workflow handoff.

- M2.3.1 in progress: install exact-version FP8 distilled transformer + FP4 text encoder + Flux2 VAE, verify sizes and SHA256.
- M2.3.2 pending: batch-one 768x1024 generation and single-reference edit, inspect art and measure elapsed time/available commit/sampled GPU usage.
- M2.3.3 pending: save browser/API workflows, source provenance, local paths and honest limitations.

No checkpoint training, automatic layout model, cloud inference, or API product implementation is included.

## 2026-10-08 — M2.3 result

M2.3.1-M2.3.3 completed. All three weights hash-verified; generation and reference editing succeeded locally. Default 576x768 workflows exported. 768x1024 succeeded but left 0.36 GiB available commit, so it is not the default. Saved browser recipes do not invoke the external runner's memory guard. Full M2.1/M2.2, M3 and M4 are still deferred. Measurements and visual limits are in README.

## 2026-10-08 — M2.4 SVG text and composition demo

User requests continued feasibility analysis plus a small SVG typography demo and final layer compositor. Approve this bounded local slice; API and autonomous layout remain deferred.

- M2.4.1: define a layered beverage-poster JSON and render Chinese text into independent editable SVG and transparent PNG layers.
- M2.4.2: compose with the existing Klein background; export complete SVG and flattened PNG without invoking image generation.
- M2.4.3: change only price text; verify input hash, unaffected layer hashes, transparent layer exports and unchanged background pixels outside the text mask; visually inspect both revisions and document limitations.

M2.4.1-M2.4.3 completed2026-10-08: six-layer Chinese SVG typography, final CPU PNG/SVG composition, visual review, source/layer hashes and pixel-isolation checks. Scope is manually authored576x768 layout with bounded wrapping/shrinking. No API or generative typography added.
