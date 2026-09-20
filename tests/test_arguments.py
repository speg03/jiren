from jiren.arguments import (
    create_variable_parser,
    parse_cli_arguments,
    parse_variable_options,
)


def test_parse_cli_arguments_separates_variable_options():
    _, args, variable_options = parse_cli_arguments(
        ["--strict", "-", "--", "--greeting=hello"]
    )

    assert args.strict is True
    assert args.template == "-"
    assert variable_options == ["--greeting=hello"]


def test_variable_parser_includes_template_variables_and_data_defaults():
    parser = create_variable_parser(
        {"greeting": {"message": "hello"}},
        {"greeting.message", "name"},
        max_depth=1,
    )

    assert parse_variable_options(parser, ["--name=world"]) == {
        "greeting": {"message": "hello"},
        "name": "world",
    }


def test_variable_parser_supports_nested_values():
    parser = create_variable_parser({}, {"user.profile.name"}, max_depth=2)

    assert parse_variable_options(parser, ["--user.profile.name=you"]) == {
        "user": {"profile": {"name": "you"}}
    }
