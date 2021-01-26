import io
import os
from tempfile import TemporaryDirectory

import pytest
from jiren import __version__ as jiren_version
from jiren.cli import main


class TestCLI:
    @pytest.mark.parametrize(
        "template,command,expected",
        [
            ("{{ greeting }}", "jiren -- --greeting hello", "hello\n"),
            ("{{ greeting }}", "jiren -- --greeting=hello", "hello\n"),
            ("{{ greeting }}", "jiren --input=- -- --greeting=hello", "hello\n"),
        ],
    )
    def test_main(self, monkeypatch, template, command, expected):
        stdin = io.StringIO(template)
        stdout = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", command.split())
            m.setattr("sys.stdin", stdin)
            m.setattr("sys.stdout", stdout)
            main()

        assert stdout.getvalue() == expected

    def test_main_version(self, monkeypatch):
        command = "jiren --version"
        stdin = io.StringIO()
        stdout = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", command.split())
            m.setattr("sys.stdin", stdin)
            m.setattr("sys.stdout", stdout)

            with pytest.raises(SystemExit):
                main()

        expected = "jiren version {}\n".format(jiren_version)
        assert stdout.getvalue() == expected

    @pytest.mark.parametrize(
        "template,command,expected",
        [("{{ greeting }}", "jiren --input={} -- --greeting=hello", "hello\n")],
    )
    def test_main_with_file(self, monkeypatch, template, command, expected):
        template_dir = TemporaryDirectory(prefix="jiren-")
        template_file = os.path.join(template_dir.name, "template.j2")
        with open(template_file, "w") as f:
            f.write(template)

        stdout = io.StringIO()

        with monkeypatch.context() as m:
            m.setattr("sys.argv", command.format(template_file).split())
            m.setattr("sys.stdout", stdout)
            main()

        assert stdout.getvalue() == expected
