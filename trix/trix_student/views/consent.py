from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView


class ConsentFormView(LoginRequiredMixin, TemplateView):
    template_name = "trix_student/consent_form.django.html"

    def post(self, request, **kwargs):
        request.user.consent_datetime = timezone.now()
        request.user.save()
        return redirect('/')
