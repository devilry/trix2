from django.db.models import Q

from trix.trix_core import models
from trix.trix_course.views import base


class CourseDashboardView(base.TrixCourseBaseView):
    model = models.Course
    template_name = "trix_course/course_dashboard.django.html"
    context_object_name = "courses"
    paginate_by = 20

    def get_queryset(self):
        search = self.request.GET.get('q')
        courses = self.model.objects.all()
        # Filter out courses where the user is not an admin
        if not self.request.user.is_admin:
            courses = courses.filter(admins__id=self.request.user.id)
        if search:
            if search.isdigit():
                courses = courses.filter(id=int(search))
            else:
                courses = courses.filter(Q(course_tag__tag__icontains=search)
                                         | Q(description__icontains=search))  # noqa: W503
        return courses

    def get_context_data(self, **kwargs):
        context = super(CourseDashboardView, self).get_context_data(**kwargs)
        context['num_courses'] = len(context['courses'])
        return context
