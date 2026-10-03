# game-arts

AI-assisted game-art exploration, started on 2026-10-02. Stage 1 produces a finished asset on a local GPU. Stage 2 formalizes the production process into a reusable workflow only if Stage 1 results are effective.

## Start Here

1. Read `AGENTS.md` for project conventions and safety rules.
2. Read `context/project-overview.md` for scope and open questions.
3. Read `tasks/milestones.md` and `tasks/active.md` for progress and next steps.
4. Record decisions in `tasks/decisions.md` and completed work in `logs/worklog.md`.

## Documentation Structure

- `context/`: stable background, architecture, glossary, and research notes.
- `tasks/`: milestones, active tasks, backlog, and decisions.
- `prompts/`: reusable prompts.
- `logs/`: chronological implementation and verification records.

## Current State

- `M1` completed: documentation and local Git initialization.
- `M2` completed: initial workflow/monetization research and progress record. See `context/research-notes.md` for evidence and limitations.
- `M2.2` completed: researched local text-to-pixel-character production and validation in both Godot and Unity. Read [the technical proposal](context/architecture.md) and [sources](context/research-notes.md#technical-research-2026-10-03).
- `M3` remains planning only. Proposed first output: one demon with idle/walk animations. No setup, model download, generation or engine validation has begun.
- Future dual-engine production validation is complex. M1-M4 are the known sequence; proposed M3 specifications and acceptance targets remain to be selected before execution.

## Template Provenance

Adapted from `E:\projects\project-manager\project-template` on 2026-10-02.
The existing `game-arts` directory is the project root; no dated wrapper directory is required.
