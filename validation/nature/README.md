# M3.8 nature sample validation - 2026-10-06

Delivered first independent ground, grass and tree samples, version 0.1.0. Existing coast and stone assets are untouched.

## Verified

- Ground/grass source generation and actual renderer inspection. Three ground layers each have 1K color/normal/roughness maps in two treatments. UV0 covers the surface; vertex RGB stores explicit normalized layer weights. Each of the three grass variants has full-width UV0 and independent UV2 bend weights. Imported grass checks found 260 root vertices across six styled wrappers, all zero-weight.
- Tree import checks: 5,974/3,070 near/far triangles; Bark and Leaves shader roles separate; 58 zero-height base vertices across LODs per styled tree; four trunk collision sections; two instances keep independent wind materials. Same-camera, fixed-wind near/far screenshots inspected; broader far leaves reduce, but do not eliminate, canopy changes.
- Each asset ZIP was extracted ALONE into a new project (ground, grass, tree), imported and checked. The demo archive was independently imported and loaded. See fresh-results.json and fresh-*-*.log. No original coast folder is needed.
- Packaging audits all scene/material resource paths stay within each asset folder; ZIP CRC and SHA256 entries are checked.
- Final Windows build ran 30.00 seconds, with empty stderr. Six 1440 x 810 PNG captures exist and were checked. Runtime logical viewport is 1600 x 900. RTX 5060 Laptop GPU, Forward+. After a five-second warmup: mean frame delta 5.73 ms, p95 8.33 ms; peak observed draw calls 48, primitives 42400. See delivery/. This includes automated view changes/captures and then the bark view; it is not a controlled optimization comparison or a cross-device FPS promise.

## Retained failures and corrections

Initial import occurred before demo.tscn was built and reported that missing scene; subsequent imports/load checks passed. Early tree export warned about n-gon cap tangents; explicit triangles and cap UVs fixed it. Root QA found the slanted trunk base had no zero-height vertices; the first ring was flattened and the check passed. Early Windows capture calls were inside assert expressions, which release builds omit; screenshots were missing despite a completion print. Moved file saving outside assert, repeated export/runtime, and verified all six final PNGs. Earlier final/ and windows/ logs are historical; delivery/ is the actual capture evidence.

## Remaining art and performance work

These are initial procedural material studies, not accepted photorealistic art or finished sale products. Bark/branch-junction refinement, botanical specificity, stronger differentiation of the cartoon art direction, tiling reduction and full-coast composition remain open. Tree LOD switches abruptly; grass has distance cutoff without a card LOD or crossfade. Demo grass shadows are off. Controlled same-camera before/after profiling, additional platforms and human buyer review are follow-ups; no speedup is claimed.

Local artifacts: builds/nature-0.1.0-ground.zip, -grass.zip, -tree.zip, -demo.zip, -sources.zip, -windows.zip; builds/nature-study.exe. Source code and docs only are committed; resources stay local.

## Realistic grass v2 / M3.8.7

Evidence: realistic-v2/delivery/nature-1.png through nature-6.png and metrics.json from the final exported executable; realistic-v2/wind-0.0.png, wind-1.8.png and wind-3.0.png show two fixed phases and a relit view. The initial realistic-v2/nature-*.png captures had missing MultiMeshes from headless authoring and are not acceptance evidence. Rebuilding with a real renderer resolved that issue.

Standalone grass and demo 0.1.1 archive imports pass. Root/UV checks report 286 rooted vertices; cartoon-before.json hashes match final cartoon resources. The first Windows capture used an old executable because embedded PCK replacement failed; windows/ is invalid evidence for v2. A newly named nature-study-0.1.1.exe was exported successfully and delivery/ is the replacement evidence. This is a mixed-camera smoke run, not an optimization comparison or full temporal-aliasing assessment. Fine distant blades and grazing highlights still need art work; no photorealistic acceptance claimed.

Versioned delivery verified: builds/nature-study-0.1.1.exe; delivery/nature-3.png visually contains v2 thin curved grass. Final 20.00-second exported run: mean 4.25 ms, p95 4.17 ms, peak 48 draw calls / 44,688 primitives, empty stderr. Windows ZIP contains this versioned executable. The old unversioned exe remains unchanged after its replacement failed.

## M3.8.8 mixed profiles

mixed-grass/nature-3.png is the actual 0.1.2 Windows capture at the previous grass camera. Structural check: 286 anchored roots; all three profiles and width classes per clump; height range greater than 2x per clump. Cartoon hashes match the prior baseline. Independent grass/demo 0.1.2 imports pass. Screenshot confirms upright/curved and broad/narrow mixing. Final runtime evidence: mixed-grass/runtime.log, runtime.err and metrics.json. Other presets are parameter configurations, not separately rendered art-accepted deliveries.

## M3.8.9 ground pass

ground-v2/nature-2.png and nature-3.png are actual 0.1.3 exported captures; six views and metrics.json are present. Windows 20 s mean 4.26 ms / p95 4.17 ms, 48 peak draws, 45,876 primitives, empty stderr. Ground cartoon hashes match ground-v2/cartoon-before.json. Ground layer weights/collision structure pass; 0.1.3 ground/demo archives import independently. Ground is flat with small gravel, so no terrain-displacement/plant-conformance claim. Full-patch textures are unique, not a validated seamless atlas; only meadow preset has visual evidence.
