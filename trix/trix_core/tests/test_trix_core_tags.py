from django.test import TestCase

from trix.trix_core.templatetags import trix_core_tags


class TestTrixMarkdown(TestCase):
    def test_simple(self):
        self.assertEquals(
            trix_core_tags.trix_assignment_markdown('# Hello world\n'),
            '&lt;h1&gt;Hello world&lt;/h1&gt;')
