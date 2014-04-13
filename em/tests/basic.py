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

    def setUp(self):
        """
        Prepare some helper stuff for tests.
        """
        super(BasicFunctionalityTestCase, self).setUp()

        #: a sample text to be used in different test cases
        self.text = [
            'I am immortal, I have inside me blood of kings - yeah - yeah',
            'I have no rival, no man can be my equal',
            'Take me to the future of you all',
        ]

    def test_run_with_default(self):
        output = self.execute(['em', 'rival', 'RED'], self.text)
        self.assertColoredPhraseIn('rival', 'red', output)

    def test_run_with_no_result(self):
        output = self.execute(['em', 'Monte-Cristo', 'RED'], self.text)
        self.assertColoredPhraseNotIn('Monte-Cristo', 'red', output)

    def test_run_with_a_few_words(self):
        output = self.execute(['em', 'no man', 'green'], self.text)
        self.assertColoredPhraseIn('no man', 'green', output)

    def test_run_with_line_mode(self):
        output = self.execute(['em', 'future', 'blue', '-l'], self.text)
        self.assertColoredPhraseIn(self.text[-1], 'blue', output)

    def test_run_with_ignore_case(self):
        output = self.execute(['em', 'No MaN', 'bold'], self.text)
        self.assertColoredPhraseNotIn('no man', 'bold', output)

        output = self.execute(['em', 'No MaN', 'cyan', '-i'], self.text)
        self.assertColoredPhraseIn('no man', 'cyan', output)

    def test_run_with_multiple_arguments(self):
        output = self.execute(['em', 'BLOOD', 'red', '-i', '-l'], self.text)
        self.assertColoredPhraseIn(self.text[0], 'red', output)

    def test_formatting_feature(self):
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
                output = self.execute(['em', 'immortal', fmt], self.text)
                self.assertColoredPhraseIn('immortal', fmt, output)
