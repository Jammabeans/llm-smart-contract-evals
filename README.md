# llm-smart-contract-evals

Small research repository for benchmarking LLM performance on real smart-contract vulnerabilities.

## Why this exists

Many LLM smart-contract evaluations are synthetic or underspecified. This repository is intended to provide a simple, transparent benchmark format using readable vulnerable snippets with explicit ground truth.

## v0.1 scope

This version includes:

- benchmark schema and seed cases
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

Working v0.1 baseline: seed benchmark cases, prompt generation, Anthropic raw-run execution, and manual scoring/summarization workflow.

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

