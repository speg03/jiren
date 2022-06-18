from typing import Any

import jinja2
from jinja2 import meta


class Template:
    def __init__(self, source: str):
        env = jinja2.Environment()
        self._template = env.from_string(source)

        ast = env.parse(source)
        self.variables = meta.find_undeclared_variables(ast)

    def render(self, *args: Any, **kwargs: Any) -> str:
        return self._template.render(*args, **kwargs)
