from django.views.generic import ListView
from trix.trix_core import models


class AssignmentListView(ListView):
    model = models.Assignment
    template_name = "trix_student/assignments.django.html"
