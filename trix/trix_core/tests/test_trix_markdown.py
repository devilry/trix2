from django.test import TestCase

from trix.trix_core import trix_markdown


class TestTrixMarkdown(TestCase):
    def test_simple(self):
        self.assertEqual(
            trix_markdown.assignment_markdown('# Hello world\n'),
            '<h1>Hello world</h1>')

    def test_nl2br(self):
        self.assertEqual(
            trix_markdown.assignment_markdown('Hello\nworld'),
            '<p>Hello<br>\nworld</p>')
