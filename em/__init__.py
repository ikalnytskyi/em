#!/usr/bin/env python
# coding: utf-8
"""
    em
    ~~

    Em is a terminal tool that prints FILE(s), or standard input to standard
    output and highlights the expressions that are matched the PATTERN.

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


__version__ = '0.3'


#: True if Python 2.x interpreter was detected
PY2 = sys.version_info[0] == 2


def get_ansi_color(color):
    """
    Returns an ANSI-escape code for a given color.
    """
    colors = {
        # attributes
        'reset':        '\033[0m',
        'bold':         '\033[1m',
        'underline':    '\033[4m',

        # foregrounds
        'grey':         '\033[30m',
        'red':          '\033[31m',
        'green':        '\033[32m',
        'yellow':       '\033[33m',
        'blue':         '\033[34m',
        'magenta':      '\033[35m',
        'cyan':         '\033[36m',
        'white':        '\033[37m',

        # backgrounds
        'ongrey':       '\033[40m',
        'onred':        '\033[41m',
        'ongreen':      '\033[42m',
        'onyellow':     '\033[43m',
        'onblue':       '\033[44m',
        'onmagenta':    '\033[45m',
        'oncyan':       '\033[46m',
        'onwhite':      '\033[47m',
    }
    return colors.get(color.lower())


def error(statuscode, cause, message):
    """
    Print a given `message` to standard error and terminate the program
    with `statuscode` value. It's a good practice to use Unix convention
    for status code: `2` for command line syntax error and `1` for all
    other kind of errors.
    """
    print('{0}: {1}: {2}'.format(__name__, cause, message), file=sys.stderr)
    sys.exit(statuscode)


def iterate_over_stream(stream):
    """
    Iterate over lines from a given `stream`. Unlike stream's iterative
    interface this function doesn't block code execution in Python 2.x.
    """
    BUF_SIZE = 32768

    for buf in iter(lambda: os.read(stream.fileno(), BUF_SIZE), b''):
        for line in buf.decode(sys.getfilesystemencoding()).splitlines():
            yield line


def emphasize_line(line, pattern, color):
    """
    Highlight a given `line` with a given `color` if the `pattern` has
    been found in the line.
    """
    if pattern.search(line):
        color = get_ansi_color(color)
        reset = get_ansi_color('reset')
        return '{0}{1}{2}'.format(color, line, reset)
    return line


def emphasize_pattern(line, pattern, color):
    """
    Search for `pattern` in the `line` and highlight it if it has been
    found.
    """
    color = get_ansi_color(color)
    reset = get_ansi_color('reset')
    return pattern.sub(r'{0}\1{1}'.format(color, reset), line)


def emphasize(stream, patterns):
    """
    Emphasize a given `patterns` in a given `stream` and print the result
    to `stdout`. The `patterns` argument must be represent as a dictionry
    where the key is a pattern, and the value is a format lexem
    (e.g. RED, BLUE, UNDERLINE).
    """
    # compile patterns for quick execution
    def re_compile(k, v):
        flags = re.UNICODE
        flags |= re.IGNORECASE if v['ignore_case'] else 0
        return re.compile('(%s)' % k, flags)
    patterns = {re_compile(k, v): v for k, v in patterns.items()}

    # don't use `stream.read()` (or its iterative interface) here as it can
    # possibly block until the block of the requested size is read fully
    # (actual for python 2.x)
    for line in iterate_over_stream(stream):
        for pattern, settings in patterns.items():
            color = settings['format']
            if settings['line_mode']:
                line = emphasize_line(line, pattern, color)
            else:
                line = emphasize_pattern(line, pattern, color)
        print(line.encode(sys.getfilesystemencoding()) if PY2 else line)


def get_arguments():
    """
    Create and parse command line interface.
    """
    def _str_to_unicode(string):
        return string.decode(sys.getfilesystemencoding()) if PY2 else string

    parser = argparse.ArgumentParser(
        description=_(
            'Em is a terminal tool that prints FILE(s), or standard '
            'input to standard output and highlights the expressions that '
            'are matched the PATTERN.'),
        epilog=_(
            'With no FILE, or when FILE is -, read standard input.'
            '  '
            'The FORMAT option must be one of: BOLD, UNDERLINE, [ON]GREY, '
            '[ON]RED, [ON]GREEN, [ON]YELLOW, [ON]BLUE, [ON]MAGENTA, [ON]CYAN '
            'or [ON]WHITE.'),

        # disable it and add help option manually
        # we need this trick to localize help message
        add_help=False
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

    arg = parser.add_argument('-v', '--version', action='version')
    arg.version = '%(prog)s ' + __version__
    arg.help = _("show program's version number and exit")

    arg = parser.add_argument('-h', '--help', action='help')
    arg.help = _('show this help message and exit')

    # TODO: add option to load pattern/format settings from the file

    return parser.parse_args()


def validate_arguments(arguments):
    """
    Validate arguments from the command line.
    """
    if not get_ansi_color(arguments.format):
        error(2, arguments.format, _('Unknown format value'))


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
            emphasize(stream, patterns)

            # don't close stdin
            if filename != '-':
                stream.close()

        # since Python 3.3 `IOEror` has been merge into `OSError`, but
        # still available as alias to the last one
        except IOError as e:
            error(1, e.filename, e.strerror)


if __name__ == '__main__':
    main()
