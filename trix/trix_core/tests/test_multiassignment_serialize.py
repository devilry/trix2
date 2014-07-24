import yaml
from django.test import TestCase
from trix.trix_core.models import Assignment
from trix.trix_core import multiassignment_serialize


class TestMultiassignmentSerialize(TestCase):
    def test_yaml_load_sanity(self):
        data = list(yaml.load_all("""
---
title: Test One
tags:
- inf1000
- oblig1
- arrays
text: |-
    Hello

    Cruel

    World
---
title: Test Two
text: Testtext
"""))
        self.assertEquals(len(data), 2)
        self.assertEquals(data[0], {
            'title': 'Test One',
            'tags': ['inf1000', 'oblig1', 'arrays'],
            'text': 'Hello\n\nCruel\n\nWorld'
        })
        self.assertEquals(data[1], {
            'title': 'Test Two',
            'text': 'Testtext'
        })

    def test_serialize_assignments_single(self):
        assignment = Assignment.objects.create(
            title='A title',
            text='A text'
        )
        self.assertEquals(
            multiassignment_serialize.serialize([assignment]),
            ('id: 1\n'
             'title: A title\n'
             'tags: []\n'
             'text: |-\n'
             '  A text\n'))

    def test_serialize_assignments_single_with_tags(self):
        assignment = Assignment.objects.create(
            title='A title',
            text='A text'
        )
        assignment.tags.create(tag='testtag')
        assignment.tags.create(tag='testtag2')
        self.assertEquals(
            multiassignment_serialize.serialize([assignment]),
            ('id: 1\n'
             'title: A title\n'
             'tags: [testtag, testtag2]\n'
             'text: |-\n'
             '  A text\n'))

    def test_serialize_assignments_single_with_solution(self):
        assignment = Assignment.objects.create(
            title='A title',
            text='A text',
            solution='A solution'
        )
        self.assertEquals(
            multiassignment_serialize.serialize([assignment]),
            ('id: 1\n'
             'title: A title\n'
             'tags: []\n'
             'text: |-\n'
             '  A text\n'
             'solution: |-\n'
             '  A solution\n'))
