import logging

from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse

from allauth.account.views import LoginView, LogoutView
from allauth.socialaccount.adapter import get_adapter

logger = logging.getLogger(__name__)


def selecting_provider_view(request):
    available_providers = get_adapter(request).list_providers(request)
    configured_providers = getattr(settings, 'SOCIALACCOUNT_PROVIDERS', {})
    providers = [p for p in available_providers if p.id in configured_providers]
    return render(request, 'trix_auth/select_provider.django.html', {'providers': providers})


class AllauthLoginView(LoginView):
    def get(self, *args, **kwargs):
        redirect_url = self.request.GET.get('next', '')
        if redirect_url == '':
            redirect_url = reverse('trix_student_dashboard')
        adapter = get_adapter(self.request)
        socialaccount_providers = getattr(settings, 'SOCIALACCOUNT_PROVIDERS', {})
        if not socialaccount_providers:
            logger.warning('AllauthLoginView accessed with no IdP configured.')
            return HttpResponseRedirect(reverse('trix_login'))
        if len(socialaccount_providers) > 1:
            logger.warning(f'AllauthLoginView accessed directly with {len(socialaccount_providers)} IdPs. Redirecting to selector.')
            return HttpResponseRedirect(reverse('select_provider'))
        provider = adapter.get_provider(self.request, list(socialaccount_providers)[0])
        return HttpResponseRedirect(
            provider.get_login_url(
                request=self.request,
                process='login', next=redirect_url))


class AllauthLogoutView(LogoutView):
    template_name = 'trix_auth/auth_logout.django.html'

    def get_redirect_url(self):
        '''Redirect to log out from the identity provider (IdP) as well.'''
        logout_urls = getattr(settings, 'TRIX_SOCIALACCOUNT_LOGOUT_URLS', {})

        methods = self.request.session.get('account_authentication_methods')
        if methods:
            session_login_method = methods[0]
            if (
                session_login_method['method'] == 'socialaccount'
                and session_login_method['provider'] in logout_urls
            ):
                return logout_urls[session_login_method['provider']]
        return super(AllauthLogoutView, self).get_redirect_url()
