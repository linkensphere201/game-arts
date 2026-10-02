# Research Notes

## Research Scope

- Date: 2026-10-02.
- IDs: `M2.1.1` (workflow concepts), `M2.1.2` (monetization and initial direction).
- Method: Initial review of official sources and discussion with the user. No customer interviews, paid orders, production trials, or revenue measurements have been conducted.

## Core Concepts

- An AI workflow organizes models, tools, data, and human review into repeatable steps with defined inputs, outputs, and acceptance checks.
- In Anthropic's engineering terminology, workflows primarily follow predefined paths; agents dynamically choose their process and tools. They can be combined [S1].
- In ComfyUI, a workflow is a connected node graph; its structure can be represented as JSON [S2, S3]. A shared workflow file still depends on its required environment and components.
- Human review can be an explicit workflow step. n8n documents approval or rejection before selected tool executions [S4].

## Evidence and Limits

| Finding | Evidence | What it does not establish |
|---|---|---|
| Commercial workflow implementation and integration services exist. | n8n's official service partner directory [S5]. | Typical provider income, our customer demand, or our profitability. |
| ComfyUI workflows can be deployed as APIs. | Official Comfy API documentation [S6]. | That an online product will attract paying users or retain them. |
| Repeatable orchestration and human review are supported patterns. | [S1-S4]. | Identical generated outputs or consistently acceptable game assets. |

## Monetization Options Considered

| Model | Deliverable | Main challenge to validate |
|---|---|---|
| Finished assets | Usable game-art packs | Quality, consistency, buyer demand. |
| Custom delivery | Assets matching a customer brief | Communication, revision effort, delivery time. |
| Workflow templates | Reusable workflow plus instructions | Reproduction, compatibility, support burden. |
| Team implementation | Integrated production process | Reliability, integration, maintenance. |
| Online tool | Usage-based or subscription access | Acquisition, compute costs, retention. |

These are candidate business models, not measured revenue opportunities.

## Initial Conclusion Accepted by the User

On 2026-10-02, the user agreed with prioritizing a small, concrete custom-delivery offer to validate demand before investing in templates or an online tool.

Proposed progression: sample assets and a paid pilot -> repeatable delivery -> reusable workflow -> consider templates or an online service if evidence supports them.

Value depends on accepted customer outcomes and viable delivery economics. Building a workflow alone does not establish a business.

## Candidate Experiment (Not Yet Selected)

A consistent-style game-item icon set for an independent developer was discussed as an example. Neither this asset category nor this customer segment is confirmed.

Possible process: brief -> references and prompts -> candidate generation -> human selection and correction -> specification checks -> export and archive.

Before a pilot, specify asset count, style, dimensions, background, formats, acceptance criteria, delivery time, and included revisions. No price or delivery commitment has been set.

## Validation Questions

- Demand: Who needs the deliverable enough to pay for a small trial?
- Delivery: Can a second batch meet the same style and quality requirements?
- Economics: What time and cost are required per accepted asset, including failed generations, manual edits, communication, and revisions?
- Constraints: What tools, hardware, input assets, and applicable commercial-use terms need checking for the selected offer?

Track order revenue, model/compute cost, labor and rework, acquisition/platform fees, and ongoing support where applicable. No market price or profit forecast is claimed.

## Sources

Official pages consulted during the initial discussion on 2026-10-02; not re-fetched during this documentation update.

- [S1: Anthropic - Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [S2: Comfy - About Comfy](https://support.comfy.org/articles/9806306061-about-comfy)
- [S3: Comfy workflow JSON specification](https://github.com/Comfy-Org/docs/blob/main/specs/workflow_json.mdx)
- [S4: n8n - Human review for tools](https://docs.n8n.io/advanced-ai/human-in-the-loop-tools/)
- [S5: n8n Service Partner Directory](https://experts.n8n.io/)
- [S6: Comfy API deployment](https://support.comfy.org/articles/2703236295-comfy-api-deploy-your-comfyui-workflow-as-an-api)

## Local GPU Constraint Added After Initial Research

- [`M2.1.4`] The user requires the workflow to run on a local GPU. This is a selection gate for future production tools and models.
- Earlier hosted API examples demonstrate a general monetization option only; they are not a selected implementation or a required dependency for this project.
- Confirm target GPU/VRAM and runtime environment before recommending models. Compare candidates by local compatibility, output quality, peak memory, runtime, repeatability, and applicable commercial-use terms.
- For local delivery economics, record GPU time, electricity and hardware allocation where applicable, plus labor and failed attempts; do not use hosted API pricing as the sole cost model.
- Local inference is not a claim of offline capability or verified performance. These have not been tested.

## Latest User Direction: Two Stages

- [`M2.1.5`] Stage 1: produce a finished asset using the local GPU and judge its effectiveness.
- Stage 2: only if Stage 1 is effective, turn the successful production process into a reusable workflow.
- This supersedes the earlier recommendation to make a paid custom-delivery pilot the immediate next step. Paid demand and business economics remain later research topics.
- The first asset, hardware, and effectiveness criteria are still undefined. No output quality, local performance, or business outcome has been validated.
