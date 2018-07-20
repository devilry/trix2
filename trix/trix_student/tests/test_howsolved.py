import json
from django.test import TestCase
from django.urls import reverse

from trix.project.develop.testhelpers.user import create_user
from trix.project.develop.testhelpers.login import LoginTestCaseMixin
from trix.trix_core import models


class TestHowSolved(TestCase, LoginTestCaseMixin):
    def setUp(self):
        self.testuser = create_user('testuser@example.com')
        self.assignment = models.Assignment.objects.create(title='Test')

    def _geturl(self, id):
        return reverse('trix_student_howsolved', args=[id])

    def test_create(self):
        self.assertEquals(models.HowSolved.objects.count(), 0)
        response = self.post_as(
            self.testuser, self._geturl(self.assignment.id),
            content_type='application/json',
            data=json.dumps({
                'howsolved': 'bymyself'
            })
        )
        self.assertEquals(response.status_code, 200)
        responsedata = json.loads(response.content)
        self.assertEquals(responsedata, {'howsolved': 'bymyself'})
        self.assertEquals(models.HowSolved.objects.count(), 1)
        solved = models.HowSolved.objects.first()
        self.assertEquals(solved.howsolved, 'bymyself')

    def test_update(self):
        models.HowSolved.objects.create(
            user=self.testuser, assignment=self.assignment,
            howsolved='withhelp')
        self.assertEquals(models.HowSolved.objects.count(), 1)
        response = self.post_as(
            self.testuser, self._geturl(self.assignment.id),
            content_type='application/json',
            data=json.dumps({
                'howsolved': 'bymyself'
            })
        )
        self.assertEquals(response.status_code, 200)
        responsedata = json.loads(response.content)
        self.assertEquals(responsedata, {'howsolved': 'bymyself'})
        self.assertEquals(models.HowSolved.objects.count(), 1)
        solved = models.HowSolved.objects.first()
        self.assertEquals(solved.howsolved, 'bymyself')

    def test_post_invalid_json(self):
        response = self.post_as(self.testuser, self._geturl(self.assignment.id))
        self.assertEquals(response.status_code, 400)
        responsedata = json.loads(response.content)
        self.assertEquals(responsedata, {'error': 'Invalid JSON data.'})

    def test_post_invalid_assignment_id(self):
        response = self.post_as(
            self.testuser, self._geturl(100001),
            content_type='application/json',
            data=json.dumps({'howsolved': 'bymyself'}))
        self.assertEquals(response.status_code, 404)

    def test_post_invalid_howsolved(self):
        response = self.post_as(
            self.testuser, self._geturl(self.assignment.id),
            content_type='application/json',
            data=json.dumps({'howsolved': 'invalid'}))
        self.assertEquals(response.status_code, 400)

    def test_delete(self):
        models.HowSolved.objects.create(
            user=self.testuser, assignment=self.assignment,
            howsolved='withhelp')
        self.assertEquals(models.HowSolved.objects.count(), 1)
        response = self.delete_as(
            self.testuser, self._geturl(self.assignment.id))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(models.HowSolved.objects.count(), 0)

    def test_delete_invalid_assignment_id(self):
        response = self.delete_as(
            self.testuser, self._geturl(100001))
        self.assertEquals(response.status_code, 404)
