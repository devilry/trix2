from django.views.generic import DetailView
from trix.trix_core import models


class CourseDetailView(DetailView):
    model = models.Course
    pk_url_kwarg = 'course_id'
    template_name = "trix_student/course.django.html"

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        assignments = models.Assignment.objects.filter_by_tag(obj.course_tag)
        context['assignment_list'] = assignments
        return context