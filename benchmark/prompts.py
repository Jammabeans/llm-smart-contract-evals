from __future__ import annotations

import json
from pathlib import Path


def load_cases(path: str) -> list[dict]:
    """Load benchmark cases from a JSON file path."""
    case_path = Path(path)
    with case_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("cases file must contain a JSON list")

    return data


def build_prompt(case: dict, prompt_style: str = "baseline") -> str:
    """Build an analysis prompt for a single benchmark case."""
    if prompt_style not in {"baseline", "senior_auditor_concise"}:
        raise ValueError("prompt_style must be 'baseline' or 'senior_auditor_concise'")

    contract_path = Path(case["contract_file"])
    contract_code = contract_path.read_text(encoding="utf-8")

    if prompt_style == "baseline":
        header = (
            "You are auditing a Solidity smart contract for security issues.\n"
            "Determine whether a vulnerability exists. If yes, identify the vulnerability type, "
            "severity, exploit path, and remediation."
        )
    else:
        header = (
            "Act as a senior smart-contract auditor. Be concise and evidence-driven.\n"
            "State whether a vulnerability exists, then provide severity, exploit explanation, "
            "and a practical fix."
        )

    prompt = (
        f"{header}\n\n"
        f"Case ID: {case['case_id']}\n"
        f"Title: {case['title']}\n"
        f"Category: {case['category']}\n"
        f"Task: {case['task_prompt']}\n\n"
        "Required output:\n"
        "1) Vulnerability exists? (yes/no)\n"
        "2) Vulnerability type\n"
        "3) Severity\n"
        "4) Exploit explanation\n"
        "5) Recommended remediation\n\n"
        "Solidity code:\n"
        "```solidity\n"
        f"{contract_code}\n"
        "```\n"
    )

    return prompt

