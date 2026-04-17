#!/usr/bin/env python3
"""Summarize a do task so work can resume after an interruption."""

from __future__ import annotations

import argparse
import sys

from task_artifacts import (
    DEFAULT_TASKS_DIR,
    PHASE_FILES,
    extract_section_body,
    latest_task_md,
    load_task,
    resolve_task_reference,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Show a concise resume summary for a do task."
    )
    parser.add_argument(
        "task_ref",
        nargs="?",
        help="Task path, full slug, or unique task-id suffix",
    )
    parser.add_argument(
        "--tasks-dir",
        default=DEFAULT_TASKS_DIR,
        help=f"Task root directory used for slug/task-id lookup (default: {DEFAULT_TASKS_DIR})",
    )
    parser.add_argument(
        "--latest",
        action="store_true",
        help="Resume the most recently updated task",
    )
    parser.add_argument(
        "--active",
        action="store_true",
        help="Resume the most recently updated non-completed task",
    )
    return parser.parse_args()


def choose_task_md(args: argparse.Namespace):
    flags = sum(1 for value in (args.task_ref is not None, args.latest, args.active) if value)
    if flags != 1:
        raise ValueError("provide exactly one of task_ref, --latest, or --active")
    if args.task_ref:
        return resolve_task_reference(args.task_ref, args.tasks_dir)
    if args.latest:
        return latest_task_md(args.tasks_dir, active_only=False)
    return latest_task_md(args.tasks_dir, active_only=True)


def print_section(label: str, body: str | None) -> None:
    value = body if body else "Not recorded."
    print(f"{label}:")
    print(value)


def main() -> int:
    try:
        args = parse_args()
        task_md_path = choose_task_md(args)
        frontmatter, content = load_task(task_md_path)
        current_phase = frontmatter["current_phase"]
        current_file = PHASE_FILES[current_phase]
        phase_path = task_md_path.parent / current_file
        blockers = extract_section_body(content, "Blockers")
        phase_content = phase_path.read_text(encoding="utf-8") if phase_path.is_file() else ""
        phase_next_step = extract_section_body(phase_content, "Next Step")

        print(f"Task: {frontmatter['task']}")
        print(f"Slug: {frontmatter['slug']}")
        print(f"Status: {frontmatter['status']}")
        print(f"Current phase: {current_phase}")
        print(f"Current phase file: {current_file}")
        print(f"Started at: {frontmatter['started_at']}")
        print(f"Last updated: {frontmatter.get('updated_at', frontmatter['started_at'])}")
        print(f"Task file: {task_md_path}")
        print(f"Phase file: {phase_path}")
        print_section("Phase Next Step", phase_next_step)
        print_section("Blockers", blockers)
    except Exception as exc:  # pragma: no cover - CLI error surface
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
