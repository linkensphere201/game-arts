# Project Overview

## Basic Info

- Project name: game-arts.
- Start date: 2026-10-02.
- Owner: To be defined.
- Current status: Two-stage direction confirmed: local GPU finished output first, workflow formalization only if results are effective.

## Goal

Stage 1: use a local GPU to produce a finished game-art asset and evaluate its practical quality. Stage 2: if the result is effective, organize the proven production steps into a reusable workflow. Commercial validation remains a later topic.

## Scope

### Current Scope

- Maintain project conventions, research evidence, decisions, tasks, and work logs.
- Record the initial research and user-accepted direction under `M2`.

### Candidate Next Scope

- Define one finished asset and its acceptance criteria for the local GPU trial.
- Run the first local production trial once its scope is defined; assess the result before planning workflow formalization.
- These are pending planning items; no customer outreach, purchase, deployment, or production run has started.

## Current Priorities

- Select the first asset category and confirm target GPU/VRAM.
- Define finished-output acceptance criteria and local runtime/memory measurements.
- Classify the implementation scope and establish subsequent milestones before building.

## Constraints

- Keep project files under `E:\projects\game-arts`.
- Follow `AGENTS.md` and user-provided global safety rules.
- Use English for AI-maintained documents and Chinese for conversation by default.
- No technology stack, pricing, budget, or launch schedule has been selected.

## Open Questions

- What finished asset should Stage 1 produce, and how will its effectiveness be judged?
- Which asset category and style should the first sample cover?
- What inputs, hardware, tools, time, and budget are available?
- What constitutes an accepted asset and a successful pilot?

## Evidence

See `context/research-notes.md` for sources, limitations, candidate models, and validation questions. The icon-set example is illustrative, not a confirmed product requirement.

## Local GPU Requirement

- [`M2.1.4`] Hard requirement from the user: the AI production workflow must run on a local GPU.
- The required production path must support local model inference without mandatory hosted inference APIs or rented cloud GPUs.
- GPU model, VRAM, available system memory, driver/backend compatibility, and acceptable runtime remain to be established before tool/model selection.
- Local GPU execution does not by itself imply fully offline operation; network access and model-download requirements remain unspecified.
