from django.conf.urls import re_path

from trix.trix_course.views import course, administer, remove, add

urlpatterns = [
    re_path(r'^(?P<pk>\d+)/remove/(?P<user_id>\d+)$',
            remove.RemoveCourseAdminView.as_view(),
            name='trix_remove_admin'),
    re_path(r'^(?P<course_id>\d+)/$', administer.CourseAdminView.as_view(), name='trix_course_admin'),
    re_path(r'^(?P<course_id>\d+)/add/$', add.AddCourseAdminListView.as_view(), name="trix_add_admin"),
    re_path(r'^(?P<course_id>\d+)/update/(?P<user_id>\d+)/$', add.UpdateCourseAdminView.as_view(),
            name="trix_add_admin_update"),
    re_path(r'^(?P<course_id>\d+)/update/$', add.UpdateCourseAdminView.as_view(),
            name="trix_add_admin_update"),
    re_path(r'^$', course.CourseDashboardView.as_view(), name='trix_course_dashboard'),
]
