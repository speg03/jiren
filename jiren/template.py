from argparse import ArgumentParser

import jinja2
from jinja2.meta import find_undeclared_variables


class Template(jinja2.Template):
    def __init__(self, source):
        super().__init__()

        ast = self.environment.parse(source)

        self.source = source
        self.variables = find_undeclared_variables(ast)


class TemplateParser:
    def __init__(self, source, required=False):
        self.template = Template(source)
        self.required = required

    def apply(self, variable_args):
        parser = ArgumentParser()
        group = parser.add_argument_group("Template variables")
        for v in self.template.variables:
            group.add_argument("--{}".format(v), required=self.required)
        args = parser.parse_args(variable_args)

        variables = {k: v for k, v in vars(args).items() if v is not None}
        return self.template.render(**variables)
