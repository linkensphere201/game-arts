# Milestone Register

## Complexity

- Initialization slice: Simple.
- Overall project classification: Pending scope definition.
- Planning gate: Documentation initialization authorized by the user; product implementation planning pending.

For complex work, define the complete known milestone sequence `M1` through `Mn` and approve milestone-level acceptance targets before implementation begins. This register currently covers only the authorized initialization step.

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

## Decomposition

### M1

- [x] `M1.1` Establish project conventions and working documents.
  - [x] `M1.1.1` Copy and adapt the template; verify file inventory, safety rules, and status consistency.

## Future Planning

Define subsequent milestones once the product scope is known. Preserve the completed `M1` IDs.

## Initialization Follow-up

- [x] `M1.1.2` Initialize the local Git repository on `main`, configure `origin`, and prepare the initial documentation commit.
