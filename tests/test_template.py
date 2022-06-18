from jiren.template import Template


class TestTemplate:
    def test_init(self):
        source = "hello, {{ name }}"
        template = Template(source)
        assert template.variables == {"name"}

    def test_render(self):
        source = "hello, {{ name }}"
        template = Template(source)
        assert template.render(name="world") == "hello, world"
        assert template.render({"name": "world"}) == "hello, world"
