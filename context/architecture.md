# Architecture

## Overview

Pending project definition. No product architecture or technology stack has been selected.

## Key Components

- To be defined.

## Data Flow

- To be defined.

## External Dependencies

- None selected.

## Notes

- The documentation structure is described in `README.md`.
- Record confirmed architecture here when implementation planning begins.

## Confirmed Execution Constraint

- [`M2.1.4`] The AI production workflow must support local GPU execution. Required generation/inference steps must not depend on a hosted inference service.
- No model, orchestration tool, GPU backend, or deployment package is selected yet.
- Validate the selected workflow on the actual target GPU, recording model/version, resolution, batch size, peak VRAM, runtime, and output acceptance results.
- A successful local run is required before claiming hardware compatibility. No GPU benchmark or execution has been performed.

## Staged Implementation Direction

- [`M2.1.5`] Stage 1 may use manual steps and existing local tools to produce a finished asset. A reusable workflow is not a prerequisite for this trial.
- Stage 2 captures and formalizes the successful process only if the output is effective. Existing node-based tools may be used in Stage 1 without making workflow productization its deliverable.
