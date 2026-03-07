import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_command(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        list(args),
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def copy_cli_fixture(tmpdir: str) -> Path:
    fixture_root = Path(tmpdir) / "fixture"
    fixture_root.mkdir()
    for name in ("scripts", "TEMPLATES"):
        shutil.copytree(
            REPO_ROOT / name,
            fixture_root / name,
            ignore=shutil.ignore_patterns("__pycache__"),
        )
    return fixture_root


class ScriptCliTests(unittest.TestCase):
    def test_calculate_score_supports_audit_only_metrics(self) -> None:
        metrics_path = REPO_ROOT / "assets" / "example_audit_only_metrics.json"
        result = run_command(
            "python3",
            "scripts/calculate_score.py",
            str(metrics_path),
            cwd=REPO_ROOT,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Evaluation mode: audit-only", result.stdout)
        self.assertIn("ATPS: incomplete", result.stdout)
        self.assertIn("AIFS: incomplete", result.stdout)

    def test_calculate_score_writes_markdown_for_audit_only(self) -> None:
        metrics_path = REPO_ROOT / "assets" / "example_audit_only_metrics.json"
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "audit.md"
            result = run_command(
                "python3",
                "scripts/calculate_score.py",
                str(metrics_path),
                "--md-out",
                str(output_path),
                cwd=REPO_ROOT,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            report = output_path.read_text(encoding="utf-8")
            self.assertIn("- Evaluation mode: audit-only", report)
            self.assertIn("- ATPS: incomplete", report)
            self.assertIn("- AIFS: incomplete", report)

    def test_init_area_scaffolds_audit_only_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = copy_cli_fixture(tmpdir)
            result = run_command(
                "python3",
                "scripts/init_area.py",
                "--area-id",
                "smoke-area",
                "--human-name",
                "Smoke Area",
                "--primary-path",
                "apps/api/src/modules/auth",
                cwd=fixture_root,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            baseline_metrics = json.loads(
                (
                    fixture_root
                    / "AREAS"
                    / "smoke-area"
                    / "metrics"
                    / "baseline.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(baseline_metrics["evaluation_mode"], "audit-only")
            self.assertIsNone(baseline_metrics["dynamic"])
            self.assertTrue(
                (
                    fixture_root
                    / "AREAS"
                    / "smoke-area"
                    / "reports"
                    / "comparison.md"
                ).exists()
            )

    def test_init_task_creates_numbered_task_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_root = copy_cli_fixture(tmpdir)
            result = run_command(
                "python3",
                "scripts/init_task.py",
                "--area-id",
                "smoke-area",
                "--task-id",
                "smoke-area-007",
                "--slug",
                "audit",
                "--type",
                "repo-qa",
                "--difficulty",
                "low",
                "--problem-statement",
                "Verify the scripted scaffolding flow.",
                cwd=fixture_root,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            task_path = (
                fixture_root / "AREAS" / "smoke-area" / "tasks" / "007_audit.md"
            )
            self.assertTrue(task_path.exists())
            content = task_path.read_text(encoding="utf-8")
            self.assertIn("- Task ID: smoke-area-007", content)
            self.assertIn("Verify the scripted scaffolding flow.", content)


if __name__ == "__main__":
    unittest.main()
