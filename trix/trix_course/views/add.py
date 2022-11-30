from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from trix.trix_core.models import Course, User
from trix.trix_course.views import base


class AddCourseAdminListView(base.TrixCourseBaseView):
    model = Course
    template_name = "trix_course/add_course_admin.django.html"
    paginate_by = 20

    def get(self, request, **kwargs):
        course_id = kwargs['course_id']
        course = get_object_or_404(Course, id=course_id)
        if request.user.is_course_owner(course):
            return super(AddCourseAdminListView, self).get(request, **kwargs)
        else:
            raise PermissionDenied

    def get_queryset(self):
        search = self.request.GET.get('q')
        course = Course.objects.get(id=self.kwargs['course_id'])
        users = User.objects.filter(is_active=True).exclude(owner=course)
        if not self.request.user.is_superuser:
            users = users.exclude(admin=course)
        if search:
            users = users.filter(email__icontains=search)
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
        course = Course.objects.get(id=kwargs['course_id'])

        if not request.user.is_course_owner(course):
            raise PermissionDenied

        # Add admin or owner based on type of post.
        if 'admin' in request.POST:
            self._add_admins(request, course, [kwargs['user_id']])
        elif 'owner' in request.POST:
            self._add_owners(request, course, [kwargs['user_id']])
        elif 'admin_list' in request.POST:
            self._add_admins(request, course, request.POST.getlist('selected_students'))
        elif 'owner_list' in request.POST:
            self._add_owners(request, course, request.POST.getlist('selected_students'))
        return redirect(reverse('trix_add_admin', kwargs={'course_id': kwargs['course_id']}))

    def _add_admins(self, request, course, id_list):
        for user_id in id_list:
            user = User.objects.get(id=user_id)
            course.admins.add(user)
            messages.success(request, _(f"{user.displayname} added as a course admin."))

    def _add_owners(self, request, course, id_list):
        for user_id in id_list:
            user = User.objects.get(id=user_id)
            course.admins.add(user)
            course.owner.add(user)
            messages.success(request, _(f"{user.displayname} added as course owner."))
