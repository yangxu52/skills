---
name: how-to-build-high-quality-skill
description: Create, rewrite, review, or upgrade a reusable agent skill package. Use when asked to build a new skill, improve SKILL.md, sharpen description-based triggering, add gotchas, decide what belongs in references/scripts/assets, add setup or memory or on-demand hooks, or evaluate a draft skill against high-signal authoring rules. Do not use for generic prompt writing or one-off instructions that are not meant to become a reusable skill.
---

# Build High-Quality Skills

Use this skill to author skills that trigger cleanly, stay lean, and get better through repeated use.

## Read Order

1. Read `references/build-checklist.md` first.
2. Read `references/source-article-notes.md` when you need the primary ideas, examples, or tradeoffs from the source article.
3. Use the system `skill-creator` utilities only for scaffolding, `agents/openai.yaml`, and basic validation.

## Workflow

1. Start from a real repeated task.
   - Identify the job the skill must do more than once.
   - Pick one dominant skill type.
   - Split the skill if it clearly mixes several categories.
2. Write metadata first.
   - Treat `description` as trigger logic, not a summary.
   - Include trigger phrases, adjacent non-triggers, and the exact job the skill handles.
3. Design the folder before filling content.
   - Keep `SKILL.md` as the hub.
   - Move detailed references, examples, and setup notes into `references/`.
   - Move repeated or deterministic operations into `scripts/`.
   - Move templates or output artifacts into `assets/`.
4. Write the main file for fast scanning.
   - Keep goal, boundaries, workflow, gotchas, output expectations, and resource navigation.
   - Remove background explanation that another agent does not need.
5. Add only the extras the workflow truly needs.
   - Add setup when user-specific context must be collected once and reused.
   - Add memory when previous runs improve future runs.
   - Add scripts when the agent keeps rebuilding the same logic.
   - Add hooks when temporary guardrails help during a session.
6. Validate and iterate.
   - Add should-trigger and should-not-trigger examples.
   - Test the skill with only its own files and a realistic request.
   - Update gotchas from real failures.

## Design Rules

- Do not state the obvious.
- Do not railroad the agent with brittle step-by-step command transcripts.
- Prefer reusable constraints, heuristics, and decision rules.
- Give the agent code when it keeps reconstructing boilerplate.
- Store persistent memory in a stable location if upgrading the skill may replace the skill folder.
- Keep the main file lean enough that another agent can scan it quickly.

## Output Requirements

When you produce or revise a skill, ensure the result includes:

- A precise `name` and trigger-oriented `description`
- A lean `SKILL.md` that acts as the hub
- Only the resource folders the skill actually needs
- A `Gotchas` section or equivalent failure-focused guidance
- Trigger examples, non-trigger examples, and validation notes
- `agents/openai.yaml` aligned with the final skill intent when the host supports it

## Gotchas

- Do not turn `description` into catalog copy; it is routing logic for the model.
- Do not fill `SKILL.md` with article summary, rationale, or tutorial prose that belongs in references.
- Do not create extra documents that are not part of using the skill.
- Do not invent generic gotchas; capture real failure patterns.
- Do not add scripts, memory, or hooks unless the workflow materially benefits from them.
- Do not keep a broad umbrella skill when the trigger space is actually several different skills.

## Release Checks

- Verify should-trigger and should-not-trigger examples.
- Verify the skill still works when only its own files are available.
- Verify `agents/openai.yaml` matches the final intent.
- Run the official validator when possible.
- If the validator is unavailable, run the manual checks in `references/build-checklist.md`.
- Use `references/trigger-examples.md` as the starting trigger set for this skill.

## Resource Navigation

- `references/build-checklist.md`
- `references/source-article-notes.md`
- `references/trigger-examples.md`
