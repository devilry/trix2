from django.conf import settings
from trix.trix_core import models
from trix.trix_student.views import base


class CourseListView(base.TrixListViewBase):
    model = models.Course
    template_name = "trix_student/dashboard.django.html"

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['TRIX_STUDENT_GETTINGSTARTEDGUIDE_URL'] =\
            settings.TRIX_STUDENT_GETTINGSTARTEDGUIDE_URL
        return context
