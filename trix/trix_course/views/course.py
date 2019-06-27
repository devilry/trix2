from functools import reduce
from trix.trix_core import models
from trix.trix_student.views import base


class CourseDashboardView(base.TrixListViewBase):
    model = models.Course
    template_name = "trix_course/course_dashboard.django.html"
    context_object_name = "course"

    def get(self, request, **kwargs):
        #
        return super(CourseDashboardView, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CourseDashboardView, self).get_context_data(**kwargs)
        print(context)
        return context
