# jiren

jiren is an application that generates text from a template. The format of the template is based on jinja2.

[![PyPI](https://img.shields.io/pypi/v/jiren.svg)](https://pypi.org/project/jiren/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jiren.svg)](https://pypi.org/project/jiren/)
[![Build Status](https://travis-ci.com/speg03/jiren.svg?branch=master)](https://travis-ci.com/speg03/jiren)
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
echo "hello, {{ name }}" | jiren --var.name=world
```
Output:
```
hello, world
```

An example of reading a template from a file:

Command:
```sh
cat <<EOF >template.j2
hello, {{ name }}
EOF

jiren template.j2 --var.name=world
```
Output:
```
hello, world
```

In this example, the template contains a variable called `name`. You can set values for variables in a template using program arguments passed to the` jiren` command. Note that the program arguments must be prefixed with `--var.`.

If you want to know more about template format, please refer to jinja2 document ( http://jinja.pocoo.org/ ).


### Variables in a template

You can use the help to check the variables defined in a template.

Command:
```sh
echo "hello, {{ name }}" | jiren --help
```
Output:
```
usage: jiren [-h] [--var.name VAR.NAME] [template]

Generate text from a template

positional arguments:
  template             Template file path. If omitted, read a template from
                       stdin.

optional arguments:
  -h, --help           show this help message and exit

variables:
  --var.name VAR.NAME
```
