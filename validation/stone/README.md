# M3.7 independent stone validation

2026-10-06, first sample. Godot 4.7.2 Windows Forward+, RTX 5060 Laptop GPU.

- Bake retry succeeded: 20,480 source triangles to 2,560 game triangles, 1K albedo/normal/roughness; editable packed Blender source saved.
- Actual overview and realistic/cartoon closeup captures inspected in stone-3.png / stone-1.png / stone-2.png. Same shape in both styles; art acceptance remains open.
- Fresh project extracted from the asset ZIP only: import passed. validate_asset.gd verifies two linked wrappers, shared mesh, triangle count, non-null materials, collision and map sizes. fresh-check.log reports STONE_ASSET_OK.
- Four delivery ZIPs pass CRC and embedded SHA256 checks. Package script audits text resource references stay within stone_asset and resolve.
- Windows export clean; executable completed three timed captures (about six seconds) with STONE_CAPTURE_OK and empty host-errors.log and exit code 0 in windows/. This is a short smoke test, not a performance benchmark.

Retained failures: bake.log contains the packed-texture export permission failure; bake-retry.log records successful separate-map export. build.log contains the early camera-before-construction error; build-final.log and render-final.log record the corrected build. No deletion of diagnostic evidence.

Local archives: builds/limestone-0.1.0-{godot,demo,source,windows}.zip. No remote upload. The archive's authoring script expects this repository layout; use the .blend directly for standalone manual editing. Bare GLB has no textures attached; use wrappers or reconnect the supplied maps.

The first Windows smoke run under the sandbox reported user-log and root-certificate access errors. The normal-host retry completed cleanly; both logs are retained.
