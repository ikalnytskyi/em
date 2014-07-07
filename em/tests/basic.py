# coding: utf-8
"""
    em.tests.basic
    ~~~~~~~~~~~~~~

    Tests basic stuff: public interface, not internal stuff.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""
from __future__ import unicode_literals

from em.tests import EmTestCase


class BasicFunctionalityTestCase(EmTestCase):
    #: a sample text to be used in different test cases
    text = [
        'I am immortal, I have inside me blood of kings - yeah - yeah',
        'I have no rival, no man can be my equal',
        'Take me to the future of you all',
    ]

    #: default color
    default_format = 'red'

    def test_run_with_no_result(self):
        output = self.execute(['em', 'Monte-Cristo'], self.text)
        self.assertColoredPhraseNotIn('Monte-Cristo', self.default_format, output)

    def test_run_with_one_word(self):
        output = self.execute(['em', 'rival'], self.text)
        self.assertColoredPhraseIn('rival', self.default_format, output)

    def test_run_with_few_words(self):
        output = self.execute(['em', 'no man'], self.text)
        self.assertColoredPhraseIn('no man', self.default_format, output)

    def test_run_with_line_mode(self):
        output = self.execute(['em', 'future', '-l'], self.text)
        self.assertColoredPhraseIn(self.text[-1], self.default_format, output)

    def test_run_with_ignore_case(self):
        output = self.execute(['em', 'No MaN'], self.text)
        self.assertColoredPhraseNotIn('no man', self.default_format, output)

        output = self.execute(['em', 'No MaN', '-i'], self.text)
        self.assertColoredPhraseIn('no man', self.default_format, output)

    def test_run_with_multiple_arguments(self):
        output = self.execute(['em', 'BLOOD', '-f', 'cyan', '-i', '-l'], self.text)
        self.assertColoredPhraseIn(self.text[0], 'cyan', output)

    def test_run_with_format(self):
        formats = (
            'bold',
            'underline',

            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',

            'ongrey',
            'onred',
            'ongreen',
            'onyellow',
            'onblue',
            'onmagenta',
            'oncyan',
            'onwhite',
        )

        for format_ in formats:
            # test both uppercased and lowercased variants
            for fmt in (format_.lower(), format_.upper()):
                output = self.execute(['em', 'immortal', '-f', fmt], self.text)
                self.assertColoredPhraseIn('immortal', fmt, output)
