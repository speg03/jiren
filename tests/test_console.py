from jiren.console import Console


class TestConsole:
    def test_run(self):
        stdin = "{{ greeting }}, {{ message }}"
        arguments = "--greeting=hello --message=world"
        console = Console(stdin, arguments)

        expected = "hello, world"
        actual = console.run()

        assert expected == actual
