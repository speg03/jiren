import jinja2
from jinja2.meta import find_undeclared_variables


class Template:
    def __init__(self, template_str):
        self.env = jinja2.Environment()
        self.template_str = template_str

    def variables(self):
        ast = self.env.parse(self.template_str)
        return find_undeclared_variables(ast)

    def render(self, *args, **kwargs):
        template = self.env.from_string(self.template_str)
        return template.render(*args, **kwargs)
