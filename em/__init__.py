#!/usr/bin/env python
# coding: utf-8
"""
    em
    ~~

    em program is a terminal tool that prints FILE(s), or standard input
    to standard output and highlights the expressions that are matched
    the PATTERN.

    The expression will be highlighted iff the terminal is ANSI-compatible.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""
from __future__ import print_function, unicode_literals

import re
import os
import sys
import gettext
import argparse


__version__ = '0.1'


#: FileNotFoundError has been introduced in Python 3.3, and replaced
#: more abstract IOError.
if not hasattr(__builtins__, 'FileNotFoundError'):
    FileNotFoundError = IOError


def get_ansi_color(color):
    """
    Returns an ANSI-escape code for a given color.
    """
    colors = {
        # attributes
        'reset':        '\033[0m',
        'bold':         '\033[1m',
        'underline':    '\033[4m',

        # colors
        'grey':         '\033[30m',
        'red':          '\033[31m',
        'green':        '\033[32m',
        'yellow':       '\033[33m',
        'blue':         '\033[34m',
        'magenta':      '\033[35m',
        'cyan':         '\033[36m',
        'white':        '\033[37m',
    }
    return colors.get(color.lower())


def show_error_and_exit(status_code, message):
    """
    Print a given error message to standard error and terminate the program.
    """
    print(message, file=sys.stderr)
    sys.exit(status_code)


def emphasize(stream, patterns):
    """
    Emphasize a given ``patterns`` in a given ``stream`` and print the
    result to ``stdout``. The ``patterns`` argument must be represent as
    a dictionay where the key is a pattern, and the value is a format
    lexem (e.g. RED, BLUE, UNDERLINE).
    """
    # compile patterns for quick execution
    def re_compile(k, v):
        return re.compile('(%s)' % k, re.I if v['ignore_case'] else 0)
    patterns = {re_compile(k, v): v for k, v in patterns.items()}

    # colorize matched patterns with ANSI-escapes
    for line in stream:
        for pattern, style in patterns.items():
            line = pattern.sub(r'{style}\1{reset}'.format(
                style=get_ansi_color(style['format']),
                reset=get_ansi_color('reset')
            ), line)
        sys.stdout.write(line)


def get_arguments():
    """
    Create and parse command line interface.
    """
    parser = argparse.ArgumentParser(
        description=_(
            '%(prog)s program is a terminal tool that prints FILE(s), '
            'or standard input to standard output and highlights the '
            'expressions that are matched the PATTERN.'),
        epilog=_(
            'With no FILE, or when FILE is -, read standard input.'
            '  '
            'The FORMAT option must be one of: BOLD, UNDERLINE, GREY, RED, '
            'GREEN, YELLOW, BLUE, MAGENTA, CYAN or WHITE.')
    )

    arg = parser.add_argument('pattern', metavar='PATTERN')
    arg.help = _('a pattern to highlight')

    arg = parser.add_argument('format', metavar='FORMAT')
    arg.help = _('a color to highlight matched expressions')

    arg = parser.add_argument('files', metavar='FILE', nargs='*', default=['-'])
    arg.help = _('search for pattern in these file(s)')

    arg = parser.add_argument('-i', '--ignore-case', action='store_true')
    arg.help = _('ignore case distinctions')

    arg = parser.add_argument('-s', '--safe-output', action='store_true')
    arg.help = _('print ansi sequences only on tty')

    parser.add_argument(
        '--version', action='version', version='%(prog)s ' + __version__)

    # TODO: add option to load pattern/format settings from the file

    return parser.parse_args()


def validate_arguments(arguments):
    """
    Validate arguments from the command line.
    """
    if not get_ansi_color(arguments.format):
        show_error_and_exit(2, '{0}: {1}: {2}'.format(
            __name__, arguments.format,
            _('Unknown format value')
        ))


def main():
    PY2 = sys.version_info[0] == 2

    # initialize localization subsystem
    localedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locale')
    if PY2:
        gettext.install('em', localedir, unicode=True)
    else:
        gettext.install('em', localedir)

    # parse command line arguments and validate it.
    # terminate the program if error was occured.
    arguments = get_arguments()
    validate_arguments(arguments)
    patterns = {
        arguments.pattern: {
            'format': arguments.format,
            'ignore_case': arguments.ignore_case,
        }
    }

    # iterate over the files and highlight the given patterns
    for filename in arguments.files:
        try:
            stream = sys.stdin if filename == '-' else open(filename, 'r')

            if arguments.safe_output and not sys.stdout.isatty():
                sys.stdout.write(stream.read())
            else:
                emphasize(stream, patterns)

        except FileNotFoundError as e:
            show_error_and_exit(2, '{0}: {1}: {2}'.format(
                __name__, e.filename, e.strerror
            ))
        finally:
            if filename != '-':
                stream.close()


if __name__ == '__main__':
    main()
