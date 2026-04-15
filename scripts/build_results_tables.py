from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from benchmark.scorer import (
    REQUIRED_COLUMNS,
    compute_total_score,
    load_scores_csv,
    summarize_scores,
    validate_scores,
)


SUMMARY_COLUMNS = [
    "model_name",
    "prompt_style",
    "num_cases",
    "avg_total_score",
    "avg_detection_score",
    "avg_localization_score",
    "avg_exploit_reasoning_score",
    "avg_severity_score",
    "avg_fix_score",
]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build case-level and summary score tables")
    parser.add_argument("--scores-csv", required=True)
    parser.add_argument("--case-output-csv", required=True)
    parser.add_argument("--summary-output-csv", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    records = load_scores_csv(args.scores_csv)
    errors = validate_scores(records)
    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    case_output_path = Path(args.case_output_csv)
    summary_output_path = Path(args.summary_output_csv)
    case_output_path.parent.mkdir(parents=True, exist_ok=True)
    summary_output_path.parent.mkdir(parents=True, exist_ok=True)

    case_columns = list(REQUIRED_COLUMNS) + ["total_score"]
    with case_output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=case_columns)
        writer.writeheader()
        for record in records:
            row = dict(record)
            row["total_score"] = compute_total_score(record)
            writer.writerow(row)

    summaries = summarize_scores(records)
    with summary_output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_COLUMNS)
        writer.writeheader()
        for summary in summaries:
            writer.writerow(summary)

    print(f"Wrote case-level table: {case_output_path} ({len(records)} rows)")
    print(f"Wrote summary table: {summary_output_path} ({len(summaries)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

