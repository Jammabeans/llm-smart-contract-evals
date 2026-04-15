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

VALID_SEVERITIES = {"low", "medium", "high", "critical"}


def test_cases_have_required_fields_and_contract_files_exist() -> None:
    cases = load_cases("benchmark/cases.json")
    assert len(cases) == 3
    case_ids: set[str] = set()

    for case in cases:
        assert REQUIRED_FIELDS.issubset(case.keys()), case.get("case_id")
        assert isinstance(case["case_id"], str)
        assert case["case_id"] not in case_ids
        case_ids.add(case["case_id"])

        assert case["severity"] in VALID_SEVERITIES
        assert isinstance(case["tags"], list)

        ground_truth = case["ground_truth"]
        assert isinstance(ground_truth, dict)
        assert REQUIRED_GROUND_TRUTH_FIELDS.issubset(ground_truth.keys()), case["case_id"]
        assert isinstance(ground_truth["affected_functions"], list)

        contract_path = Path(case["contract_file"])
        assert contract_path.exists(), f"missing contract file for {case['case_id']}"

