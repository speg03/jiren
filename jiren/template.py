from jinja2 import Environment
from jinja2.meta import find_undeclared_variables


class Template:
    def __init__(self, source):
        self.environment = Environment()
        self.source = source

    def variables(self):
        ast = self.environment.parse(self.source)
        return find_undeclared_variables(ast)

    def render(self, *args, **kwargs):
        template = self.environment.from_string(self.source)
        return template.render(*args, **kwargs)
