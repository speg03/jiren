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

Generate text from a template using the `jiren` command. The `jiren` command can read templates from stdin.

Command:
```sh
echo "hello, {{ message }}" | jiren --message=world
```
Output:
```
hello, world
```

In this example, the template contains a variable called `message`. If you want to know more about template format, please refer to jinja2 document ( http://jinja.pocoo.org/ ).

You can use the help to check the variables defined in the template.

Command:
```sh
echo "hello, {{ message }}" | jiren --help
```
Output:
```
usage: jiren [-h] [--message MESSAGE]

optional arguments:
  -h, --help         show this help message and exit
  --message MESSAGE
```
