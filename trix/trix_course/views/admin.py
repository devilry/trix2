from django.shortcuts import get_object_or_404

from trix.trix_core import models
from trix.trix_student.views import base


class CourseAdminView(base.TrixListViewBase):
    model = models.Course
    template_name = "trix_course/course_admin.django.html"

    def get(self, request, **kwargs):
        self.course_id = kwargs['course_id']
        self.course = get_object_or_404(models.Course, id=self.course_id)
        return super(CourseAdminView, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CourseAdminView, self).get_context_data(**kwargs)
        context['course'] = self.course
        context['edit_perm'] = self.request.user.has_perm('Course.edit_admins')
        print(self.request.user.has_perm('Course.edit_admins'))
        return context
