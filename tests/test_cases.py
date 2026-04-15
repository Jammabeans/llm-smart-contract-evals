from __future__ import annotations

from pathlib import Path

from benchmark.prompts import load_cases


REQUIRED_FIELDS = {
    "case_id",
    "title",
    "category",
    "severity",
    "contract_file",
    "language",
    "public_reference",
    "task_prompt",
    "ground_truth",
    "tags",
}

REQUIRED_GROUND_TRUTH_FIELDS = {
    "vulnerability_exists",
    "vulnerability_type",
    "affected_functions",
    "root_cause",
    "exploit_path",
    "impact",
    "severity_rationale",
    "recommended_fix",
}


def test_cases_have_required_fields_and_contract_files_exist() -> None:
    cases = load_cases("benchmark/cases.json")
    assert len(cases) == 3

    for case in cases:
        assert REQUIRED_FIELDS.issubset(case.keys()), case.get("case_id")

        ground_truth = case["ground_truth"]
        assert isinstance(ground_truth, dict)
        assert REQUIRED_GROUND_TRUTH_FIELDS.issubset(ground_truth.keys()), case["case_id"]

        contract_path = Path(case["contract_file"])
        assert contract_path.exists(), f"missing contract file for {case['case_id']}"

