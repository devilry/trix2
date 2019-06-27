from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from trix.trix_course.views import course

urlpatterns = [
    url('^$', course.CourseDashboardView.as_view(), name='trix_course_dashboard'),
]
