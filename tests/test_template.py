import jiren


class TestTemplate:
    def test_variables(self):
        template_str = "hello, {{ message }}"
        template = jiren.Template(template_str)

        expected = {"message"}
        actual = template.variables()

        assert expected == actual

    def test_render(self):
        template_str = "hello, {{ message }}"
        template = jiren.Template(template_str)

        expected = "hello, world"
        actual = template.render(message="world")

        assert expected == actual
