# Artifact Templates

Use these templates when task artifacts need to be created or repaired manually. Prefer ` scripts/init_task.py ` for normal initialization.

## Status Model

- Allowed `status` values: `in_progress`, `blocked`, `completed`
- Allowed `current_phase` values:
  - `phase1-understand`
  - `phase2-plan`
  - `phase3-implement`
  - `phase4-review`
  - `phase5-complete`
- Keep YAML frontmatter and the `## Status` bullets synchronized.
- Prefer ` scripts/update_task_status.py ` for status changes instead of hand-editing `task.md`.
- Only mark a task `completed` when `current_phase` is `phase5-complete`.
- Add `updated_at` and keep it fresh on every phase/status transition so resume works after interruptions.

## Directory Shape

Initial:

```text
.local/tasks/<date>-<short-name>-<task-id>/
  task.md
  phase1-understand.md
  artifacts/
```

Later phases are created only when the task enters them:

```text
.local/tasks/<date>-<short-name>-<task-id>/
  phase2-plan.md
  phase3-implement.md
  phase4-review.md
  phase5-complete.md
  artifacts/
```

## task.md

```md
---
task: "..."
slug: "2026-04-17-login-refactor-a1b2c3"
status: "in_progress"
current_phase: "phase1-understand"
started_at: "2026-04-17"
updated_at: "2026-04-17T10:20:30"
---

# Task

## Goal

## Scope

## Status

## Current Artifacts
- [phase1-understand.md](phase1-understand.md)
- `artifacts/`

## Resume Snapshot

## Blockers

## Final Summary
```

To repair status fields manually, update both of these areas together:

- Frontmatter:
  - `status: "..."`
  - `current_phase: "..."`
  - `updated_at: "..."`
- Body:
  - `- Current phase: `...``
  - `- Overall status: `...``
  - `- Last updated: `...``

To reconnect manually, start from:

1. `task.md`
2. the phase file named in `## Resume Snapshot`
3. the current phase file's `## Next Step`
4. `## Blockers`

## phase1-understand.md

```md
# Phase 1 Understand

## Goal

## Inputs

## Requirements

## Constraints

## Non-goals

## Codebase Findings

## Blocking Questions

## Clarifications

## Exit Criteria

## Next Step
```

## phase2-plan.md

```md
# Phase 2 Plan

## Goal

## Change Strategy

## Files to Touch

## Execution Order

## Test Plan

## Risks

## Mitigations

## Approval Need

## Why Approval Is Needed

## Approval Status

## Delegation Decision

## Exit Criteria

## Next Step
```

## phase3-implement.md

```md
# Phase 3 Implement

## Goal

## Planned Changes

## Changes Made

## Deviations From Plan

## Commands Run

## Verification Summary

## Review Fixups

## Exit Criteria

## Next Step
```

## phase4-review.md

```md
# Phase 4 Review

## Goal

## Correctness Findings

## Complexity Findings

## Regression Risks

## Required Fixes

## Review Outcome

## Next Step
```

## phase5-complete.md

```md
# Phase 5 Complete

## Outcome

## Key Decisions

## Modified Files

## Verification

## Residual Risks

## Follow-ups
```
