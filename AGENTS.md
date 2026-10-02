# Project Agents Guide

## Purpose

This directory is the root of the game-arts project. Keep project documentation and future implementation inside this directory.

The goal is to keep project context, tasks, and decisions organized so that future work can continue smoothly.

## Scope

- This file applies to the current project directory and its subdirectories
- Keep all project-specific content inside this directory
- Do not mix content from other projects into this folder

## Read First

Before doing substantial work, read files in this order:

1. `README.md`
2. `context/project-overview.md`
3. `context/research-notes.md` for exploratory projects
4. `tasks/active.md`
5. `tasks/decisions.md`
6. `tasks/milestones.md` for milestone scope and stable task IDs
7. `context/architecture.md` if technical context is needed

## Directory Rules

- `context/` stores stable background knowledge
- `context/research-notes.md` stores exploratory notes, open questions, and interim findings
- `tasks/` stores active work, backlog, and decisions
- `prompts/` stores prompts worth reusing
- `logs/` stores chronological work notes
- Prefer updating an existing document over creating a duplicate one

## Working Rules

- Use English for AI-maintained project documents unless the user explicitly asks for another language
- Use Chinese for conversation by default unless the user requests another language
- Prefer small, clear, reversible changes
- Briefly explain intended edits before changing files
- Use existing project docs to infer context before asking questions
- If assumptions are made, state them clearly
- Stay within the current task scope unless the user asks for broader changes
- For exploratory work, prefer fact gathering, concept clarification, and question framing before solutioning
- Distinguish clearly between facts, assumptions, open questions, and recommendations
- If normal file editing is blocked by the environment but the user has clearly requested the change, escalation may be used to complete the requested write safely

## Documentation Rules

- Put stable knowledge in `context/`
- Put exploratory background learning and research notes in `context/research-notes.md`
- Put current execution status in `tasks/`
- Record important decisions in `tasks/decisions.md`
- Add reusable prompts only when they are likely to help again
- Update docs after meaningful work so the next collaborator can continue quickly

## Task Management

- Read `tasks/milestones.md` before planning or implementation.
- Classify the project as simple or complex.
- For a complex project, define and approve the known milestone sequence `M1` through `Mn` before implementation begins.
- Use `M<n>` for milestones, `M<n>.<s>` for subgoals, and `M<n>.<s>.<t>` for executable tasks.
- Add a fourth numeric level only when an executable task requires further decomposition.
- Assign IDs sequentially within their parent; never renumber or reuse an ID after progress reporting or implementation begins.
- Keep cancelled or superseded IDs and mark their final state.
- Reference the most specific applicable ID in active status, backlog, decisions, implementation notes, tests, and work-log entries.
- Add new requests or ideas to `tasks/backlog.md`
- Track in-progress work in `tasks/active.md`
- Move major conclusions or tradeoffs into `tasks/decisions.md`
- Record notable progress in `logs/worklog.md`

## Naming Rules

- Use `YYYY-MM-DD` for dates
- Prefer short and descriptive file names
- Keep files in Markdown or plain text unless another format is necessary

## Safety

- Never delete files unless the user explicitly confirms the deletion; stop and ask first.
- Before any dangerous command, show the exact command, explain its purpose and possible risks, and ask the user to reply exactly `CONFIRMED`. Proceed only after that confirmation. Commands listed in an applicable `CODEX_DANGEROUS_COMMANDS.md` are dangerous. The global command list is available at `C:\Users\hp\.codex\CODEX_DANGEROUS_COMMANDS.md`; read it before evaluating potentially dangerous commands.
- Preserve user-authored content unless edits are requested
- Avoid broad rewrites when a targeted update is sufficient

## Output Style

- Be concise, practical, and easy to scan
- Surface assumptions, risks, and next steps when useful
- Favor actionable summaries over long restatements

## Windows Editing

- Prefer PowerShell overwrite writes for template-derived Markdown or text when patching is unreliable because of encoding, BOM, or line-ending mismatches.

## Automatic Commit Checkpoints

- The user authorizes normal, non-force Git commits after a coherent amount of task-owned work has accumulated, when working in a Git repository.
- Use completion of an independently testable numbered task, subtask, or implementation slice as the default checkpoint.
- During a long slice, create a checkpoint before changing modules or repositories, before risky packaging or migration work, or when the relevant working set reaches roughly eight files.
- Before each commit, inspect the actual diff, run the narrowest meaningful verification, and stage only task-owned files.
- Keep separate repositories in separate commits. Exclude unrelated changes, generated packages, credentials, local data, and ignored artifacts.
- Do not create a normal completion commit for known failing or incoherent code. Use a clearly labeled checkpoint only when preserving substantial incomplete work is materially safer, and record the remaining failure.
- This authorization covers `git add` and normal `git commit` only; it does not authorize force operations, history rewriting, destructive Git commands, or automatic push.
