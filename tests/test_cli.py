import io
import os
from tempfile import TemporaryDirectory

import pytest

from jiren.cli import Application, main


class TestApplication:
    @pytest.mark.parametrize(
        "inputs,argv,expected",
        [
            ("{{ greeting }}", ["--", "--greeting=hello"], "hello\n"),
            ("{{ greeting }}", ["--strict", "--", "--greeting=hello"], "hello\n"),
            ("{{ greeting }}", [], "\n"),
            ("{{ greeting | default('hi') }}", [], "hi\n"),
            ("hello", [], "hello\n"),
            ("", [], "\n"),
        ],
    )
    def test_run(self, monkeypatch, inputs, argv, expected):
        argv = ["jiren"] + argv
        stdin = io.StringIO(inputs)
        stdout = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", argv)
            m.setattr("sys.stdin", stdin)
            m.setattr("sys.stdout", stdout)
            Application().run()

        assert stdout.getvalue() == expected

    @pytest.mark.parametrize(
        "inputs,argv,expected",
        [("{{ greeting }}", ["--", "--greeting=hello"], "hello\n")],
    )
    def test_run_with_file(self, monkeypatch, inputs, argv, expected):
        template_dir = TemporaryDirectory(prefix="jiren-")
        template_file = os.path.join(template_dir.name, "template.j2")
        with open(template_file, "w") as f:
            f.write(inputs)

        argv = ["jiren", "--input=" + template_file] + argv
        stdout = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", argv)
            m.setattr("sys.stdout", stdout)
            Application().run()

        assert stdout.getvalue() == expected

    def test_run_strictly(self, monkeypatch):
        argv = ["jiren", "--strict"]
        stdin = io.StringIO("{{ greeting }}")
        stderr = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", argv)
            m.setattr("sys.stdin", stdin)
            m.setattr("sys.stderr", stderr)

            with pytest.raises(SystemExit):
                Application().run()

        expected = "jiren: error: the following arguments are required: --greeting"
        assert expected in stderr.getvalue()


class TestCLI:
    def test_main(self, monkeypatch):
        argv = ["jiren", "--", "--greeting=hello"]
        stdin = io.StringIO("{{ greeting }}")
        stdout = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", argv)
            m.setattr("sys.stdin", stdin)
            m.setattr("sys.stdout", stdout)
            main()

        assert stdout.getvalue() == "hello\n"
