#!/usr/bin/env python3
"""Initialize tracked task artifacts for the do skill."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from uuid import uuid4

from task_artifacts import (
    DEFAULT_TASKS_DIR,
    INITIAL_PHASE,
    PHASE_FILES,
    build_slug,
    create_task_dir,
    derive_short_name,
    ensure_phase_file,
    iso_now,
    resolve_tasks_dir,
    task_md,
    write_text,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a do task directory with the initial task artifacts."
    )
    parser.add_argument("task_description", help="Human-readable task description")
    parser.add_argument(
        "--tasks-dir",
        default=DEFAULT_TASKS_DIR,
        help=f"Task root directory relative to the current repo (default: {DEFAULT_TASKS_DIR})",
    )
    parser.add_argument(
        "--date",
        dest="task_date",
        default=date.today().isoformat(),
        help="Task date in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--short-name",
        help="Two-word kebab-case short name. If omitted, derive from the description.",
    )
    parser.add_argument(
        "--task-id",
        default=uuid4().hex[:6],
        help="Short task id suffix (default: random 6-char hex)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        short_name = derive_short_name(args.task_description, args.short_name)
        slug = build_slug(args.task_date, short_name, args.task_id)
        tasks_dir = resolve_tasks_dir(args.tasks_dir)
        task_dir = create_task_dir(tasks_dir, slug)
        updated_at = iso_now()

        write_text(task_dir / "task.md", task_md(args.task_description, slug, args.task_date, updated_at))
        ensure_phase_file(task_dir, INITIAL_PHASE, args.task_description)
        (task_dir / "artifacts").mkdir()
    except Exception as exc:  # pragma: no cover - CLI error surface
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Created task directory: {task_dir}")
    print(f"Task slug: {slug}")
    print("Files:")
    print("  - task.md")
    print(f"  - {PHASE_FILES[INITIAL_PHASE]}")
    print("  - artifacts/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
