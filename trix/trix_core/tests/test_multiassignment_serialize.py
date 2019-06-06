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
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], {
            'title': 'Test One',
            'tags': ['inf1000', 'oblig1', 'arrays'],
            'text': 'Hello\n\nCruel\n\nWorld'
        })
        self.assertEqual(data[1], {
            'title': 'Test Two',
            'text': 'Testtext'
        })

    def test_deserializer_grouped_correctly(self):
        deserializer = multiassignment_serialize.Deserializer(yaml.safe_dump_all([
            {'id': 1, 'title': 'Existing1'},
            {'title': 'New'},
            {'id': 2, 'title': 'Existing2'},
        ]), course_tag='duck1000')
        self.assertEqual(
            deserializer.deserialized_assignments_with_id,
            {1: {'id': 1, 'title': 'Existing1'}, 2: {'id': 2, 'title': 'Existing2'}}
        )
        self.assertEqual(
            deserializer.deserialized_assignments_without_id,
            [{'title': 'New'}]
        )

    def test_serialize_assignments_single(self):
        assignment = coremodels.Assignment.objects.create(
            title='A title',
            text='A text'
        )
        self.assertEqual(
            multiassignment_serialize.serialize([assignment]),
            ('id: {}\n'
             'title: A title\n'
             'tags: []\n'
             'hidden: false\n'
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
        self.assertEqual(
            multiassignment_serialize.serialize([assignment]),
            ('id: {}\n'
             'title: A title\n'
             'tags: [testtag, testtag2]\n'
             'hidden: false\n'
             'text: |-\n'
             '  A text\n').format(assignment.id)
        )

    def test_serialize_assignments_single_with_solution(self):
        assignment = coremodels.Assignment.objects.create(
            title='A title',
            text='A text',
            solution='A solution'
        )
        self.assertEqual(
            multiassignment_serialize.serialize([assignment]),
            ('id: {}\n'
             'title: A title\n'
             'tags: []\n'
             'hidden: false\n'
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
        self.assertEqual(
            multiassignment_serialize.serialize([assignment1, assignment2]),
            ('id: {}\n'
             'title: A1\n'
             'tags: []\n'
             'hidden: false\n'
             'text: |-\n'
             '  text1\n'
             '---\n'
             'id: {}\n'
             'title: A2\n'
             'tags: []\n'
             'hidden: false\n'
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
        ]), course_tag='duck1000')

        assignments_by_tag = {}
        existing_assignments = deserializer._validate_existing_assignments(assignments_by_tag)
        self.assertEqual(len(existing_assignments), 2)
        self.assertEqual(
            set(assignments_by_tag.keys()),
            set(['duck1000', 'oblig1', 'oblig2', 'week3']))
        self.assertEqual(
            assignments_by_tag['duck1000'], [assignment2, assignment1])
        self.assertEqual(
            assignments_by_tag['oblig2'], [assignment2])

    def test_deserializer_validate_existing_assignments_invalid(self):
        assignment1 = coremodels.Assignment.objects.create(
            title='Existing1', text='text1')
        assignment1.tags.create(tag='duck1000')
        deserializer = multiassignment_serialize.Deserializer(yaml.safe_dump_all([
            {'id': assignment1.id},
        ]), course_tag='duck1000')
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
            {'id': assignment1.id, 'title': 'Updated1', 'text': 'updatedText1',
             'tags': ['oblig1']},
            {'title': 'New1', 'text': 'newText1'},
            {'title': 'New2', 'text': 'newText2',
             'tags': ['duck1000', 'oblig1'],
             'solution': 'newSolution'},
            {'id': assignment2.id, 'title': 'Updated2', 'text': 'updatedText2',
             'tags': ['duck1000', 'oblig2'],
             'solution': 'updatedSolution'},
        ]), course_tag='duck1000')
        deserializer.sync()

        assignment1 = coremodels.Assignment.objects.get(id=assignment1.id)
        assignment2 = coremodels.Assignment.objects.get(id=assignment2.id)
        newassignment1 = coremodels.Assignment.objects.get(title='New1')
        newassignment2 = coremodels.Assignment.objects.get(title='New2')

        self.assertEqual(assignment1.title, 'Updated1')
        self.assertEqual(assignment1.solution, '')
        self.assertEqual(assignment2.title, 'Updated2')
        self.assertEqual(assignment2.solution, 'updatedSolution')
        self.assertEqual(
            set([tagobject.tag for tagobject in assignment1.tags.all()]),
            set(['duck1000', 'oblig1']))
        self.assertEqual(
            set([tagobject.tag for tagobject in assignment2.tags.all()]),
            set(['duck1000', 'oblig2']))
        self.assertEqual(
            set([tagobject.tag for tagobject in newassignment1.tags.all()]),
            set(['duck1000']))
        self.assertEqual(
            set([tagobject.tag for tagobject in newassignment2.tags.all()]),
            set(['duck1000', 'oblig1']))
