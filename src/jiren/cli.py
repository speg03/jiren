import argparse
import sys

import yaml

from .template import Template
from .versions import jinja2_version, jiren_version


def main():
    parser = argparse.ArgumentParser(add_help=False, description="Template renderer")
    parser.add_argument(
        "-h", "--help", action="store_true", help="Show this message and exit."
    )
    parser.add_argument(
        "-V", "--version", action="store_true", help="Show the version and exit."
    )
    parser.add_argument(
        "--required",
        action="store_true",
        help="A specific value must be provided for each variable.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="All variables contained in the data file must be used in the template.",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=argparse.FileType("r"),
        help=(
            "Deprecated. Use the template argument instead. "
            'An input template file path. If "-" is provided, use stdin.'
        ),
    )
    parser.add_argument(
        "-d",
        "--data",
        type=argparse.FileType("r"),
        help="A structured data file path. Accepts JSON or YAML files.",
    )
    # TODO: Change the template argument to FileType when removing the input option.
    parser.add_argument(
        "template",
        nargs="?",
        help='A template file path. If "-" is provided, use stdin.',
    )
    parser.add_argument(
        "variables", nargs="*", help='"--" followed by options for variables.'
    )
    args = parser.parse_args()

    template_source = None
    variable_options = args.variables
    # If the deprecated input option is used, the template argument is considered to be
    # the first of the variables argument.
    if args.input:
        template_source = args.input.read()
        if args.template is not None:
            variable_options = [args.template]
            variable_options.extend(args.variables)
    elif args.template == "-":
        template_source = sys.stdin.read()
    elif args.template:
        with open(args.template, "r") as f:
            template_source = f.read()

    variable_parser = argparse.ArgumentParser(add_help=False, usage=argparse.SUPPRESS)
    variable_group = variable_parser.add_argument_group("variables")

    template = None
    if template_source is not None:
        template = Template(template_source)
        for v in template.variables:
            sanitized_name = v.replace("_", "-").strip("-")
            variable_group.add_argument(f"--{sanitized_name}", dest=v)

    if args.help:
        parser.print_help()
        print()
        variable_parser.print_help()
        parser.exit(0)
    elif args.version:
        print(f"jiren, version {jiren_version}")
        print(f"jinja2, version {jinja2_version}")
        parser.exit(0)
    elif template is None:
        parser.error("the following arguments are required: --input")

    # Load variables contained in the data file. Must be in dictionary format.
    provided_data = yaml.safe_load(args.data) if args.data else {}
    if not isinstance(provided_data, dict):
        parser.error(f"the data file must have at least one key: {args.data.name}")

    # In strict mode, exit if any variables are not present in the template.
    unknown_variables = set(provided_data.keys()) - template.variables
    if args.strict and unknown_variables:
        parser.error(
            "the data file contains unknown variables: "
            f"{', '.join(sorted(unknown_variables))}"
        )

    # Load variables from command line arguments.
    variable_args = variable_parser.parse_args(variable_options)
    variables = {k: v for k, v in vars(variable_args).items() if v is not None}

    # Merge variables in data files and command line arguments.
    provided_data.update(variables)

    # In required mode, exit if a variable in the template is not provided.
    missing_variables = template.variables - set(provided_data.keys())
    if args.required and missing_variables:
        parser.error(
            "the following variables are required: "
            f"{', '.join(sorted(missing_variables))}"
        )

    rendered_text = template.render(provided_data)
    print(rendered_text)
