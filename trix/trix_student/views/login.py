# from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.urlresolvers import reverse


class TrixAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254,
        label=_('Email'))

    def __init__(self, *args, **kwargs):
        super(TrixAuthenticationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('login', _('Log in')))
        self.helper.form_action = reverse('trix-login')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            if '@' in username:
                email = username
                User = get_user_model()
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    pass
                else:
                    username = user.email
            self.user_cache = authenticate(email=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    _("Please enter a correct email and password. Note that both fields are be case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data


def loginview(request):
    return login(request,
        template_name='trix_student/login.django.html',
        authentication_form=TrixAuthenticationForm
    )