from django.http import HttpResponseRedirect
from django.conf import settings

from allauth.account.views import LoginView, LogoutView
from allauth.socialaccount import providers


class AllauthLoginView(LoginView):
    def get(self, *args, **kwargs):
        all_providers = providers.registry.get_list(request=self.request)
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
