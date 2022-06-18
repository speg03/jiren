import io

import pytest

from jiren import versions
from jiren.cli import main


@pytest.mark.parametrize(
    "template,variables,expected",
    [
        ("{{ greeting }}", "--greeting=hello", "hello\n"),
        ("{{ greeting }}", "", "\n"),
        ("{{ greeting | default('hi') }}", "", "hi\n"),
        ("{{ __greeting__message__ }}", "--greeting--message=hello", "hello\n"),
        ("hello", "", "hello\n"),
        ("", "", "\n"),
    ],
)
def test_main(monkeypatch, template, variables, expected):
    command = f"jiren --input=- -- {variables}"
    stdin = io.StringIO(template)
    stdout = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stdout", stdout)
        main()

    assert stdout.getvalue() == expected


def test_main_help(monkeypatch):
    command = "jiren --help"
    stdout = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdout", stdout)

        with pytest.raises(SystemExit):
            main()

    assert stdout.getvalue().startswith("usage:")


def test_main_help_with_variables(monkeypatch):
    command = "jiren --input=- --help"
    stdin = io.StringIO("{{ greeting }}")
    stdout = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stdout", stdout)

        with pytest.raises(SystemExit):
            main()

    assert stdout.getvalue().startswith("usage:")
    assert "--greeting GREETING" in stdout.getvalue()


def test_main_version(monkeypatch):
    command = "jiren --version"
    stdout = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdout", stdout)

        with pytest.raises(SystemExit):
            main()

    assert f"jiren, version {versions.jiren_version}" in stdout.getvalue()


@pytest.mark.parametrize(
    "template,variables,expected",
    [("{{ greeting }}", "--greeting=hello", "hello\n")],
)
def test_main_with_file(monkeypatch, tmp_path, template, variables, expected):
    template_file = tmp_path / "template.j2"
    template_file.write_text(template)

    command = f"jiren --input={template_file} -- {variables}"
    stdout = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdout", stdout)
        main()

    assert stdout.getvalue() == expected


def test_main_with_no_inputs(monkeypatch):
    command = "jiren"
    stderr = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stderr", stderr)

        with pytest.raises(SystemExit):
            main()

    assert "the following arguments are required: --input" in stderr.getvalue()


def test_main_with_unknown_variable(monkeypatch):
    command = "jiren --input=- -- --unknown=argument"
    stdin = io.StringIO("{{ greeting }}")
    stderr = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stderr", stderr)

        with pytest.raises(SystemExit):
            main()

    assert "unrecognized arguments: --unknown=argument" in stderr.getvalue()


def test_main_with_required_option(monkeypatch):
    command = "jiren --input=- --required"
    stdin = io.StringIO("{{ greeting }}")
    stderr = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stderr", stderr)

        with pytest.raises(SystemExit):
            main()

    assert "the following arguments are required: --greeting" in stderr.getvalue()
