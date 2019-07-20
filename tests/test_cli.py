import io
import os
import tempfile

import pytest

from jiren.cli import main


class TestCLI:
    @pytest.mark.parametrize(
        "inputs,argv,expected",
        [
            ("{{ greeting }}", ["--var.greeting=hello"], "hello\n"),
            ("{{ greeting }}", [], "\n"),
            ("{{ greeting | default('hi') }}", [], "hi\n"),
        ],
    )
    def test_main(self, monkeypatch, inputs, argv, expected):
        argv = ["jiren"] + argv
        stdin = io.StringIO(inputs)
        stdout = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", argv)
            m.setattr("sys.stdin", stdin)
            m.setattr("sys.stdout", stdout)
            main()

        actual = stdout.getvalue()
        assert expected == actual

    @pytest.mark.parametrize(
        "inputs,argv,expected",
        [("{{ greeting }}", ["--var.greeting=hello"], "hello\n")],
    )
    def test_main_with_infile(self, monkeypatch, inputs, argv, expected):
        template_dir = tempfile.TemporaryDirectory(prefix="jiren-")
        template_file = os.path.join(template_dir.name, "template.j2")
        with open(template_file, "w") as f:
            f.write(inputs)

        argv = ["jiren", template_file] + argv
        stdout = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", argv)
            m.setattr("sys.stdout", stdout)
            main()

        actual = stdout.getvalue()
        assert expected == actual
