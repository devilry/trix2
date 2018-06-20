from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.urlresolvers import reverse


class TrixAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form using crispy form helper.
    """

    def __init__(self, request=None, *args, **kwargs):
        super(TrixAuthenticationForm, self).__init__(request, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('login', _('Log in')))
        self.helper.form_action = reverse('trix-login')
