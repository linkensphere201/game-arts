# Project Overview

Project: game-arts. Started 2026-10-02. Godot-first technical MVP delivered 2026-10-04.

## Goal and Confirmed Sequence

Stage 1 produces usable game art on a local GPU. Stage 2 formalizes a reusable workflow only after effective output is demonstrated. The user initially requested both Godot and Unity, then explicitly prioritized Godot for the first MVP; Unity is deferred.

## Current Result

One 64x64 demon sprite with idle and walk animations, a portable Godot resource folder, a demo that actually imports it, and a tested Windows executable. The selected concept was generated locally using DreamShaper 8. Pixel cleanup and animation were art-directed local processing, not AI-generated coherent animation frames.

Fresh import into a differently named nested folder, demo controls and a 60-second standalone run passed. One selected-prompt replay produced identical RGB pixels in the same runtime. See [validation](../validation/README.md).

## Hardware and Practical Findings

RTX 5060 Laptop GPU, 8151 MiB VRAM, driver 592.27; approximately 31.64 GiB RAM and no configured swap reported during inspection. SDXL attempts failed under the tested loading configurations. DreamShaper 8 at 512x512 succeeded with conservative ComfyUI memory flags; sampled total GPU memory reached 3248 MiB. This does not prove all models or future workloads fit.

## Scope and Remaining Decisions

- The local inference requirement is satisfied for this specific production run.
- Finished resources run independently of generation tools.
- Visual quality is prototype-level; user art acceptance, commercial terms and buyer demand are not established.
- General text-to-animation automation, additional views/actions, Unity and workflow productization remain future work.
- Follow `AGENTS.md`; English maintained docs, Chinese conversation. Local runtime/download storage remains under project `.local/`, excluded from Git. No automatic push.

See [production record](../production/README.md), [research history](research-notes.md), and [active status](../tasks/active.md).

## Confirmed Production Route (2026-10-05, M2.3.3)

AI-assisted production is the accepted direction: AI references and script assistance -> editable Blender models/materials/rigs/animations -> Godot integration and validation -> human quality acceptance. Keep intermediate artifacts editable and each step independently reviewable. Direct AI 3D generation is an optional bounded tool, not the default complete production process. Local generative-art inference and the two-stage output-before-workflow sequence remain in force. The first 3D asset/slice, style and acceptance criteria remain to be selected; the earlier room/chest/demon examples are proposals.

## Current 3D scene (M3.4)

The first 3D environment is a compact 40 x 36 m sunny coastal meadow, authorized on 2026-10-05. See [scene demo](../scene-demo/README.md). Blender 4.5.14 LTS portable is installed inside `.local/blender/`; the scene has editable Blender source, explicit GLB exports and native Godot resources. AI-assisted offline construction is used; no 3D generative model is required. Scene assets precede characters.
