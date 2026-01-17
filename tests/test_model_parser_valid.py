import pytest
from app.model import DependencyExpressionModel


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("a", "a"),
        ("a & b", ["a", "&", "b"]),
        ("a | b", ["a", "|", "b"]),
        ("a | b | c", ["a", "|", "b", "|", "c"]),
        ("a & b & c", ["a", "&", "b", "&", "c"]),
        ("a & (b | c)", ["a", "&", ["b", "|", "c"]]),
        ("(a & b) | (b & c)", [["a", "&", "b"], "|", ["b", "&", "c"]]),
        ("((a))", "a"),
        ("job_1 & job2", ["job_1", "&", "job2"]),
        ("_a | _b", ["_a", "|", "_b"]),
        # whitespace robustness
        ("  a   &   ( b |  c ) ", ["a", "&", ["b", "|", "c"]]),
    ],
)
def test_parse_valid_expressions(expr, expected):
    assert DependencyExpressionModel.parse(expr) == expected


def test_operator_precedence_and_binds_tighter_than_or():
    # a | (b & c)
    assert DependencyExpressionModel.parse("a | b & c") == ["a", "|", ["b", "&", "c"]]
    # (a & b) | c
    assert DependencyExpressionModel.parse("a & b | c") == [["a", "&", "b"], "|", "c"]


def test_parentheses_override_precedence():
    # (a | b) & c
    assert DependencyExpressionModel.parse("(a | b) & c") == [["a", "|", "b"], "&", "c"]
    # a & (b | c)
    assert DependencyExpressionModel.parse("a & (b | c)") == ["a", "&", ["b", "|", "c"]]
