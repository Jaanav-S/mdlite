from mdlite import render, render_inline


def test_headings():
    assert render("# Title") == "<h1>Title</h1>"
    assert render("### Small ###") == "<h3>Small</h3>"


def test_paragraphs_are_separated_by_blank_lines():
    assert render("one\ntwo\n\nthree") == "<p>one\ntwo</p>\n<p>three</p>"


def test_bold_and_italic():
    assert render_inline("**bold** and *it*") == "<strong>bold</strong> and <em>it</em>"


def test_inline_code_is_not_formatted():
    assert render_inline("`a *b* c`") == "<code>a *b* c</code>"


def test_links():
    assert render_inline("[site](https://example.com)") == '<a href="https://example.com">site</a>'


def test_html_is_escaped():
    assert render_inline("<script>") == "&lt;script&gt;"


def test_unordered_list():
    assert render("- a\n- b") == "<ul>\n<li>a</li>\n<li>b</li>\n</ul>"
