import pytest

from jiren.renderer import (
    InvalidDataError,
    MissingVariablesError,
    UnknownDataVariablesError,
    render_template,
    template_variables,
)


@pytest.mark.parametrize(
    "template_source,variables,expected",
    [
        ("{{ greeting }}", {"greeting": "hello"}, "hello"),
        ("{{ greeting }}", {}, ""),
        ("{{ greeting | default('hi') }}", {}, "hi"),
        ("hello", {}, "hello"),
        ("", {}, ""),
    ],
)
def test_render_template(template_source, variables, expected):
    assert render_template(template_source, variables=variables) == expected


def test_template_variables():
    assert template_variables("{{ greeting }}, {{ name }}") == {"greeting", "name"}


def test_render_template_with_data_source():
    data_source = "greeting:\n  message: hello\n  target: world"

    rendered = render_template(
        "{{ greeting.message }}, {{ greeting.target }}", data_source=data_source
    )

    assert rendered == "hello, world"


def test_render_template_command_line_variables_override_data_source():
    rendered = render_template(
        "{{ message }}, {{ name }}",
        data_source="message: hello",
        variables={"message": "hey", "name": "you"},
    )

    assert rendered == "hey, you"


def test_render_template_rejects_non_mapping_data_source():
    with pytest.raises(
        InvalidDataError, match="the data file must have at least one key"
    ):
        render_template("{{ greeting }}", data_source="hello")


def test_render_template_rejects_unknown_data_variables_in_strict_mode():
    with pytest.raises(
        UnknownDataVariablesError,
        match="the data file contains unknown variables: a, b, c",
    ):
        render_template("{{ greeting }}", data_source="a: 1\nb: 2\nc: 3", strict=True)


def test_render_template_rejects_missing_variables_in_required_mode():
    with pytest.raises(
        MissingVariablesError,
        match="the following variables are required: greeting",
    ):
        render_template("{{ greeting }}", required=True)
