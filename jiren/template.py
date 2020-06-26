import jinja2
from jinja2.meta import find_undeclared_variables


class Template(jinja2.Template):
    def __init__(self, source):
        super().__init__()

        ast = self.environment.parse(source)

        self.source = source
        self.variables = find_undeclared_variables(ast)
