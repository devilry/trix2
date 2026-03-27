from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import View

from trix.trix_core import models
from trix.trix_student.views.common import AssignmentListViewBase


class AssignmentListView(AssignmentListViewBase):
    model = models.Assignment
    template_name = "trix_student/assignments.django.html"
    paginate_by = 20

    def _get_user_is_admin(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                return True
            else:
                return False
        else:
            return False

    def get_all_available_assignments(self):
        assignment_ids = [_f for _f in self.kwargs['assignment_ids'].split('&') if _f]
        return models.Assignment.objects.filter(id__in=assignment_ids)

    def get_already_selected_tags(self):
        return []

    def get_nonremoveable_tags(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(AssignmentListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            progress = self._get_progress()
            context['progress_percentage'] = int(progress['percent'])
        return context

class AssignmentsProgressPartialView(AssignmentListViewBase):
    def _get_user_is_admin(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                return True
            else:
                return False
        else:
            return False

    def get_all_available_assignments(self):
        assignment_ids = [_f for _f in self.kwargs['assignment_ids'].split('&') if _f]
        return models.Assignment.objects.filter(id__in=assignment_ids)

    def get(self, request, *args, **kwargs):
        tags_string = request.GET.get('tags', '') or ''
        if tags_string:
            self.selected_tags = [t for t in tags_string.split(',') if t]
            self.selected_tags.sort()
        else:
            self.selected_tags = []

        try:
            self.selectable_tags = self._get_selectable_tags()
        except Exception:
            self.selectable_tags = []
        try:
            self.non_removeable_tags = self.get_nonremoveable_tags()
        except Exception:
            self.non_removeable_tags = []

        assignment_list = list(self.get_queryset())
        assignmentlist_with_howsolved = self._get_assignmentlist_with_howsolved(assignment_list)

        progress = self._get_progress()
        progress_percentage = int(progress['percent'])

        ctx = {
            'assignmentlist_with_howsolved': assignmentlist_with_howsolved,
            'progress_percentage': progress_percentage,
            'non_removeable_tags': self.non_removeable_tags,
            'selected_tags': self.selected_tags,
            'selectable_tags': self.selectable_tags,
        }
        html = render_to_string('trix_student/include/progressbox.django.html', ctx, request=request)
        return HttpResponse(html, content_type='text/html')
