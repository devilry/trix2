from django.db.models import Q
from django.shortcuts import get_object_or_404

from trix.trix_core.models import Course
from trix.trix_course.views import base


class CourseAdminView(base.TrixCourseBaseView):
    model = Course
    template_name = "trix_course/course_admin.django.html"

    def get(self, request, **kwargs):
        self.course = get_object_or_404(Course, id=kwargs['course_id'])
        return super(CourseAdminView, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CourseAdminView, self).get_context_data(**kwargs)
        context['course'] = self.course
        # Check if user is course owner
        context['owner'] = self.request.user.is_course_owner(self.course)
        admin_list = self.course.admins.all()
        search = self.request.GET.get('q')
        if search:
            owner = True if search == "owner" else False
            admin_list = admin_list.filter(Q(email__icontains=search)
                                           | Q(owner=owner))  # noqa: W503
        context['admin_list'] = admin_list
        return context
