from collections.abc import Mapping
from typing import Any

from .template import Template


class RenderError(Exception):
    pass


class InvalidDataError(RenderError):
    pass


class UnknownDataVariablesError(RenderError):
    pass


class MissingVariablesError(RenderError):
    pass


def template_variables(template_source: str) -> set[str]:
    return Template(template_source).variables


def _data_variable_paths(data: Mapping[str, Any], prefix: str = "") -> set[str]:
    paths = set()
    for key, value in data.items():
        path = f"{prefix}.{key}" if prefix else key
        if isinstance(value, Mapping) and value:
            paths.update(_data_variable_paths(value, path))
        else:
            paths.add(path)
    return paths


def _has_variable(data: Mapping[str, Any], variable: str) -> bool:
    value: Any = data
    for key in variable.split("."):
        if not isinstance(value, Mapping) or key not in value:
            return False
        value = value[key]
    return True


def _paths_are_related(data_path: str, template_path: str) -> bool:
    return (
        data_path == template_path
        or data_path.startswith(f"{template_path}.")
        or template_path.startswith(f"{data_path}.")
    )


def render_template(
    template_source: str,
    *,
    data_source: Mapping[str, Any] | None = None,
    strict: bool = False,
    required: bool = False,
) -> str:
    template = Template(template_source)
    provided_data = dict(data_source or {})

    unknown_variables = {
        path
        for path in _data_variable_paths(provided_data)
        if not any(
            _paths_are_related(path, variable) for variable in template.variables
        )
    }
    if strict and unknown_variables:
        raise UnknownDataVariablesError(
            "the data file contains unknown variables: "
            f"{', '.join(sorted(unknown_variables))}"
        )

    missing_variables = {
        variable
        for variable in template.variables
        if not _has_variable(provided_data, variable)
    }
    if required and missing_variables:
        raise MissingVariablesError(
            "the following variables are required: "
            f"{', '.join(sorted(missing_variables))}"
        )

    return template.render(provided_data)
