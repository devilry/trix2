from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _

from trix.trix_core import models


class ProfilePageView(LoginRequiredMixin, ListView):
    template_name = 'trix_student/users.django.html'
    model = models.HowSolved
    paginate_by = 2

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
