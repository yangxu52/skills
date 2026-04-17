---
name: do
description: Structured task orchestration for larger coding work such as multi-file features, refactors, migrations, or risky changes that benefit from explicit phases, persistent task artifacts, and a separate review pass. Use when the user explicitly wants to drive a sizable task with a tracked workflow, when the task clearly needs Understand, Plan, Implement, Review, and Complete stages, or when the user wants to resume, reconnect, continue, or pick up an existing tracked task by path, slug, or task-id. Do not use for small fixes, quick questions, or simple one-file edits.
---

# do

Use this skill to drive larger coding tasks through explicit phases with durable artifacts under ` .local/tasks/ `.

## Use This Skill For

- Multi-file features, refactors, migrations, or risky edits that benefit from staged execution.
- User requests that explicitly ask to "use do", "run this as a tracked task", or otherwise want a structured workflow.
- Work that needs a separate review pass before closure.
- Interrupted tracked work that needs to reconnect to an existing task before continuing.

## Do Not Use This Skill For

- Small fixes, quick answers, or simple one-file edits.
- Tasks where the overhead of task artifacts would exceed the actual work.
- Work that is primarily brainstorming with no intent to execute.

## Workflow

1. Understand
   - Create task artifacts immediately if they do not exist yet, or reconnect to an existing task if the user is resuming work.
   - Extract requirements, constraints, acceptance criteria, non-goals, similar code paths, relevant modules, conventions, and test commands.
   - Ask the user only blocking questions. Record answers in ` phase1-understand.md `.
2. Plan
   - Produce a minimal-change implementation plan in ` phase2-plan.md `.
   - Name the files to touch, execution order, test plan, risks, and mitigations.
   - Decide whether the plan needs explicit user approval before implementation.
   - Decide whether any delegation is warranted. Default to local execution.
3. Implement
   - Execute the plan with focused changes.
   - Record what changed, notable deviations from the plan, and the narrowest relevant verification in ` phase3-implement.md `.
4. Review
   - Perform a distinct review pass for correctness, edge cases, regressions, and unnecessary complexity.
   - Record findings and disposition in ` phase4-review.md `.
   - If review drives more code changes, append the fixups back to ` phase3-implement.md `.
5. Complete
   - Write the delivery summary, modified files, verification steps, residual risks, and follow-ups in ` phase5-complete.md `.
   - Update ` task.md ` so the status and current phase reflect reality.

## Task Initialization

- Work from the target repository root so ` .local/tasks/ ` lands in the active repo rather than inside the skill library.
- If no task directory exists yet, run:

```bash
python path/to/skills/do/scripts/init_task.py "task description" --short-name two-word
```

- Initialization creates only the minimal entry artifacts:

```text
.local/tasks/<date>-<short-name>-<task-id>/
  task.md
  phase1-understand.md
  artifacts/
```

- When the task moves between phases or becomes blocked/completed, prefer:

```bash
python path/to/skills/do/scripts/update_task_status.py <task-ref> --phase phase2-plan --status in_progress
```

- ` update_task_status.py ` creates the target phase file on demand if it does not already exist.
- Use the directory naming rule ` <date>-<short-name>-<task-id> `.
- Prefer an explicit ` --short-name ` when the request is in Chinese or does not already contain clean English words.
- Reuse the same task directory throughout the whole task. Do not create a fresh directory per phase.

## Task Reconnection

- A task can be resumed by:
  - task directory path
  - full slug such as ` 2026-04-17-login-refactor-a1b2c3 `
  - unique short ` task-id ` suffix such as ` a1b2c3 `
- To inspect a task before continuing, run:

```bash
python path/to/skills/do/scripts/resume_task.py <task-ref>
```

- To resume the most recent active task, run:

```bash
python path/to/skills/do/scripts/resume_task.py --active
```

- Natural-language trigger examples for explicit use:
  - ` Use $do to resume task a1b2c3 `
  - ` Use $do to resume task 2026-04-17-login-refactor-a1b2c3 `
  - ` Use $do to reconnect task a1b2c3 `

## Artifact Rules

- Treat ` task.md ` as the task index and status file, not as a dump for every note.
- Prefer ` scripts/update_task_status.py ` over manual edits when changing `task.md` `status` or `current_phase`.
- Treat ` task.md ` as the reconnection entrypoint: it should always tell the next session where to resume.
- Keep each phase file truthful and phase-specific. Do not backfill a clean story that hides actual uncertainty or plan changes.
- Update artifacts at phase boundaries. Do not postpone all writing until the end.
- Keep detailed scratch output, logs, or generated reports in ` artifacts/ ` when they are useful but too noisy for phase files.
- Use the minimal state model unless the skill is explicitly upgraded: `in_progress`, `blocked`, `completed`.
- Treat `completed` as valid only when `current_phase` is `phase5-complete`.

## Phase Rules

### Understand

- Stop and ask the user only when a blocking ambiguity would change the implementation direction.
- Merge clarification into ` phase1-understand.md ` instead of creating a separate clarify artifact.
- Exit this phase only when the task is concrete enough to plan.

### Plan

- Favor minimal change sets, reuse of existing patterns, and the fewest new files that still keep the code clean.
- Make the plan concrete enough that implementation is a bounded execution step rather than renewed exploration.
- Do not require user approval by default.
- Record approval only when the plan includes destructive changes, architectural divergence, major dependency changes, risky public-contract changes, or multiple materially different valid paths.
- When approval is needed, stop after ` phase2-plan.md ` and ask the user to confirm before entering ` phase3-implement.md `.

### Implement

- Follow the plan, but record meaningful deviations instead of pretending the plan was perfect.
- Run the narrowest relevant checks first. Expand only when risk justifies it.

### Review

- Review is not a restatement of implementation.
- Look for correctness issues, edge cases, failure modes, behavioral regressions, and needless complexity.
- Keep findings concrete and actionable.

### Complete

- Summarize what actually shipped, how it was verified, and what remains unverified.
- Call out residual risks instead of implying full certainty.

### Reconnect

- Before resuming work, run ` scripts/resume_task.py ` or inspect ` task.md ` directly.
- Read ` task.md ` first, then the current phase file named in the resume output.
- Treat the current phase file's ` ## Next Step ` as the most execution-oriented hint for what to do next.
- If a task has drifted, update ` task.md ` and the relevant phase file before continuing implementation.

## Delegation Rules

- Default to local execution.
- Delegate only when the subtask is clearly bounded, non-trivial, and does not block the next immediate local step.
- Do not split work just to mimic parallelism.
- If delegation is used, keep ownership boundaries clear and write disjoint scopes.

## Gotchas

- Do not use this skill for tiny tasks.
- Do not move into implementation before ` phase1-understand.md ` and ` phase2-plan.md ` are concrete enough to bound the work.
- Do not let ` phase2-plan.md ` become generic advice. It must name files, order, and verification.
- Do not turn `Plan` into a mandatory approval ceremony for routine work.
- Do not let ` phase4-review.md ` collapse into an implementation summary.
- Do not bind the workflow to worktrees, specialized agents, or fixed command transcripts.
- Do not let ` task.md ` absorb all phase details.
- Do not create future phase files just because they exist in the overall workflow; create them when the task actually enters that phase.

## Validation

- Verify the task directory naming matches ` <date>-<short-name>-<task-id> `.
- Verify the current phase file exists, and that entering a later phase creates its phase file on demand.
- Verify ` task.md ` points to the current phase and final status.
- Verify ` phase5-complete.md ` contains concrete verification commands or an explicit note about what was not verified.
- Verify ` scripts/update_task_status.py ` can change both frontmatter and the `## Status` summary without desynchronizing them.
- Verify ` scripts/resume_task.py ` can resolve a task by path, full slug, or unique short ` task-id `.

## Resource Navigation

- Run ` scripts/init_task.py --help ` for task initialization options.
- Run ` scripts/update_task_status.py --help ` for status update options.
- Run ` scripts/resume_task.py --help ` for reconnection and resume options.
- Read ` references/artifact-templates.md ` when you need to recreate or repair task artifacts manually.
- Read ` references/trigger-examples.md ` when tuning whether the skill should or should not trigger.
