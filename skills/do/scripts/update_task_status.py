#!/usr/bin/env python3
"""Update do task status fields and phase artifacts safely."""

from __future__ import annotations

import argparse
import sys

from task_artifacts import (
    ALLOWED_PHASES,
    ALLOWED_STATUSES,
    DEFAULT_TASKS_DIR,
    ensure_phase_file,
    iso_now,
    load_task,
    resolve_task_reference,
    sync_task_md_content,
    write_text,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Safely update status/current_phase in a do task task.md file."
    )
    parser.add_argument(
        "task_ref",
        help="Task path, full slug, or unique task-id suffix",
    )
    parser.add_argument(
        "--tasks-dir",
        default=DEFAULT_TASKS_DIR,
        help=f"Task root directory used for slug/task-id lookup (default: {DEFAULT_TASKS_DIR})",
    )
    parser.add_argument(
        "--phase",
        choices=sorted(ALLOWED_PHASES),
        help="New current_phase value",
    )
    parser.add_argument(
        "--status",
        choices=sorted(ALLOWED_STATUSES),
        help="New status value",
    )
    return parser.parse_args()


def validate_transition(status: str, phase: str) -> None:
    if status == "completed" and phase != "phase5-complete":
        raise ValueError("status 'completed' requires current_phase 'phase5-complete'")


def main() -> int:
    args = parse_args()
    if not args.phase and not args.status:
        print("error: provide at least one of --phase or --status", file=sys.stderr)
        return 1

    try:
        task_md_path = resolve_task_reference(args.task_ref, args.tasks_dir)
        task_dir = task_md_path.parent
        frontmatter, content = load_task(task_md_path)

        new_phase = args.phase or frontmatter["current_phase"]
        new_status = args.status or frontmatter["status"]
        validate_transition(new_status, new_phase)

        ensure_phase_file(task_dir, new_phase, frontmatter["task"])
        frontmatter["current_phase"] = new_phase
        frontmatter["status"] = new_status
        frontmatter["updated_at"] = iso_now()

        updated_content = sync_task_md_content(content, frontmatter, task_dir)
        write_text(task_md_path, updated_content)
    except Exception as exc:  # pragma: no cover - CLI error surface
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Updated {task_md_path}")
    print(f"current_phase={new_phase}")
    print(f"status={new_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
