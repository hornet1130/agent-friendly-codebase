#!/usr/bin/env python3
"""Calculate the readiness score for a work-area metrics JSON file.

Usage:
  python scripts/calculate_score.py metrics.json
  python scripts/calculate_score.py metrics.json --md-out report.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

READINESS_KEYS = [
    "boundary_entrypoints",
    "commands_env",
    "contracts",
    "context_hierarchy",
    "examples_persistence",
]


def load_json(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_metrics(data: dict[str, Any], path: str) -> None:
    if "context" not in data:
        raise ValueError(f"{path}: expected top-level key 'context'")
    context = data["context"]
    if not isinstance(context, dict):
        raise ValueError(f"{path}: 'context' must be an object")
    for key in ["area", "proof_path", "evidence_refs"]:
        if key not in context:
            raise ValueError(f"{path}: missing context key '{key}'")
    if not isinstance(context["area"], str) or not context["area"]:
        raise ValueError(f"{path}: context 'area' must be a non-empty string")
    if not isinstance(context["proof_path"], str) or not context["proof_path"]:
        raise ValueError(f"{path}: context 'proof_path' must be a non-empty string")
    evidence_refs = context["evidence_refs"]
    if not isinstance(evidence_refs, list) or not evidence_refs or not all(
        isinstance(item, str) and item for item in evidence_refs
    ):
        raise ValueError(
            f"{path}: context 'evidence_refs' must be a non-empty list of strings"
        )
    ambiguities = context.get("ambiguities", [])
    if not isinstance(ambiguities, list) or not all(
        isinstance(item, str) for item in ambiguities
    ):
        raise ValueError(f"{path}: context 'ambiguities' must be a list of strings")

    if "readiness" not in data:
        raise ValueError(f"{path}: expected top-level key 'readiness'")

    readiness = data["readiness"]
    if not isinstance(readiness, dict):
        raise ValueError(f"{path}: 'readiness' must be an object")

    for key in READINESS_KEYS:
        if key not in readiness:
            raise ValueError(f"{path}: missing readiness key '{key}'")
        value = readiness[key]
        if not isinstance(value, (int, float)) or value < 0 or value > 8:
            raise ValueError(f"{path}: readiness '{key}' must be a number in [0, 8]")

    if "justification" not in data:
        raise ValueError(f"{path}: expected top-level key 'justification'")
    justification = data["justification"]
    if not isinstance(justification, dict):
        raise ValueError(f"{path}: 'justification' must be an object")
    for key in READINESS_KEYS:
        if key not in justification:
            raise ValueError(f"{path}: missing justification key '{key}'")
        entry = justification[key]
        if not isinstance(entry, dict):
            raise ValueError(f"{path}: justification '{key}' must be an object")
        if "reason" not in entry:
            raise ValueError(f"{path}: justification '{key}' is missing 'reason'")
        if "evidence_refs" not in entry:
            raise ValueError(f"{path}: justification '{key}' is missing 'evidence_refs'")
        if not isinstance(entry["reason"], str) or not entry["reason"]:
            raise ValueError(
                f"{path}: justification '{key}' reason must be a non-empty string"
            )
        if not isinstance(entry["evidence_refs"], list) or not entry["evidence_refs"] or not all(
            isinstance(item, str) and item for item in entry["evidence_refs"]
        ):
            raise ValueError(
                f"{path}: justification '{key}' evidence_refs must be a non-empty list of strings"
            )


def readiness_band(acrs: float) -> dict[str, str]:
    if acrs >= 32:
        return {
            "label": "good",
            "description": "agent-friendly on static readiness",
        }
    if acrs >= 24:
        return {
            "label": "so-so",
            "description": "workable, but static friction remains",
        }
    return {
        "label": "bad",
        "description": "not yet agent-friendly on static readiness",
    }


def compute_scores(data: dict[str, Any]) -> dict[str, Any]:
    context = data["context"]
    readiness = data["readiness"]
    justification = data["justification"]
    s1 = readiness["boundary_entrypoints"]
    s2 = readiness["commands_env"]
    s3 = readiness["contracts"]
    s4 = readiness["context_hierarchy"]
    s5 = readiness["examples_persistence"]
    acrs = round(s1 + s2 + s3 + s4 + s5, 2)
    band = readiness_band(acrs)

    return {
        "label": data.get("label", "unknown"),
        "context": {
            "area": context["area"],
            "proof_path": context["proof_path"],
            "evidence_refs": list(context["evidence_refs"]),
            "ambiguities": list(context.get("ambiguities", [])),
            "coordination_scope": context.get("coordination_scope"),
        },
        "justification": {
            key: {
                "reason": justification[key]["reason"],
                "evidence_refs": list(justification[key]["evidence_refs"]),
            }
            for key in READINESS_KEYS
        },
        "ACRS": acrs,
        "band": band,
        "readiness_breakdown": {
            "S1_boundary_entrypoints": round(s1, 2),
            "S2_commands_env": round(s2, 2),
            "S3_contracts": round(s3, 2),
            "S4_context_hierarchy": round(s4, 2),
            "S5_examples_persistence": round(s5, 2),
        },
    }


def print_report(scores: dict[str, Any]) -> None:
    band = scores["band"]
    context = scores["context"]
    print(f"Label: {scores['label']}")
    print(f"Area: {context['area']}")
    print(f"Proof path: {context['proof_path']}")
    print(f"ACRS: {scores['ACRS']}/40")
    print(f"Readiness band: {band['label']}")
    print(f"Readiness summary: {band['description']}")
    print(f"Evidence refs: {len(context['evidence_refs'])}")
    if context.get("coordination_scope"):
        print(f"Coordination scope: {context['coordination_scope']}")
    if context["ambiguities"]:
        print(f"Ambiguities: {len(context['ambiguities'])}")
    print("\nReadiness breakdown:")
    for key, value in scores["readiness_breakdown"].items():
        print(f"  - {key}: {value}")
    print("\nJustification summary:")
    for key in READINESS_KEYS:
        entry = scores["justification"][key]
        print(f"  - {key}: {len(entry['evidence_refs'])} refs")


def build_markdown_report(scores: dict[str, Any]) -> str:
    band = scores["band"]
    context = scores["context"]
    lines = [
        "# SCORE REPORT",
        "",
        f"## {scores['label']}",
        "",
        f"- Area: {context['area']}",
        f"- Proof path: {context['proof_path']}",
        f"- ACRS: {scores['ACRS']}/40",
        f"- Readiness band: {band['label']}",
        f"- Readiness summary: {band['description']}",
        f"- Evidence refs: {len(context['evidence_refs'])}",
        "",
        "### Readiness breakdown",
        "",
    ]
    if context.get("coordination_scope"):
        lines.insert(8, f"- Coordination scope: {context['coordination_scope']}")
    if context["ambiguities"]:
        lines.extend(["### Ambiguities", ""])
        for item in context["ambiguities"]:
            lines.append(f"- {item}")
        lines.append("")
    for key, value in scores["readiness_breakdown"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "### Justification summary", ""])
    for key in READINESS_KEYS:
        entry = scores["justification"][key]
        lines.append(f"- {key}: {entry['reason']}")
    return "\n".join(lines) + "\n"


def write_json_output(path: Path, scores: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"result": scores}
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metrics", help="Metrics JSON file")
    parser.add_argument("--json-out", help="Optional JSON output path")
    parser.add_argument("--md-out", help="Optional Markdown output path")
    return parser.parse_args(argv[1:])


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    data = load_json(args.metrics)
    validate_metrics(data, args.metrics)
    scores = compute_scores(data)
    print_report(scores)

    if args.json_out:
        write_json_output(Path(args.json_out), scores)

    if args.md_out:
        md_path = Path(args.md_out)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(build_markdown_report(scores), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
