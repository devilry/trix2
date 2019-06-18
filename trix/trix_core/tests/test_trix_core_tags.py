from django.test import TestCase

from trix.trix_core.templatetags import trix_core_tags


class TestTrixMarkdown(TestCase):
    def test_simple(self):
        self.assertEqual(
            trix_core_tags.trix_assignment_markdown('# Hello world\n'),
            '<h1>Hello world</h1>')
