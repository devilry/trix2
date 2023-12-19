from django.urls import re_path

from .api import ReadyCheck, LiveCheck

urlpatterns = [
    re_path('_api/application-state/ready', ReadyCheck.as_view(), name='trix_core_application_state_ready'),
    re_path('_api/application-state/alive', LiveCheck.as_view(), name='trix_core_application_state_alive'),
]
