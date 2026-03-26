# High-Quality Skill Checklist

## 1. Choose the Right Skill Shape

- Pick one dominant skill type.
- Prefer a clean fit over a broad umbrella skill.
- Split the skill if it clearly spans multiple categories.

Common categories from the source article:

- Library and API reference
- Product verification
- Data fetching and analysis
- Business process and team automation
- Code scaffolding and templates
- Code quality and review
- CI/CD and deployment
- Runbooks
- Infrastructure operations

## 2. Write Triggerable Metadata

- Keep the folder name and `name` field identical.
- Use lowercase letters, digits, and hyphens only.
- Write `description` for the model, not for humans browsing a catalog.
- State what the skill does, when it should trigger, and nearby requests that should not trigger it.
- Include the phrases a user would actually say.

## 3. Keep `SKILL.md` Lean

- Keep only durable instructions in the main file.
- State goal, boundaries, workflow, and resource navigation.
- Add a `Gotchas` section or equivalent high-signal failure section.
- Remove setup prose, long examples, and deep reference material from the main file.
- Avoid extra docs such as `README.md` or `CHANGELOG.md`.

## 4. Use Progressive Disclosure

- Put detailed docs and examples in `references/`.
- Put repeated or deterministic operations in `scripts/`.
- Put templates or output artifacts in `assets/`.
- Make the main file a hub that points to the right file at the right moment.

## 5. Avoid Low-Value Instructions

- Do not state the obvious.
- Do not restate generic model capabilities.
- Do not overfit the workflow to one exact command sequence.
- Do not turn the skill into a brittle checklist when flexible decision-making is needed.

## 6. Add the Right Extras

Add setup only when the skill needs stable user-specific context.

- Persist setup data if reuse matters.
- Ask for missing setup data only when needed.

Add memory only when history improves future runs.

- Use logs, JSON, or SQLite only when prior executions matter.
- Store persistent memory in a stable location if skill upgrades may replace the skill folder.

Add scripts when the agent keeps rebuilding the same logic.

- Keep scripts non-interactive.
- Provide `--help`.
- Use stdout for results and stderr for diagnostics.
- Prefer structured output and meaningful exit codes.

Add hooks only when session-scoped guardrails are useful.

- Keep risky hooks on demand.
- Avoid always-on hooks that create constant friction.

## 7. Plan Distribution and Composition

- Repo-local skills are easy to share but add context overhead.
- Marketplace or plugin distribution needs curation to avoid bad or redundant skills.
- Reference other installed skills by name when composition is useful.

## 8. Measure and Iterate

- Add should-trigger examples.
- Add should-not-trigger examples.
- Prefer gotchas learned from real failures over speculative warnings.
- Measure usage or under-triggering if the environment supports it.
- Keep iterating after real use; the first version should be small.

## 9. Validate Before Shipping

- Remove all template placeholders.
- Verify `agents/openai.yaml` matches the final skill intent.
- Run the official validator when possible.
- If the official validator is unavailable, manually verify:
  - `SKILL.md` has valid frontmatter and no stray template text.
  - The skill is readable without outside explanation.
  - Resource folders match real needs.
  - The trigger description is specific enough to fire correctly.

## 10. Bootstrap Review Questions

Use these questions to review the skill with its own rules:

- Does the description read like routing logic rather than a summary?
- Is there one dominant skill type, or is the skill trying to do several jobs at once?
- Does `SKILL.md` act as a hub rather than a long explainer?
- Is there a real `Gotchas` section with concrete failure modes?
- Are setup, memory, scripts, or hooks added only when justified?
- Would another agent understand how to use the skill without outside narration?
- Are the trigger and non-trigger expectations explicit enough to test?
