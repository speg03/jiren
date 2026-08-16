---
icon: lucide/rocket
---

# jiren

_jiren_ renders [Jinja templates](https://jinja.palletsprojects.com/) from files or standard input, using variables supplied on the command line or in structured data files.

## Installation

jiren requires Python 3.10 or later.

Install jiren with pip:

```console
$ pip install jiren
```

Or install it as an isolated tool with [uv](https://docs.astral.sh/uv/):

```console
$ uv tool install jiren
```

To run jiren without installing it, use `uvx`:

```console
$ uvx jiren --help
```

## Documentation

- [Concept](concept.md): Why jiren exists and how it helps you work with template variables.
- [Reference](reference.md): Usage, template input, variables, data files, and validation options.
