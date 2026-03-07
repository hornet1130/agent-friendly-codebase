#!/usr/bin/env python3
"""Summarize repeated codebase-for-ai self-eval run files."""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any

from build_self_eval_metrics import build_metrics, load_json, validate_run
from calculate_score import compute_scores, rating


def summarize_values(values: list[float]) -> dict[str, float]:
    return {
        "count": len(values),
        "median": round(statistics.median(values), 2),
        "mean": round(sum(values) / len(values), 2),
        "min": round(min(values), 2),
        "max": round(max(values), 2),
    }


def summarize_runs(run_paths: list[str]) -> dict[str, Any]:
    run_entries: list[dict[str, Any]] = []
    score_buckets: dict[str, list[float]] = {"ACRS": [], "ATPS": [], "AIFS": []}
    dynamic_buckets: dict[str, list[float]] = {}

    for path_str in run_paths:
        path = Path(path_str)
        run = load_json(path)
        validate_run(run)
        metrics = build_metrics(run)
        scores = compute_scores(metrics)

        run_entries.append(
            {
                "path": str(path),
                "label": scores["label"],
                "ACRS": scores["ACRS"],
                "ATPS": scores["ATPS"],
                "AIFS": scores["AIFS"],
                "rating": rating(scores["AIFS"]),
            }
        )

        for key in score_buckets:
            score_buckets[key].append(float(scores[key]))

        for key, value in scores["dynamic_breakdown"].items():
            dynamic_buckets.setdefault(key, []).append(float(value))

    return {
        "runs": run_entries,
        "summary": {
            "run_count": len(run_entries),
            "scores": {key: summarize_values(values) for key, values in score_buckets.items()},
            "dynamic_breakdown": {
                key: summarize_values(values) for key, values in dynamic_buckets.items()
            },
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize repeated codebase-for-ai self-eval runs."
    )
    parser.add_argument("run_jsons", nargs="+", help="Completed self-eval run JSON files")
    parser.add_argument("--out", help="Optional output path for the summary JSON")
    args = parser.parse_args()

    if not args.run_jsons:
        raise ValueError("at least one self-eval run json path is required")

    summary = summarize_runs(args.run_jsons)
    rendered = json.dumps(summary, indent=2, sort_keys=True) + "\n"

    if args.out:
        Path(args.out).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
