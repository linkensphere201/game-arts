# Coastal Scene Validation

M3.4.3, 2026-10-05. Technical delivery complete; user art acceptance remains pending.

| Check | Result | Evidence |
|---|---|---|
| Blender installation | PASS: 4.5.14 LTS portable, official SHA-256 matched | Version/source/hash in scene-demo/README.md |
| Editable source reopen | PASS: five component meshes and 5,913-vertex terrain source | blender-sources.json |
| Actual GLB export/import | PASS: six Blender GLBs; clean Godot import | fresh-import.log |
| Fresh project without .godot cache | PASS: separate .local/coast-fresh-final directory, no engine errors | fresh-import.log, fresh-physics.log |
| Ground and capsule traversal | PASS: 20/20 ray samples; about 14 m path; 509 grounded frames after settling; no failures | physics.log, fresh-physics.log |
| Camera/HUD controls | PASS: view 2 changes camera, H toggles interface | Same physics logs; test source in scene-demo/authoring/validate_scene.gd |
| Windows export | PASS: clean final export; executable identical to the tested build | export.log, export-identity.json |
| Standalone graphical runtime | PASS: 60 seconds, exit 0, empty error log | windows-runtime.log, windows-runtime-errors.log, windows-process.json |
| Actual rendered output | PASS: overview, meadow and beach screenshots inspected | coast-1.png, coast-2.png, coast-3.png |

## Final scene and performance

Godot 4.7.2 standard, Forward+/Vulkan, RTX 5060 Laptop GPU, NVIDIA driver 592.27. Terrain is **40 x 36 m**, with 10,147 grass instances, 212 flowers, five trees and a bounded coast/path. Ocean extends as visual background. No characters or streaming world.

The exported run rendered at 1600 x 900. After a five-second warmup, 13,125 sampled frames averaged 4.191 ms; p95 was 4.167 ms. This is a short, single-device run of the three saved viewpoints with an apparent 240 FPS presentation cap, not an uncapped throughput benchmark or a promise for other hardware. Screenshot writes occur during the measured interval. Peak VRAM was not measured.

## Visual review and limitations

The final overview shows the grassy foreground/path, tree shadows, sandy coastline and turquoise sea without the earlier obstructing foreground canopy. Grass/flower detail is visible in the meadow view; sand, rocks and coast are visible in the beach view. Wind and analytical water motion use local shaders. Style is deliberately simple low-poly; water is opaque, shoreline foam approximate, and distant ripple repetition remains visible. This is an environment prototype, not commercially accepted art.

The default navigation is an unrestricted free camera, not a playable character. Physics was checked with a temporary capsule in the automated test. Terrain is finite; leaving the intended views can reveal borders. Trunk/rock/ground collisions do not imply leaf collision or swimming. No lightmap, terrain streaming or mobile/web validation.

Native scene meshes are saved snapshots of the imported GLBs. Fresh import/portability is verified, but automatic propagation of later GLB edits into the assembled scene is not implemented. The README describes the explicit replace/rebuild boundary; do not overwrite subsequent hand edits accidentally.

## Reproduction

From the repository root:

```powershell
& .local/godot/Godot_v4.7.2-stable_win64_console.exe --headless --path scene-demo --fixed-fps 60 --script res://authoring/validate_scene.gd
& builds/sunward-coast.exe --resolution 1600x900 -- --capture-dir=E:/projects/game-arts/validation/coast --qa-seconds=60
python tools/package-coast.py
```

For fresh import, copy scene-demo to a new directory excluding `.godot` and `__pycache__`, run Godot with `--headless --editor --import --quit`, then run the same validation script against that directory. Initial sandbox-only certificate/cache warnings, missing vertex-color override, headless MultiMesh serialization loss, preview overexposure and a missing export-preset include_filter were corrected or avoided in the final logged checks. Original iteration logs remain under ignored `.local/runs/`.
