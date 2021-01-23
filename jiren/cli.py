import sys
from argparse import ArgumentParser

from . import __version__ as jiren_version
from .template import TemplateParser


class Application:
    def run(self):
        command_parser = ArgumentParser()
        command_parser.add_argument(
            "-V", "--version", help="show the version and exit", action="store_true"
        )
        command_parser.add_argument(
            "--required",
            action="store_true",
            help="Required the specific values for all variables.",
        )
        command_parser.add_argument(
            "-i",
            "--input",
            help='An input template file path. If "-" or omitted, use stdin.',
        )
        command_parser.add_argument(
            "variables", nargs="*", help="Arguments for variables in the template"
        )
        command_args = command_parser.parse_args()

        if command_args.version:
            print("jiren version {}".format(jiren_version))
            sys.exit(0)
        if command_args.input is None or command_args.input == "-":
            source = sys.stdin.read()
        else:
            with open(command_args.input, "r") as f:
                source = f.read()

        template_parser = TemplateParser(source, required=command_args.required)
        rendered_text = template_parser.apply(command_args.variables)
        print(rendered_text)


def main():
    Application().run()
