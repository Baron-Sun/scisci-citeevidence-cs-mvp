from __future__ import annotations


def format_markdown_sections(blocks: list[str]) -> str:
    """Join markdown blocks with readable blank-line separation."""
    cleaned = [_clean_block(block) for block in blocks if _clean_block(block)]
    return "\n\n".join(cleaned) + "\n"


def _clean_block(block: str) -> str:
    lines = [line.rstrip() for line in str(block).strip().splitlines()]
    return "\n".join(lines).strip()
