from __future__ import annotations

from citeevidence.markdown import format_markdown_sections


def test_format_markdown_sections_adds_blank_lines() -> None:
    markdown = format_markdown_sections(["# Title", "## Section", "| a |\n|---|\n| 1 |"])

    assert markdown.startswith("# Title\n\n## Section\n\n| a |")
    assert markdown.endswith("\n")
    assert "\n\n\n" not in markdown
