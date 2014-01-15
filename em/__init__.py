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


__version__ = '0.2.1'


#: True if Python 2.x interpreter was detected.
PY2 = sys.version_info[0] == 2

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


def iterate_over_stream(stream):
    """
    Iterate over lines from a given ``stream``. Unlike stream's iterative
    interface this function doesn't block code execution in Python 2.x.
    """
    BUF_SIZE = 32768

    for buf in iter(lambda: os.read(stream.fileno(), BUF_SIZE), b''):
        for line in buf.decode(sys.getfilesystemencoding()).splitlines():
            yield line


def emphasize(stream, patterns):
    """
    Emphasize a given ``patterns`` in a given ``stream`` and print the
    result to ``stdout``. The ``patterns`` argument must be represent as
    a dictionay where the key is a pattern, and the value is a format
    lexem (e.g. RED, BLUE, UNDERLINE).
    """
    # compile patterns for quick execution
    def re_compile(k, v):
        flags = re.UNICODE
        flags |= re.IGNORECASE if v['ignore_case'] else 0
        return re.compile('(%s)' % k, flags)
    patterns = {re_compile(k, v): v for k, v in patterns.items()}

    # don't use stream.read() (or its iterative interface) here as it can
    # possibly block until the block of the requested size is read fully
    # (actual for python 2.x)
    for line in iterate_over_stream(stream):
        # colorize matched patterns with ANSI-escapes
        for pattern, settings in patterns.items():
            if settings['line_mode'] and pattern.search(line):
                line = '{style}{line}{reset}'.format(
                    style=get_ansi_color(settings['format']),
                    line=line,
                    reset=get_ansi_color('reset')
                )
            else:
                line = pattern.sub(r'{style}\1{reset}'.format(
                    style=get_ansi_color(settings['format']),
                    reset=get_ansi_color('reset')
                ), line)
        print(line)


def get_arguments():
    """
    Create and parse command line interface.
    """
    def _str_to_unicode(string):
        return string.decode(sys.getfilesystemencoding()) if PY2 else string

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
    arg.type = _str_to_unicode

    arg = parser.add_argument('format', metavar='FORMAT')
    arg.help = _('a color to highlight matched expressions')

    arg = parser.add_argument('files', metavar='FILE', nargs='*', default=['-'])
    arg.help = _('search for pattern in these file(s)')
    arg.type = _str_to_unicode

    arg = parser.add_argument('-i', '--ignore-case', action='store_true')
    arg.help = _('ignore case distinctions')

    arg = parser.add_argument('-l', '--line-mode', action='store_true')
    arg.help = _('highlight entire line')

    arg = parser.add_argument('-s', '--safe-mode', action='store_true')
    arg.help = _('highlight only when stdout refers to tty')

    arg = parser.add_argument('--version', action='version')
    arg.version = '%(prog)s ' + __version__
    arg.help = _("show program's version number and exit")

    # TODO: add option to load pattern/format settings from the file

    # localization trick (originally stores in argparse module)
    _('show this help message and exit')
    _("show program's version number and exit")

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
    # initialize localization subsystem
    localedir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'locale')
    kwargs = {'unicode': True, } if PY2 else {}
    gettext.install('em', localedir, **kwargs)

    # parse command line arguments and validate it.
    # terminate the program if error was occured.
    arguments = get_arguments()
    validate_arguments(arguments)
    patterns = {
        arguments.pattern: {
            'format': arguments.format,
            'ignore_case': arguments.ignore_case,
            'line_mode': arguments.line_mode,
        }
    }

    # iterate over the files and highlight the given patterns
    for filename in arguments.files:
        try:
            stream = sys.stdin if filename == '-' else open(filename, 'r')

            if arguments.safe_mode and not sys.stdout.isatty():
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
