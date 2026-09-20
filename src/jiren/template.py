from collections.abc import Mapping
from typing import Any

from minijinja import Environment


class Template:
    def __init__(self, source: str):
        self.env = Environment(templates={"source": source})
        self.variables = self.env.undeclared_variables_in_template("source")

    def render(
        self, context: Mapping[str, Any] | None = None, /, **override_context: Any
    ) -> str:
        if context is not None:
            context = {**context, **override_context}
        else:
            context = override_context
        return self.env.render_template("source", **context)
