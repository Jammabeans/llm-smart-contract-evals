from __future__ import annotations

import csv
from pathlib import Path

from scripts.init_scoring_sheet import OUTPUT_COLUMNS, main


def _read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_init_scoring_sheet_writes_expected_columns_and_ok_rows(tmp_path: Path) -> None:
    output_csv = tmp_path / "manual" / "scores_blank.csv"

    rc = main(
        [
            "--raw-jsonl",
            "tests/fixtures/sample_raw_outputs.jsonl",
            "--output-csv",
            str(output_csv),
        ]
    )
    assert rc == 0
    assert output_csv.exists()

    with output_csv.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == OUTPUT_COLUMNS
        rows = list(reader)

    assert len(rows) == 3
    assert [row["case_id"] for row in rows] == ["case_001", "case_002", "case_001"]

    for row in rows:
        assert row["detection_score"] == ""
        assert row["localization_score"] == ""
        assert row["exploit_reasoning_score"] == ""
        assert row["severity_score"] == ""
        assert row["fix_score"] == ""
        assert row["failure_mode"] == ""
        assert row["evaluator_notes"] == ""


def test_init_scoring_sheet_preserves_input_order_for_ok_rows(tmp_path: Path) -> None:
    output_csv = tmp_path / "manual" / "scores_blank_order.csv"

    rc = main(
        [
            "--raw-jsonl",
            "tests/fixtures/sample_raw_outputs.jsonl",
            "--output-csv",
            str(output_csv),
        ]
    )
    assert rc == 0

    rows = _read_csv(output_csv)
    ordered_keys = [(r["run_id"], r["case_id"]) for r in rows]
    assert ordered_keys == [
        ("run_20260415T120000Z", "case_001"),
        ("run_20260415T120000Z", "case_002"),
        ("run_20260415T120000Z", "case_001"),
    ]

