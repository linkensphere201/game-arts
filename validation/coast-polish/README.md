# Coastal Polish Validation

M3.4.5, 2026-10-06. Technical checks passed; visual approval remains with the user.

- Same 40 x 36 m terrain and three camera views as the baseline.
- Local `before-overview.png` preserves the previous overview. `coast-1.png` through `coast-3.png` show the updated exported build, not a mockup.
- New water shader compiled and rendered in Forward+/Vulkan without errors. Ocean detail fades with distance; shoreline foam is broken and advances/recedes analytically. Water remains opaque and does not simulate fluid or swimming.
- Meadow distribution: 6,202 grass instances and 184 flowers. Softer verges and patchwise tint/density replace the earlier uniform distribution. Secondary prop randomization changes when the seeded scatter sequence changes; this is not a pixel-identical isolated shader comparison.
- Physics/control regression: 20/20 ground rays, a roughly 14 m capsule route, 509 grounded frames after settling, viewpoint and HUD checks passed (`physics.log`).
- Windows export passed (`export.log`). Exported executable ran for 30 seconds and exited 0; stderr empty (`windows-runtime-errors.log`, `windows-process.json`).
- At 1600 x 900 on this RTX 5060 Laptop GPU, 5,886 post-warmup frames averaged 4.248 ms, p95 4.167 ms. Presentation is capped; screenshot writes are included. This is a short regression check, not an uncapped benchmark.
- Terrain/collision geometry and packaging structure are unchanged; the earlier fresh-import evidence remains historical. Fresh import was not repeated for this shader/scatter-only pass.

Visual assessment: parallel white bands and dense repetitive distant sparkle are reduced; depth color is stronger; vegetation edges and density are less uniform. Tree/shrub geometry, ground flatness, finite scene borders and manual reimport limitations remain follow-ups. No sale-ready claim.

Images, runtime data/logs, native scenes and builds are local-only under the source-only publication policy. Only this report, code and updated documentation are eligible for commits/publication.
