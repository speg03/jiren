import io

import pytest

from jiren import __version__
from jiren.cli import main


def test_main_renders_template_from_stdin(monkeypatch):
    stdout = io.StringIO()

    monkeypatch.setattr("sys.argv", ["jiren", "-", "--", "--greeting=hello"])
    monkeypatch.setattr("sys.stdin", io.StringIO("{{ greeting }}"))
    monkeypatch.setattr("sys.stdout", stdout)

    main()

    assert stdout.getvalue() == "hello\n"


def test_main_renders_omitted_template_from_stdin(monkeypatch):
    stdout = io.StringIO()

    monkeypatch.setattr("sys.argv", ["jiren", "--", "--greeting=hello"])
    monkeypatch.setattr("sys.stdin", io.StringIO("{{ greeting }}"))
    monkeypatch.setattr("sys.stdout", stdout)

    main()

    assert stdout.getvalue() == "hello\n"


def test_main_reads_template_and_data_files(monkeypatch, tmp_path):
    template_file = tmp_path / "template.jinja"
    template_file.write_text("{{ greeting.message }}, {{ greeting.target }}")
    data_file = tmp_path / "data.yaml"
    data_file.write_text("greeting:\n  message: hello\n  target: world")
    stdout = io.StringIO()

    monkeypatch.setattr(
        "sys.argv", ["jiren", f"--data={data_file}", str(template_file)]
    )
    monkeypatch.setattr("sys.stdout", stdout)

    main()

    assert stdout.getvalue() == "hello, world\n"


def test_main_reads_structured_data_from_command_line(monkeypatch):
    stdout = io.StringIO()

    monkeypatch.setattr(
        "sys.argv",
        ["jiren", '--data-string={"count": 42, "enabled": true}'],
    )
    monkeypatch.setattr(
        "sys.stdin",
        io.StringIO("{{ count + 1 }}, {{ enabled | lower }}"),
    )
    monkeypatch.setattr("sys.stdout", stdout)

    main()

    assert stdout.getvalue() == "43, true\n"


def test_main_rejects_data_and_data_string_together(monkeypatch, tmp_path):
    data_file = tmp_path / "data.yaml"
    stderr = io.StringIO()

    monkeypatch.setattr(
        "sys.argv",
        ["jiren", f"--data={data_file}", "--data-string=greeting: hello"],
    )
    monkeypatch.setattr("sys.stderr", stderr)

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2
    assert "--data-string: not allowed with argument -d/--data" in stderr.getvalue()


def test_main_reports_unreadable_template_file(monkeypatch, tmp_path):
    template_file = tmp_path / "missing.jinja"
    stderr = io.StringIO()

    monkeypatch.setattr("sys.argv", ["jiren", str(template_file)])
    monkeypatch.setattr("sys.stderr", stderr)

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2
    assert f"cannot read template file: {template_file}" in stderr.getvalue()


def test_main_reports_unreadable_data_file(monkeypatch, tmp_path):
    data_file = tmp_path / "missing.yaml"
    stderr = io.StringIO()

    monkeypatch.setattr("sys.argv", ["jiren", f"--data={data_file}"])
    monkeypatch.setattr("sys.stdin", io.StringIO("{{ greeting }}"))
    monkeypatch.setattr("sys.stderr", stderr)

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2
    assert f"cannot read data file: {data_file}" in stderr.getvalue()


def test_main_help_with_stdin_template_includes_variable_options(monkeypatch):
    stdout = io.StringIO()

    monkeypatch.setattr("sys.argv", ["jiren", "--help", "-"])
    monkeypatch.setattr("sys.stdin", io.StringIO("{{ greeting }}"))
    monkeypatch.setattr("sys.stdout", stdout)

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 0
    assert stdout.getvalue().startswith("usage:")
    assert "--greeting GREETING" in stdout.getvalue()


def test_main_help_without_template_does_not_read_stdin(monkeypatch):
    stdin = io.StringIO("{{ greeting }}")
    stdout = io.StringIO()

    monkeypatch.setattr("sys.argv", ["jiren", "--help"])
    monkeypatch.setattr("sys.stdin", stdin)
    monkeypatch.setattr("sys.stdout", stdout)

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 0
    assert stdout.getvalue().startswith("usage:")
    assert stdin.read() == "{{ greeting }}"


def test_main_prints_version(monkeypatch):
    stdout = io.StringIO()

    monkeypatch.setattr("sys.argv", ["jiren", "--version"])
    monkeypatch.setattr("sys.stdout", stdout)

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 0
    assert stdout.getvalue() == f"{__version__}\n"


def test_main_converts_core_errors_to_argument_errors(monkeypatch, tmp_path):
    data_file = tmp_path / "data.yaml"
    data_file.write_text("unused: value")
    stderr = io.StringIO()

    monkeypatch.setattr("sys.argv", ["jiren", f"--data={data_file}", "--strict"])
    monkeypatch.setattr("sys.stdin", io.StringIO("{{ greeting }}"))
    monkeypatch.setattr("sys.stderr", stderr)

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2
    assert "the data file contains unknown variables: unused" in stderr.getvalue()


def test_main_includes_data_path_for_invalid_data(monkeypatch, tmp_path):
    data_file = tmp_path / "data.yaml"
    data_file.write_text("not a mapping")
    stderr = io.StringIO()

    monkeypatch.setattr("sys.argv", ["jiren", f"--data={data_file}"])
    monkeypatch.setattr("sys.stdin", io.StringIO("{{ greeting }}"))
    monkeypatch.setattr("sys.stderr", stderr)

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2
    assert f"the data file must have at least one key: {data_file}" in stderr.getvalue()


def test_main_labels_data_string_for_invalid_data(monkeypatch):
    stderr = io.StringIO()

    monkeypatch.setattr("sys.argv", ["jiren", "--data-string=not a mapping"])
    monkeypatch.setattr("sys.stdin", io.StringIO("{{ greeting }}"))
    monkeypatch.setattr("sys.stderr", stderr)

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 2
    assert (
        "the data file must have at least one key: --data-string" in stderr.getvalue()
    )
