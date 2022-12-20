from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DeleteView

from trix.trix_core.models import Course, User


class RemoveCourseAdminView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = "trix_course/remove_course_admin.django.html"
    user_id = None

    def get(self, request, **kwargs):
        self.user_id = kwargs['user_id']
        course = get_object_or_404(Course, id=kwargs['pk'])
        if request.user.is_course_owner(course):
            return super(RemoveCourseAdminView, self).get(request, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(RemoveCourseAdminView, self).get_context_data(**kwargs)
        context['admin_user'] = User.objects.get(id=self.user_id)
        return context

    def delete(self, request, *args, **kwargs):
        '''
        Removes a single given admin from the course.
        '''
        course_id = kwargs['pk']
        user_id = kwargs['user_id']
        course = Course.objects.get(id=course_id)
        admin_user = User.objects.get(id=user_id)

        # Check if we only want to remove as an owner
        if request.POST.get('owner'):
            course.owner.remove(admin_user)
        else:
            course.admins.remove(admin_user)
            if admin_user in course.owner.all():
                course.owner.remove(admin_user)

        return redirect('trix_course_admin', course_id=course_id)
