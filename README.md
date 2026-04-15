# llm-smart-contract-evals

Small research repository for benchmarking LLM performance on real smart-contract vulnerabilities.

## Why this exists

Many LLM smart-contract evaluations are synthetic or underspecified. This repository is intended to provide a simple, transparent benchmark format using readable vulnerable snippets with explicit ground truth.

## v0.1 scope

This version includes:

- benchmark schema and 7 public-audit-derived cases
- prompt builder and case loading utilities
- case validation tooling
- raw evaluation runner for Anthropic (JSONL + run manifest)
- manual scoring rubric
- score summarization tooling

v0.1 does **not** include:

- automatic grading of free-form model outputs
- many-model benchmarking infrastructure
- judge-model scoring
- web UI / agent framework

## Current status

v0.1 currently includes 7 benchmark cases with explicit provenance labels.
Cases are either exact excerpts, minimized reconstructions, or sanitized variants based on public findings, and are intentionally simplified for reproducibility while preserving the core vulnerability pattern.

## Quick start

```bash
python -m pip install -e .[dev]
pytest
python scripts/validate_cases.py
```

## Run an evaluation

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

Dry run (no API calls; writes placeholder raw records):

```bash
python scripts/run_eval.py \
  --model claude-3-5-haiku-latest \
  --prompt-style baseline \
  --output results/raw/dry_run.jsonl \
  --dry-run
```

Real run (calls Anthropic Messages API and stores raw outputs):

```bash
python scripts/run_eval.py \
  --model claude-3-5-haiku-latest \
  --prompt-style senior_auditor_concise \
  --output results/raw/run_001.jsonl
```

v0.1 stores raw model outputs for later analysis. Scoring remains a separate manual workflow documented in [`benchmark/scoring.md`](benchmark/scoring.md).

## Manual scoring workflow

1) Run eval and collect raw JSONL outputs:

```bash
python scripts/run_eval.py \
  --model claude-3-5-haiku-latest \
  --prompt-style baseline \
  --output results/raw/run_001.jsonl
```

2) Initialize a blank scoring sheet (only `status == "ok"` rows are included):

```bash
python scripts/init_scoring_sheet.py \
  --raw-jsonl results/raw/run_001.jsonl \
  --output-csv results/manual/run_001_scores_blank.csv
```

3) Manually fill in rubric fields in the CSV (`*_score`, `failure_mode`, `evaluator_notes`).

4) Build case-level and summary results tables:

```bash
python scripts/build_results_tables.py \
  --scores-csv results/manual/run_001_scores_filled.csv \
  --case-output-csv results/tables/run_001_case_results.csv \
  --summary-output-csv results/tables/run_001_summary.csv
```

