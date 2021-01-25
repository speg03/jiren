import pytest
from jiren import Template
from jiren.template import TemplateParser


class TestTemplate:
    def test_init(self):
        source = "hello, {{ name }}"
        template = Template(source)
        assert template.source == source
        assert template.variables == {"name"}

    def test_render(self):
        source = "hello, {{ name }}"
        template = Template(source)
        assert template.render(name="world") == "hello, world"


class TestTemplateParser:
    def test_init(self):
        source = "hello, {{ name }}"
        parser = TemplateParser(source, required=True)
        assert parser.template.source == source
        assert parser.template.variables == {"name"}
        assert parser.required is True

    @pytest.mark.parametrize(
        "source,variable_args,expected",
        [
            ("{{ greeting }}", ["--greeting", "hello"], "hello"),
            ("{{ greeting }}", ["--greeting=hello"], "hello"),
            ("{{ greeting }}", [], ""),
            ("{{ greeting }}", None, ""),
            ("{{ greeting | default('hi') }}", None, "hi"),
            ("hello", None, "hello"),
            ("", None, ""),
        ],
    )
    def test_apply(self, source, variable_args, expected):
        parser = TemplateParser(source)
        assert parser.apply(variable_args) == expected

    def test_apply_with_unknown(self):
        source = "hello, {{ name }}"
        parser = TemplateParser(source)

        with pytest.raises(ValueError):
            parser.apply(["--unknown", "argument"])

    def test_apply_with_required(self):
        source = "hello, {{ name }}"
        parser = TemplateParser(source, required=True)

        with pytest.raises(ValueError):
            parser.apply([])
