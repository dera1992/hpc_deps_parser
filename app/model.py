from __future__ import annotations
from dataclasses import dataclass
from typing import Any


class ParseError(ValueError):
    """Raised when the expression is not a valid dependency expression."""


@dataclass(frozen=True)
class Token:
    kind: str   # "ID", "AND", "OR", "LPAREN", "RPAREN", "EOF"
    value: str
    pos: int


class DependencyExpressionModel:
    """
    Model layer:
    - tokenizes the expression
    - parses it into a nested Python list structure
    - rejects invalid expressions by raising ParseError
    """

    @staticmethod
    def parse(expression: str) -> Any:
        tokens = DependencyExpressionModel._tokenize(expression)
        parser = DependencyExpressionModel._Parser(tokens)
        return parser.parse()

    @staticmethod
    def _tokenize(expr: str) -> list[Token]:
        tokens: list[Token] = []
        i = 0
        n = len(expr)

        def add(kind: str, value: str, pos: int):
            tokens.append(Token(kind, value, pos))

        while i < n:
            ch = expr[i]

            if ch.isspace():
                i += 1
                continue

            if ch == "&":
                add("AND", "&", i)
                i += 1
                continue

            if ch == "|":
                add("OR", "|", i)
                i += 1
                continue

            if ch == "(":
                add("LPAREN", "(", i)
                i += 1
                continue

            if ch == ")":
                add("RPAREN", ")", i)
                i += 1
                continue

            # Identifiers: [A-Za-z_][A-Za-z0-9_]*
            if ch.isalpha() or ch == "_":
                start = i
                i += 1
                while i < n and (expr[i].isalnum() or expr[i] == "_"):
                    i += 1
                add("ID", expr[start:i], start)
                continue

            raise ParseError(f"Unexpected character '{ch}' at position {i}")

        add("EOF", "", n)
        return tokens

    class _Parser:
        """
        Recursive-descent parser with precedence:

          expr     := or_expr
          or_expr  := and_expr ( '|' and_expr )*
          and_expr := primary ( '&' primary )*
          primary  := ID | '(' expr ')'

        This enforces:
        - '&' binds tighter than '|'
        - parentheses override precedence
        """

        def __init__(self, tokens: list[Token]):
            self.tokens = tokens
            self.i = 0

        def cur(self) -> Token:
            return self.tokens[self.i]

        def consume(self, kind: str) -> Token:
            tok = self.cur()
            if tok.kind != kind:
                raise ParseError(f"Expected {kind} at position {tok.pos}, got {tok.kind}")
            self.i += 1
            return tok

        def match(self, kind: str) -> bool:
            if self.cur().kind == kind:
                self.i += 1
                return True
            return False

        def parse(self) -> Any:
            node = self.parse_or()
            if self.cur().kind != "EOF":
                tok = self.cur()
                raise ParseError(f"Unexpected token '{tok.value}' at position {tok.pos}")
            return node

        def parse_or(self) -> Any:
            left = self.parse_and()
            parts = [left]
            while self.match("OR"):
                right = self.parse_and()
                parts.extend(["|", right])
            return parts[0] if len(parts) == 1 else parts

        def parse_and(self) -> Any:
            left = self.parse_primary()
            parts = [left]
            while self.match("AND"):
                right = self.parse_primary()
                parts.extend(["&", right])
            return parts[0] if len(parts) == 1 else parts

        def parse_primary(self) -> Any:
            tok = self.cur()

            if tok.kind == "ID":
                self.consume("ID")
                return tok.value

            if tok.kind == "LPAREN":
                lpar = self.consume("LPAREN")
                inner = self.parse_or()
                if self.cur().kind != "RPAREN":
                    t = self.cur()
                    raise ParseError(
                        f"Unclosed '(' starting at position {lpar.pos}; expected ')' near {t.pos}"
                    )
                self.consume("RPAREN")
                return inner

            raise ParseError(f"Expected identifier or '(' at position {tok.pos}")
