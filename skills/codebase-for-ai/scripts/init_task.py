#!/usr/bin/env python3
"""Create a task file from the task template.

Usage:
  python init_task.py --area-id auth-api --task-id auth-api-001 \
    --slug bug_login_refresh --type bug-fix --difficulty medium
  python init_task.py --area-id auth-api --task-id auth-api-001 \
    --slug bug_login_refresh --type bug-fix --difficulty medium \
    --repo-root /path/to/target-repo
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def target_repo_root(repo_root_arg: str | None) -> Path:
    if repo_root_arg:
        return Path(repo_root_arg).resolve()
    return Path.cwd()


def derive_filename(task_id: str, slug: str) -> str:
    match = re.search(r"(\d+)$", task_id)
    prefix = match.group(1) if match else task_id.replace("/", "_")
    return f"{prefix}_{slug}.md"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--area-id", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--slug", default="task")
    parser.add_argument("--type", dest="task_type", default="bug-fix")
    parser.add_argument("--difficulty", default="medium")
    parser.add_argument("--problem-statement", default="")
    parser.add_argument(
        "--repo-root",
        help="Target repository root where AREAS/<area>/ should be written. Defaults to the current working directory.",
    )
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    skill_dir = skill_root()
    output_root = target_repo_root(args.repo_root)
    template_path = skill_dir / "assets" / "TEMPLATES" / "TASK.md"
    output_path = output_root / "AREAS" / args.area_id / "tasks" / derive_filename(
        args.task_id, args.slug
    )

    content = template_path.read_text(encoding="utf-8")
    content = content.replace("- Task ID:", f"- Task ID: {args.task_id}", 1)
    content = content.replace("- Area ID:", f"- Area ID: {args.area_id}", 1)
    content = content.replace(
        "- Type: bug-fix | feature | refactor | test | repo-qa",
        f"- Type: {args.task_type}",
        1,
    )
    content = content.replace(
        "- Difficulty: low | medium | high",
        f"- Difficulty: {args.difficulty}",
        1,
    )
    if args.problem_statement:
        content = content.replace("## Problem statement\n", "## Problem statement\n\n", 1)
        content = content.replace("## Scope", f"{args.problem_statement}\n\n## Scope", 1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists() and not args.overwrite:
        raise SystemExit(f"{output_path} already exists. Use --overwrite to replace it.")
    output_path.write_text(content, encoding="utf-8")
    print(f"Created task template at {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
