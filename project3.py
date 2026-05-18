# project3.py
#
# ICS 33 Spring 2026
# Project 3: Why Not Smile?
#
# The main module that executes your Grin interpreter.
#
# WHAT YOU NEED TO DO: You'll need to implement the outermost shell of your
# program here, but consider how you can keep this part as simple as possible,
# offloading as much of the complexity as you can into additional modules in
# the 'grin' package, isolated in a way that allows you to unit test them.

import grin
import sys


def main() -> None:
    lines = []

    for line in sys.stdin:
        stripped_line = line.rstrip('\r\n')
        if stripped_line == '.':
            break
        lines.append(stripped_line)

    try:
        parsed_program = list(grin.parse(lines))

        print(f"Successfully parsed {len(parsed_program)} lines of Grin code.")

    except grin.GrinParseError as e:
        print(e)
    except grin.GrinLexError as e:
        print(e)


if __name__ == '__main__':
    main()
