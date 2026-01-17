from app.view import DependencyExpressionView


def test_view_render_success_contains_input_and_output():
    out = DependencyExpressionView.render_success("a & b", ["a", "&", "b"])
    assert "Parsed successfully" in out
    assert "input:" in out
    assert "a & b" in out
    assert "output:" in out
    assert "['a', '&', 'b']" in out


def test_view_render_error_contains_input_and_error():
    err = ValueError("boom")
    out = DependencyExpressionView.render_error("a &", err)
    assert "Invalid expression" in out
    assert "input:" in out
    assert "a &" in out
    assert "error:" in out
    assert "boom" in out
