import argparse
from collections.abc import Sequence
from copy import deepcopy
from typing import Any

from nestargs import NestedArgumentParser


def parse_cli_arguments(
    command_line_args: Sequence[str],
) -> tuple[argparse.ArgumentParser, argparse.Namespace, list[str]]:
    """Parse primary CLI options and separate template-variable options."""
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

    if "--" in command_line_args:
        separator_index = command_line_args.index("--")
        parser_args = command_line_args[:separator_index]
        variable_options = list(command_line_args[separator_index + 1 :])
    else:
        parser_args = command_line_args
        variable_options = []
    return parser, parser.parse_args(parser_args), variable_options


def create_variable_parser(
    data_source: dict[str, Any], variables: set[str], *, max_depth: int
) -> NestedArgumentParser:
    """Create a parser for template variables using data-source defaults."""
    parser = NestedArgumentParser(add_help=False, usage=argparse.SUPPRESS)
    parser.add_arguments_from_dict(
        _add_template_variables(data_source, variables), max_depth=max_depth
    )
    return parser


def parse_variable_options(
    parser: NestedArgumentParser, variable_options: Sequence[str]
) -> dict[str, Any]:
    """Parse template-variable options into a nested mapping."""
    return _namespace_to_dict(parser.parse_args(variable_options))


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
