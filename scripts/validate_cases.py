from __future__ import annotations

import json
import sys
from pathlib import Path


CASES_PATH = Path("benchmark/cases.json")

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


def validate() -> list[str]:
    errors: list[str] = []

    if not CASES_PATH.exists():
        return [f"missing file: {CASES_PATH}"]

    with CASES_PATH.open("r", encoding="utf-8") as f:
        cases = json.load(f)

    if not isinstance(cases, list):
        return ["benchmark/cases.json must contain a JSON list"]

    for idx, case in enumerate(cases, start=1):
        label = case.get("case_id", f"index_{idx}") if isinstance(case, dict) else f"index_{idx}"

        if not isinstance(case, dict):
            errors.append(f"{label}: case must be an object")
            continue

        missing = REQUIRED_FIELDS - set(case.keys())
        if missing:
            errors.append(f"{label}: missing required fields: {sorted(missing)}")

        ground_truth = case.get("ground_truth")
        if not isinstance(ground_truth, dict):
            errors.append(f"{label}: ground_truth must be an object")
        else:
            gt_missing = REQUIRED_GROUND_TRUTH_FIELDS - set(ground_truth.keys())
            if gt_missing:
                errors.append(f"{label}: missing ground_truth fields: {sorted(gt_missing)}")

        contract_file = case.get("contract_file")
        if isinstance(contract_file, str):
            contract_path = Path(contract_file)
            if not contract_path.exists():
                errors.append(f"{label}: missing contract file: {contract_file}")
        else:
            errors.append(f"{label}: contract_file must be a string")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return 1

    print("Validation passed: benchmark/cases.json is consistent with required fields and contract files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

