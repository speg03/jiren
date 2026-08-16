import argparse
import logging
import sys

from . import __version__
from .renderer import InvalidDataError, RenderError, render_template, template_variables


def main():
    parser = argparse.ArgumentParser(add_help=False, description="Template renderer")
    parser.add_argument(
        "-h", "--help", action="store_true", help="Show this message and exit."
    )
    parser.add_argument(
        "-V", "--version", action="store_true", help="Show the version and exit."
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable log output for debugging."
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
    data_group = parser.add_mutually_exclusive_group()
    data_group.add_argument(
        "-d",
        "--data",
        help="A structured data file path. Accepts JSON or YAML files.",
    )
    data_group.add_argument(
        "--data-string",
        help="Structured JSON or YAML data supplied directly on the command line.",
    )
    parser.add_argument(
        "template",
        nargs="?",
        help='A template file path. Omit it or provide "-" to use stdin.',
    )

    command_line_args = sys.argv[1:]
    if "--" in command_line_args:
        separator_index = command_line_args.index("--")
        parser_args = command_line_args[:separator_index]
        variable_options = command_line_args[separator_index + 1 :]
    else:
        parser_args = command_line_args
        variable_options = []
    args = parser.parse_args(parser_args)

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    logger = logging.getLogger(__name__)
    logger.debug("arguments: %s", args)

    if args.template is None and args.help:
        parser.print_help()
        parser.exit(0)
    elif args.version:
        print(__version__)
        parser.exit(0)

    if args.template is None or args.template == "-":
        template_source = sys.stdin.read()
    else:
        try:
            with open(args.template, "r") as f:
                template_source = f.read()
        except OSError:
            parser.error(f"cannot read template file: {args.template}")

    data_source = None
    if args.data:
        try:
            with open(args.data, "r") as f:
                data_source = f.read()
        except OSError:
            parser.error(f"cannot read data file: {args.data}")
    elif args.data_string:
        data_source = args.data_string

    variable_parser = argparse.ArgumentParser(add_help=False, usage=argparse.SUPPRESS)
    variable_group = variable_parser.add_argument_group("variables")

    logger.debug("template: %s", template_source)
    variables_in_template = template_variables(template_source)
    for v in variables_in_template:
        sanitized_name = v.replace("_", "-").strip("-")
        variable_group.add_argument(f"--{sanitized_name}", dest=v)
    logger.debug("variables in the template: %s", sorted(variables_in_template))

    if args.help:
        parser.print_help()
        print()
        variable_parser.print_help()
        parser.exit(0)

    # Load variables from command line arguments.
    variable_args = variable_parser.parse_args(variable_options)
    variables = {k: v for k, v in vars(variable_args).items() if v is not None}
    logger.debug("variables from command line: %s", variables)

    try:
        rendered_text = render_template(
            template_source,
            data_source=data_source,
            variables=variables,
            strict=args.strict,
            required=args.required,
        )
    except InvalidDataError as error:
        parser.error(f"{error}: {args.data}")
    except RenderError as error:
        parser.error(str(error))

    print(rendered_text)
