import argparse

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
        "-i",
        "--input",
        type=argparse.FileType("r"),
        help='An input template file path. If "-" is provided, use stdin.',
    )
    parser.add_argument(
        "variables", nargs="*", help='"--" followed by options for variables.'
    )
    args = parser.parse_args()

    variable_parser = argparse.ArgumentParser(add_help=False, usage=argparse.SUPPRESS)
    variable_group = variable_parser.add_argument_group("variables")

    if args.input:
        template = Template(args.input.read())
        for v in template.variables:
            sanitized_name = v.replace("_", "-").lstrip("-").rstrip("-")
            variable_group.add_argument(
                f"--{sanitized_name}", dest=v, required=args.required
            )

    if args.help:
        parser.print_help()
        print()
        variable_parser.print_help()
        parser.exit(0)
    elif args.version:
        print(f"jiren, version {jiren_version}")
        print(f"jinja2, version {jinja2_version}")
        parser.exit(0)
    elif args.input is None:
        parser.error("the following arguments are required: --input")

    variable_args = variable_parser.parse_args(args.variables or [])
    variables = {k: v for k, v in vars(variable_args).items() if v is not None}

    # The template is not Unbound
    rendered_text = template.render(variables)  # type: ignore
    print(rendered_text)
