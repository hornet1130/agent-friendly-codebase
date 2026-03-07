#!/usr/bin/env python3
"""Initialize a work-area scaffold inside a target repository's AREAS/.

Usage:
  python init_area.py --area-id auth-api \
    --human-name "Authentication API module" \
    --primary-path apps/api/src/modules/auth
  python init_area.py --area-id auth-api \
    --human-name "Authentication API module" \
    --primary-path apps/api/src/modules/auth \
    --profile-template AREA_PROFILE.node-monorepo.md
  python init_area.py --area-id auth-api \
    --human-name "Authentication API module" \
    --primary-path apps/api/src/modules/auth \
    --repo-root /path/to/target-repo
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def target_repo_root(repo_root_arg: str | None) -> Path:
    if repo_root_arg:
        return Path(repo_root_arg).resolve()
    return Path.cwd()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str, overwrite: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return
    path.write_text(content, encoding="utf-8")


def initialize_profile(
    template: str,
    area_id: str,
    human_name: str,
    primary_path: str,
) -> str:
    replacements = {
        "- Area ID:": f"- Area ID: {area_id}",
        "- Human name:": f"- Human name: {human_name}",
        "- Primary paths:": f"- Primary paths: `{primary_path}`",
    }
    lines = []
    for line in template.splitlines():
        replaced = line
        for marker, value in replacements.items():
            if line.startswith(marker):
                replaced = value
                break
        lines.append(replaced)
    return "\n".join(lines) + "\n"


def initialize_report(template: str, area_id: str, state: str) -> str:
    content = template
    content = content.replace("- Area ID:", f"- Area ID: {area_id}", 1)
    content = content.replace("- State: baseline | transformed", f"- State: {state}", 1)
    return content


def metrics_stub(label: str) -> dict:
    return {
        "label": label,
        "evaluation_mode": "audit-only",
        "readiness": {
            "boundary_entrypoints": 0,
            "commands_env": 0,
            "contracts": 0,
            "context_hierarchy": 0,
            "examples_persistence": 0,
        },
        "dynamic": None,
        "missing_measurements": [
            "Dynamic task runs have not been executed yet.",
            "Set evaluation_mode to 'full' and add dynamic metrics after running the task set.",
        ],
        "notes": "Replace placeholder values with measured data before using them as evidence.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--area-id", required=True)
    parser.add_argument("--human-name", required=True)
    parser.add_argument("--primary-path", required=True)
    parser.add_argument(
        "--profile-template",
        default="AREA_PROFILE.md",
        help="Template file name under assets/TEMPLATES/ or an absolute/relative file path",
    )
    parser.add_argument(
        "--repo-root",
        help="Target repository root where AREAS/<area>/ should be written. Defaults to the current working directory.",
    )
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    skill_dir = skill_root()
    output_root = target_repo_root(args.repo_root)
    area_dir = output_root / "AREAS" / args.area_id
    tasks_dir = area_dir / "tasks"
    reports_dir = area_dir / "reports"
    metrics_dir = area_dir / "metrics"

    template_path = Path(args.profile_template)
    if not template_path.is_absolute():
        candidate = skill_dir / "assets" / "TEMPLATES" / args.profile_template
        template_path = candidate if candidate.exists() else Path(args.profile_template).resolve()
    if not template_path.exists():
        raise SystemExit(f"Profile template not found: {args.profile_template}")

    profile_template = read_text(template_path)
    report_template = read_text(skill_dir / "assets" / "TEMPLATES" / "EVALUATION_REPORT.md")

    write_text(
        area_dir / "PROFILE.md",
        initialize_profile(
            profile_template,
            area_id=args.area_id,
            human_name=args.human_name,
            primary_path=args.primary_path,
        ),
        overwrite=args.overwrite,
    )
    tasks_dir.mkdir(parents=True, exist_ok=True)
    write_text(
        reports_dir / "baseline.md",
        initialize_report(report_template, args.area_id, "baseline"),
        overwrite=args.overwrite,
    )
    write_text(
        reports_dir / "transformed.md",
        initialize_report(report_template, args.area_id, "transformed"),
        overwrite=args.overwrite,
    )
    write_text(
        reports_dir / "comparison.md",
        "# COMPARISON REPORT\n\n"
        "Generate this file after both metrics files are measured.\n\n"
        "Suggested command:\n\n"
        f"`python /path/to/codebase-for-ai/scripts/calculate_score.py AREAS/{args.area_id}/metrics/baseline.json "
        f"AREAS/{args.area_id}/metrics/transformed.json --md-out AREAS/{args.area_id}/reports/comparison.md`\n",
        overwrite=args.overwrite,
    )

    for state in ("baseline", "transformed"):
        metrics_path = metrics_dir / f"{state}.json"
        if not metrics_path.exists() or args.overwrite:
            metrics_path.parent.mkdir(parents=True, exist_ok=True)
            metrics_path.write_text(
                json.dumps(metrics_stub(f"{args.area_id}-{state}"), indent=2) + "\n",
                encoding="utf-8",
            )

    print(f"Initialized work area scaffold at {area_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
