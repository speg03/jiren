import pytest

from jiren.renderer import (
    InvalidDataError,
    MissingVariablesError,
    UnknownDataVariablesError,
    merge_template_data,
    parse_data_source,
    render_template,
    template_variables,
)


@pytest.mark.parametrize(
    "template_source,data_source,expected",
    [
        ("{{ greeting }}", {"greeting": "hello"}, "hello"),
        ("{{ greeting }}", {}, ""),
        ("{{ greeting | default('hi') }}", {}, "hi"),
        ("hello", {}, "hello"),
        ("", {}, ""),
    ],
)
def test_render_template(template_source, data_source, expected):
    assert render_template(template_source, data_source=data_source) == expected


def test_template_variables():
    assert template_variables("{{ greeting.message }}, {{ name }}") == {
        "greeting.message",
        "name",
    }


@pytest.mark.parametrize(
    "source,expected",
    [
        ("greeting: hello", {"greeting": "hello"}),
        ('{"count": 42, "enabled": true}', {"count": 42, "enabled": True}),
        (None, {}),
    ],
)
def test_parse_data_source(source, expected):
    assert parse_data_source(source) == expected


@pytest.mark.parametrize("source", ["not a mapping", "- item", "null"])
def test_parse_data_source_rejects_non_mapping(source):
    with pytest.raises(
        InvalidDataError, match="the data file must have at least one key"
    ):
        parse_data_source(source)


def test_merge_template_data_preserves_source_values_and_prunes_added_none_values():
    data_source = {
        "message": None,
        "greeting": {"message": "hello", "target": "world"},
    }
    variable_values = {
        "message": None,
        "name": None,
        "greeting": {"message": "hey", "target": "world", "extra": None},
    }

    assert merge_template_data(data_source, variable_values) == {
        "message": None,
        "greeting": {"message": "hey", "target": "world"},
    }


def test_render_template_with_data_source():
    data_source = {"greeting": {"message": "hello", "target": "world"}}

    rendered = render_template(
        "{{ greeting.message }}, {{ greeting.target }}", data_source=data_source
    )

    assert rendered == "hello, world"


def test_render_template_uses_combined_data_source():
    rendered = render_template(
        "{{ message }}, {{ name }}",
        data_source={"message": "hey", "name": "you"},
    )

    assert rendered == "hey, you"


def test_render_template_rejects_unknown_data_variables_in_strict_mode():
    with pytest.raises(
        UnknownDataVariablesError,
        match="the data file contains unknown variables: a, b, c",
    ):
        render_template(
            "{{ greeting }}", data_source={"a": 1, "b": 2, "c": 3}, strict=True
        )


def test_render_template_accepts_nested_data_variables_in_strict_mode():
    assert (
        render_template(
            "{{ greeting.message }}",
            data_source={"greeting": {"message": "hello"}},
            strict=True,
        )
        == "hello"
    )


def test_render_template_rejects_unknown_nested_data_variables_in_strict_mode():
    with pytest.raises(
        UnknownDataVariablesError,
        match="the data file contains unknown variables: greeting.target",
    ):
        render_template(
            "{{ greeting.message }}",
            data_source={"greeting": {"message": "hello", "target": "world"}},
            strict=True,
        )


def test_render_template_rejects_missing_variables_in_required_mode():
    with pytest.raises(
        MissingVariablesError,
        match="the following variables are required: greeting",
    ):
        render_template("{{ greeting }}", required=True)


def test_render_template_rejects_missing_nested_variables_in_required_mode():
    with pytest.raises(
        MissingVariablesError,
        match="the following variables are required: greeting.message",
    ):
        render_template(
            "{{ greeting.message }}", data_source={"greeting": {}}, required=True
        )
