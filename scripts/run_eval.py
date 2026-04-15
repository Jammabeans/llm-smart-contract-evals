from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from benchmark.llm_client import run_anthropic_prompt
from benchmark.prompts import build_prompt, load_cases


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run raw Anthropic benchmark evaluation")
    parser.add_argument("--model", required=True)
    parser.add_argument(
        "--prompt-style",
        required=True,
        choices=["baseline", "senior_auditor_concise"],
    )
    parser.add_argument("--output", required=True)
    parser.add_argument("--cases-path", default="benchmark/cases.json")
    parser.add_argument("--case-ids", default="")
    parser.add_argument("--max-cases", type=int, default=None)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=800)
    parser.add_argument("--delay-seconds", type=float, default=0.0)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def _select_cases(cases: list[dict], case_ids_arg: str, max_cases: int | None) -> list[dict]:
    selected = cases
    if case_ids_arg.strip():
        requested = [c.strip() for c in case_ids_arg.split(",") if c.strip()]
        case_by_id = {c.get("case_id"): c for c in cases}
        missing = [case_id for case_id in requested if case_id not in case_by_id]
        if missing:
            raise ValueError(f"Unknown case_id(s): {', '.join(missing)}")

        selected = [case_by_id[case_id] for case_id in requested]

    if max_cases is not None:
        selected = selected[:max_cases]

    return selected


def _write_jsonl_line(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cases = load_cases(args.cases_path)
    selected_cases = _select_cases(cases, args.case_ids, args.max_cases)
    selected_case_ids = [c["case_id"] for c in selected_cases]

    run_id = f"run_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    if output_path.exists():
        output_path.unlink()

    print(f"Running {len(selected_cases)} case(s) with model={args.model} style={args.prompt_style}")

    for i, case in enumerate(selected_cases, start=1):
        prompt = build_prompt(case, prompt_style=args.prompt_style)
        timestamp_utc = datetime.now(timezone.utc).isoformat()

        response_text = ""
        status = "dry_run"
        error = ""

        if not args.dry_run:
            try:
                response_text = run_anthropic_prompt(
                    prompt=prompt,
                    model_name=args.model,
                    max_tokens=args.max_tokens,
                    temperature=args.temperature,
                )
                status = "ok"
            except Exception as exc:
                status = "error"
                error = str(exc)

        record = {
            "run_id": run_id,
            "timestamp_utc": timestamp_utc,
            "provider": "anthropic",
            "model_name": args.model,
            "prompt_style": args.prompt_style,
            "case_id": case["case_id"],
            "contract_file": case["contract_file"],
            "public_reference": case["public_reference"],
            "prompt": prompt,
            "response_text": response_text,
            "status": status,
            "error": error,
        }

        _write_jsonl_line(output_path, record)
        print(f"[{i}/{len(selected_cases)}] {case['case_id']} -> {status}")

        if not args.dry_run and args.delay_seconds > 0 and i < len(selected_cases):
            time.sleep(args.delay_seconds)

    manifest = {
        "run_id": run_id,
        "provider": "anthropic",
        "model_name": args.model,
        "prompt_style": args.prompt_style,
        "cases_path": args.cases_path,
        "selected_case_ids": selected_case_ids,
        "num_cases": len(selected_cases),
        "dry_run": args.dry_run,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "delay_seconds": args.delay_seconds,
    }

    manifest_path = output_path.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote output: {output_path}")
    print(f"Wrote manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

