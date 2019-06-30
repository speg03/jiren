import argparse
import sys

import jiren


class Console:
    def __init__(self, stdin=None, arguments=None):
        self.stdin = stdin or "".join(sys.stdin.readlines())
        self.arguments = arguments.split() if arguments else None

    def run(self):
        template_str = self.stdin
        template = jiren.Template(template_str)

        parser = argparse.ArgumentParser()
        for v in template.variables():
            parser.add_argument("--" + v)
        args = parser.parse_args(self.arguments)

        return template.render(**vars(args))


def main():  # pragma: no cover
    console = Console()
    print(console.run())
