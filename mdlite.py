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


def parse_code(lines, i):
    lang = FENCE.match(lines[i]).group(1)
    body = []
    i += 1
    while i < len(lines) and not FENCE.match(lines[i]):
        body.append(lines[i])
        i += 1
    attr = f' class="language-{lang}"' if lang else ""
    code = html.escape("\n".join(body), quote=False)
    return f"<pre><code{attr}>{code}</code></pre>", i + 1


def parse_quote(lines, i):
    inner = []
    while i < len(lines) and lines[i].startswith(">"):
        inner.append(lines[i][1:].removeprefix(" "))
        i += 1
    return f"<blockquote>\n{render(chr(10).join(inner))}\n</blockquote>", i


def starts_block(line):
    return bool(
        HEADING.match(line) or FENCE.match(line) or HR.match(line)
        or UL_ITEM.match(line) or OL_ITEM.match(line) or line.startswith(">")
    )


def parse_paragraph(lines, i):
    para = []
    while i < len(lines) and lines[i].strip() and (not para or not starts_block(lines[i])):
        para.append(lines[i])
        i += 1
    return f"<p>{render_inline(chr(10).join(para))}</p>", i


def render(source):
    """Convert a Markdown string to HTML."""
    lines = source.replace("\r\n", "\n").split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
        elif m := HEADING.match(line):
            level = len(m.group(1))
            out.append(f"<h{level}>{render_inline(m.group(2))}</h{level}>")
            i += 1
        elif FENCE.match(line):
            block, i = parse_code(lines, i)
            out.append(block)
        elif HR.match(line):
            out.append("<hr>")
            i += 1
        elif UL_ITEM.match(line):
            block, i = parse_list(lines, i, UL_ITEM, "ul")
            out.append(block)
        elif OL_ITEM.match(line):
            block, i = parse_list(lines, i, OL_ITEM, "ol")
            out.append(block)
        elif line.startswith(">"):
            block, i = parse_quote(lines, i)
            out.append(block)
        else:
            block, i = parse_paragraph(lines, i)
            out.append(block)
    return "\n".join(out)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        with open(argv[0], encoding="utf-8") as fh:
            source = fh.read()
    else:
        source = sys.stdin.read()
    print(render(source))


if __name__ == "__main__":
    main()
