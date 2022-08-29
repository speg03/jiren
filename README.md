# jiren

jiren is an application that generates text from a template. The format of the template is based on jinja2.

[![PyPI](https://img.shields.io/pypi/v/jiren)](https://pypi.org/project/jiren/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jiren)](https://pypi.org/project/jiren/)
[![Python Tests](https://github.com/speg03/jiren/actions/workflows/python-tests.yml/badge.svg)](https://github.com/speg03/jiren/actions/workflows/python-tests.yml)
[![codecov](https://codecov.io/gh/speg03/jiren/branch/main/graph/badge.svg?token=bFdpze6ELR)](https://codecov.io/gh/speg03/jiren)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/speg03/jiren/main.svg)](https://results.pre-commit.ci/latest/github/speg03/jiren/main)

Read this in Japanese: [日本語](https://github.com/speg03/jiren/blob/main/README.ja.md)

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
echo "hello, {{ name }}" | jiren - -- --name=world
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

jiren template.j2 -- --name=world
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
echo "{{ message }}, {{ name }}" | jiren --help -
```
Outputs:
```
... (omitted)

variables:
  --name NAME
  --message MESSAGE
```


### Default values

You can set default values for variables for which no values was specified. This is based on the jinja2 specification.

Command:
```sh
echo "{{ message }}, {{ name | default('world') }}" | jiren - -- --message=hello
```
Outputs:
```
hello, world
```


### Option: data

You can pass a file with variables defined structurally using the `--data` option.

Command:
```sh
cat <<EOF >data.yaml
greeting:
  message: hello
  name: world
EOF

echo "{{ greeting.message }}, {{ greeting.name }}" | jiren --data=data.yaml -
```
Outputs:
```
hello, world
```


### Option: strict

If the `--strict` option is used with the `--data` option, all variables in the data file must be used in the template.

Command:
```sh
cat <<EOF >data.yaml
message: hello
invalid_key: invalid
EOF

echo "{{ message }}" | jiren --data=data.yaml --strict -
```
Outputs:
```
jiren: error: the data file contains unknown variables: invalid_key
```


### Option: required

When using the `--required` option, you must specify values for all variables.

Command:
```sh
echo "{{ message }}, {{ name }}" | jiren --required - -- --message=hello
```
Outputs:
```
jiren: error: the following variables are required: name
```
