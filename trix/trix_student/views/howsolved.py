from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from trix.trix_core import models

import json


class HowsolvedView(View):
    """docstring for UpdateHowSolvedView"""
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        self.howsolved = request.POST.get('howsolved', None)
        self.assignment_id = request.POST.get('assignment_id', None)

        self.assignment = get_object_or_404(models.Assignment, id=self.assignment_id)
        self.assignment_solution = self.assignment.assignmentsolution_set\
                .filter(id=self.assignment.id)\
                .filter(user=request.user)

        if self.assignment_solution:
            self.assignment_solution[0].howsolved=self.howsolved
            self.assignment_solution[0].save()
        else:
            self.assignment_solution.create(howsolved=self.howsolved, assignment=self.assignment, user=request.user)

        response_data = {}
        response_data['success'] = 'True'
        response_data['howsolved'] = self.howsolved
        return HttpResponse(json.dumps(response_data), content_type='application/json')