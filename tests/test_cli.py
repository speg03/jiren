import io
import os
import tempfile

import pytest

from jiren.cli import Application, main


class TestApplication:
    @pytest.mark.parametrize(
        "inputs,argv,expected",
        [
            ("{{ greeting }}", ["--var.greeting=hello"], "hello\n"),
            ("{{ greeting }}", [], "\n"),
            ("{{ greeting | default('hi') }}", [], "hi\n"),
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
        [("{{ greeting }}", ["--var.greeting=hello"], "hello\n")],
    )
    def test_run_with_infile(self, monkeypatch, inputs, argv, expected):
        template_dir = tempfile.TemporaryDirectory(prefix="jiren-")
        template_file = os.path.join(template_dir.name, "template.j2")
        with open(template_file, "w") as f:
            f.write(inputs)

        argv = ["jiren", template_file] + argv
        stdout = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", argv)
            m.setattr("sys.stdout", stdout)
            Application().run()

        assert stdout.getvalue() == expected


class TestCLI:
    def test_main(self, monkeypatch):
        argv = ["jiren", "--var.greeting=hello"]
        stdin = io.StringIO("{{ greeting }}")
        stdout = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", argv)
            m.setattr("sys.stdin", stdin)
            m.setattr("sys.stdout", stdout)
            main()

        assert stdout.getvalue() == "hello\n"
