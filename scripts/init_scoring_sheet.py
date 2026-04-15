from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


OUTPUT_COLUMNS = [
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
]

REQUIRED_RAW_FIELDS = {
    "run_id",
    "model_name",
    "prompt_style",
    "case_id",
    "status",
}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Initialize a blank manual scoring CSV from raw JSONL outputs"
    )
    parser.add_argument("--raw-jsonl", required=True)
    parser.add_argument("--output-csv", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    raw_path = Path(args.raw_jsonl)
    output_path = Path(args.output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows_to_write: list[dict] = []
    skipped = 0

    with raw_path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            if not line.strip():
                continue

            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError(f"line {idx}: raw record must be a JSON object")

            missing = REQUIRED_RAW_FIELDS - set(record.keys())
            if missing:
                raise ValueError(f"line {idx}: missing required raw fields: {sorted(missing)}")

            if record["status"] != "ok":
                skipped += 1
                continue

            rows_to_write.append(
                {
                    "run_id": record["run_id"],
                    "model_name": record["model_name"],
                    "prompt_style": record["prompt_style"],
                    "case_id": record["case_id"],
                    "detection_score": "",
                    "localization_score": "",
                    "exploit_reasoning_score": "",
                    "severity_score": "",
                    "fix_score": "",
                    "failure_mode": "",
                    "evaluator_notes": "",
                }
            )

    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows_to_write)

    print(f"Skipped non-ok rows: {skipped}")
    print(f"Wrote scoring sheet: {output_path} ({len(rows_to_write)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

