from app.controller import DependencyExpressionController
from app.model import DependencyExpressionModel
from app.view import DependencyExpressionView


def test_controller_success_path_returns_success_view():
    controller = DependencyExpressionController(DependencyExpressionModel(), DependencyExpressionView())
    out = controller.handle_parse_request("a & (b | c)")
    assert "Parsed successfully" in out
    assert "a & (b | c)" in out
    assert "['a', '&', ['b', '|', 'c']]" in out


def test_controller_error_path_returns_error_view():
    controller = DependencyExpressionController(DependencyExpressionModel(), DependencyExpressionView())
    out = controller.handle_parse_request("a &")
    assert "Invalid expression" in out
    assert "a &" in out
