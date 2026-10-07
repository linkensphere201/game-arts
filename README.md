# game-arts

## Remote repository: code and documentation only

The user requested source-only publication on 2026-10-05. Generated art resources, Blender files, GLBs, Godot scene/resource outputs, screenshots, validation data/logs, archives, executable builds, model weights and local tools remain local. This supersedes earlier statements that finished art or demo scenes are tracked for remote delivery. Artifact links below describe local deliverables and may not resolve in a fresh clone.

A fresh clone is not immediately runnable: generate the Blender/GLB assets and Godot scenes using the authoring instructions in `scene-demo/README.md` first. Code, shaders, project/export configuration, authored production specifications and documentation are retained.

Publication uses `codex/source-only`, based on the previously published remote `main`, so the original resource-bearing local commits are not its ancestors. The original local `main` and its resources are preserved. For subsequent publication, work from the source-only lineage; do not merge or push the resource-bearing local history. Resource ignore rules do not remove files already present in old commits.


Godot-first sprite MVP delivered on 2026-10-04: text prompt -> local GPU character draft -> art-directed pixel cleanup and animation -> reusable Godot resource -> importing demo and Windows build.

## Open the Result

| Deliverable | Location |
|---|---|
| Reusable asset and import instructions | [assets/ember-imp](assets/ember-imp/README.md) |
| Godot demo project | [demo/project.godot](demo/project.godot) |
| Demo controls | [demo/README.md](demo/README.md) |
| Actual Godot screenshot | [validation/godot-demo.png](validation/godot-demo.png) |
| Animated sprite preview | [validation/sprite-preview.gif](validation/sprite-preview.gif) |
| Local Windows executable | `builds/ember-imp-demo.exe` |
| Local asset ZIP | `builds/ember-imp-godot.zip` |
| Local demo-source ZIP | `builds/ember-imp-demo-source.zip` |

Open the project with Godot 4.7.2, or run the Windows executable. The completed asset and demo do not need Python, ComfyUI or model files. ZIPs/builds are local ignored outputs; tracked sources can recreate them.

## Result and Limits

- 64x64 character, 4 idle frames and 6 walk frames, 8 FPS, binary alpha and 23 shared opaque colors.
- DreamShaper 8 generated the selected draft on the RTX 5060 Laptop GPU. SDXL trials failed in this machine's memory configuration and are recorded, not counted as successes.
- Animation uses art-directed pixel leg redraws and cutout motion. This is a single-character technical MVP, not proven general text-to-animation automation or a commercially polished pack.
- Fresh-project import, demo controls, a 60-second Windows run and one pixel-identical local generation replay passed. See [validation](validation/README.md).
- Unity is deferred. Stage 2 workflow productization remains conditional on output quality and acceptable effort.

## Documentation and Local Resources

Read [AGENTS.md](AGENTS.md) for conventions, [active status](tasks/active.md) and [milestones](tasks/milestones.md) for progress, and [production record](production/README.md) for prompts, model provenance, commands, failures and [exact resource locations](production/README.md#local-resource-locations).

All project-managed downloaded archives, model weights, portable tools and logs live under `E:\projects\game-arts\.local\`, ignored by Git. They are not system-wide installations. Nothing is automatically pushed.

## Provenance

Project started 2026-10-02. Documentation was adapted from `E:\projects\project-manager\project-template`. M1 initialized documentation/Git; M2 recorded research; M3 delivers the Godot MVP. Earlier decisions remain in [the decision log](tasks/decisions.md).

## 3D scene

The new [Sunward Coast demo](scene-demo/README.md) is a compact 40 x 36 m outdoor scene with grass, sunshine and coast. Open `scene-demo/project.godot` in Godot 4.7.2. Editable Blender sources are under `art-source/environment/`; Blender 4.5.14 portable is in `.local/blender/blender-4.5.14-windows-x64/`. Scene delivery validation is tracked separately from the earlier sprite MVP.

## Poster and cover side task

[Poster/cover generation research](side-tasks/2026-10-07-poster-cover/README.md), created2026-10-07: local-first reference-image editing, independent editable text layers and a future API. Research is complete; quantized Klein local generation/editing validation (M2.3) passed on 2026-10-08. Full layered-poster implementation and API remain deferred. This is independent of the existing game-art milestones.
