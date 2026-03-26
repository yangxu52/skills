# AGENTS Guidelines

## Scope

- Apply to ` skills/ ` and all descendants unless a deeper `AGENTS.md` overrides them.
- Treat this directory as a personal skills asset library with light curation, adaptation, and accumulation workflows.
- This repository is intentionally special: ` AGENTS.md ` may contain both execution rules and repository-specific skill working guidance when that guidance materially improves maintenance quality.

## Collaboration

- Use Simplified Chinese in collaboration messages.
- Keep changes aligned with the real directory layout.
- Prefer small, focused edits; do not mix unrelated cleanup into the same change.

## Repository Purpose

- Use this repository to accumulate reusable skill assets rather than one-off prompts.
- Prefer skills that encode stable workflows, domain judgment, practical patterns, or repeatable execution logic.
- When importing or deriving a skill from external material, rewrite it for agent use instead of preserving user-facing prose.

## Directory Rules

- Store library-level documents at the root of ` skills/ `.
- Store reusable skill packages under ` skills/skills/<skill-name>/ `.
- Keep each skill self-contained. ` SKILL.md ` is required; ` agents/ `, ` references/ `, ` scripts/ `, and ` assets/ ` are optional.
- Document any new top-level folder in ` README.md ` in the same change.

## Skill Source Types

This library may contain different kinds of skills. Keep the maintenance approach consistent with the source type:

- Hand-written skills:
  - Created directly for this library.
  - Freely revise structure and content as the skill evolves.
- Adapted skills:
  - Derived from articles, internal notes, existing prompts, or other repositories.
  - Keep the useful ideas, but rewrite for the local skill shape and local quality bar.
- Imported skills:
  - Brought in mostly intact from another source for reference or later refinement.
  - If preserving upstream shape is important, avoid casual local edits and record the source clearly inside the skill's own references.

## Documentation Rules

- Use ` AGENTS.md ` only for execution rules and constraints.
- Use ` README.md ` for repository purpose, structure, and asset inventory.
- Keep copied external guidance only when it still matches this library; otherwise rewrite or delete it.
- Keep source links and source-specific notes in skill references, not in unrelated root documents.

## Skill Writing Principles

- Focus on agent capabilities and practical usage patterns.
- Prefer content that changes what the agent will do, not generic explanation the model likely already knows.
- Ignore or aggressively compress user-facing introductions, getting-started material, installation guides, and other low-signal prose unless the skill truly depends on them.
- Keep the skill concise. Do not create extra references just to look complete.
- Use progressive disclosure: keep ` SKILL.md ` lean and move detail to ` references/ ` only when it helps.
- Organize for reuse. One skill should solve one coherent recurring job.
- Prefer concrete decision rules, examples, and failure patterns over broad theory.

## Skill Content Guidance

- ` SKILL.md ` should act as the hub:
  - purpose
  - trigger logic
  - workflow
  - boundaries
  - resource navigation
- ` references/ ` should hold detailed explanations, source notes, examples, and deeper operational knowledge.
- ` scripts/ ` should exist only when deterministic or repeated logic is worth encoding in code.
- ` assets/ ` should hold templates or output artifacts, not reference prose.

## Quality Bar For Imported Material

- Do not copy source material verbatim when synthesis is better.
- Remove stale assumptions tied to another repository, organization, or toolchain.
- Remove instructions that depend on files or workflows that do not exist here.
- Preserve the high-signal parts:
  - good trigger descriptions
  - concrete usage patterns
  - domain-specific gotchas
  - practical examples
  - validation heuristics

## Editing Rules

- Keep text files in UTF-8 without BOM and use LF line endings.
- Preserve existing skills unless the user asks to remove or replace them.
- When the directory layout changes, update affected path references in the same change.
- Remove stale or misleading derived documents when they no longer match the current skill.
- When rewriting a skill from external material, prefer restructuring over incremental patching if the original shape is fundamentally wrong for this library.
- Keep naming stable unless there is a clear triggering or discoverability benefit in renaming.

## Validation

- After moving or copying a skill, verify the target directory contains the expected files.
- After editing a skill library document, check that paths, folder names, and descriptions still match the actual structure.
- If an official validator cannot run, record the manual validation result clearly.
- After adapting an imported skill, verify that no unrelated upstream workflow terms remain in root-level library documents.
