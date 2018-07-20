import json
from django.views.generic import View
from django import http
from django.shortcuts import get_object_or_404
from django import forms

from trix.trix_core import models


class HowSolvedForm(forms.ModelForm):
    class Meta:
        model = models.HowSolved
        fields = ['howsolved']


class HowsolvedView(View):
    """
    View of how the assignment was solved.
    """
    http_method_names = ['post', 'delete']

    def _bad_request_response(self, data):
        return http.HttpResponseBadRequest(json.dumps(data), content_type='application/json')

    def _not_found_response(self, data):
        return http.HttpResponseNotFound(json.dumps(data), content_type='application/json')

    def _200_response(self, data):
        return http.HttpResponse(json.dumps(data), content_type='application/json')

    def _get_assignment(self):
        return get_object_or_404(models.Assignment, id=self.kwargs['assignment_id'])

    def _get_howsolved(self, assignment_id):
        return models.HowSolved.objects\
            .filter(assignment_id=assignment_id, user=self.request.user)\
            .get()

    def post(self, request, **kwargs):
        try:
            data = json.loads(request.body)
        except ValueError:
            return self._bad_request_response({
                'error': 'Invalid JSON data.'
            })

        form = HowSolvedForm(data)
        if form.is_valid():
            howsolved = form.cleaned_data['howsolved']
            assignment = self._get_assignment()

            try:
                howsolvedobject = self._get_howsolved(assignment.id)
            except models.HowSolved.DoesNotExist:
                howsolvedobject = models.HowSolved.objects.create(
                    howsolved=howsolved,
                    assignment=assignment,
                    user=request.user)
            else:
                howsolvedobject.howsolved = howsolved
                howsolvedobject.save()

            return self._200_response({'howsolved': howsolvedobject.howsolved})
        else:
            return self._bad_request_response({
                'error': form.errors.as_text()
            })

    def delete(self, request, **kwargs):
        try:
            howsolved = self._get_howsolved(self.kwargs['assignment_id'])
        except models.HowSolved.DoesNotExist:
            return self._not_found_response({
                'message': 'No HowSolved for this user and assignment.'
            })
        else:
            howsolved.delete()
            return self._200_response({'success': True})
