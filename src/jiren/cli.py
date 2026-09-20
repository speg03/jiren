import argparse
import logging
import sys
from copy import deepcopy
from typing import Any

import yaml
from nestargs import NestedArgumentParser

from . import __version__
from .renderer import InvalidDataError, RenderError, render_template, template_variables


def _add_template_variables(
    data_source: dict[str, Any], variables: set[str]
) -> dict[str, Any]:
    argument_values = deepcopy(data_source)
    for variable in variables:
        current = argument_values
        *parents, key = variable.split(".")
        for parent in parents:
            value = current.get(parent)
            if not isinstance(value, dict):
                value = {}
                current[parent] = value
            current = value
        current.setdefault(key, None)
    return argument_values


def _namespace_to_dict(value: Any) -> Any:
    if isinstance(value, argparse.Namespace):
        return {key: _namespace_to_dict(item) for key, item in vars(value).items()}
    return value


def _remove_added_none_values(
    values: dict[str, Any], data_source: dict[str, Any]
) -> dict[str, Any]:
    result = {}
    for key, value in values.items():
        source_value = data_source.get(key)
        if isinstance(value, dict):
            source_mapping = source_value if isinstance(source_value, dict) else {}
            result[key] = _remove_added_none_values(value, source_mapping)
        elif value is not None or key in data_source:
            result[key] = value
    return result


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
    parser.add_argument(
        "--max-depth",
        type=int,
        default=1,
        help="Maximum nesting depth for command-line variables.",
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

    logger.debug("template: %s", template_source)
    variables_in_template = template_variables(template_source)
    logger.debug("variables in the template: %s", sorted(variables_in_template))

    try:
        data: dict[str, Any] = {}
        if data_source is not None:
            loaded_data = yaml.safe_load(data_source)
            if not isinstance(loaded_data, dict):
                raise InvalidDataError("the data file must have at least one key")
            data = loaded_data
    except InvalidDataError as error:
        data_label = args.data if args.data else "--data-string"
        parser.error(f"{error}: {data_label}")

    variable_parser = NestedArgumentParser(add_help=False, usage=argparse.SUPPRESS)
    variable_parser.add_arguments_from_dict(
        _add_template_variables(data, variables_in_template), max_depth=args.max_depth
    )

    if args.help:
        parser.print_help()
        print()
        variable_parser.print_help()
        parser.exit(0)

    # Load variables from command line arguments.
    variable_args = variable_parser.parse_args(variable_options)
    data = _remove_added_none_values(_namespace_to_dict(variable_args), data)
    logger.debug("variables from command line: %s", data)

    try:
        rendered_text = render_template(
            template_source,
            data_source=data,
            strict=args.strict,
            required=args.required,
        )
    except RenderError as error:
        parser.error(str(error))

    print(rendered_text)
