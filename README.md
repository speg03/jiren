# jiren

jiren is an application that generates text from a template. The format of the template is based on jinja2.

[![PyPI](https://img.shields.io/pypi/v/jiren.svg)](https://pypi.org/project/jiren/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jiren.svg)](https://pypi.org/project/jiren/)
[![Python Tests](https://github.com/speg03/jiren/workflows/Python%20Tests/badge.svg)](https://github.com/speg03/jiren/actions?query=workflow%3A%22Python+Tests%22)
[![codecov](https://codecov.io/gh/speg03/jiren/branch/master/graph/badge.svg)](https://codecov.io/gh/speg03/jiren)

Read this in Japanese: [日本語](https://github.com/speg03/jiren/blob/master/README.ja.md)

## Installation

```sh
pip install jiren
```

## Usage

### Generate text

Generate text from a template using the `jiren` command. This command can read a template from stdin or files.

An example of reading a template from stdin:

Command:
```sh
echo "hello, {{ name }}" | jiren -- --name=world
```
Outputs:
```
hello, world
```

An example of reading a template from a file:

Command:
```sh
cat <<EOF >template.j2
hello, {{ name }}
EOF

jiren -i template.j2 -- --name=world
```
Outputs:
```
hello, world
```

In this example, the template contains a variable called `name`. You can set values for variables in a template using program arguments passed to the `jiren` command. Note that the arguments for the variables must be located after `--`.

If you want to know more about template format, please refer to jinja2 document ( http://jinja.pocoo.org/ ).


### Variables in a template

You can use the help to check the variables defined in a template.

Command:
```sh
echo "{{ greeting }}, {{ name }}" | jiren -- --help
```
Outputs:
```
... (omitted)

variables:
  --name NAME
  --greeting GREETING
```


### Default values

You can set default values for variables for which no values was specified. This is based on the jinja2 specification.

Command:
```sh
echo "{{ greeting }}, {{ name | default('world') }}" | jiren -- --greeting=hello
```
Outputs:
```
hello, world
```


### Option: required

When using the `--required` option, you must specify values for all variables.

Command:
```sh
echo "{{ greeting }}, {{ name }}" | jiren --required -- --greeting=hello
```
Outputs:
```
... (omitted)

jiren: error: the following arguments are required: --name
```
