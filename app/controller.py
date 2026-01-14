from __future__ import annotations
from app.model import DependencyExpressionModel, ParseError
from app.view import DependencyExpressionView


class DependencyExpressionController:
    """Controller layer: orchestrates model + view."""

    def __init__(self, model: DependencyExpressionModel, view: DependencyExpressionView):
        self.model = model
        self.view = view

    def handle_parse_request(self, expression: str) -> str:
        try:
            parsed = self.model.parse(expression)
            return self.view.render_success(expression, parsed)
        except ParseError as e:
            return self.view.render_error(expression, e)
