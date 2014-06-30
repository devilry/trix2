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
        self.assignment_id = request.POST.get('assignment_id', None)

        self.assignment = get_object_or_404(models.Assignment, id=self.assignment_id)
        self.assignment_solution = self.assignment.assignment_set\
                .filter(id=self.assignment.id)\
                .filter(user=request.user)

        if self.assignment_solution:
            self.assignment_solution.howsolved = self.howsolved
            self.assignment_solution.save()
        else:
            models.AssignmentSolution.create(howsolved=self.howsolved, assignment=self.assignment, user=request.user)

        response_data = {}
        response_data['success'] = 'True'
        return HttpResponse(json.dumps(response_data), content_type='application/json')