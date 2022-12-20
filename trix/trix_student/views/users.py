from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import Http404
from django.urls import reverse_lazy

from trix.trix_core import models
from trix.trix_student.views import base


class ProfilePageView(LoginRequiredMixin, base.TrixListViewBase):
    template_name = 'trix_student/users.django.html'
    model = models.HowSolved

    def get_context_data(self):
        context = super(ProfilePageView, self).get_context_data()
        context['solved_assignments'] = self.get_solved_assignments()
        context['user_role'] = self.get_user_role()
        return context

    def get_solved_assignments(self):
        return models.HowSolved.objects.all()

    def get_user_role(self):
        if self.request.user.is_superuser:
            return _('Superuser')
        elif self.request.user.is_admin_on_anything():
            courses = models.Course.objects.filter(admins__id=self.request.user.id)
            courses_string = ', '.join([str(course) for course in courses])
            return _('Administrator for ') + courses_string
        else:
            return _('Student')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'trix_student/user_delete.django.html'
    model = models.User
    success_url = reverse_lazy('trix_student_dashboard')
    success_message = _('Brukeren din er nå slettet')

    def get_object(self, queryset=None):
        user = super(UserDeleteView, self).get_object()
        if not user.id == self.request.user.id:
            raise Http404
        return user

    def get_success_url(self) -> str:
        messages.success(self.request, self.success_message)
        return super().get_success_url()
