from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

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
