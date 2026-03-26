# Source Article Notes

Primary source:

- Thariq Shihipar, "Lessons from Building Claude Code: How We Use Skills"
- LinkedIn, published March 18, 2026
- URL: https://www.linkedin.com/pulse/lessons-from-building-claude-code-how-we-use-skills-thariq-shihipar-iclmc

This file paraphrases the article for skill-authoring use. Treat it as the primary content reference for this skill.

## What a Skill Really Is

- A skill is not just a markdown file.
- A skill is a folder that can include scripts, assets, data, and configuration.
- Strong skills use that folder structure deliberately rather than pushing everything into one file.

## The Nine Common Skill Categories

The article groups working skills into nine recurring categories:

1. Library and API reference
2. Product verification
3. Data fetching and analysis
4. Business process and team automation
5. Code scaffolding and templates
6. Code quality and review
7. CI/CD and deployment
8. Runbooks
9. Infrastructure operations

The article's practical advice is to make a skill fit one category cleanly. Skills that straddle several categories are harder to maintain and harder to trigger correctly.

## High-Signal Authoring Rules

### Do not state the obvious

- Focus on information that pushes the model away from its default habits.
- The article uses design guidance as an example: the useful part is not generic UI advice, but the specific taste adjustments and anti-patterns the model keeps missing.

### Build a gotchas section

- The article treats gotchas as the highest-signal content in a skill.
- Build this section from real failure modes, not imagined warnings.
- Keep expanding it as the skill is used.

### Use the filesystem for progressive disclosure

- Treat the filesystem as part of the context design.
- Keep the main skill file short and point to deeper files only when needed.
- Put detailed references in `references/`, templates in `assets/`, and code in `scripts/`.

### Avoid railroading

- Do not lock the agent into a brittle, overly specific path.
- Give the model the constraints and intent it needs, then leave room to adapt.

### Think through setup

- Some skills need user-specific setup, such as a preferred Slack channel.
- Persist setup data when the skill benefits from reuse.
- Ask for setup only when it is missing.

### Treat description as trigger logic

- The article is explicit that the description field is for the model.
- It is not a summary blurb.
- It should tell the model when to reach for the skill.

### Use memory carefully

- Some skills improve if they remember prior runs.
- Logs, JSON, or SQLite can all work.
- Do not assume the skill folder is a safe long-term store if upgrades may replace it.

### Give the agent code

- Scripts and helper libraries let the agent spend turns on composition rather than rebuilding boilerplate.
- This is especially useful for analysis, verification, or workflows with repeatable mechanics.

### Use hooks on demand

- Hooks are powerful when they add temporary guardrails.
- The article's examples are deliberately session-scoped, such as blocking risky commands only when doing production work.

## Distribution Guidance

- Repo-local distribution is simple and works well for smaller teams.
- Every checked-in skill adds a bit of context overhead.
- Larger organizations benefit from a curated marketplace or plugin flow.
- The article warns that bad or redundant skills are easy to create, so distribution needs curation.

## Composition and Measurement

- Skills can reference other installed skills by name.
- Measurement matters: the article describes logging skill usage to see which skills are popular and which may be under-triggering.

## Working Style Implied by the Article

- Start small.
- Use real tasks quickly.
- Iterate based on failure modes.
- Keep the best skills narrow, practical, and highly reusable.
