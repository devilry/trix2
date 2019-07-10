from functools import reduce

from trix.trix_core import models
from trix.trix_course.views import base


class CourseDashboardView(base.TrixCourseBaseView):
    model = models.Course
    template_name = "trix_course/course_dashboard.django.html"
    context_object_name = "courses"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(CourseDashboardView, self).get_context_data(**kwargs)
        # Filter out courses where the user is not an admin
        if not self.request.user.is_admin:
            context['courses'] = self.model.objects.filter(admins__id=self.request.user.id)
        context['num_courses'] = len(context['courses'])
        return context
