#!/usr/bin/env python3
"""Calculate AI-Friendliness scores from one or two metrics JSON files.

Usage:
  python scripts/calculate_score.py metrics.json
  python scripts/calculate_score.py baseline.json transformed.json
  python scripts/calculate_score.py metrics.json --md-out report.md
  python scripts/calculate_score.py baseline.json transformed.json --md-out comparison.md
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict

READINESS_KEYS = [
    "boundary_entrypoints",
    "commands_env",
    "contracts",
    "context_hierarchy",
    "examples_persistence",
]

DYNAMIC_KEYS = [
    "resolve_rate",
    "valid_patch_rate",
    "regression_free_rate",
    "context_precision",
    "context_recall",
    "first_relevant_hit_rate",
    "human_intervention_free_rate",
    "review_acceptance_rate",
    "sequence_gain",
    "cost_reduction_rate",
]


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def validate_metrics(data: Dict[str, Any], path: str) -> None:
    if "readiness" not in data or "dynamic" not in data:
        raise ValueError(f"{path}: expected top-level keys 'readiness' and 'dynamic'")

    for key in READINESS_KEYS:
        if key not in data["readiness"]:
            raise ValueError(f"{path}: missing readiness key '{key}'")
        value = data["readiness"][key]
        if not isinstance(value, (int, float)) or value < 0 or value > 8:
            raise ValueError(f"{path}: readiness '{key}' must be a number in [0, 8]")

    for key in DYNAMIC_KEYS:
        if key not in data["dynamic"]:
            raise ValueError(f"{path}: missing dynamic key '{key}'")
        value = data["dynamic"][key]
        if not isinstance(value, (int, float)):
            raise ValueError(f"{path}: dynamic '{key}' must be numeric")
        if key in {"sequence_gain", "cost_reduction_rate"}:
            if value < -1 or value > 1:
                raise ValueError(f"{path}: dynamic '{key}' must be in [-1, 1]")
        else:
            if value < 0 or value > 1:
                raise ValueError(f"{path}: dynamic '{key}' must be in [0, 1]")


def compute_scores(data: Dict[str, Any]) -> Dict[str, Any]:
    r = data["readiness"]
    d = data["dynamic"]

    s1 = r["boundary_entrypoints"]
    s2 = r["commands_env"]
    s3 = r["contracts"]
    s4 = r["context_hierarchy"]
    s5 = r["examples_persistence"]
    acrs = s1 + s2 + s3 + s4 + s5

    d1 = 20 * clamp(d["resolve_rate"])
    d2 = 10 * clamp(d["valid_patch_rate"])
    d3 = 10 * clamp(d["regression_free_rate"])
    d4 = (
        5 * clamp(d["context_precision"])
        + 3 * clamp(d["context_recall"])
        + 2 * clamp(d["first_relevant_hit_rate"])
    )
    d5 = (
        3 * clamp(d["human_intervention_free_rate"])
        + 2 * clamp(d["review_acceptance_rate"])
    )
    d6 = (
        3 * clamp(d["sequence_gain"], 0.0, 1.0)
        + 2 * clamp(d["cost_reduction_rate"], 0.0, 1.0)
    )
    atps = d1 + d2 + d3 + d4 + d5 + d6
    aifs = acrs + atps

    return {
        "label": data.get("label", "unknown"),
        "ACRS": round(acrs, 2),
        "ATPS": round(atps, 2),
        "AIFS": round(aifs, 2),
        "readiness_breakdown": {
            "S1_boundary_entrypoints": round(s1, 2),
            "S2_commands_env": round(s2, 2),
            "S3_contracts": round(s3, 2),
            "S4_context_hierarchy": round(s4, 2),
            "S5_examples_persistence": round(s5, 2),
        },
        "dynamic_breakdown": {
            "D1_resolve_rate": round(d1, 2),
            "D2_valid_patch_rate": round(d2, 2),
            "D3_regression_free_rate": round(d3, 2),
            "D4_context_efficiency": round(d4, 2),
            "D5_human_dependence": round(d5, 2),
            "D6_reuse_gain": round(d6, 2),
        },
    }


def rating(aifs: float) -> str:
    if aifs >= 85:
        return "agent-ready"
    if aifs >= 70:
        return "workable with low to moderate friction"
    if aifs >= 50:
        return "partially workable, high guidance cost"
    return "human-dependent area"


def print_report(scores: Dict[str, Any]) -> None:
    print(f"Label: {scores['label']}")
    print(f"ACRS: {scores['ACRS']}/40")
    print(f"ATPS: {scores['ATPS']}/60")
    print(f"AIFS: {scores['AIFS']}/100")
    print(f"Rating: {rating(scores['AIFS'])}")
    print("\nReadiness breakdown:")
    for k, v in scores["readiness_breakdown"].items():
        print(f"  - {k}: {v}")
    print("\nDynamic breakdown:")
    for k, v in scores["dynamic_breakdown"].items():
        print(f"  - {k}: {v}")


def compare_entries(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    comparison: Dict[str, Dict[str, Any]] = {}
    for key in ["ACRS", "ATPS", "AIFS"]:
        before = float(a[key])
        after = float(b[key])
        delta = after - before
        relative_pct = (delta / before * 100.0) if before != 0 else math.inf
        comparison[key] = {
            "before": round(before, 2),
            "after": round(after, 2),
            "delta": round(delta, 2),
            "relative_pct": relative_pct if math.isinf(relative_pct) else round(relative_pct, 2),
        }
    return comparison


def compare_scores(a: Dict[str, Any], b: Dict[str, Any]) -> None:
    keys = ["ACRS", "ATPS", "AIFS"]
    print(f"Comparison: {a['label']} -> {b['label']}")
    for key in keys:
        before = float(a[key])
        after = float(b[key])
        delta = after - before
        relative = (delta / before * 100.0) if before != 0 else math.inf
        rel_str = "inf" if math.isinf(relative) else f"{relative:.2f}%"
        sign = "+" if delta >= 0 else ""
        print(f"  - {key}: {before:.2f} -> {after:.2f} ({sign}{delta:.2f}, {rel_str})")


def build_markdown_report(first: Dict[str, Any], second: Dict[str, Any] | None = None) -> str:
    lines = [
        "# SCORE REPORT",
        "",
        f"## {first['label']}",
        "",
        f"- ACRS: {first['ACRS']}/40",
        f"- ATPS: {first['ATPS']}/60",
        f"- AIFS: {first['AIFS']}/100",
        f"- Rating: {rating(float(first['AIFS']))}",
        "",
        "### Readiness breakdown",
        "",
    ]
    for key, value in first["readiness_breakdown"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "### Dynamic breakdown", ""])
    for key, value in first["dynamic_breakdown"].items():
        lines.append(f"- {key}: {value}")

    if second is None:
        return "\n".join(lines) + "\n"

    lines.extend(
        [
            "",
            f"## {second['label']}",
            "",
            f"- ACRS: {second['ACRS']}/40",
            f"- ATPS: {second['ATPS']}/60",
            f"- AIFS: {second['AIFS']}/100",
            f"- Rating: {rating(float(second['AIFS']))}",
            "",
            "### Readiness breakdown",
            "",
        ]
    )
    for key, value in second["readiness_breakdown"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "### Dynamic breakdown", ""])
    for key, value in second["dynamic_breakdown"].items():
        lines.append(f"- {key}: {value}")

    comparison = compare_entries(first, second)
    lines.extend(["", "## Comparison", ""])
    for key, values in comparison.items():
        rel = values["relative_pct"]
        rel_str = "inf" if math.isinf(rel) else f"{rel:.2f}%"
        sign = "+" if values["delta"] >= 0 else ""
        lines.append(
            f"- {key}: {values['before']:.2f} -> {values['after']:.2f} "
            f"({sign}{values['delta']:.2f}, {rel_str})"
        )
    return "\n".join(lines) + "\n"


def write_json_output(path: Path, first: Dict[str, Any], second: Dict[str, Any] | None = None) -> None:
    if second is None:
        payload: Dict[str, Any] = {"result": first}
    else:
        payload = {
            "baseline": first,
            "transformed": second,
            "comparison": compare_entries(first, second),
        }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metrics", nargs="+", help="One or two metrics JSON files")
    parser.add_argument("--json-out", help="Optional JSON output path")
    parser.add_argument("--md-out", help="Optional Markdown output path")
    args = parser.parse_args(argv[1:])
    if len(args.metrics) not in {1, 2}:
        parser.error("expected one or two metrics JSON files")
    return args


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    first_path = args.metrics[0]
    first = load_json(first_path)
    validate_metrics(first, first_path)
    first_scores = compute_scores(first)
    print_report(first_scores)

    second_scores = None
    if len(args.metrics) == 2:
        print("\n" + "=" * 72 + "\n")
        second_path = args.metrics[1]
        second = load_json(second_path)
        validate_metrics(second, second_path)
        second_scores = compute_scores(second)
        print_report(second_scores)
        print("\n" + "=" * 72 + "\n")
        compare_scores(first_scores, second_scores)

    if args.json_out:
        write_json_output(Path(args.json_out), first_scores, second_scores)

    if args.md_out:
        md_path = Path(args.md_out)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(
            build_markdown_report(first_scores, second_scores),
            encoding="utf-8",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
