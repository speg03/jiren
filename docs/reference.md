---
icon: lucide/terminal
---

# Reference

## Usage

```console
$ jiren [OPTIONS] [TEMPLATE] [-- VARIABLE_OPTIONS]
```

`TEMPLATE` is a template file path. Omit it, or pass `-`, to read the template from standard input. Pass values for template variables after `--`.

Values passed after `--` are strings. Use `--data` or `--data-string` when values need JSON or YAML types, such as numbers, booleans, lists, or nested objects.

## Render a template

Read a template from standard input:

```console
$ echo "hello, {{ name }}" | jiren -- --name=world
hello, world
```

Read a template from a file:

```console
$ echo "hello, {{ name }}" > template.jinja
$ jiren template.jinja -- --name=world
hello, world
```

jiren uses MiniJinja instead of Jinja2, so some Jinja2 template syntax is not supported. See the [MiniJinja compatibility documentation](https://github.com/mitsuhiko/minijinja/blob/main/COMPATIBILITY.md) for supported syntax and differences.

## Nested command-line variables

Use dot-separated variable paths after `--` to provide nested values:

```console
$ echo "{{ greeting.message }}" | jiren -- --greeting.message=hello
hello
```

The default `--max-depth=1` supports one nested level. For a deeper path, pass the remaining nested value as a JSON string to the deepest available option:

```console
$ echo "{{ user.profile.name }}" | jiren -- --user.profile='{"name":"you"}'
you
```

Alternatively, set `--max-depth` to pass each level as a separate option:

```console
$ echo "{{ user.profile.name }}" | jiren --max-depth=2 -- --user.profile.name=you
you
```

## Inspect template variables

Pass `--help` with a template to list the variables it uses:

```console
$ echo "{{ message }}, {{ name }}" | jiren --help -
...

variables:
  --name NAME
  --message MESSAGE
```

Use `jiren --help` without a template argument to show general usage without reading standard input. Use `-` explicitly when help should include variables from a template provided on standard input.

## Default values

Jinja default filters can provide values when a variable is not supplied:

```console
$ echo "{{ message }}, {{ name | default('world') }}" | jiren -- --message=hello
hello, world
```

## Options

### `--data PATH`, `-d PATH`

Load template variables from a JSON or YAML data file.

```console
$ cat <<EOF > data.yaml
greeting:
  message: hello
  name: world
EOF

$ echo "{{ greeting.message }}, {{ greeting.name }}" | jiren --data=data.yaml
hello, world
```

Values passed after `--` override values with the same top-level name from the data file.

### `--data-string DATA`

Load template variables from JSON or YAML supplied directly on the command line. This is useful for values that must retain their types without creating a data file.

```console
$ echo "{{ count + 1 }}, {{ enabled | lower }}" | jiren --data-string='{"count": 42, "enabled": true}'
43, true
```

`--data-string` cannot be combined with `--data`.

### `--max-depth DEPTH`

Set the maximum nesting depth for command-line variable paths. The default is `1`; values beyond that depth are passed as JSON strings.

### `--strict`

With `--data`, report top-level data-file keys that are not used by the template.

```console
$ cat <<EOF > data.yaml
message: hello
invalid_key: invalid
EOF

$ echo "{{ message }}" | jiren --data=data.yaml --strict
jiren: error: the data file contains unknown variables: invalid_key
```

### `--required`

Require a value for every variable used by the template.

```console
$ echo "{{ message }}, {{ name }}" | jiren --required -- --message=hello
jiren: error: the following variables are required: name
```

`--required` checks whether every template variable was provided, even when the template uses a Jinja `default` filter for that variable.

### `--debug`

Enable debug log output.

### `--version`, `-V`

Print the installed jiren version and exit.
