from __future__ import annotations
from typing import Any


class DependencyExpressionView:
    """View layer: formats output for presentation (CLI/string)."""

    @staticmethod
    def render_success(expression: str, parsed: Any) -> str:
        return (
            "✅ Parsed successfully\n"
            f"  input:  {expression}\n"
            f"  output: {parsed}\n"
        )

    @staticmethod
    def render_error(expression: str, error: Exception) -> str:
        return (
            " Invalid expression\n"
            f"  input: {expression}\n"
            f"  error: {error}\n"
        )
