from django.views.generic import ListView
from trix.trix_core import models


class CourseListView(ListView):
    model = models.Course
    template_name = "trix_student/dashboard.django.html"
