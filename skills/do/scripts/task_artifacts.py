#!/usr/bin/env python3
"""Shared helpers for do task artifacts."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path


DEFAULT_TASKS_DIR = ".local/tasks"
INITIAL_PHASE = "phase1-understand"
PHASE_ORDER = [
    "phase1-understand",
    "phase2-plan",
    "phase3-implement",
    "phase4-review",
    "phase5-complete",
]
PHASE_TITLES = {
    "phase1-understand": "Phase 1 Understand",
    "phase2-plan": "Phase 2 Plan",
    "phase3-implement": "Phase 3 Implement",
    "phase4-review": "Phase 4 Review",
    "phase5-complete": "Phase 5 Complete",
}
PHASE_FILES = {phase: f"{phase}.md" for phase in PHASE_ORDER}
PHASE_FILENAMES = tuple(PHASE_FILES.values())
ALLOWED_PHASES = set(PHASE_ORDER)
ALLOWED_STATUSES = {
    "in_progress",
    "blocked",
    "completed",
}
FRONTMATTER_RE = re.compile(r"\A---\n(?P<frontmatter>.*?)\n---\n", re.DOTALL)
SECTION_RE_TEMPLATE = r"(?ms)^## {heading}\n\n.*?(?=^## |\Z)"
KNOWN_FRONTMATTER_ORDER = [
    "task",
    "slug",
    "status",
    "current_phase",
    "started_at",
    "updated_at",
]


def iso_now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def normalize_short_name(value: str) -> str:
    words = re.findall(r"[a-z0-9]+", value.lower())
    if not words:
        return "task-work"
    if len(words) == 1:
        words.append("work")
    return "-".join(words[:2])


def derive_short_name(task_description: str, provided: str | None) -> str:
    if provided:
        return normalize_short_name(provided)
    return normalize_short_name(task_description)


def build_slug(task_date: str, short_name: str, task_id: str) -> str:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", task_date):
        raise ValueError("--date must use YYYY-MM-DD")
    cleaned_id = re.sub(r"[^a-z0-9]", "", task_id.lower())
    if not cleaned_id:
        raise ValueError("--task-id must contain at least one alphanumeric character")
    return f"{task_date}-{short_name}-{cleaned_id[:8]}"


def parse_frontmatter(content: str) -> tuple[dict[str, str], tuple[int, int]]:
    match = FRONTMATTER_RE.match(content)
    if not match:
        raise ValueError("task.md must start with YAML frontmatter")
    frontmatter: dict[str, str] = {}
    for line in match.group("frontmatter").splitlines():
        if not line.strip():
            continue
        key, sep, raw_value = line.partition(":")
        if not sep:
            raise ValueError(f"invalid frontmatter line: {line}")
        frontmatter[key.strip()] = json.loads(raw_value.strip())
    return frontmatter, match.span("frontmatter")


def render_frontmatter(frontmatter: dict[str, str]) -> str:
    lines: list[str] = []
    seen: set[str] = set()
    for key in KNOWN_FRONTMATTER_ORDER:
        if key in frontmatter:
            lines.append(f"{key}: {yaml_string(frontmatter[key])}")
            seen.add(key)
    for key, value in frontmatter.items():
        if key not in seen:
            lines.append(f"{key}: {yaml_string(value)}")
    return "\n".join(lines)


def replace_frontmatter(content: str, frontmatter: dict[str, str]) -> str:
    _, (start, end) = parse_frontmatter(content)
    return content[:start] + render_frontmatter(frontmatter) + content[end:]


def section_pattern(heading: str) -> re.Pattern[str]:
    return re.compile(SECTION_RE_TEMPLATE.format(heading=re.escape(heading)))


def replace_or_append_section(content: str, heading: str, body: str) -> str:
    section = f"## {heading}\n\n{body.strip()}\n\n"
    pattern = section_pattern(heading)
    if pattern.search(content):
        return pattern.sub(section, content, count=1)
    if not content.endswith("\n"):
        content += "\n"
    return content.rstrip() + "\n\n" + section


def existing_phase_files(task_dir: Path) -> list[str]:
    return [filename for filename in PHASE_FILENAMES if (task_dir / filename).is_file()]


def render_status_section(current_phase: str, status: str, updated_at: str) -> str:
    return "\n".join(
        [
            f"- Current phase: `{current_phase}`",
            f"- Overall status: `{status}`",
            f"- Last updated: `{updated_at}`",
            "",
            "Use `scripts/update_task_status.py` to keep these fields synchronized.",
        ]
    )


def render_current_artifacts_section(phase_files: list[str]) -> str:
    lines = [f"- [{filename}]({filename})" for filename in phase_files]
    lines.append("- `artifacts/`")
    return "\n".join(lines)


def render_resume_snapshot_section(current_phase: str, status: str, updated_at: str) -> str:
    current_file = PHASE_FILES[current_phase]
    return "\n".join(
        [
            f"- Status: `{status}`",
            f"- Current phase: `{current_phase}`",
            f"- Current phase file: `{current_file}`",
            f"- Last updated: `{updated_at}`",
        ]
    )


def task_md(task_description: str, slug: str, task_date: str, updated_at: str) -> str:
    frontmatter = render_frontmatter(
        {
            "task": task_description,
            "slug": slug,
            "status": "in_progress",
            "current_phase": INITIAL_PHASE,
            "started_at": task_date,
            "updated_at": updated_at,
        }
    )
    return f"""---
{frontmatter}
---

# Task

## Goal

{task_description}

## Scope

- [ ] Fill in scope boundaries during Phase 1.

## Status

{render_status_section(INITIAL_PHASE, "in_progress", updated_at)}

## Current Artifacts

{render_current_artifacts_section([PHASE_FILES[INITIAL_PHASE]])}

## Resume Snapshot

{render_resume_snapshot_section(INITIAL_PHASE, "in_progress", updated_at)}

## Blockers

- None recorded.

## Final Summary

Pending.
"""


def phase1_md(task_description: str) -> str:
    return f"""# Phase 1 Understand

## Goal

Build a concrete understanding of the task before planning or changing code.

## Inputs

- Task: {task_description}

## Requirements

## Constraints

## Non-goals

## Codebase Findings

## Blocking Questions

## Clarifications

## Exit Criteria

- [ ] The task is concrete enough to plan.
- [ ] Blocking questions are resolved or explicitly deferred.

## Next Step

Move to `phase2-plan.md`.
"""


def phase2_md() -> str:
    return """# Phase 2 Plan

## Goal

Turn the understanding into a bounded, minimal-change execution plan.

## Change Strategy

## Files to Touch

## Execution Order

## Test Plan

## Risks

## Mitigations

## Approval Need

- No approval required yet.

## Why Approval Is Needed

- Record this only when the plan should stop for explicit user confirmation.

## Approval Status

- `not_needed`

## Delegation Decision

## Exit Criteria

- [ ] The change set is concrete enough to implement.
- [ ] Verification steps are identified.

## Next Step

Move to `phase3-implement.md`.
"""


def phase3_md() -> str:
    return """# Phase 3 Implement

## Goal

Implement the planned changes and record meaningful deviations.

## Planned Changes

## Changes Made

## Deviations From Plan

## Commands Run

## Verification Summary

## Review Fixups

## Exit Criteria

- [ ] Planned changes are implemented or deferred with justification.
- [ ] Relevant checks have been run or explicitly skipped.

## Next Step

Move to `phase4-review.md`.
"""


def phase4_md() -> str:
    return """# Phase 4 Review

## Goal

Run a distinct review pass for correctness, regressions, and needless complexity.

## Correctness Findings

## Complexity Findings

## Regression Risks

## Required Fixes

## Review Outcome

## Next Step

Move to `phase5-complete.md`.
"""


def phase5_md() -> str:
    return """# Phase 5 Complete

## Outcome

## Key Decisions

## Modified Files

## Verification

## Residual Risks

## Follow-ups
"""


def phase_content(phase: str, task_description: str) -> str:
    if phase == "phase1-understand":
        return phase1_md(task_description)
    if phase == "phase2-plan":
        return phase2_md()
    if phase == "phase3-implement":
        return phase3_md()
    if phase == "phase4-review":
        return phase4_md()
    if phase == "phase5-complete":
        return phase5_md()
    raise ValueError(f"unknown phase: {phase}")


def ensure_phase_file(task_dir: Path, phase: str, task_description: str) -> Path:
    if phase not in ALLOWED_PHASES:
        raise ValueError(f"unknown phase: {phase}")
    phase_path = task_dir / PHASE_FILES[phase]
    if not phase_path.exists():
        write_text(phase_path, phase_content(phase, task_description))
    return phase_path


def create_task_dir(base_dir: Path, slug: str) -> Path:
    base_dir.mkdir(parents=True, exist_ok=True)
    task_dir = base_dir / slug
    if task_dir.exists():
        raise FileExistsError(f"Task directory already exists: {task_dir}")
    task_dir.mkdir()
    return task_dir


def resolve_tasks_dir(tasks_dir: str) -> Path:
    return Path(tasks_dir).expanduser().resolve()


def resolve_task_reference(task_ref: str, tasks_dir: str = DEFAULT_TASKS_DIR) -> Path:
    candidate = Path(task_ref).expanduser()
    if candidate.exists():
        resolved = candidate.resolve()
        if resolved.is_dir():
            task_md_path = resolved / "task.md"
        else:
            task_md_path = resolved
        if not task_md_path.is_file():
            raise FileNotFoundError(f"task.md not found: {task_md_path}")
        return task_md_path

    root = resolve_tasks_dir(tasks_dir)
    if not root.exists():
        raise FileNotFoundError(f"tasks directory not found: {root}")

    exact = root / task_ref / "task.md"
    if exact.is_file():
        return exact

    matches: list[Path] = []
    for entry in root.iterdir():
        if not entry.is_dir():
            continue
        if entry.name == task_ref or entry.name.endswith(f"-{task_ref}"):
            task_md_path = entry / "task.md"
            if task_md_path.is_file():
                matches.append(task_md_path)

    if not matches:
        raise FileNotFoundError(f"task reference not found: {task_ref}")
    if len(matches) > 1:
        refs = ", ".join(path.parent.name for path in matches)
        raise ValueError(f"task reference is ambiguous: {task_ref} -> {refs}")
    return matches[0]


def load_task(task_md_path: Path) -> tuple[dict[str, str], str]:
    content = task_md_path.read_text(encoding="utf-8")
    frontmatter, _ = parse_frontmatter(content)
    for key in ("task", "slug", "status", "current_phase", "started_at"):
        if key not in frontmatter:
            raise ValueError(f"required frontmatter key missing: {key}")
    return frontmatter, content


def sync_task_md_content(
    content: str,
    frontmatter: dict[str, str],
    task_dir: Path,
) -> str:
    updated = replace_frontmatter(content, frontmatter)
    phase_files = existing_phase_files(task_dir)
    updated = replace_or_append_section(
        updated,
        "Status",
        render_status_section(
            frontmatter["current_phase"],
            frontmatter["status"],
            frontmatter["updated_at"],
        ),
    )
    updated = replace_or_append_section(
        updated,
        "Current Artifacts",
        render_current_artifacts_section(phase_files),
    )
    updated = replace_or_append_section(
        updated,
        "Resume Snapshot",
        render_resume_snapshot_section(
            frontmatter["current_phase"],
            frontmatter["status"],
            frontmatter["updated_at"],
        ),
    )
    return updated


def latest_task_md(tasks_dir: str, active_only: bool = False) -> Path:
    root = resolve_tasks_dir(tasks_dir)
    if not root.exists():
        raise FileNotFoundError(f"tasks directory not found: {root}")

    candidates: list[tuple[str, Path]] = []
    for entry in root.iterdir():
        if not entry.is_dir():
            continue
        task_md_path = entry / "task.md"
        if not task_md_path.is_file():
            continue
        frontmatter, _ = load_task(task_md_path)
        if active_only and frontmatter["status"] == "completed":
            continue
        candidates.append((frontmatter.get("updated_at", frontmatter["started_at"]), task_md_path))

    if not candidates:
        qualifier = "active " if active_only else ""
        raise FileNotFoundError(f"no {qualifier}tasks found under {root}")
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


def extract_section_body(content: str, heading: str) -> str | None:
    pattern = re.compile(
        rf"(?ms)^## {re.escape(heading)}\n\n(?P<body>.*?)(?=^## |\Z)"
    )
    match = pattern.search(content)
    if not match:
        return None
    return match.group("body").strip()
