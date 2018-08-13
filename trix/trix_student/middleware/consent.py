from django.shortcuts import redirect
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed


class ConsentMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        disable_consent = getattr(settings, 'DISABLE_CONSENT', None)
        if disable_consent:
            raise MiddlewareNotUsed

    def __call__(self, request):
        response = self.get_response(request)

        if 'consent' in request.path or 'logout' in request.path or 'delete' in request.path:
            return response

        if request.user.is_authenticated and not request.user.has_consented:
            return redirect('trix_consent_form')

        return response
