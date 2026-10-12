# M3.5 candidate validation - 2026-10-06

Current candidate: 0.2.0-rc1. See [release evidence](../../scene-demo/sunward_coast/docs/RELEASE.md) for scope, metrics and remaining sale gates.

| Check | Result | Local evidence |
|---|---|---|
| Self-contained pack / instance isolation | 17 wrappers pass; distinct materials and MultiMesh buffers | pack-check.log, fresh-controls.log |
| GLB geometry reimport | Width increased 20%; wrapper and collision configuration preserved | fresh-reimport.json, reimport-before.log, reimport-after.log |
| Physics/control route | 20 probes; 14 m capsule route; view/H toggle pass | physics-retry.log |
| Windows High | 45 seconds, exit 0, empty stderr; mean 6.13 ms / p95 8.33 ms | high/ |
| Windows Low | 30 seconds, exit 0, empty stderr; mean 6.01 ms / p95 8.33 ms | low/ |
| Chinese tuning panel | 8 seconds, exit 0; screenshot inspected | settings/ |
| Component gallery | Actual rendered image inspected | gallery.png |
| ZIP integrity | CRC and per-file SHA256 verified for all four archives | builds manifest (outside this folder) |
| Extracted buyer demo | Independent import and 90 headless frames pass | zip-import-retry.log, zip-run.log |

Failures retained for diagnosis: physics.log contains the initial script parsing failure, corrected before the successful physics-retry run. zip-import.log records a sandbox system-certificate-store read error; import and runtime succeeded outside that sandbox in zip-import-retry.log and zip-run.log. Neither failure is silently counted as a clean pass.

Screenshots are local generated outputs, not tracked or uploaded. The 1920 x 1080 captures use a reported 1600 x 900 logical viewport with canvas_items scaling. Metrics are short frame-delta observations, not a hardware-independent FPS guarantee. No significant Low-preset speedup established. Fresh tests retain their isolated directories under .local/; original assets were not altered by the reimport probe.

![Current overview](high/coast-1.png)

![Component gallery](gallery.png)
