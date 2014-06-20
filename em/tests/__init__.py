# coding: utf-8
"""
    em.tests
    ~~~~~~~~

    Tests Em itself.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""
from __future__ import unicode_literals

import unittest
import subprocess


class EmTestCase(unittest.TestCase):
    """
    Base class for all the tests that Em uses.
    """

    def get_ansi_color(self, color):
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

    def assertColoredPhraseIn(self, phrase, color, output):
        # builds a finite pattern to be searched in output
        pattern = '{color}{phrase}{reset}'.format(
            color=self.get_ansi_color(color),
            phrase=phrase,
            reset=self.get_ansi_color('reset'),
        )

        # makes assert
        self.assertIn(pattern, output)

    def assertColoredPhraseNotIn(self, phrase, color, output):
        # builds a finite pattern to be searched in output
        pattern = '{color}{phrase}{reset}'.format(
            color=self.get_ansi_color(color),
            phrase=phrase,
            reset=self.get_ansi_color('reset'),
        )

        # makes assert
        self.assertNotIn(pattern, output)

    def execute(self, command, standard_input=None):
        """
        Runs a given command and returns its result.

        :param command: a command to execute
        :param standard_input: a standard input for a given command;
            must be either a string or a list of strings
        :returns: standard output of the command
        """
        # unpack a given list of strings to a single string
        if isinstance(standard_input, (list, tuple,)):
            standard_input = '\n'.join(standard_input)

        if isinstance(standard_input, (str,)):
            standard_input = standard_input.encode('utf-8')

        # run a given command
        p = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        # send data to stdin if needed
        standard_output, _ = p.communicate(input=standard_input)
        return standard_output.decode('utf-8')


if 'assertIn' not in dir(EmTestCase):
    EmTestCase.assertIn = lambda _, v, c: v in c

if 'assertNotIn' not in dir(EmTestCase):
    EmTestCase.assertNotIn = lambda _, v, c: v not in c
