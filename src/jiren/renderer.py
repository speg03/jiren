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


def render_template(
    template_source: str,
    *,
    data_source: Mapping[str, Any] | None = None,
    strict: bool = False,
    required: bool = False,
) -> str:
    template = Template(template_source)
    provided_data = dict(data_source or {})

    unknown_variables = set(provided_data) - template.variables
    if strict and unknown_variables:
        raise UnknownDataVariablesError(
            "the data file contains unknown variables: "
            f"{', '.join(sorted(unknown_variables))}"
        )

    missing_variables = template.variables - set(provided_data)
    if required and missing_variables:
        raise MissingVariablesError(
            "the following variables are required: "
            f"{', '.join(sorted(missing_variables))}"
        )

    return template.render(provided_data)
