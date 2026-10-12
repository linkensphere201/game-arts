# 0.2.0-rc1 - 2026-10-06

## Changes

- Expanded to 16 props plus terrain: three trees, two shrubs, three rocks, two grasses, two flowers, bench, driftwood, pebbles and reeds.
- Branched/varied tree crowns, blue/white flower patches, shoreline detail, wet sand, ground grain, closed terrain sides, calmer broken water/foam patterns.
- Linked GLB wrapper scenes and a standalone component gallery.
- Inspector controls and bilingual live preview controls; per-instance materials/buffers, grass density/distance presets and spatial batching.
- Four local archives: Godot pack, runnable source demo, Windows demo and editable Blender files. Each contains a SHA256 inventory; a separate manifest identifies complete archives.

## Validation

Godot 4.7.2, Windows, Forward+, RTX 5060 Laptop GPU. Only the pack folder was copied to a fresh project and imported successfully. All 17 linked wrappers instantiate. A copied tree GLB was widened by 20%; actual wrapper geometry updated after reimport, its file remained unchanged and its collision configuration was preserved. Two environment instances retained independent grass buffers and water/wind/sunlight settings. Physics: 20 ground probes passed; a capsule traversed the tested 14 m route. This is not exhaustive collision or gameplay certification.

Exported runs at a requested 1920 x 1080 window completed without reported errors: High 45 seconds, Low 30 seconds, panel 8 seconds. The project reports a 1600 x 900 logical viewport with canvas_items stretch; screenshots are 1920 x 1080. High mean frame time 6.13 ms and p95 8.33 ms; Low mean 6.01 ms and p95 8.33 ms, measured after five seconds warmup. These are short local frame-delta observations, not GPU profiling or cross-device benchmarks; differing run durations and camera dwell limit comparison. Low offers no demonstrated material speedup in these runs.

Actual rendered overview, meadow, beach, gallery and Chinese panel captures were inspected. Commercial art acceptance remains open. Headless tests alone do not establish visual quality.

## Before public sale

- Owner approves the art direction and candidate preview, or requests another art pass.
- An independent Godot user installs the pack and confirms documentation/usability.
- Owner finalizes asset license, support policy, attribution/AI disclosure and storefront claims.
- Test any additional engine versions/platforms before claiming support; evaluate more complete performance profiles on target buyer hardware.
- Capture final approved storefront imagery and validate buyer demand/pricing.

No listing has been published and no sale-readiness guarantee is made. Characters and general workflow productization remain out of scope.
