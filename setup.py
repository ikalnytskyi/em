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

    $ tail -f /path/to/log | em "DEBUG|INFO" GREEN | em "WARN" yellow


Links
`````

* `documentation <http://em.readthedocs.org/>`_
* `source code <https://github.com/ikalnitsky/em>`_

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
    include_package_data=True,
    packages=[
        'em',
    ],
    entry_points={
        'console_scripts': ['em = em:main'],
    },
    classifiers=[
        'Topic :: Utilities',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: BSD License',
    ],
    platforms=['Linux', 'MacOS', 'Unix']
)
