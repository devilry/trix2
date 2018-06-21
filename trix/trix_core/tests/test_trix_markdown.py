from django.test import TestCase

from trix.trix_core import trix_markdown


class TestTrixMarkdown(TestCase):
    def test_simple(self):
        self.assertEquals(
            trix_markdown.assignment_markdown('# Hello world\n'),
            '&lt;h1&gt;Hello world&lt;/h1&gt;')

    def test_nl2br(self):
        self.assertEquals(
            trix_markdown.assignment_markdown('Hello\nworld'),
            '&lt;p&gt;Hello&lt;br&gt;\nworld&lt;/p&gt;')
