from __future__ import annotations

import os


def extract_anthropic_text(response: object) -> str:
    """Extract and join text blocks from an Anthropic Messages API response."""
    content = getattr(response, "content", None)
    if content is None and isinstance(response, dict):
        content = response.get("content")

    text_blocks: list[str] = []
    for block in content or []:
        block_type = getattr(block, "type", None)
        block_text = getattr(block, "text", None)

        if isinstance(block, dict):
            block_type = block.get("type", block_type)
            block_text = block.get("text", block_text)

        if block_type == "text" and isinstance(block_text, str) and block_text.strip():
            text_blocks.append(block_text)

    if not text_blocks:
        raise ValueError("Anthropic response contained no text content")

    return "\n".join(text_blocks)


def run_anthropic_prompt(
    prompt: str,
    model_name: str,
    max_tokens: int = 800,
    temperature: float = 0.0,
    client: object | None = None,
) -> str:
    """Run a single Anthropic Messages API prompt and return plain text output."""
    if client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set")

        try:
            from anthropic import Anthropic
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("Anthropic SDK is not installed") from exc

        client = Anthropic(api_key=api_key)

    response = client.messages.create(
        model=model_name,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return extract_anthropic_text(response)

