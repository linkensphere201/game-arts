# Decisions

## Decision Log

### 2026-10-02

- Decision [`M1.1.1`]: Use `E:\projects\project-manager\project-template` as the documentation baseline.
- Reason: The user requested the source project's conventions and document skeleton for a new project.
- Impact: Retain the 12-document structure and adapt project identity, safety rules, and initialization status.

- Decision [`M1.1.1`]: Initialize directly in `E:\projects\game-arts`.
- Reason: The user explicitly requested the current directory; the repeated source path was interpreted as `E:\projects\project-manager`.
- Impact: No dated wrapper directory or unrelated source workspace content is copied.

- Decision [`M1`]: Defer product scope and architecture until requirements are provided.
- Reason: Only documentation initialization has been specified.
- Impact: `M1` represents initialization only; later milestones will follow scope definition.

- Decision [`M1.1.2`]: Initialize Git with `main` and set `origin` to `git@github.com:linkensphere201/game-arts.git`.
- Reason: The user requested repository initialization and supplied the remote address.
- Impact: Local version control is enabled. Remote publication requires a separate push request.

- Decision [`M2.1.2`]: Prioritize validating a small custom game-art delivery offer before investing in workflow templates or an online tool.
- Reason: The user explicitly agreed with this initial judgment after the workflow and monetization discussion.
- Impact: Select a concrete buyer and output, then validate paid demand, repeatable quality, and delivery economics. This is a strategic direction, not proof of product-market fit or authorization to contact customers.

- Decision [`M2.1.3`]: Keep the icon-set example and independent-developer segment as candidates; preserve uncertainty about pricing, tooling, budget, and schedule.
- Reason: Those details were illustrative and have not been selected by the user.
- Impact: Record them as planning questions rather than implementation requirements. Official service listings establish that commercial services exist, not an income forecast.

- Decision [`M2.1.4`]: Require local GPU execution for the AI production workflow.
- Reason: The user explicitly stated that the workflow must run on a local GPU.
- Impact: Filter models and tools for a complete local inference path; do not make hosted inference APIs or cloud GPUs mandatory. Establish the target hardware and validate an actual local run before claiming compatibility. Fully offline operation was not requested.

- Decision [`M2.1.5`]: Follow the user's two-stage sequence: first produce a finished asset on a local GPU; then, if results are effective, formalize the process into a workflow.
- Reason: The user explicitly clarified the stage order after adding the local GPU requirement.
- Impact: This supersedes the immediate paid-pilot ordering in `M2.1.2`. Prioritize local production feasibility and finished-output quality. Keep customer trials and monetization as later topics; no generalized workflow implementation is required in Stage 1.
