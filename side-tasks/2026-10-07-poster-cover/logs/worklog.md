# Work Log

## 2026-10-07 — poster-cover/M1.1.1-M1.1.3

Created from the project-manager project-template using the create-task skill's document builder, adapted destination to a game-arts side-task directory to honor repository scope. Read parent project status and kept existing game-art work intact.

Reviewed official cards/repos for RealVisXL, Animagine, FLUX.2 klein4B, AnyText2, Qwen generation/editing/layer decomposition, Kontext, BiRefNet, LayerDiffuse, Diffusers reference adapters and ComfyUI API routes. Recorded source links, local prior-test evidence, resource uncertainty, layer semantics, M1-M4 proposal and bounded acceptance plan.

Research only: no new weights, no inference, no API code, no deletions or push. M2-M4 remain proposed. Parent indexes updated for discoverability; IDs are qualified as poster-cover/M1 etc. outside this folder.

## 2026-10-08 — poster-cover/M2.3

Installed and hash-verified Klein4B FP8, Qwen3 FP4 encoder and Flux2 VAE. Download script fixed for Windows PowerShell array enumeration and unavailable Get-FileHash (uses .NET SHA256). Early failed download-worker logs retained; final files match upstream hashes. Added native-node browser/API workflow builder and runner with memory preflight, own-job low-commit interrupt, provenance and2-second resource sampling. Existing ComfyUI runtime unchanged.

Validated original beverage background768x1024 (70.2s;7859MiB;0.36GiB minimum available commit), strawberry reference edit576x768 (22.9s;4659MiB;4.53GiB), and default-size generation576x768 (20.9s;4405MiB;2.40GiB). Visually inspected all three. Saved576x768 as default. No full-precision comparison, actual editable text/layer composition, API, or commercial acceptance. No push; generated assets remain ignored.

## 2026-10-08 — M2.4

Added local Sharp/librsvg compositor and PowerShell wrapper, authored JSON layout, independent text SVG/PNG exports and a reproducible verification script. Inspected original29 and revised19 posters plus complete-SVG raster export. Exactly1066 changed pixels are restricted to price masks;5 other layers hash-identical;420407 uncovered pixels equal the source background. Chinese wrapping and overflow rejection checked. Fontconfig profile-cache warnings resolved by setting environment before Node startup; all caches local. No model calls/packages/font downloads. Rendering positions are manual; font portability and richer typography remain future work.
