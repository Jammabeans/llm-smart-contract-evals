from __future__ import annotations

import csv
from pathlib import Path

from scripts.build_results_tables import main


def _read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_build_results_tables_writes_case_and_summary_outputs(tmp_path: Path) -> None:
    case_output = tmp_path / "tables" / "case_results.csv"
    summary_output = tmp_path / "tables" / "summary_results.csv"

    rc = main(
        [
            "--scores-csv",
            "tests/fixtures/sample_scores.csv",
            "--case-output-csv",
            str(case_output),
            "--summary-output-csv",
            str(summary_output),
        ]
    )

    assert rc == 0
    assert case_output.exists()
    assert summary_output.exists()

    case_rows = _read_csv(case_output)
    assert len(case_rows) == 4
    assert "total_score" in case_rows[0]

    summary_rows = _read_csv(summary_output)
    assert len(summary_rows) == 2
    grouped_keys = {(r["model_name"], r["prompt_style"]) for r in summary_rows}
    assert grouped_keys == {
        ("gpt-4o-mini", "baseline"),
        ("claude-3.5-sonnet", "senior_auditor_concise"),
    }


def test_build_results_tables_returns_nonzero_on_invalid_scores(tmp_path: Path) -> None:
    bad_scores = tmp_path / "bad_scores.csv"
    bad_scores.write_text(
        "run_id,model_name,prompt_style,case_id,detection_score,localization_score,"
        "exploit_reasoning_score,severity_score,fix_score,failure_mode,evaluator_notes\n"
        "run_bad,bad-model,invalid_style,case_001,3,1,1,1,1,not_allowed,bad row\n",
        encoding="utf-8",
    )

    case_output = tmp_path / "tables" / "bad_case_results.csv"
    summary_output = tmp_path / "tables" / "bad_summary_results.csv"

    rc = main(
        [
            "--scores-csv",
            str(bad_scores),
            "--case-output-csv",
            str(case_output),
            "--summary-output-csv",
            str(summary_output),
        ]
    )

    assert rc == 1
    assert not case_output.exists()
    assert not summary_output.exists()

