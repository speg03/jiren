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
    command = f"jiren - -- {variables}"
    stdin = io.StringIO(template)
    stdout = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stdout", stdout)
        main()

    assert stdout.getvalue() == expected


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
def test_main_with_input(monkeypatch, template, variables, expected):
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
    command = "jiren --help -"
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


def test_main_with_template_file(monkeypatch, tmp_path):
    template_file = tmp_path / "template.j2"
    template_file.write_text("{{ greeting }}")

    command = f"jiren {template_file} -- --greeting=hello"
    stdout = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdout", stdout)
        main()

    assert stdout.getvalue() == "hello\n"


def test_main_with_json_data_file(monkeypatch, tmp_path):
    data_file = tmp_path / "data.json"
    data_file.write_text("{'greeting': {'message': 'hello', 'target': 'world'} }")

    command = f"jiren --data={data_file} -"
    stdin = io.StringIO("{{ greeting.message }}, {{ greeting.target }}")
    stdout = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stdout", stdout)
        main()

    assert stdout.getvalue() == "hello, world\n"


def test_main_with_yaml_data_file(monkeypatch, tmp_path):
    data_file = tmp_path / "data.yaml"
    data_file.write_text("greeting:\n  message: hello\n  target: world")

    command = f"jiren --data={data_file} -"
    stdin = io.StringIO("{{ greeting.message }}, {{ greeting.target }}")
    stdout = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stdout", stdout)
        main()

    assert stdout.getvalue() == "hello, world\n"


def test_main_with_data_file_and_arguments(monkeypatch, tmp_path):
    data_file = tmp_path / "data.yaml"
    data_file.write_text("message: hello")

    command = f"jiren --data={data_file} - -- --message=hey --name=you"
    stdin = io.StringIO("{{ message }}, {{ name }}")
    stdout = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stdout", stdout)
        main()

    assert stdout.getvalue() == "hey, you\n"


def test_main_with_json_data_file_unknown_variables(monkeypatch, tmp_path):
    data_file = tmp_path / "data.json"
    data_file.write_text("{'a': 1, 'b': 2, 'c': 3}")

    command = f"jiren --data={data_file} -"
    stdin = io.StringIO("{{ greeting }}")
    stdout = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stdout", stdout)
        main()

    assert stdout.getvalue() == "\n"


def test_main_strictly_with_json_data_file_unknown_variables(monkeypatch, tmp_path):
    data_file = tmp_path / "data.json"
    data_file.write_text("{'a': 1, 'b': 2, 'c': 3}")

    command = f"jiren --data={data_file} --strict -"
    stdin = io.StringIO("{{ greeting }}")
    stderr = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stderr", stderr)

        with pytest.raises(SystemExit):
            main()

    assert "the data file contains unknown variables: a, b, c" in stderr.getvalue()


def test_main_with_yaml_data_file_no_keys(monkeypatch, tmp_path):
    data_file = tmp_path / "data.yaml"
    data_file.write_text("hello")

    command = f"jiren --data={data_file} -"
    stdin = io.StringIO("{{ greeting }}")
    stderr = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stderr", stderr)

        with pytest.raises(SystemExit):
            main()

    assert f"the data file must have at least one key: {data_file}" in stderr.getvalue()


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
    command = "jiren - -- --unknown=argument"
    stdin = io.StringIO("{{ greeting }}")
    stderr = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stderr", stderr)

        with pytest.raises(SystemExit):
            main()

    assert "unrecognized arguments: --unknown=argument" in stderr.getvalue()


def test_main_with_required(monkeypatch, tmp_path):
    data_file = tmp_path / "data.yaml"
    data_file.write_text("greeting: hello")

    command = f"jiren --data={data_file} --required -"
    stdin = io.StringIO("{{ greeting }}")
    stdout = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stdout", stdout)
        main()

    assert stdout.getvalue() == "hello\n"


def test_main_with_no_required_variables(monkeypatch):
    command = "jiren --required -"
    stdin = io.StringIO("{{ greeting }}")
    stderr = io.StringIO()

    with monkeypatch.context() as m:
        m.setattr("sys.argv", command.split())
        m.setattr("sys.stdin", stdin)
        m.setattr("sys.stderr", stderr)

        with pytest.raises(SystemExit):
            main()

    assert "the following variables are required: greeting" in stderr.getvalue()
