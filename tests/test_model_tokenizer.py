import pytest
from app.model import DependencyExpressionModel, ParseError


def test_tokenizer_ignores_whitespace():
    tokens = DependencyExpressionModel._tokenize("  a   &   ( b |  c )  ")
    # token kinds and values (ignoring positions)
    got = [(t.kind, t.value) for t in tokens]
    assert got == [
        ("ID", "a"),
        ("AND", "&"),
        ("LPAREN", "("),
        ("ID", "b"),
        ("OR", "|"),
        ("ID", "c"),
        ("RPAREN", ")"),
        ("EOF", ""),
    ]


@pytest.mark.parametrize(
    "expr, expected_pairs",
    [
        ("a&b", [("ID", "a"), ("AND", "&"), ("ID", "b"), ("EOF", "")]),
        ("a|b|c", [("ID", "a"), ("OR", "|"), ("ID", "b"), ("OR", "|"), ("ID", "c"), ("EOF", "")]),
        ("(a)", [("LPAREN", "("), ("ID", "a"), ("RPAREN", ")"), ("EOF", "")]),
        ("job_1 & job2", [("ID", "job_1"), ("AND", "&"), ("ID", "job2"), ("EOF", "")]),
        ("_x1|_y2", [("ID", "_x1"), ("OR", "|"), ("ID", "_y2"), ("EOF", "")]),
    ],
)
def test_tokenizer_basic(expr, expected_pairs):
    tokens = DependencyExpressionModel._tokenize(expr)
    assert [(t.kind, t.value) for t in tokens] == expected_pairs


@pytest.mark.parametrize(
    "expr, bad_char",
    [
        ("a + b", "+"),
        ("a @ b", "@"),
        ("a # b", "#"),
    ],
)
def test_tokenizer_rejects_invalid_characters(expr, bad_char):
    with pytest.raises(ParseError) as e:
        DependencyExpressionModel._tokenize(expr)
    assert "Unexpected character" in str(e.value)
    assert bad_char in str(e.value)

