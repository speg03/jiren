import logging
import sys

from . import __version__
from .arguments import (
    create_variable_parser,
    parse_cli_arguments,
    parse_variable_options,
)
from .renderer import (
    InvalidDataError,
    RenderError,
    merge_template_data,
    parse_data_source,
    render_template,
    template_variables,
)


def main():
    """Run the jiren command-line interface."""
    parser, args, variable_options = parse_cli_arguments(sys.argv[1:])

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
        data = parse_data_source(data_source)
    except InvalidDataError as error:
        data_label = args.data if args.data else "--data-string"
        parser.error(f"{error}: {data_label}")

    variable_parser = create_variable_parser(
        variables_in_template, max_depth=args.max_depth
    )

    if args.help:
        parser.print_help()
        print()
        variable_parser.print_help()
        parser.exit(0)

    # Load variables from command line arguments.
    variable_values = parse_variable_options(variable_parser, variable_options)
    data = merge_template_data(data, variable_values)
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
