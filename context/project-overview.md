# Project Overview

## Goal and Status

Project: game-arts. Started 2026-10-02. `M1` initialization and `M2` research are complete; `M3` implementation has not started.

Stage 1 produces usable pixel-art game characters on the local GPU and verifies them in both Godot and Unity. Stage 2 formalizes the process into a reusable workflow only if Stage 1 is effective. Commercial validation remains later work.

## Confirmed Scope

- `M2.1.4`: required inference runs locally without mandatory hosted APIs or cloud GPU rental.
- `M2.1.5`: finished output precedes workflow productization; manual steps are acceptable in the trial.
- `M2.2.1`: both Godot and Unity environments must be verifiable.
- `M2.2.2`: target text-described pixel characters, for example a demon, that can be imported and used in games.
- `M2.2.3`: current authorization is research and documentation only. No installation or production work starts in this slice.

## Proposed Next Experiment

One side-view demon, 64x64 cells, four idle frames and six walk frames. A shared PNG/metadata package is adapted into native Godot and Unity animation resources and verified in standalone builds. These are recommended defaults, not approved specifications. See [architecture](architecture.md).

## Hardware Evidence and Constraints

Earlier inspection reported NVIDIA GeForce RTX 5060 Laptop GPU, 8151 MiB VRAM and driver 592.27. RAM, available disk and actual runtime compatibility remain unverified. No successful local inference or engine build is claimed.

Keep project files under `E:\projects\game-arts`. Follow `AGENTS.md`, use English for maintained documents and Chinese for conversation. No model/editor purchases, pricing, launch schedule or mandatory online inference have been selected. Download/setup connectivity is distinct from local inference; fully offline operation is not established.

## Remaining Choices

- Perspective, cell size, animation scope and style details.
- Acceptable manual art work and total trial effort.
- Exact engine patches, local runtime and model revisions after compatibility checks.
- Acceptance of the proposed M3 targets before implementation; future execution is classified as complex.

Evidence and alternatives: [research notes](research-notes.md). No art quality, performance, market demand or profitability has been validated.
