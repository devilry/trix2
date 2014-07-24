import yaml
from django.test import TransactionTestCase

from trix.trix_core import models as coremodels
from trix.trix_core import multiassignment_serialize


class TestMultiassignmentSerialize(TransactionTestCase):
    def test_yaml_load_sanity(self):
        data = list(yaml.safe_load_all("""
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

    def test_deserializer_grouped_correctly(self):
        deserializer = multiassignment_serialize.Deserializer(yaml.safe_dump_all([
            {'id': 1, 'title': 'Existing1'},
            {'title': 'New'},
            {'id': 2, 'title': 'Existing2'},
        ]), coursetag='duck1000')
        self.assertEquals(
            deserializer.deserialized_assignments_with_id,
            {1: {'id': 1, 'title': 'Existing1'}, 2: {'id': 2, 'title': 'Existing2'}}
        )
        self.assertEquals(
            deserializer.deserialized_assignments_without_id,
            [{'title': 'New'}]
        )

    def test_serialize_assignments_single(self):
        assignment = coremodels.Assignment.objects.create(
            title='A title',
            text='A text'
        )
        self.assertEquals(
            multiassignment_serialize.serialize([assignment]),
            ('id: {}\n'
             'title: A title\n'
             'tags: []\n'
             'text: |-\n'
             '  A text\n').format(assignment.id)
        )

    def test_serialize_assignments_single_with_tags(self):
        assignment = coremodels.Assignment.objects.create(
            title='A title',
            text='A text'
        )
        assignment.tags.create(tag='testtag')
        assignment.tags.create(tag='testtag2')
        self.assertEquals(
            multiassignment_serialize.serialize([assignment]),
            ('id: {}\n'
             'title: A title\n'
             'tags: [testtag, testtag2]\n'
             'text: |-\n'
             '  A text\n').format(assignment.id)
        )

    def test_serialize_assignments_single_with_solution(self):
        assignment = coremodels.Assignment.objects.create(
            title='A title',
            text='A text',
            solution='A solution'
        )
        self.assertEquals(
            multiassignment_serialize.serialize([assignment]),
            ('id: {}\n'
             'title: A title\n'
             'tags: []\n'
             'text: |-\n'
             '  A text\n'
             'solution: |-\n'
             '  A solution\n').format(assignment.id)
        )

    def test_serialize_assignments_multi(self):
        assignment1 = coremodels.Assignment.objects.create(
            title='A1',
            text='text1'
        )
        assignment2 = coremodels.Assignment.objects.create(
            title='A2',
            text='text2'
        )
        self.assertEquals(
            multiassignment_serialize.serialize([assignment1, assignment2]),
            ('id: {}\n'
             'title: A1\n'
             'tags: []\n'
             'text: |-\n'
             '  text1\n'
             '---\n'
             'id: {}\n'
             'title: A2\n'
             'tags: []\n'
             'text: |-\n'
             '  text2\n'
             ).format(assignment1.id, assignment2.id)
        )

    def test_deserializer_validate_existing_assignments(self):
        assignment1 = coremodels.Assignment.objects.create(
            title='Existing1', text='text1')
        assignment2 = coremodels.Assignment.objects.create(
            title='Existing2', text='text2')
        duck1000tag = coremodels.Tag.objects.create(tag='duck1000')
        assignment1.tags.add(duck1000tag)
        assignment2.tags.add(duck1000tag)
        deserializer = multiassignment_serialize.Deserializer(yaml.safe_dump_all([
            {'id': assignment1.id, 'title': 'Updated1', 'text': 'updatedText1',
             'tags': ['oblig1']},
            {'title': 'New'},
            {'id': assignment2.id, 'title': 'Updated2', 'text': 'updatedText2',
             'tags': ['duck1000', 'oblig2', 'week3']},
        ]), coursetag='duck1000')
        
        assignments_by_tag = {}
        existing_assignments = deserializer._validate_existing_assignments(assignments_by_tag)
        self.assertEquals(len(existing_assignments), 2)
        self.assertEquals(
            set(assignments_by_tag.keys()),
            set(['duck1000', 'oblig1', 'oblig2', 'week3']))
        self.assertEquals(
            assignments_by_tag['duck1000'], [assignment1, assignment2])
        self.assertEquals(
            assignments_by_tag['oblig2'], [assignment2])

    def test_deserializer_validate_existing_assignments_invalid(self):
        assignment1 = coremodels.Assignment.objects.create(
            title='Existing1', text='text1')
        assignment1.tags.create(tag='duck1000')
        deserializer = multiassignment_serialize.Deserializer(yaml.safe_dump_all([
            {'id': assignment1.id},
        ]), coursetag='duck1000')
        with self.assertRaises(multiassignment_serialize.DeserializerValidationErrors):
            deserializer._validate_existing_assignments(assignments_by_tag={})

    def test_deserializer_sync(self):
        assignment1 = coremodels.Assignment.objects.create(
            title='Existing1', text='text1')
        assignment2 = coremodels.Assignment.objects.create(
            title='Existing2', text='text2')
        duck1000tag = coremodels.Tag.objects.create(tag='duck1000')
        assignment1.tags.add(duck1000tag)
        assignment2.tags.add(duck1000tag)
        deserializer = multiassignment_serialize.Deserializer(yaml.safe_dump_all([
            {'id': assignment1.id, 'title': 'Updated1', 'text': 'updatedText1'},
            {'id': assignment2.id, 'title': 'Updated2', 'text': 'updatedText2'},
        ]), coursetag='duck1000')
        deserializer.sync()

        assignment1 = coremodels.Assignment.objects.get(id=assignment1.id)
        assignment2 = coremodels.Assignment.objects.get(id=assignment2.id)
        self.assertEquals(assignment1.title, 'Updated1')
        self.assertEquals(assignment2.title, 'Updated2')
