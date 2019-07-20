# jiren

jiren is an application that generates text from templates. The format of the template is based on jinja2.

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

Generate text from a template using the `jiren` command. This command can read templates from stdin or files.

An example of reading a template from stdin:

Command:
```sh
echo "hello, {{ message }}" | jiren --var.message=world
```
Output:
```
hello, world
```

An example of reading a template from a file:

Command:
```sh
cat <<EOF >template.j2
hello, {{ message }}
EOF

jiren template.j2 --var.message=world
```
Output:
```
hello, world
```

In this example, the template contains a variable called `message`. You can set the value of the `message` variable using program arguments passed to the` jiren` command. Note that the program arguments must be prefixed with `--var.`.

If you want to know more about template format, please refer to jinja2 document ( http://jinja.pocoo.org/ ).

You can use the help to check the variables defined in the template.

Command:
```sh
echo "hello, {{ message }}" | jiren --help
```
Output:
```
usage: jiren [-h] [--var.message VAR.MESSAGE] [infile]

positional arguments:
  infile

optional arguments:
  -h, --help            show this help message and exit

variables:
  --var.message VAR.MESSAGE
```
