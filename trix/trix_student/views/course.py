from django.shortcuts import get_object_or_404

from trix.trix_core import models
from trix.trix_student.views.common import AssignmentListViewBase


class CourseDetailView(AssignmentListViewBase):
    template_name = "trix_student/course.django.html"
    paginate_by = 20

    def get(self, request, **kwargs):
        self.course_id = kwargs['course_id']
        self.course = get_object_or_404(models.Course, id=self.course_id)
        return super(CourseDetailView, self).get(request, **kwargs)

    def _get_user_is_admin(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                return True
            else:
                return self.course.admins.filter(id=self.request.user.id)
        else:
            return False

    def get_all_available_assignments(self):
        return (models.Assignment.objects
                .filter_by_tag(self.course.course_tag)
                .filter_by_tag(self.course.active_period))

    def get_already_selected_tags(self):
        already_selected_tags = [
            self.course.course_tag.tag,
            self.course.active_period.tag
        ]
        return already_selected_tags

    def get_nonremoveable_tags(self):
        return [self.course.course_tag, self.course.active_period]

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['course'] = self.course
        return context
