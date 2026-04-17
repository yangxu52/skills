# Source Notes

` light-do ` is adapted from two related upstream ideas:

- Claude Code ` do ` from ` stellarlinkco/myclaude `
- the lighter ` requirements ` workflow from the same repository

## Kept From do

- Explicit phase structure instead of jumping straight into code
- Separate review pass instead of treating implementation as self-justifying
- Escalation mindset when risk or uncertainty grows

## Kept From requirements

- Lighter-weight flow for clearer, smaller work
- Early clarification of requirements before coding
- Practical emphasis on implementation rather than heavy planning artifacts

## Intentionally Removed

- Multi-agent role orchestration and ` codeagent-wrapper ` assumptions
- Heavy task persistence and tracked phase files by default
- Scoring gates, repository-scan artifacts, and mandatory spec generation
- Large-plan overhead that would collapse the distinction from ` do `

## Design Decision

` light-do ` is not a miniature copy of ` do `. It is the lightweight sibling:

- still structured
- still phased
- still reviewed
- but optimized for speed, clarity, and low overhead
