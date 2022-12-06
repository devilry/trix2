from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from trix.trix_student.views.base import TrixTemplateViewBase


class ConsentFormView(LoginRequiredMixin, TrixTemplateViewBase):
    template_name = "trix_student/consent_form.django.html"

    def post(self, request, **kwargs):
        request.user.consent_datetime = timezone.now()
        request.user.save()
        return redirect('/')
