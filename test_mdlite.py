from mdlite import render, render_inline


def test_headings():
    assert render("# Title") == "<h1>Title</h1>"
    assert render("### Small ###") == "<h3>Small</h3>"
