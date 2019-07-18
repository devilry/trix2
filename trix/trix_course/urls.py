from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from trix.trix_course.views import course, administer, remove, add

urlpatterns = [
    url('^(?P<pk>\d+)/remove/(?P<user_id>\d+)$',
        remove.RemoveCourseAdminView.as_view(),
        name='trix_remove_admin'),
    url('^(?P<course_id>\d+)/$', administer.CourseAdminView.as_view(), name='trix_course_admin'),
    url('^(?P<course_id>\d+)/add/$', add.AddCourseAdminListView.as_view(), name="trix_add_admin"),
    url('^(?P<course_id>\d+)/update/(?P<user_id>\d+)/$', add.UpdateCourseAdminView.as_view(),
        name="trix_add_admin_update"),
    url('^(?P<course_id>\d+)/update/$', add.UpdateCourseAdminView.as_view(),
        name="trix_add_admin_update"),
    url('^$', course.CourseDashboardView.as_view(), name='trix_course_dashboard'),
]
