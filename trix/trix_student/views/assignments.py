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
