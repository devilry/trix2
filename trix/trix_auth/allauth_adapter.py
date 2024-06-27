from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.signals import pre_social_login
from django.contrib.auth import get_user_model
from django.conf import settings
from django.dispatch import receiver


def update_user_with_socialaccount(email, request, sociallogin, connecting):
    expected_response = getattr(settings, 'SOCIALACCOUNT_EXPECTED_RESPONSES', {}). \
                                get(sociallogin.account.provider, None)
    if expected_response:
        response_keys = sociallogin.account.extra_data.keys()
        if response_keys != expected_response.keys():
            try:
                extra_keys = set(response_keys).difference(expected_response.keys())
                if extra_keys:
                    for key in extra_keys:
                        sociallogin.account.extra_data.pop(key, None)
                    raise MisalignedProviderResponseError('{} unexpected element(s) removed from extra_data.'.format(len(extra_keys)))
                else:
                    raise MisalignedProviderResponseError('Expected element(s) missing from response.')
            except MisalignedProviderResponseError as err:
                try:
                    from sentry_sdk import capture_exception as sentry_capture_exception, set_user as sentry_set_user
                    if email:
                        sentry_set_user({"email": email})
                    sentry_capture_exception(err)
                except ImportError:
                    pass

    sociallogin.user.set_unusable_password()
    sociallogin.user.full_clean()
    sociallogin.user.save()
    sociallogin.save(request, connecting)


class MisalignedProviderResponseError(Exception):
    """
    Raised by :class:`.TrixSocialAccountAdapter` if the response from a social
    account provider lack expected root elements and/or had surplus root
    elements when compared with `SOCIALACCOUNT_EXPECTED_RESPONSES`.
    """
    def __init__(self, msg):
        self.msg = msg


class TrixSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        email = sociallogin.account.extra_data.get('email', '') or ''

        try:
            existing_user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            sociallogin.user.email = email
            connecting = False
        else:
            sociallogin.user = existing_user
            connecting = True

        update_user_with_socialaccount(email, request, sociallogin, connecting)
        return sociallogin.user

    def is_auto_signup_allowed(self, request, sociallogin):
        return getattr(settings, 'SOCIALACCOUNT_AUTO_SIGNUP', True)


@receiver(pre_social_login)
def pre_social_login_handler(request, sociallogin, **kwargs):
    email = sociallogin.account.extra_data.get('email', '') or ''

    try:
        existing_user = get_user_model().objects.get(email=email)
    except get_user_model().DoesNotExist:
        pass
    else:
        existing_socialaccount = SocialAccount.objects.filter(provider=sociallogin.account.provider, extra_data__contains={'email': email})
        if not existing_socialaccount:
            sociallogin.user = existing_user
            update_user_with_socialaccount(email, request, sociallogin, connecting=True)
            return sociallogin.user
