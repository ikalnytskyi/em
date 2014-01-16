.. title:: Welcome to Em

Introduction
------------

Em is a terminal tool that prints FILE(s), or standard input to standard
output and highlights the expressions that are matched the PATTERN.

.. image:: /_static/em-example.png
    :align: center

The expression will be highlighted iff the terminal is ANSI-compatible.
This criterion is met by most popular terminal emulators on Linux, Unix
and MacOS.


Installation
------------

Em is a small script written in Python without any further dependencies
but things that are shipped with Python 2.7, Python 3.2 or above. Quick
installation::

    $ [sudo] pip install em


Quickstart
----------

Em is cool and easy to use. The most practical usecase for me::

    $ tail -f /path/to/log | em "ERROR" red | em "iphone:" green

The example above highlights all occurrences of «ERROR» in red and all
occurrences of «iphone:» in green when watching the log.

But you can use em in the following way::

    $ em "ERROR|CRITICAL" red /path/to/log

which prints the log and highlights all occurrences of «ERROR» or
«CRITICAL» in red.


Options
-------

Here is a command line interface of Em::

    usage: em [-h] [-i] [-l] [-v] PATTERN FORMAT [FILE [FILE ...]]

    Em is a terminal tool that prints FILE(s), or standard input to standard
    output and highlights the expressions that are matched the PATTERN.

    positional arguments:
      PATTERN            a pattern to highlight
      FORMAT             a color to highlight matched expressions
      FILE               search for pattern in these file(s)

    optional arguments:
      -h, --help         show this help message and exit
      -i, --ignore-case  ignore case distinctions
      -l, --line-mode    highlight entire line
      -v, --version      show program's version number and exit

    With no FILE, or when FILE is -, read standard input. The FORMAT option must
    be one of: BOLD, UNDERLINE, GREY, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN or
    WHITE.

The CLI is clear, but some option descriptions are below:

======================   =====================================================
 ``--ignore-case``        Case insensitive search for the PATTERN.
----------------------   -----------------------------------------------------
 ``--line-mode``          Highlights the entire line if PATTERN was found in
                          the line.
======================   =====================================================


Contribute
----------

Found a bug? Have a good idea for improving Em? Go to `em's github`_ page
and create a new issue or fork. Also, if you like what I'm doing I would
appreciate some support through `gittip`_.


.. _em's github:  https://github.com/ikalnitsky/em
.. _gittip:  https://www.gittip.com/ikalnitsky/
