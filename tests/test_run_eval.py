from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.run_eval import main


REQUIRED_RECORD_FIELDS = {
    "run_id",
    "timestamp_utc",
    "provider",
    "model_name",
    "prompt_style",
    "case_id",
    "contract_file",
    "public_reference",
    "prompt",
    "response_text",
    "status",
    "error",
}


def _read_jsonl(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def test_run_eval_dry_run_writes_jsonl_and_manifest(tmp_path: Path) -> None:
    output_path = tmp_path / "raw" / "run_test.jsonl"

    rc = main(
        [
            "--model",
            "claude-3-5-haiku-latest",
            "--prompt-style",
            "baseline",
            "--output",
            str(output_path),
            "--dry-run",
        ]
    )

    assert rc == 0
    assert output_path.exists()

    records = _read_jsonl(output_path)
    assert len(records) == 3

    for record in records:
        assert set(record.keys()) == REQUIRED_RECORD_FIELDS
        assert record["provider"] == "anthropic"
        assert record["prompt_style"] == "baseline"
        assert record["status"] == "dry_run"
        assert record["response_text"] == ""
        assert record["error"] == ""

    manifest_path = output_path.with_suffix(".manifest.json")
    assert manifest_path.exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["provider"] == "anthropic"
    assert manifest["num_cases"] == 3
    assert manifest["dry_run"] is True
    assert len(manifest["selected_case_ids"]) == 3


def test_run_eval_dry_run_case_subset_selection(tmp_path: Path) -> None:
    output_path = tmp_path / "raw" / "run_subset.jsonl"
    requested_ids = "case_003,case_001"

    rc = main(
        [
            "--model",
            "claude-3-5-haiku-latest",
            "--prompt-style",
            "senior_auditor_concise",
            "--output",
            str(output_path),
            "--case-ids",
            requested_ids,
            "--max-cases",
            "2",
            "--dry-run",
        ]
    )

    assert rc == 0
    records = _read_jsonl(output_path)
    assert len(records) == 2
    assert [record["case_id"] for record in records] == ["case_003", "case_001"]
    assert all(record["prompt_style"] == "senior_auditor_concise" for record in records)
    assert all(record["status"] == "dry_run" for record in records)

    manifest = json.loads(output_path.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    assert manifest["num_cases"] == 2
    assert manifest["selected_case_ids"] == ["case_003", "case_001"]


def test_run_eval_unknown_case_id_raises_clear_error(tmp_path: Path) -> None:
    output_path = tmp_path / "raw" / "run_unknown.jsonl"

    with pytest.raises(ValueError, match=r"Unknown case_id\(s\): case_999"):
        main(
            [
                "--model",
                "claude-3-5-haiku-latest",
                "--prompt-style",
                "baseline",
                "--output",
                str(output_path),
                "--case-ids",
                "case_001,case_999",
                "--dry-run",
            ]
        )

