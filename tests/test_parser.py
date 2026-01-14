import pytest
from app.model import DependencyExpressionModel, ParseError


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("a & b", ["a", "&", "b"]),
        ("a | b | c", ["a", "|", "b", "|", "c"]),
        ("a & (b | c)", ["a", "&", ["b", "|", "c"]]),
        ("(a & b) | (c & d)", [["a", "&", "b"], "|", ["c", "&", "d"]]),
        # precedence: '&' binds tighter than '|'
        ("a | b & c", ["a", "|", ["b", "&", "c"]]),
        ("a & b | c", [["a", "&", "b"], "|", "c"]),
        # whitespace tolerance
        ("  a   &   ( b |  c ) ", ["a", "&", ["b", "|", "c"]]),
        # identifiers
        ("job_1 & job2", ["job_1", "&", "job2"]),
    ],
)
def test_valid_expressions(expr, expected):
    assert DependencyExpressionModel.parse(expr) == expected


@pytest.mark.parametrize(
    "expr",
    [
        "",             # empty
        "   ",          # empty (spaces)
        "&",            # operator without operands
        "|",
        "a &",          # missing operand
        "a |",          # missing operand
        "(a & b",       # missing closing paren
        "a & b)",       # extra closing paren
        "()",           # empty parentheses not allowed by grammar
        "a (b | c)",    # missing operator
        "a && b",       # invalid token
        "a || b",       # invalid token
        "a & | b",      # malformed
        ")",            # stray closing paren
        "(",            # stray opening paren
        "1a & b",       # invalid identifier start
        "a + b",        # invalid character
    ],
)
def test_invalid_expressions(expr):
    with pytest.raises(ParseError):
        DependencyExpressionModel.parse(expr)
