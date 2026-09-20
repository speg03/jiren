import pytest

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


def test_parse_cli_arguments_rejects_negative_max_depth(capsys):
    with pytest.raises(SystemExit) as error:
        parse_cli_arguments(["--max-depth=-1"])

    assert error.value.code == 2
    assert (
        "argument --max-depth: must be greater than or equal to 0"
        in capsys.readouterr().err
    )


def test_variable_parser_includes_template_variables_with_none_defaults():
    parser = create_variable_parser({"greeting.message", "name"}, max_depth=1)

    assert parse_variable_options(parser, ["--name=world"]) == {
        "greeting": {"message": None},
        "name": "world",
    }


def test_variable_parser_treats_scalar_overrides_as_strings():
    parser = create_variable_parser({"count", "enabled"}, max_depth=1)

    assert parse_variable_options(parser, ["--count=2", "--enabled=false"]) == {
        "count": "2",
        "enabled": "false",
    }


def test_variable_parser_supports_nested_values():
    parser = create_variable_parser({"user.profile.name"}, max_depth=2)

    assert parse_variable_options(parser, ["--user.profile.name=you"]) == {
        "user": {"profile": {"name": "you"}}
    }
