---
icon: lucide/lightbulb
---

# Concept

Jinja is a widely used template engine in the Python ecosystem. jiren was created to make Jinja templates convenient to use directly from the command line, without writing a Python script for a small rendering task.

## Template-aware command line

jiren detects the variables used by a template and presents them in its help output. This lets you inspect the inputs a template expects before rendering it. The same variable names become command-line options after `--`, keeping the invocation close to the template itself.

## Make input mistakes visible

Templates are often rendered from data files maintained by scripts or configuration. jiren includes validation options to make mistakes easier to find:

- `--required` reports variables that the template needs but that were not supplied.
- `--strict` reports entries in a data file that the template does not use.

These checks help prevent silent output changes caused by missing values or misspelled and obsolete data keys. See the [reference](reference.md) for details and examples.
