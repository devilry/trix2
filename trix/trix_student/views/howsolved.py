import json
from django.views.generic import View
from django import forms, http
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from urllib import parse

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

    def _200_json(self, data):
        return http.HttpResponse(json.dumps(data), content_type='application/json')

    def _200_html_fragment(self, ctx, hx_trigger=None):
        """
        Render the assignment include and return it as HTML (needed for hx-swap).
        If hx_trigger is provided (a dict) it adds a HX-Trigger header so
        clients can refresh other fragments such as the progress partial.
        """
        html = render_to_string('trix_student/include/assignment.django.html', ctx, request=self.request)
        resp = http.HttpResponse(html, content_type='text/html')
        if hx_trigger is not None:
            resp['HX-Trigger'] = json.dumps(hx_trigger)
        return resp

    def _get_assignment(self):
        return get_object_or_404(models.Assignment, id=self.kwargs['assignment_id'])

    def _get_howsolved(self, assignment_id):
        return models.HowSolved.objects\
            .filter(assignment_id=assignment_id, user=self.request.user)\
            .get()

    def _is_htmx(self):
        return self.request.headers.get('HX-Request') == 'true'

    def post(self, request, **kwargs):
        try:
            data = json.loads(request.body)
        except ValueError:
            return self._bad_request_response({'error': 'Invalid JSON data.'})

        form = HowSolvedForm(data)
        if not form.is_valid():
            return self._bad_request_response({'error': form.errors.as_text()})

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

        course = models.Course.objects.filter(course_tag__in=assignment.tags.all()).first()
        user_is_admin = False
        if request.user.is_authenticated:
            if request.user.is_admin:
                user_is_admin = True
            elif course is not None and hasattr(course, 'admins'):
                try:
                    user_is_admin = course.admins.filter(id=request.user.id).exists()
                except Exception:
                    user_is_admin = False

        urlencoded_success_url = parse.urlencode({'success_url': request.get_full_path()})

        ctx = {
            'assignment': assignment,
            'howsolved': howsolvedobject.howsolved,
            'disable_howsolved_box': False,
            'course': course,
            'user_is_admin': user_is_admin,
            'urlencoded_success_url': urlencoded_success_url,
        }

        if self._is_htmx():
            hx_trigger = {'assignmentUpdated': assignment.id}
            return self._200_html_fragment(ctx, hx_trigger=hx_trigger)
        else:
            return self._200_json({'howsolved': howsolvedobject.howsolved})

    def delete(self, request, **kwargs):
        assignment = self._get_assignment()
        try:
            howsolved = self._get_howsolved(self.kwargs['assignment_id'])
        except models.HowSolved.DoesNotExist:
            return self._not_found_response({
                'message': 'No HowSolved for this user and assignment.'
            })
        else:
            howsolved.delete()

            course = models.Course.objects.filter(course_tag__in=assignment.tags.all()).first()
            user_is_admin = False
            if request.user.is_authenticated:
                if request.user.is_admin:
                    user_is_admin = True
                elif course is not None and hasattr(course, 'admins'):
                    try:
                        user_is_admin = course.admins.filter(id=request.user.id).exists()
                    except Exception:
                        user_is_admin = False

            urlencoded_success_url = parse.urlencode({'success_url': request.get_full_path()})

            ctx = {
                'assignment': assignment,
                'howsolved': '',
                'disable_howsolved_box': False,
                'course': course,
                'user_is_admin': user_is_admin,
                'urlencoded_success_url': urlencoded_success_url,
            }

            if self._is_htmx():
                hx_trigger = {'assignmentUpdated': assignment.id}
                return self._200_html_fragment(ctx, hx_trigger=hx_trigger)
            else:
                return self._200_json({'success': True})
