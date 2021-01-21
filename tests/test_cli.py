import io
import os
from tempfile import TemporaryDirectory

import pytest

from jiren import __version__ as jiren_version
from jiren.cli import Application, main


class TestApplication:
    @pytest.mark.parametrize(
        "template,command,expected",
        [
            ("{{ greeting }}", "jiren -- --greeting=hello", "hello\n"),
            ("{{ greeting }}", "jiren --input=- -- --greeting=hello", "hello\n"),
            ("{{ greeting }}", "jiren --required -- --greeting=hello", "hello\n"),
            ("{{ greeting }}", "jiren", "\n"),
            ("{{ greeting | default('hi') }}", "jiren", "hi\n"),
            ("hello", "jiren", "hello\n"),
            ("", "jiren", "\n"),
        ],
    )
    def test_run(self, monkeypatch, template, command, expected):
        stdin = io.StringIO(template)
        stdout = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", command.split())
            m.setattr("sys.stdin", stdin)
            m.setattr("sys.stdout", stdout)
            Application().run()

        assert stdout.getvalue() == expected

    def test_run_version(self, monkeypatch):
        command = "jiren --version"
        stdin = io.StringIO()
        stdout = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", command.split())
            m.setattr("sys.stdin", stdin)
            m.setattr("sys.stdout", stdout)

            with pytest.raises(SystemExit):
                Application().run()

        expected = "jiren version {}\n".format(jiren_version)
        assert stdout.getvalue() == expected

    @pytest.mark.parametrize(
        "template,command,expected",
        [("{{ greeting }}", "jiren --input={} -- --greeting=hello", "hello\n")],
    )
    def test_run_with_file(self, monkeypatch, template, command, expected):
        template_dir = TemporaryDirectory(prefix="jiren-")
        template_file = os.path.join(template_dir.name, "template.j2")
        with open(template_file, "w") as f:
            f.write(template)

        stdout = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", command.format(template_file).split())
            m.setattr("sys.stdout", stdout)
            Application().run()

        assert stdout.getvalue() == expected

    def test_run_with_required(self, monkeypatch):
        command = "jiren --required"
        stdin = io.StringIO("{{ greeting }}")
        stderr = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", command.split())
            m.setattr("sys.stdin", stdin)
            m.setattr("sys.stderr", stderr)

            with pytest.raises(SystemExit):
                Application().run()

        expected = "jiren: error: the following arguments are required: --greeting"
        assert expected in stderr.getvalue()


class TestCLI:
    def test_main(self, monkeypatch):
        command = "jiren -- --greeting=hello"
        stdin = io.StringIO("{{ greeting }}")
        stdout = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", command.split())
            m.setattr("sys.stdin", stdin)
            m.setattr("sys.stdout", stdout)
            main()

        assert stdout.getvalue() == "hello\n"
