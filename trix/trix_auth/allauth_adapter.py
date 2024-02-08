from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.signals import pre_social_login
from django.contrib.auth import get_user_model
from django.conf import settings
from django.dispatch import receiver


def update_user_with_socialaccount(request, sociallogin, connecting):
    sociallogin.user.set_unusable_password()
    sociallogin.user.full_clean()
    sociallogin.user.save()
    sociallogin.save(request, connecting)


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

        update_user_with_socialaccount(request, sociallogin, connecting)
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
        existing_socialaccount = SocialAccount.objects.filter(provider='dataporten', extra_data__contains={'email': email})
        if not existing_socialaccount:
            sociallogin.user = existing_user
            update_user_with_socialaccount(request, sociallogin, connecting=True)
            return sociallogin.user
