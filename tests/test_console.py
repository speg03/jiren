import io

import pytest

from jiren.cli import main


class TestCLI:
    @pytest.mark.parametrize(
        "inputs,argv,expected",
        [
            (
                "{{ greeting }}, {{ message }}",
                ["--greeting=hello", "--message=world"],
                "hello, world\n",
            ),
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
