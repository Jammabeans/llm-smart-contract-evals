# llm-smart-contract-evals

Small research repository for benchmarking LLM performance on real smart-contract vulnerabilities.

## Why this exists

Many LLM smart-contract evaluations are synthetic or underspecified. This repository is intended to provide a simple, transparent benchmark format using readable vulnerable snippets with explicit ground truth.

## v0.1 scope

This version only includes the scaffold:

- benchmark case schema and seed cases
- minimal vulnerable Solidity snippets
- prompt-construction utilities
- case validation script
- basic tests for case integrity and prompt generation

Out of scope in v0.1:

- model/provider API integrations
- scoring/leaderboard logic
- web app or agent framework

## Current status

Scaffold + schema + seed cases.

## Quick start

```bash
python -m pip install -e .[dev]
pytest
python scripts/validate_cases.py
```

