# Milestone Register

## Complexity

- Initialization and initial research/documentation slices: Simple.
- Overall project classification: Pending scope definition.
- Planning gate: Initial research and documentation authorized; service-first exploration direction accepted. Product implementation planning remains pending.

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

`M2` IDs were assigned when recording the completed discussion on 2026-10-02. Completion means the initial research record is complete, not that demand or profitability is proven.

## Future Planning

Define subsequent milestones once the product scope is known. Preserve all completed IDs.
