from django.shortcuts import get_object_or_404, redirect

from trix.trix_core.models import Course
from trix.trix_course.views import base


class CourseAdminView(base.TrixCourseBaseView):
    model = Course
    template_name = "trix_course/course_admin.django.html"

    def get(self, request, **kwargs):
        self.course_id = kwargs['course_id']
        self.course = get_object_or_404(Course, id=self.course_id)
        return super(CourseAdminView, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CourseAdminView, self).get_context_data(**kwargs)
        user = self.request.user
        context['course'] = self.course
        # Check if user is course owner
        context['owner'] = user.is_course_owner(self.course)
        # Get the list of owners
        context['owner_list'] = self.course.owner.all()
        return context
