# Local SVG Poster Demo — poster-cover/M2.4

A bounded CPU-only typography/composition demo over the existing Klein beverage background. No diffusion endpoint, cloud service or new model is invoked. It does not implement automatic visual layout, extracted product layers, a live editor, PSD text, or an API server.

## Run from game-arts root

```powershell
& tools/compose-poster.ps1
& tools/compose-poster.ps1 -Output .local/poster-cover/svg-demo/v2 -LayerId price -Text 19
```

The wrapper defaults to the discovered Codex bundled Node/Sharp runtime. Override `-NodePath` and `-ModulePath` for another Node installation containing Sharp. Tested Sharp0.35.4/libvips8.18.6/librsvg2.62.91. No packages were installed. Fontconfig environment must be set before starting Node on Windows; the wrapper does this and keeps its cache under `.local/poster-cover/fontconfig/`. Early cache warnings were resolved by setting the parent process environment rather than changing it after Node started.

Source `layout.json` contains the canvas, background path, regular/bold font paths and six ordered text boxes. Supported fields: literal text/newlines, position, bounds, size/minimum size, line spacing, regular/bold weight, solid fill. Chinese grapheme wrapping and bounded font shrinking are implemented; overflow fails rather than silently clipping. Line breaks are basic, not typographic Chinese punctuation rules or English word-aware hyphenation. Space-only measurement is approximate; actual rendered ink bounds are checked. Layout positions and hierarchy are authored, not predicted by AI.

The demonstration reads Microsoft YaHei fonts already installed in Windows and records their SHA256 values; it does not bundle them. SVG text remains editable and requires matching fonts on another machine. A production service needs explicitly selected deployable font files and glyph coverage tests. Font hashes document inputs but do not implement a full cross-machine font/fallback guarantee.

## Output

Default directory: `E:/projects/game-arts/.local/poster-cover/svg-demo/v1/`; price revision: `v2/`.

- `background.png`: byte-identical copy of the source PNG.
- `layers/<id>.svg`: one full-canvas transparent SVG per text layer, with real text/tspan elements.
- `layers/<id>.png`: corresponding transparent raster layer.
- `poster.png`: ordered CPU alpha composition.
- `poster.svg`: self-contained embedded background plus editable text elements.
- `layout.json`: resolved text size/line breaks and source strings, reusable with the compositor.
- `manifest.json`: font/background/layer/output hashes, renderer versions and elapsed time.

Changing text rerenders CPU layers and composition; the prototype does not yet cache unchanged layer rendering. It never regenerates or changes the background. Repeating a command intentionally overwrites exports in that chosen directory; use a new output directory to retain revisions. Background dimensions must match the canvas exactly; no implicit stretching occurs. The edit CLI can change one named text layer per invocation; the callable `compose()` function accepts multiple overrides.

## Verified on 2026-10-08

- Both ordinary six-layer exports passed and were visually inspected at576x768.
- v1 price29 -> v2 price19: exactly1066 pixels changed, all inside the union of the price-layer alpha masks.
- Other5 SVG/PNG text layers remained hash-identical.
- All420407 pixels outside the v1 text masks exactly equal the original background pixels.
- Recomposition from the exported PNG layers exactly matches `poster.png`.
- A longer Chinese title exercised automatic wrapping; an excessively long title correctly raised overflow.
- Full `poster.svg` rasterized successfully and was visually inspected as `v2/poster-svg-preview.png`.
- Timed demo exports: approximately0.49s and0.24s inside the compositor, excluding Node startup. These are two local measurements, not a general latency guarantee.
- Evidence: `.local/poster-cover/svg-demo/verification.json`.

Verification (after running the wrapper in the same PowerShell session, which configures the runtime environment):

```powershell
& "$env:USERPROFILE/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe" tools/verify-poster-demo.cjs
```

The verifier preserves extra `wrap-check` and `overflow-check` outputs for inspection. Text-source JSON, compositor and verification code are versioned; exported art and font cache remain local/ignored.

## Feasibility conclusion

Independent SVG text plus CPU layer composition is feasible on this machine without more GPU capacity. The next bounded step is user review of layout, then font/style presets and predictable reflow across aspect ratios. Shadows/gradients, product alpha extraction, incremental layer caching, revisioned API endpoints and automatic layout are future work; none are implied by this demo.
