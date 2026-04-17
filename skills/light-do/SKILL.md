---
name: light-do
description: Lightweight structured development workflow for small features, light refactors, moderate multi-file edits, or otherwise bounded implementation tasks that benefit from a quick Clarify, minimal Plan, Implement, Review, and Complete sequence without heavy task tracking. Use when the user explicitly asks for light-do, a lighter version of do, or a quick structured workflow, or when the task is too substantial for ad-hoc editing but may still stay light after clarification. Do not use for tiny fixes, pure brainstorming, or large risky work that clearly needs do.
---

# light-do

Use this skill for lighter software engineering work that still benefits from a structured flow, but does not justify the full weight of ` do `.

## Use This Skill For

- Small-to-medium features with a bounded target, even if the initial request needs a short clarification pass.
- Light refactors that touch several files but do not need long-lived task artifacts.
- Moderate edits where a quick clarification pass and a short plan will prevent thrash.
- User requests that explicitly ask for ` light-do `, "lighter than do", or "a quick structured workflow".

## Do Not Use This Skill For

- Tiny one-file fixes where direct execution is faster than any phase structure.
- Open-ended discovery or brainstorming with no near-term implementation.
- Large migrations, risky architecture shifts, or tasks that already clearly need persistent tracking, stronger risk control, or multi-session handling. Use ` do ` instead.

## Workflow

1. Clarify
   - Restate the goal, scope, acceptance criteria, and key assumptions in a compact form.
   - Ask the user only the questions that would materially change the implementation.
   - If the task is already clear, keep this phase to a few bullets and move on.
   - Do not escalate to ` do ` just because the starting request was a bit vague if a short clarification makes the work straightforward.
2. Plan
   - Write a minimal execution sketch before coding.
   - Name the main files or modules to touch, the intended change shape, and the narrowest checks to run.
   - Keep the plan short. This is the main upgrade gate: if the plan cannot stay light without hiding real risk, escalate to ` do ` instead of forcing light-do to carry it.
3. Implement
   - Execute the plan directly.
   - Keep changes focused and adjust the plan inline if reality differs from the initial sketch.
4. Review
   - Perform a brief but real review pass for correctness, regressions, edge cases, and needless complexity.
   - Fix obvious issues before closing instead of treating review as a separate ceremony.
5. Complete
   - Summarize what changed, how it was checked, and any residual risk or unverified area.
   - If the task expanded beyond the intended scope, say so and recommend escalating future follow-up to ` do `.

## Lightweight Rules

- Default to in-chat phase progression. Do not create ` .local/tasks/ ` artifacts by default.
- Treat Clarify and Plan as compact checkpoints, not documentation exercises.
- Keep Plan to the minimum that makes implementation predictable:
  - touched files or modules
  - intended change shape
  - narrow verification path
- Do not require user approval after Plan by default.
- Ask for approval only when the task includes destructive changes, materially different implementation paths, or public-contract risk.

## Clarify Guidance

- Pull in the best parts of requirements-driven work without turning this into a formal requirements workflow.
- Confirm:
  - what is being built or changed
  - what success looks like
  - what constraints or non-goals matter
- When needed, ask concise blocking questions before implementation.
- Do not force a scoring system, spec document, or long repository scan.

## Plan Guidance

- Plan should usually fit in a short paragraph or a few bullets.
- Favor one decisive approach over presenting multiple elaborate options.
- Prefer existing patterns and local consistency.
- Use Plan as the main escalation checkpoint.
- If the plan starts needing substantial architecture discussion, persistent artifacts, tracked phases, or staged approvals, escalate to ` do `.

## Review Guidance

- Review is still mandatory, but it stays lightweight.
- Focus on:
  - behavioral correctness
  - changed-path edge cases
  - regressions relative to nearby code
  - unnecessary abstraction or overengineering
- Report meaningful findings only. Do not pad the review.

## Escalate To do When

- Clarify no longer keeps the task lightweight; too many unresolved questions remain for a quick execution pass.
- The plan can no longer stay short without hiding real risk.
- The work needs durable artifacts, session resumption, or explicit tracked phases.
- The implementation is large enough that a separate task record and stronger review loop are warranted.

## Gotchas

- Do not turn light-do into mini-do with the same overhead under a different name.
- Do not skip Clarify just because the task looks easy; make sure the goal and acceptance are actually aligned.
- Do not escalate too early just because the initial request was a little vague; first see whether Clarify collapses it into a simple bounded task.
- Do not let Plan become vague hand-waving. Even a light plan must name the main change surface and checks.
- Do not skip Review because the task is small.
- Do not keep using light-do once the task has clearly grown into a do-sized workflow.

## Validation

- Verify the trigger description clearly differentiates light-do from both ad-hoc edits and ` do `.
- Verify the workflow remains five phases: Clarify, Plan, Implement, Review, Complete.
- Verify Plan guidance stays intentionally lighter than ` do `.
- Verify no instructions imply ` .local/tasks/ `, scripts, or heavy persistent artifacts by default.
- Verify examples include both should-trigger and should-not-trigger cases.

## Resource Navigation

- Read ` references/trigger-examples.md ` to tune invocation boundaries.
- Read ` references/source-notes.md ` for the adaptation rationale and source mapping.
