from __future__ import annotations
from app.controller import DependencyExpressionController
from app.model import DependencyExpressionModel
from app.view import DependencyExpressionView


def main():
    controller = DependencyExpressionController(
        model=DependencyExpressionModel(),
        view=DependencyExpressionView(),
    )

    examples = [
        "a & b",
        "a | b | c",
        "a & (b | c)",
        "(a & b) | (b & c)",
        "a &",          # invalid
        "a (b | c)",    # invalid
        "a && b",       # invalid
        ")",            # invalid
    ]

    for expr in examples:
        print(controller.handle_parse_request(expr))


if __name__ == "__main__":
    main()
