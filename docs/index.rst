Welcome to em's documentation!
==============================

em_ program is a terminal tool that prints FILE(s), or standard input
to standard output and highlights the expressions that are matched the
PATTERN.

.. image:: /_static/em-example.png
    :align: center

The expression will be highlighted iff the terminal is ANSI-compatible.
This criterion is met by most popular terminal emulators on Linux, Unix
and MacOS.


Installation
------------

You will need Python 2.7, 3.2 or above to get started. If you already
have it, feel free to install em throuh pip util::

    $ (sudo) pip install em


Quickstart
----------

em is cool and easy to use. The most practical usecase for me::

    $ tail -f /path/to/log | em "ERROR" red | em "iphone:" green

The example above highlights all occurences of «ERROR» in red and all
occurences of «iphone:» in green when watching the log.

But you can use em in the following way::

    $ em "ERROR|CRITICAL" red /path/to/log

which prints the log and highlights all occurences of «ERROR» or
«CRITICAL» in red.


Options
-------

Here is a command line interface of em::

    usage: em [-h] [-i] [-s] [--version] PATTERN FORMAT [FILE [FILE ...]]

    The em program is a terminal tool that prints FILE(s), or standard input to
    standard output and highlights the expressions that are matched the PATTERN.

    positional arguments:
      PATTERN            a pattern to highlight
      FORMAT             a color to highlight matched expressions
      FILE               search for pattern in these file(s)

    optional arguments:
      -h, --help         show this help message and exit
      -i, --ignore-case  ignore case distinctions
      -s, --safe-output  print ansi sequences only on tty
      --version          show program's version number and exit

    With no FILE, or when FILE is -, read standard input. The FORMAT option must
    be one of: BOLD, UNDERLINE, GREY, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN or
    WHITE.

The CLI is clear, so I don't need to comment. :)

.. _em: https://github.com/ikalnitsky/em

