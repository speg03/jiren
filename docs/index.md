---
icon: lucide/rocket
---

# Get started

## Installation

```console
$ pip install jiren
```

## Usage

### Generate text

Generate text from a template using the `jiren` command. This command can read a template from stdin or files.

An example of reading a template from stdin:

```console
$ echo "hello, {{ name }}" | jiren -- --name=world
hello, world
```

An example of reading a template from a file:

```console
$ echo "hello, {{ name }}" >template.j2
$ jiren template.j2 -- --name=world
hello, world
```

In this example, the template contains a variable called `name`. You can set values for variables in a template using program arguments passed to the `jiren` command. Note that the arguments for the variables must be located after `--`.

If you want to know more about template format, please refer to jinja2 document ( http://jinja.pocoo.org/ ).

### Variables in a template

You can use the help to check the variables defined in a template.

```console
$ echo "{{ message }}, {{ name }}" | jiren --help -
... (omitted)

variables:
  --name NAME
  --message MESSAGE
```

Use `jiren --help` without a template argument to display the general usage
without reading stdin. Use `-` explicitly when the help should include
variables from a template provided through stdin.

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
