from jiren import versions


def test_versions():
    assert versions.jiren_version
    assert versions.jinja2_version
