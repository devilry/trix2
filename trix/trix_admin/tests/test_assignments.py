from django.core.exceptions import ValidationError
from django.test import TestCase
from trix.trix_admin.views.assignments import validate_single_tag


class TestValidateSingleTag(TestCase):
    def test_valid(self):
        validate_single_tag('test')

    def test_valid_unicodechars(self):
        validate_single_tag('v\u00e6r')

    def test_valid_numbers(self):
        validate_single_tag('2015')

    def test_valid_slash(self):
        validate_single_tag('test-ing')

    def test_invalid_comma(self):
        with self.assertRaises(ValidationError):
            validate_single_tag('test,ing')

    def test_invalid_whitespace(self):
        with self.assertRaises(ValidationError):
            validate_single_tag('test ing')
