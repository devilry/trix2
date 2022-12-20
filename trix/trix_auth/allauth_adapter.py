from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.conf import settings
from allauth.account.utils import (
    user_email
)

Users = get_user_model()


class TrixSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        email = sociallogin.account.extra_data.get('email', '') or ''

        try:
            existing_user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            sociallogin.user.email = email
        else:
            sociallogin.user = existing_user

        sociallogin.user.set_unusable_password()
        sociallogin.user.full_clean()
        sociallogin.user.save()
        sociallogin.save(request)

        return sociallogin.user

    def is_auto_signup_allowed(self, request, sociallogin):
        # If email is specified, check for duplicate and if so, no auto signup.
        auto_signup = getattr(settings, 'SOCIALACCOUNT_AUTO_SIGNUP', True)
        if auto_signup:
            email = user_email(sociallogin.user)
            # Let's check if auto_signup is really possible...
            if not email and getattr(settings, 'ACCOUNT_EMAIL_REQUIRED ', False):
                # Nope, email is required and we don't have it yet...
                auto_signup = False
        return auto_signup
