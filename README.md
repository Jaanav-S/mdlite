# mdlite

A Markdown to HTML converter in a single file, written as an exercise in
parsing. No dependencies.

## Supported syntax

- Headings (`#` to `######`)
- Paragraphs and line breaks
- `**bold**`, `*italic*` and `` `inline code` ``
- Links: `[text](url)`
- Unordered (`-`, `*`) and ordered (`1.`) lists
- Fenced code blocks with an optional language
- Blockquotes and horizontal rules

## Usage

```
python mdlite.py notes.md > notes.html
cat notes.md | python mdlite.py
```

Or from Python:

```python
from mdlite import render
html = render("# Hello\n\nSome *text*.")
```
