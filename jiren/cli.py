import sys
from argparse import ArgumentParser

from nestargs import NestedArgumentParser

from . import Template


class Application:
    def run(self):
        pre_parser = ArgumentParser(add_help=False)
        pre_parser.add_argument("infile", nargs="?")
        pre_args, _ = pre_parser.parse_known_args()

        if pre_args.infile:
            with open(pre_args.infile, "r") as f:
                source = f.read()
        else:
            source = sys.stdin.read()

        template = Template(source)

        parser = NestedArgumentParser(parents=[pre_parser])
        var_group = parser.add_argument_group("variables")
        for v in template.variables:
            var_group.add_argument("--var." + v)
        args = parser.parse_args()

        if "var" in args:
            variables = {k: v for k, v in vars(args.var).items() if v is not None}
        else:
            variables = {}
        print(template.render(**variables))


def main():
    Application().run()
