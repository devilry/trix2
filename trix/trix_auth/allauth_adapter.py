from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.signals import pre_social_login
from django.contrib.auth import get_user_model
from django.conf import settings
from django.dispatch import receiver


def get_socialaccount_claims(sociallogin):
    """
    Return a dict holding provider claims. For Allauth's OIDC provider
    they are nests under ``userinfo`` with the decoded id_token
    alongside it, while dedicated providers such as ``dataporten``
    store them flat at the root of ``extra_data``.
    """
    extra_data = sociallogin.account.extra_data
    return extra_data.get('userinfo') or extra_data.get('id_token') or extra_data


def prune_unexpected_extra_data(email, sociallogin):
    provider = sociallogin.account.provider
    expected_response = getattr(settings, 'TRIX_SOCIALACCOUNT_EXPECTED_RESPONSES', {}). \
                                get(provider, None)
    if not expected_response:
        return
    claims = get_socialaccount_claims(sociallogin)
    if claims.keys() == expected_response.keys():
        return
    extra_keys = sorted(set(claims.keys()).difference(expected_response.keys()))
    missing_keys = sorted(set(expected_response.keys()).difference(claims.keys()))
    problems = []
    if extra_keys:
        for key in extra_keys:
            claims.pop(key, None)
        problems.append('{} unexpected element{} removed from extra_data: {}'.format(
            len(extra_keys), '' if len(extra_keys) == 1 else 's', ', '.join(extra_keys)))
    if missing_keys:
        problems.append('{} expected element{} missing from response: {}'.format(
            len(missing_keys), '' if len(missing_keys) == 1 else 's', ', '.join(missing_keys)))
    err = MisalignedProviderResponseError('Provider \'{}\' returned a misaligned response: {}'.format(
                                          provider, '; '.join(problems)))
    try:
        from sentry_sdk import capture_exception as sentry_capture_exception, set_user as sentry_set_user
        if email:
            sentry_set_user({"email": email})
        sentry_capture_exception(err)
    except ImportError:
        pass


def update_user_with_socialaccount(email, request, sociallogin, connecting):
    sociallogin.user.set_unusable_password()
    sociallogin.user.full_clean()
    sociallogin.user.save()
    sociallogin.save(request, connecting)


class MisalignedProviderResponseError(Exception):
    """
    Raised by :func:`.pre_social_login_handler` if the response from a social
    account provider lack expected elements and/or had surplus elements when
    compared with `TRIX_SOCIALACCOUNT_EXPECTED_RESPONSES`.
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

    prune_unexpected_extra_data(email, sociallogin)
    if sociallogin.account.pk is not None:
        sociallogin.account.save(update_fields=['extra_data'])
        return

    try:
        existing_user = get_user_model().objects.get(email=email)
    except get_user_model().DoesNotExist:
        return
    sociallogin.user = existing_user
    update_user_with_socialaccount(email, request, sociallogin, connecting=True)
