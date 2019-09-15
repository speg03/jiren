import sys
from argparse import ArgumentParser

from nestargs import NestedArgumentParser

from . import Template


class Application:
    def run(self):
        pre_parser = ArgumentParser(add_help=False)
        pre_parser.add_argument(
            "template",
            nargs="?",
            help="Template file path. If omitted, read a template from stdin.",
        )
        pre_parser.add_argument(
            "-s",
            "--strict",
            action="store_true",
            help="You must specify values for all variables.",
        )
        pre_args, _ = pre_parser.parse_known_args()

        if pre_args.template:
            with open(pre_args.template, "r") as f:
                source = f.read()
        else:
            source = sys.stdin.read()

        template = Template(source)

        parser = NestedArgumentParser(
            description="Generate text from a template", parents=[pre_parser]
        )
        var_group = parser.add_argument_group("variables")
        for v in template.variables:
            var_group.add_argument("--var." + v, required=pre_args.strict)
        args = parser.parse_args()

        if "var" in args:
            variables = {k: v for k, v in vars(args.var).items() if v is not None}
        else:
            variables = {}
        print(template.render(**variables))


def main():
    Application().run()
