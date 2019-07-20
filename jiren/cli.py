import sys

import nestargs

import jiren


class Application:
    def run(self):
        parser = nestargs.NestedArgumentParser(add_help=False)
        parser.add_argument("infile", nargs="?")
        args, _ = parser.parse_known_args()

        if args.infile:
            with open(args.infile, "r") as f:
                template_str = f.read()
        else:
            template_str = sys.stdin.read()

        template = jiren.Template(template_str)

        var_parser = nestargs.NestedArgumentParser(parents=[parser])
        var_group = var_parser.add_argument_group("variables")
        for v in template.variables():
            var_group.add_argument("--var." + v)
        args = var_parser.parse_args()

        if "var" in args:
            variables = {k: v for k, v in vars(args.var).items() if v is not None}
        else:
            variables = {}
        print(template.render(**variables))


def main():
    Application().run()
