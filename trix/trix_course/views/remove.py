from django.core.exceptions import PermissionDenied
from django.views.generic import DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from trix.trix_core.models import Course


class RemoveCourseAdminView(DeleteView):
    model = Course

    def get(self, request, **kwargs):
        print(kwargs['course_id'])
        if request.user.is_authenticated:
            course = get_object_or_404(Course, id=kwargs['course_id'])
            if request.user.is_course_owner(course):
                return super(RemoveCourseAdminView, self).get(request, **kwargs)
            else:
                raise PermissionDenied
        else:
            return redirect('trix_login')

    def get_object(self, queryset=None):
        course = super(RemoveCourseAdminView, self).get_object()
        if not self.request.user.is_course_owner(course):
            raise PermissionDenied
        return course

    def delete(self, request, *args, **kwargs):
        '''
        Removes a single given admin from the course.
        '''
        course_id = kwargs['course_id']
        user_id = kwargs['pk']

        course = self.model.objects.filter(id=course_id).get()
        admin_user = course.admins.filter(id=user_id).get()
        course.admins.remove(admin_user)

        return redirect('trix_course_admin', course_id=course_id)
