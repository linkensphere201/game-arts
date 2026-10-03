# Milestone Register

## Complexity

- Initialization and initial research/documentation slices: Simple.
- Overall project classification: Complex for the proposed local-generation and dual-engine validation scope.
- Planning gate: Research and documentation authorized; implementation explicitly deferred. The known M1-M4 sequence is recorded; proposed M3 acceptance awaits selection.

For complex work, define the complete known milestone sequence `M1` through `Mn` and approve milestone-level acceptance targets before implementation begins. This register covers completed initialization and initial research/documentation; it is not a complete product implementation plan.

## Numbering Contract

- `M<n>`: milestone.
- `M<n>.<s>`: stable subgoal or work package.
- `M<n>.<s>.<t>`: executable task.
- `M<n>.<s>.<t>.<u>`: optional final decomposition level when required.
- Assign IDs sequentially within their parent.
- Never renumber or reuse an ID after progress reporting or implementation begins.
- Keep cancelled or superseded IDs and mark their final state.
- Reference at least one ID in every active-status, decision, implementation, test, and work-log entry.

## Milestones

| ID | Name | Goal | Acceptance target | Status |
|---|---|---|---|---|
| `M1` | AI documentation initialization | Establish the project documentation skeleton. | All 12 template documents exist, root conventions are adapted, and initial status is consistent. | Complete |
| `M2` | Initial workflow and business research | Establish concepts and a provisional validation direction. | Official sources, evidence limits, user acceptance, and pending questions are recorded. | Complete |

## Decomposition

### M1

- [x] `M1.1` Establish project conventions and working documents.
  - [x] `M1.1.1` Copy and adapt the template; verify file inventory, safety rules, and status consistency.
  - [x] `M1.1.2` Initialize Git on `main`, configure `origin`, and create the initial documentation commit.

### M2

- [x] `M2.1` Establish the initial understanding and business hypothesis.
  - [x] `M2.1.1` Research AI workflows, tools, human review, and agent distinctions.
  - [x] `M2.1.2` Review monetization models and discuss a service-first validation approach.
  - [x] `M2.1.3` Record research sources, user-accepted direction, progress, and next planning questions.
  - [x] `M2.1.4` Record the mandatory local GPU execution constraint and pending hardware validation.
  - [x] `M2.1.5` Record the user-confirmed stage order and supersede immediate paid-pilot prioritization.

`M2` IDs were assigned when recording the completed discussion on 2026-10-02. Completion means the initial research record is complete, not that demand or profitability is proven.

## Future Planning

Define subsequent milestones once the product scope is known. Preserve all completed IDs.

## Confirmed Forward Sequence (Planning)

| ID | Stage | Goal | Acceptance target | Status |
|---|---|---|---|---|
| `M3` | Stage 1: local GPU finished output | Produce a finished game-art asset on the target local GPU. | Finished output reviewed against agreed quality/use criteria; local execution and resource use recorded. Asset and thresholds pending definition. | Planning |
| `M4` | Stage 2: reusable workflow | Formalize the effective production process. | Inputs, dependencies, parameters, human steps, and exports documented; another run confirms usable results. | Conditional on M3 effectiveness |

The user confirmed the order and conditional gate. Detailed M3 decomposition and proposed acceptance are recorded below; defaults and effort thresholds remain to be selected before implementation. If M3 results are ineffective, record findings and revise the trial rather than automatically starting M4.

## M2 Technical Research Extension

- [x] `M2.2` Research the minimum local-production and dual-engine experiment.
  - [x] `M2.2.1` Collect Godot and Unity environment/import/build validation options.
  - [x] `M2.2.2` Compare text-to-pixel-character production routes and local candidates.
  - [x] `M2.2.3` Record sources, proposed asset contract, acceptance gates and execution boundaries.

## M3 Proposed Decomposition (Not Started)

Future implementation is complex. The known sequence remains M1 initialization -> M2 research -> M3 usable local output -> conditional M4 workflow formalization. Research authorization does not authorize execution; proposed M3 defaults and acceptance targets await selection before implementation.

- [ ] `M3.1` Establish independent, verifiable environments.
  - [ ] `M3.1.1` Inventory hardware/software and validate local GPU inference.
  - [ ] `M3.1.2` Validate Godot calibration scene and Windows export.
  - [ ] `M3.1.3` Validate Unity calibration scene and Windows build.
- [ ] `M3.2` Produce one usable character package.
  - [ ] `M3.2.1` Generate and approve a canonical pixel character.
  - [ ] `M3.2.2` Author short animations and export the common asset contract.
- [ ] `M3.3` Validate delivery and effectiveness.
  - [ ] `M3.3.1` Verify fresh imports and runnable builds in both engines.
  - [ ] `M3.3.2` Review quality, measured effort and the go/revise/stop decision.

Detailed proposed acceptance: [Architecture](../context/architecture.md#planned-gates-and-evidence). All execution checks are NOT RUN. M4 remains conditional; no generalized workflow is authorized by this research request.
