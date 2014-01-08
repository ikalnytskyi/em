#!/usr/bin/env python
# coding: utf-8
"""
em
==

em program is a terminal tool that prints FILE(s), or standard input
to standard output and highlights the expressions that are matched
the PATTERN.

The expression will be highlighted iff the terminal is ANSI-compatible.


em is cool
----------

.. code:: bash

    $ tail -f /path/to/log | em "DEBUG|INFO" GREEN | em "WARN" yellow


and easy to install
-------------------

.. code:: bash

    $ (sudo) pip install em

"""
from setuptools import setup
from em import __version__


setup(
    name='em',
    version=__version__,
    url='https://github.com/ikalnitsky/em',
    license='BSD',
    author='Igor Kalnitsky',
    author_email='igor@kalnitsky.org',
    description='Highlight some PATTERN in terminal\'s STDOUT',
    long_description=__doc__,
    packages=[
        'em',
    ],
    entry_points={
        'console_scripts': ['em = em:main'],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
    platforms=['Linux', 'MacOS', 'Unix']
)
