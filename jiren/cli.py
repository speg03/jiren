import argparse
import sys

import jiren


class Application:
    def run(self):
        template_str = sys.stdin.read()
        template = jiren.Template(template_str)

        parser = argparse.ArgumentParser()
        for v in template.variables():
            parser.add_argument("--" + v)
        args = parser.parse_args()

        print(template.render(**vars(args)))


def main():
    Application().run()
