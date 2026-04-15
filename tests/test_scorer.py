from __future__ import annotations

from benchmark.scorer import (
    compute_total_score,
    load_scores_csv,
    summarize_scores,
    validate_scores,
)


def test_load_scores_csv_reads_rows() -> None:
    records = load_scores_csv("tests/fixtures/sample_scores.csv")
    assert len(records) == 4
    assert records[0]["model_name"] == "gpt-4o-mini"


def test_validate_scores_success_on_sample_fixture() -> None:
    records = load_scores_csv("tests/fixtures/sample_scores.csv")
    errors = validate_scores(records)
    assert errors == []


def test_compute_total_score_sums_five_dimensions() -> None:
    record = {
        "detection_score": "2",
        "localization_score": "1",
        "exploit_reasoning_score": "2",
        "severity_score": "1",
        "fix_score": "0",
    }
    assert compute_total_score(record) == 6


def test_summarize_scores_aggregates_by_model_and_prompt_style() -> None:
    records = load_scores_csv("tests/fixtures/sample_scores.csv")
    summaries = summarize_scores(records)

    assert len(summaries) == 2
    keys = {(s["model_name"], s["prompt_style"]) for s in summaries}
    assert keys == {
        ("claude-3.5-sonnet", "senior_auditor_concise"),
        ("gpt-4o-mini", "baseline"),
    }

    gpt_summary = next(
        s
        for s in summaries
        if s["model_name"] == "gpt-4o-mini" and s["prompt_style"] == "baseline"
    )
    assert gpt_summary["num_cases"] == 2
    assert gpt_summary["avg_total_score"] == 6.5
    assert gpt_summary["avg_detection_score"] == 1.5


def test_validate_scores_failure_on_bad_records() -> None:
    bad_records = [
        {
            "run_id": "run_bad",
            "model_name": "bad-model",
            "prompt_style": "invalid_style",
            "case_id": "case_001",
            "detection_score": "3",
            "localization_score": "1",
            "exploit_reasoning_score": "x",
            "severity_score": "2",
            "fix_score": "1",
            "failure_mode": "not_allowed",
            "evaluator_notes": "bad row",
        }
    ]

    errors = validate_scores(bad_records)
    assert errors
    joined = "\n".join(errors)
    assert "prompt_style" in joined
    assert "detection_score" in joined
    assert "exploit_reasoning_score" in joined
    assert "failure_mode" in joined

