from jiren import Template


class TestTemplate:
    def test_variables(self):
        source = "hello, {{ name }}"
        template = Template(source)
        assert template.variables() == {"name"}

    def test_render(self):
        source = "hello, {{ name }}"
        template = Template(source)
        assert template.render(name="world") == "hello, world"
