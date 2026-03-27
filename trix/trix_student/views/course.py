from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator

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
        return models.Assignment.objects \
            .filter(tags=self.course.course_tag) \
            .filter(tags=self.course.active_period)

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
        if self.request.user.is_authenticated:
            context['progress_percentage'] = int(super(CourseDetailView, self)._get_progress()['percent'])
        return context


class CourseProgressPartialView(CourseDetailView):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        self.course_id = kwargs['course_id']
        self.course = get_object_or_404(models.Course, id=self.course_id)

        self.selected_tags = self._get_selected_tags()
        self.selectable_tags = self._get_selectable_tags()
        self.non_removeable_tags = self.get_nonremoveable_tags()

        assignment_list = list(self.get_queryset())
        assignmentlist_with_howsolved = self._get_assignmentlist_with_howsolved(assignment_list)

        progress = self._get_progress()
        progress_percentage = int(progress['percent'])

        ctx = {
            'assignmentlist_with_howsolved': assignmentlist_with_howsolved,
            'progress_percentage': progress_percentage,
            'non_removeable_tags': self.get_nonremoveable_tags(),
            'selected_tags': self._get_selected_tags(),
            'selectable_tags': self._get_selectable_tags(),
        }

        html = render_to_string('trix_student/include/progressbox.django.html', ctx, request=request)
        return HttpResponse(html, content_type='text/html')
