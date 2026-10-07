# Active Tasks
## Current side task — poster-cover/M2.3 (2026-10-08)

[Poster/cover generation](../side-tasks/2026-10-07-poster-cover/README.md): user authorized new task and local-model research for reference editing, independent text layers and a futureAPI. M2.3.1-M2.3.3 quantized Klein download and local generation/edit validation completed: 576x768 default, roughly21s generation and23s reference edit in the tested live runtime. Full layered-poster implementation, larger comparison and API remain deferred. Existing game-art work and model installations remain intact.


## Current Status

The Godot sprite MVP and M3.3.3 recovery are delivered. M3.4 now delivers a small 40 x 36 m coastal meadow with Blender sources, GLBs, Godot project and a validated Windows executable. User visual review is pending; characters, Unity and generalized workflow work remain deferred.

| Step | Task IDs | Result |
|---|---|---|
| 1. Define the character | M3.2.1 | Complete: brief, selected seed, final art deviations recorded |
| 2. Verify local environment | M3.1.1, M3.1.2 | Complete with DreamShaper 8 and Godot; unsuccessful SDXL trials retained |
| 3. Produce the canonical character | M3.2.1 | Complete: local AI draft plus inspected pixel cleanup |
| 4. Produce sprite animation | M3.2.2 | Complete: 4 idle / 6 walk frames; art-directed cutout animation |
| 5. Package reusable Godot resources | M3.3.1 | Complete: PNGs, SpriteFrames and scene import into a fresh relocated folder |
| 6. Import, demonstrate and validate | M3.3.1, M3.3.2 | Complete: demo controls, actual rendering, 60-second Windows run and documented results |

## Deliverables

- [Reusable asset](../assets/ember-imp/README.md).
- [Godot demonstration](../demo/README.md).
- [Validation results](../validation/README.md).
- [Production process and resource locations](../production/README.md).

## Follow-up, Not Started

- M3.1.3: Unity remains deferred from this first MVP.
- M3.3.2: User review of appearance and motion quality remains pending; technical completion is not commercial acceptance.
- M4: Do not generalize or productize until usefulness and acceptable editing effort are established. The current scripts replay one art-directed asset, not arbitrary descriptions without intervention.

## M3.3.3: Browser Workflow Repair

- User reported a missing-model dialog requesting Qwen 3 4B and Z-Image Turbo. Add the matching DreamShaper browser workflow and validate actual UI generation. Browser software exception diagnosis remains conditional on exact error details.

### M3.3.3 diagnosis result

Matching DreamShaper browser workflow is installed and was accepted by ComfyUI. End-to-end generation is blocked by demonstrated Windows commit exhaustion (event 2004, 99.40% usage). A startup preflight now prevents further loading attempts under the observed low-headroom condition. Follow-up: free commit headroom or configure a page file, then revalidate actual generation. Chrome exception linkage remains unconfirmed.


### M3.3.3 recovery verified

After the user enabled a page file and restarted, cold local inference succeeded in 8.1 seconds with pixel-identical output. Browser Run also completed successfully. The earlier blocked diagnosis above is historical. The server is running; Chrome-specific behavior remains unverified.

## Confirmed 3D Production Direction (M2.3.3, 2026-10-05)

The user accepted AI-assisted production using editable Blender assets and Godot validation with human quality review. This supersedes the proposal-only status of the route in M2.3.2, but does not select its illustrative scene/character scope. Next planning step: define the first 3D deliverable and acceptance criteria. No 3D production is running.

## Environment-first research (M2.3.4, 2026-10-05)

Manual Godot environment workflow research is complete in [architecture](../context/architecture.md#2026-10-05-manual-godot-3d-environment-workflow-m234). Environments now precede characters; earlier mixed prototype ordering is superseded. Scene theme, camera and first asset kit remain to be selected. No installation or production started.

## Current implementation: coastal meadow (M3.4, 2026-10-05)

User selected and authorized a sunny outdoor grassy coast. Execute M3.4.1 layout/assets -> M3.4.2 integration/visual review -> M3.4.3 portability/runtime evidence. Blender source authoring/export and native Godot integration are complete for a 40 x 36 m scene. M3.4.3 is complete: fresh-copy import/physics and a 60-second Windows run passed. See [scene controls](../scene-demo/README.md) and [validation](../validation/coast/README.md). Characters and M4 remain deferred.
