from django import forms
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# NOTE needed for LDAP
TRIX_LOGIN_IS_USERNAME = getattr(settings, 'TRIX_LOGIN_IS_USERNAME', False)
USERNAME_LABEL = _('Email')
if TRIX_LOGIN_IS_USERNAME:
    USERNAME_LABEL = _('Username')


class TrixAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form using crispy form helper.
    """
    username = forms.CharField(max_length=254, label=USERNAME_LABEL)

    def __init__(self, request=None, *args, **kwargs):
        super(TrixAuthenticationForm, self).__init__(request, *args, **kwargs)
        redirect_url = request.GET.get('next')
        self.fields['username'].widget.attrs.update({'autofocus': True})
        self.helper = FormHelper()
        self.helper.add_input(Submit('login', _('Log in'), formnovalidate=True))
        if redirect_url is not None:
            self.helper.form_action = reverse('trix_login') + "?next=" + redirect_url
        else:
            self.helper.form_action = reverse('trix_login')

    def clean(self):
        """
        Give correct error message based on if we use username or email.
        """
        try:
            cleaned_data = super(TrixAuthenticationForm, self).clean()
        except forms.ValidationError:
            if TRIX_LOGIN_IS_USERNAME:
                raise forms.ValidationError(
                    _("Please enter username and password. Note that both fields are "
                      "case-sensitive."))
            else:
                raise forms.ValidationError(
                    _("Please enter a correct email and password. Note that both fields are "
                      "case-sensitive.")
                )

        return cleaned_data


class TrixLoginView(LoginView):
    template_name = 'trix_auth/login.django.html'
    authentication_form = TrixAuthenticationForm
    extra_context = {'TRIX_LOGIN_MESSAGE': getattr(settings, 'TRIX_LOGIN_MESSAGE', None)}

    def get(self, *args, **kwargs):
        if getattr(settings, 'DATAPORTEN_LOGIN', False):
            return HttpResponseRedirect(reverse('account_login'))
        else:
            return super(TrixLoginView, self).get(*args, **kwargs)
