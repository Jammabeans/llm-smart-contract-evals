from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from benchmark.scorer import load_scores_csv, summarize_scores, validate_scores


def _format_float(value: float) -> str:
    return f"{value:.2f}"


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print("Usage: python scripts/summarize_scores.py <scores.csv>")
        return 1

    csv_path = args[0]
    records = load_scores_csv(csv_path)
    errors = validate_scores(records)

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    summaries = summarize_scores(records)
    if not summaries:
        print("No records found.")
        return 0

    headers = [
        "model_name",
        "prompt_style",
        "num_cases",
        "avg_total",
        "avg_detection",
        "avg_localization",
        "avg_exploit",
        "avg_severity",
        "avg_fix",
    ]

    print(" | ".join(headers))
    print("-" * 120)

    for s in summaries:
        row = [
            s["model_name"],
            s["prompt_style"],
            str(s["num_cases"]),
            _format_float(s["avg_total_score"]),
            _format_float(s["avg_detection_score"]),
            _format_float(s["avg_localization_score"]),
            _format_float(s["avg_exploit_reasoning_score"]),
            _format_float(s["avg_severity_score"]),
            _format_float(s["avg_fix_score"]),
        ]
        print(" | ".join(row))

    return 0


if __name__ == "__main__":
    sys.exit(main())

