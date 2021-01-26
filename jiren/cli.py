import sys
from argparse import ArgumentParser

from . import __version__ as jiren_version
from .template import TemplateParser


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-V", "--version", help="show the version and exit", action="store_true"
    )
    parser.add_argument(
        "--required",
        action="store_true",
        help="Required the specific values for all variables.",
    )
    parser.add_argument(
        "-i",
        "--input",
        help='An input template file path. If "-" or omitted, use stdin.',
    )
    parser.add_argument(
        "variables", nargs="*", help="Arguments for variables in the template"
    )
    args = parser.parse_args()

    if args.version:
        print("jiren version {}".format(jiren_version))
        sys.exit(0)
    if args.input is None or args.input == "-":
        source = sys.stdin.read()
    else:
        with open(args.input, "r") as f:
            source = f.read()

    template_parser = TemplateParser(source, required=args.required)
    rendered_text = template_parser.apply(args.variables)
    print(rendered_text)
