#!/usr/bin/env python
# coding: utf-8
"""
Em
--

Em is a terminal tool that prints FILE(s), or standard input to standard
output and highlights the expressions that are matched the PATTERN.

The expression will be highlighted iff the terminal is ANSI-compatible.


Em is Cool
``````````

.. code:: bash

    $ tail -f /path/to/log | em "DEBUG|INFO" -f green | em "WARN"


Links
`````

* `documentation <http://em.readthedocs.org/>`_
* `source code <https://github.com/ikalnitsky/em>`_

"""
import os
import glob
import subprocess

from setuptools import setup, Command


install_requires = []
try:
    import argparse  # NOQA
except ImportError:
    install_requires.append('argparse')


class LocaleUpdate(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        root = os.path.dirname(__file__)

        src = os.path.join(root, 'em', '__init__.py')
        pot = os.path.join(root, 'em', 'locale', 'em.pot')
        pos = glob.glob(os.path.join(
            root, 'em', 'locale', '*', 'LC_MESSAGES', 'em.po'))

        # update .pot file
        subprocess.call(['xgettext', src, '--output', pot])

        # update .po files from .pot
        for po in pos:
            subprocess.call(['msgmerge', '--update', '--backup=off', po, pot])


class LocaleCompile(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        root = os.path.dirname(__file__)
        pos = glob.glob(os.path.join(
            root, 'em', 'locale', '*', 'LC_MESSAGES', 'em.po'))

        # compile .po files to .mo
        for po in pos:
            mo = '{0}.mo'.format(os.path.splitext(po)[0])
            subprocess.call(['msgfmt', po, '--output-file', mo])


setup(
    name='em',
    version='0.4.0',
    url='https://github.com/ikalnitsky/em',
    license='BSD',
    author='Igor Kalnitsky',
    author_email='igor@kalnitsky.org',
    description="Highlight some PATTERN in terminal's STDOUT",
    long_description=__doc__,
    include_package_data=True,
    packages=[
        'em',
        'em.tests',
    ],
    install_requires=install_requires,
    test_suite='em.tests',
    entry_points={
        'console_scripts': ['em = em:main'],
    },
    classifiers=[
        'Topic :: Utilities',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: BSD License',
    ],
    platforms=['Linux', 'MacOS', 'Unix'],

    # add custom commands to manage locale files
    cmdclass={
        'locale_update': LocaleUpdate,
        'locale_compile': LocaleCompile,
    },
)
