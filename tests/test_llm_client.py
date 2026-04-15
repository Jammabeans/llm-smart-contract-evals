from __future__ import annotations

from types import SimpleNamespace

from benchmark.llm_client import extract_anthropic_text


def test_extract_anthropic_text_joins_multiple_text_blocks() -> None:
    response = SimpleNamespace(
        content=[
            SimpleNamespace(type="text", text="First part."),
            SimpleNamespace(type="tool_use", text="ignored"),
            SimpleNamespace(type="text", text="Second part."),
        ]
    )

    text = extract_anthropic_text(response)
    assert text == "First part.\nSecond part."

