from __future__ import annotations

from pathlib import Path

from benchmark.prompts import build_prompt, load_cases


def test_build_prompt_baseline_includes_contract_code() -> None:
    case = load_cases("benchmark/cases.json")[0]
    prompt = build_prompt(case, prompt_style="baseline")

    assert "Vulnerability exists? (yes/no)" in prompt
    assert "```solidity" in prompt

    expected_snippet = Path(case["contract_file"]).read_text(encoding="utf-8").strip()
    assert expected_snippet in prompt


def test_build_prompt_senior_auditor_concise_includes_contract_code() -> None:
    case = load_cases("benchmark/cases.json")[1]
    prompt = build_prompt(case, prompt_style="senior_auditor_concise")

    assert "senior smart-contract auditor" in prompt
    assert "Severity" in prompt

    expected_snippet = Path(case["contract_file"]).read_text(encoding="utf-8").strip()
    assert expected_snippet in prompt

