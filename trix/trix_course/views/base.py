from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from trix.trix_student.views import base


class TrixCourseBaseView(base.TrixListViewBase):

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_admin_on_anything():
                return super(TrixCourseBaseView, self).get(request, **kwargs)
            else:
                raise PermissionDenied
        else:
            return redirect('trix_login')
