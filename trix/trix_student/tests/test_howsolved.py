import json
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from trix.project.develop.testhelpers.user import create_user
from trix.project.develop.testhelpers.login import LoginTestCaseMixin
from trix.trix_core import models


class TestHowSolved(TestCase, LoginTestCaseMixin):
    def setUp(self):
        self.testuser = create_user('testuser@example.com', consent_datetime=timezone.now())
        self.assignment = models.Assignment.objects.create(title='Test')

    def _geturl(self, id):
        return reverse('trix_student_howsolved', args=[id])

    def test_create(self):
        self.assertEqual(models.HowSolved.objects.count(), 0)
        response = self.post_as(
            self.testuser, self._geturl(self.assignment.id),
            content_type='application/json',
            data=json.dumps({
                'howsolved': 'bymyself'
            })
        )
        self.assertEqual(response.status_code, 200)
        responsedata = json.loads(response.content)
        self.assertEqual(responsedata, {'howsolved': 'bymyself'})
        self.assertEqual(models.HowSolved.objects.count(), 1)
        solved = models.HowSolved.objects.first()
        self.assertEqual(solved.howsolved, 'bymyself')

    def test_update(self):
        models.HowSolved.objects.create(
            user=self.testuser, assignment=self.assignment,
            howsolved='withhelp')
        self.assertEqual(models.HowSolved.objects.count(), 1)
        response = self.post_as(
            self.testuser, self._geturl(self.assignment.id),
            content_type='application/json',
            data=json.dumps({
                'howsolved': 'bymyself'
            })
        )
        self.assertEqual(response.status_code, 200)
        responsedata = json.loads(response.content)
        self.assertEqual(responsedata, {'howsolved': 'bymyself'})
        self.assertEqual(models.HowSolved.objects.count(), 1)
        solved = models.HowSolved.objects.first()
        self.assertEqual(solved.howsolved, 'bymyself')

    def test_post_invalid_json(self):
        response = self.post_as(self.testuser, self._geturl(self.assignment.id))
        self.assertEqual(response.status_code, 400)
        responsedata = json.loads(response.content)
        self.assertEqual(responsedata, {'error': 'Invalid JSON data.'})

    def test_post_invalid_assignment_id(self):
        response = self.post_as(
            self.testuser, self._geturl(100001),
            content_type='application/json',
            data=json.dumps({'howsolved': 'bymyself'}))
        self.assertEqual(response.status_code, 404)

    def test_post_invalid_howsolved(self):
        response = self.post_as(
            self.testuser, self._geturl(self.assignment.id),
            content_type='application/json',
            data=json.dumps({'howsolved': 'invalid'}))
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        models.HowSolved.objects.create(
            user=self.testuser, assignment=self.assignment,
            howsolved='withhelp')
        self.assertEqual(models.HowSolved.objects.count(), 1)
        response = self.delete_as(
            self.testuser, self._geturl(self.assignment.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.HowSolved.objects.count(), 0)

    def test_delete_invalid_assignment_id(self):
        response = self.delete_as(
            self.testuser, self._geturl(100001))
        self.assertEqual(response.status_code, 404)
