from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from trix.trix_course.views import course, admin

urlpatterns = [
    url('^(?P<course_id>\d+)/$', admin.CourseAdminView.as_view(), name='trix_course_admin'),
    url('^$', course.CourseDashboardView.as_view(), name='trix_course_dashboard'),
]
