from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from trix.trix_core import models

import json


class HowsolvedView(View):
    """docstring for UpdateHowSolvedView"""
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        howsolved = request.POST.get('howsolved', None)
        assignment_id = request.POST.get('assignment_id', None)
        assignment = get_object_or_404(models.Assignment, id=assignment_id)

        try:
            assignment_solution = self.assignment.assignmentsolution_set\
                .filter(id=assignment, user=request.user).get()
        except models.AssignmentSolution.DoesNotExist:
            models.AssignmentSolution.create(
                howsolved=howsolved,
                assignment=self.assignment,
                user=request.user)
        else:
            assignment_solution.howsolved = howsolved
            assignment_solution.save()

        response_data = {}
        response_data['success'] = 'True'
        response_data['howsolved'] = self.howsolved
        return HttpResponse(json.dumps(response_data), content_type='application/json')
