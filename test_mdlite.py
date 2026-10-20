from mdlite import render, render_inline


def test_headings():
    assert render("# Title") == "<h1>Title</h1>"
    assert render("### Small ###") == "<h3>Small</h3>"


def test_paragraphs_are_separated_by_blank_lines():
    assert render("one\ntwo\n\nthree") == "<p>one\ntwo</p>\n<p>three</p>"


def test_bold_and_italic():
    assert render_inline("**bold** and *it*") == "<strong>bold</strong> and <em>it</em>"
