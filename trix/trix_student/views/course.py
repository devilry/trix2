from django.views.generic import DetailView
from trix.trix_core import models


class CourseDetailView(DetailView):
    model = models.Course
    pk_url_kwarg = 'course_id'
    template_name = "trix_student/course.django.html"