import io

from jiren.console import main


class TestConsole:
    def test_main(self, monkeypatch):
        argv = ["jiren", "--greeting=hello", "--message=world"]
        stdin = io.StringIO("{{ greeting }}, {{ message }}")
        stdout = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", argv)
            m.setattr("sys.stdin", stdin)
            m.setattr("sys.stdout", stdout)
            main()

        expected = "hello, world\n"
        actual = stdout.getvalue()

        assert expected == actual
