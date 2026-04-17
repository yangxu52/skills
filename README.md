# Personal Skills Library

This directory is my personal library of reusable skill assets. The root holds library-level documents and future shared materials. Actual skill packages live under `skills/` so the library can grow without collapsing everything into one flat folder.

## Layout

- `AGENTS.md`: execution rules for this library
- `README.md`: library overview and maintenance notes
- `skills/`: actual skill packages

## Asset Types

This library can contain several kinds of skill assets:

- Hand-written skills: created directly for this library
- Adapted skills: rewritten from articles, notes, prompts, or other repositories
- Imported skills: copied in mostly intact for reference or later refinement

The goal is not to collect raw prompts. The goal is to accumulate reusable, high-signal skill packages.

## Conventions

- Add each reusable skill as its own folder under `skills/`.
- Keep each skill self-contained and follow the standard skill shape: `SKILL.md` plus only the resource folders it actually needs.
- Keep root-level files focused on the library as a whole, not on one individual skill.
- When adding a new top-level folder for non-skill assets, document its purpose here.

## Inclusion Criteria

Prefer adding a skill when it captures one or more of the following:

- a stable repeated workflow
- domain judgment or taste that generic models often miss
- reusable decision rules
- practical gotchas from real usage
- deterministic logic worth encoding in scripts

Avoid adding material that is only:

- a one-off instruction
- generic background explanation
- a copied user guide with little adaptation
- a prompt fragment that is not a reusable skill package

## Current Inventory

| Name                              | Type    | Purpose                                                           | Status | Source                                    |
| --------------------------------- | ------- | ----------------------------------------------------------------- | ------ | ----------------------------------------- |
| `do`                              | adapted | Orchestrate larger coding tasks through tracked phases and review | active | Claude Code `do` skill, rebuilt for Codex |
| `how-to-build-high-quality-skill` | adapted | Author and review high-quality reusable agent skills              | active | Thariq Shihipar, LinkedIn, 2026-03-18     |

## Maintenance

- Keep skill descriptions trigger-oriented so they remain discoverable and useful.
- Prefer concise, high-signal references over copied external prose.
- When a skill is revised from an external source, keep the source notes inside that skill's own reference files.
- Remove stale assumptions that belong to another repository, organization, or toolchain.
- Update this file when new top-level folders or notable skills are added.
