from django.http import HttpResponseRedirect
from django.conf import settings

from allauth.account.views import LoginView, LogoutView
from allauth.socialaccount.adapter import get_adapter


class AllauthLoginView(LoginView):
    def get(self, *args, **kwargs):
        adapter = get_adapter(self.request)
        all_providers = adapter.list_providers(self.request)
        provider = all_providers[0]
        return HttpResponseRedirect(
            provider.get_login_url(
                request=self.request,
                process='login'))


class AllauthLogoutView(LogoutView):
    template_name = 'trix_auth/auth_logout.django.html'

    def get_redirect_url(self):
        # If using Dataporten, redirect to log out from Dataporten as well.
        logout_url = getattr(settings, 'DATAPORTEN_LOGOUT_URL', None)
        if getattr(settings, 'DATAPORTEN_LOGIN', False):
            return logout_url
        else:
            return super(AllauthLogoutView, self).get_redirect_url()
