from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from trix.trix_core.models import Course, User
from trix.trix_course.views import base


class AddCourseAdminListView(base.TrixCourseBaseView):
    model = Course
    template_name = "trix_course/add_course_admin.django.html"
    paginate_by = 20

    def get_queryset(self):
        course = Course.objects.get(id=self.kwargs['course_id'])
        users = User.objects.filter(is_active=True).exclude(owner=course)
        return users

    def get_context_data(self, **kwargs):
        context = super(AddCourseAdminListView, self).get_context_data(**kwargs)
        context['course'] = Course.objects.get(id=self.kwargs['course_id'])
        return context


class UpdateCourseAdminView(base.TrixCourseBaseView):
    model = Course

    def post(self, request, *args, **kwargs):
        '''
        Adds a user as a course admin or owner.
        '''
        user = User.objects.get(id=kwargs['user_id'])
        course = Course.objects.get(id=kwargs['course_id'])
        if request.POST.get('admin'):
            course.admins.add(user)
            messages.info(request, user.displayname + " added as course admin.")
        if request.POST.get('owner'):
            course.owner.add(user)
            messages.info(request, user.displayname + " added as course owner.")
        return redirect(reverse('trix_add_admin', kwargs={'course_id': 1}))
