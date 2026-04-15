from __future__ import annotations

import csv
from collections import defaultdict


REQUIRED_COLUMNS = {
    "run_id",
    "model_name",
    "prompt_style",
    "case_id",
    "detection_score",
    "localization_score",
    "exploit_reasoning_score",
    "severity_score",
    "fix_score",
    "failure_mode",
    "evaluator_notes",
}

SCORE_FIELDS = [
    "detection_score",
    "localization_score",
    "exploit_reasoning_score",
    "severity_score",
    "fix_score",
]

VALID_PROMPT_STYLES = {"baseline", "senior_auditor_concise"}

VALID_FAILURE_MODES = {
    "missed_vulnerability",
    "vague_suspicion",
    "wrong_vulnerability",
    "right_vulnerability_wrong_severity",
    "right_vulnerability_weak_fix",
    "hallucinated_issue",
    "no_major_failure",
}


def load_scores_csv(path: str) -> list[dict]:
    """Load manual scoring records from CSV into a list of dict rows."""
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def validate_scores(records: list[dict]) -> list[str]:
    """Validate scoring records and return a list of validation error messages."""
    errors: list[str] = []

    for i, record in enumerate(records, start=1):
        row_label = f"row {i}"

        missing = REQUIRED_COLUMNS - set(record.keys())
        if missing:
            errors.append(f"{row_label}: missing required columns: {sorted(missing)}")
            continue

        prompt_style = record.get("prompt_style", "")
        if prompt_style not in VALID_PROMPT_STYLES:
            errors.append(
                f"{row_label}: prompt_style must be one of {sorted(VALID_PROMPT_STYLES)}"
            )

        failure_mode = record.get("failure_mode", "")
        if failure_mode not in VALID_FAILURE_MODES:
            errors.append(
                f"{row_label}: failure_mode must be one of {sorted(VALID_FAILURE_MODES)}"
            )

        for field in SCORE_FIELDS:
            value = record.get(field, "")
            try:
                score = int(value)
            except (TypeError, ValueError):
                errors.append(f"{row_label}: {field} must be an integer 0, 1, or 2")
                continue

            if score not in {0, 1, 2}:
                errors.append(f"{row_label}: {field} must be 0, 1, or 2")

    return errors


def compute_total_score(record: dict) -> int:
    """Compute total score for a record as sum of the 5 dimension scores."""
    return sum(int(record[field]) for field in SCORE_FIELDS)


def summarize_scores(records: list[dict]) -> list[dict]:
    """Aggregate scores by (model_name, prompt_style)."""
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for record in records:
        key = (record["model_name"], record["prompt_style"])
        grouped[key].append(record)

    summaries: list[dict] = []
    for (model_name, prompt_style), group in sorted(grouped.items()):
        num_cases = len(group)
        totals = [compute_total_score(r) for r in group]

        summary = {
            "model_name": model_name,
            "prompt_style": prompt_style,
            "num_cases": num_cases,
            "avg_total_score": sum(totals) / num_cases,
            "avg_detection_score": sum(int(r["detection_score"]) for r in group) / num_cases,
            "avg_localization_score": sum(int(r["localization_score"]) for r in group)
            / num_cases,
            "avg_exploit_reasoning_score": sum(
                int(r["exploit_reasoning_score"]) for r in group
            )
            / num_cases,
            "avg_severity_score": sum(int(r["severity_score"]) for r in group) / num_cases,
            "avg_fix_score": sum(int(r["fix_score"]) for r in group) / num_cases,
        }
        summaries.append(summary)

    return summaries

