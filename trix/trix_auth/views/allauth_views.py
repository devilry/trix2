from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse

from allauth.account.views import LoginView, LogoutView
from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.models import SocialApp


class AllauthLoginView(LoginView):
    def get(self, *args, **kwargs):
        redirect_url = self.request.GET.get('next', '')
        if redirect_url == '':
            redirect_url = reverse('trix_student_dashboard')
        adapter = get_adapter(self.request)
        try:
            provider = adapter.get_provider(self.request, 'dataporten')
        except SocialApp.DoesNotExist:
            return super(AllauthLoginView, self).get(args, kwargs)

        return HttpResponseRedirect(
            provider.get_login_url(
                request=self.request,
                process='login', next=redirect_url))


class AllauthLogoutView(LogoutView):
    template_name = 'trix_auth/auth_logout.django.html'

    def get_redirect_url(self):
        # If using Dataporten, redirect to log out from Dataporten as well.
        logout_url = getattr(settings, 'DATAPORTEN_LOGOUT_URL', None)
        if getattr(settings, 'DATAPORTEN_LOGIN', False):
            return logout_url
        else:
            return super(AllauthLogoutView, self).get_redirect_url()
