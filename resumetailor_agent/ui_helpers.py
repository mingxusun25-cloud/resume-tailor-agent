from __future__ import annotations


def parse_compare_inputs(raw_text: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for block in raw_text.split("\n---\n"):
        cleaned = block.strip()
        if not cleaned or "::" not in cleaned:
            continue
        label, body = cleaned.split("::", 1)
        label = label.strip()
        body = body.strip()
        if label and body:
            pairs.append((label, body))
    return pairs
