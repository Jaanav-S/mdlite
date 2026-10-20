"""A small Markdown to HTML converter."""

import html
import re
import sys

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*$")
UL_ITEM = re.compile(r"^\s*[-*+]\s+(.*)$")
OL_ITEM = re.compile(r"^\s*\d+[.)]\s+(.*)$")
FENCE = re.compile(r"^```\s*([\w+-]*)\s*$")
HR = re.compile(r"^\s*([-*_])(\s*\1){2,}\s*$")


def render_inline(text):
    """Escape HTML and apply inline formatting to a run of text."""
    # Pull code spans out first so their contents are never formatted.
    spans = []

    def stash(match):
        spans.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"\x00{len(spans) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"  \n", "<br>\n", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], text)


def parse_list(lines, i, pattern, tag):
    items = []
    while i < len(lines):
        match = pattern.match(lines[i])
        if not match:
            break
        items.append(f"<li>{render_inline(match.group(1))}</li>")
        i += 1
    return f"<{tag}>\n" + "\n".join(items) + f"\n</{tag}>", i
