#!/usr/bin/env python3
"""Validate a codebase-for-ai self-eval run file and emit metrics JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


EXPECTED_TASK_IDS = [f"SE-{index:03d}" for index in range(1, 9)]
READINESS_KEYS = [
    "boundary_entrypoints",
    "commands_env",
    "contracts",
    "context_hierarchy",
    "examples_persistence",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def has_placeholder(value: Any) -> bool:
    if isinstance(value, str):
        return value.startswith("REPLACE_WITH_")
    if isinstance(value, list):
        return any(has_placeholder(item) for item in value)
    if isinstance(value, dict):
        return any(has_placeholder(item) for item in value.values())
    return False


def validate_readiness(readiness: dict[str, Any]) -> None:
    for key in READINESS_KEYS:
        if key not in readiness:
            raise ValueError(f"missing readiness key '{key}'")
        value = readiness[key]
        if not isinstance(value, (int, float)) or value < 0 or value > 8:
            raise ValueError(f"readiness '{key}' must be a number in [0, 8]")


def validate_task(task: dict[str, Any]) -> None:
    required_keys = [
        "task_id",
        "task_type",
        "resolved",
        "valid_patch",
        "regression_free",
        "files_read",
        "gold_files",
        "first_relevant_read_index",
        "human_intervention_needed",
        "review_accepted",
    ]
    for key in required_keys:
        if key not in task:
            raise ValueError(f"task is missing required key '{key}'")

    for key in [
        "resolved",
        "valid_patch",
        "regression_free",
        "human_intervention_needed",
        "review_accepted",
    ]:
        if not isinstance(task[key], bool):
            raise ValueError(f"{task['task_id']}: '{key}' must be boolean")

    for key in ["files_read", "gold_files"]:
        value = task[key]
        if not isinstance(value, list) or not value or not all(
            isinstance(item, str) and item for item in value
        ):
            raise ValueError(f"{task['task_id']}: '{key}' must be a non-empty list of strings")

    index = task["first_relevant_read_index"]
    if not isinstance(index, int):
        raise ValueError(f"{task['task_id']}: 'first_relevant_read_index' must be an integer")
    if index < 0 or index > len(task["files_read"]):
        raise ValueError(
            f"{task['task_id']}: first_relevant_read_index must be 0 or within the files_read range"
        )
    if index > 0 and task["files_read"][index - 1] not in set(task["gold_files"]):
        raise ValueError(
            f"{task['task_id']}: first_relevant_read_index must point to a relevant file"
        )


def ordered_unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    unique_items: list[str] = []
    for item in items:
        if item not in seen:
            unique_items.append(item)
            seen.add(item)
    return unique_items


def compute_context_metrics(task: dict[str, Any]) -> tuple[float, float, float]:
    files_read = ordered_unique(task["files_read"])
    gold_files = ordered_unique(task["gold_files"])
    overlap = set(files_read) & set(gold_files)

    precision = len(overlap) / len(files_read)
    recall = len(overlap) / len(gold_files)

    first_hit = task["first_relevant_read_index"]
    if first_hit == 0:
        first_relevant_hit_rate = 0.0
    else:
        first_relevant_hit_rate = (len(files_read) - first_hit + 1) / len(files_read)

    return precision, recall, first_relevant_hit_rate


def average(values: list[float]) -> float:
    return sum(values) / len(values)


def validate_run(data: dict[str, Any]) -> None:
    if has_placeholder(data):
        raise ValueError("self-eval run still contains template placeholder values")
    if "label" not in data or not isinstance(data["label"], str) or not data["label"]:
        raise ValueError("top-level 'label' must be a non-empty string")
    if "readiness" not in data or not isinstance(data["readiness"], dict):
        raise ValueError("top-level 'readiness' must be an object")
    validate_readiness(data["readiness"])

    tasks = data.get("tasks")
    if not isinstance(tasks, list):
        raise ValueError("top-level 'tasks' must be a list")
    if len(tasks) != len(EXPECTED_TASK_IDS):
        raise ValueError(f"expected {len(EXPECTED_TASK_IDS)} tasks, found {len(tasks)}")

    task_ids: list[str] = []
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("each task must be an object")
        validate_task(task)
        task_ids.append(task["task_id"])

    if sorted(task_ids) != EXPECTED_TASK_IDS:
        raise ValueError("duplicate or unexpected task ids in self-eval run")

    for key in ["sequence_gain", "cost_reduction_rate"]:
        value = data.get(key, 0.0)
        if not isinstance(value, (int, float)) or value < -1 or value > 1:
            raise ValueError(f"top-level '{key}' must be numeric in [-1, 1]")


def build_metrics(data: dict[str, Any]) -> dict[str, Any]:
    tasks = data["tasks"]
    precisions: list[float] = []
    recalls: list[float] = []
    first_hits: list[float] = []

    for task in tasks:
        precision, recall, first_hit = compute_context_metrics(task)
        precisions.append(precision)
        recalls.append(recall)
        first_hits.append(first_hit)

    total_tasks = len(tasks)
    dynamic = {
        "resolve_rate": sum(task["resolved"] for task in tasks) / total_tasks,
        "valid_patch_rate": sum(task["valid_patch"] for task in tasks) / total_tasks,
        "regression_free_rate": sum(task["regression_free"] for task in tasks) / total_tasks,
        "context_precision": average(precisions),
        "context_recall": average(recalls),
        "first_relevant_hit_rate": average(first_hits),
        "human_intervention_free_rate": sum(
            not task["human_intervention_needed"] for task in tasks
        )
        / total_tasks,
        "review_acceptance_rate": sum(task["review_accepted"] for task in tasks) / total_tasks,
        "sequence_gain": max(0.0, min(1.0, float(data.get("sequence_gain", 0.0)))),
        "cost_reduction_rate": max(
            0.0, min(1.0, float(data.get("cost_reduction_rate", 0.0)))
        ),
    }

    return {
        "label": data["label"],
        "readiness": data["readiness"],
        "dynamic": dynamic,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a self-eval run file and emit calculate_score metrics JSON."
    )
    parser.add_argument("run_json", help="Path to the self-eval run JSON file")
    parser.add_argument("--out", help="Optional output path for the derived metrics JSON")
    args = parser.parse_args()

    run_path = Path(args.run_json)
    data = load_json(run_path)
    validate_run(data)
    metrics = build_metrics(data)
    rendered = json.dumps(metrics, indent=2, sort_keys=True) + "\n"

    if args.out:
        Path(args.out).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
