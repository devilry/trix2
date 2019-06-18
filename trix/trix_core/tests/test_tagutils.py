from django.test import TestCase

from trix.trix_core import models as coremodels
from trix.trix_core.tagutils import bulk_update_assignment_tags


class TestTagUtils(TestCase):
    def test_bulk_update_assignment_tags(self):
        assignment1 = coremodels.Assignment.objects.create(
            title='A1', text='text1')
        assignment2 = coremodels.Assignment.objects.create(
            title='A2', text='text2')
        bulk_update_assignment_tags(
            assignments_by_tag={
                'duck1000': [assignment1, assignment2],
                'oblig2': [assignment1]
            },
            existing_assignments=[assignment1, assignment2])
        self.assertEqual(
            set([tagobject.tag for tagobject in assignment1.tags.all()]),
            set(['duck1000', 'oblig2']))
        self.assertEqual(
            set([tagobject.tag for tagobject in assignment2.tags.all()]),
            set(['duck1000']))
