from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from trix.trix_student.views import base


class TrixCourseBaseView(LoginRequiredMixin, base.TrixListViewBase):

    def get(self, request, **kwargs):
        if request.user.is_admin_on_anything():
            return super(TrixCourseBaseView, self).get(request, **kwargs)
        else:
            raise PermissionDenied
