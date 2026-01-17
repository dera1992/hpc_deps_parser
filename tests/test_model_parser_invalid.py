import pytest
from app.model import DependencyExpressionModel, ParseError


@pytest.mark.parametrize(
    "expr",
    [
        "",             # empty
        "   ",          # whitespace only
        "&",            # operator alone
        "|",
        "a &",          # missing operand
        "a |",
        "(a & b",       # missing ')'
        "a & b)",       # extra ')'
        "()",           # empty parentheses
        "( )",          # empty parentheses with spaces
        "a (b | c)",    # missing operator between a and '('
        "a b",          # missing operator
        "a & | b",      # operator chain
        "a | & b",
        ")",            # stray close paren
        "(",            # stray open paren
        "1a & b",       # invalid identifier start
        "a + b",        # invalid character
        "a || b",       # invalid tokenization / syntax
        "a && b",       # invalid tokenization / syntax
    ],
)

def test_parse_invalid_expressions(expr):
    with pytest.raises(ParseError):
        DependencyExpressionModel.parse(expr)


def test_error_message_contains_position_for_unclosed_paren():
    expr = "(a & b"
    with pytest.raises(ParseError) as e:
        DependencyExpressionModel.parse(expr)
    msg = str(e.value)
    assert "Unclosed" in msg or "expected ')'" in msg


def test_error_message_contains_position_for_unexpected_token():
    expr = "a & b c"
    with pytest.raises(ParseError) as e:
        DependencyExpressionModel.parse(expr)
    msg = str(e.value)
    assert "Unexpected" in msg
