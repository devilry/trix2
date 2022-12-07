from django.conf.urls import re_path
from django.contrib.auth.decorators import login_required

from trix.trix_student.views import dashboard, assignments, course, howsolved, \
    permalink, users, consent


urlpatterns = [
    re_path(r'^$', dashboard.CourseListView.as_view(), name='trix_student_dashboard'),
    re_path(r'^assignment/howsolved/(?P<assignment_id>\d+)$',
            login_required(howsolved.HowsolvedView.as_view()),
            name='trix_student_howsolved'),
    re_path(r'^assignments/(?P<assignment_ids>[\d+&*]+)$',
            assignments.AssignmentListView.as_view(),
            name='trix_assignments_view'),
    re_path(r'^course/(?P<course_id>\d+)$',
            course.CourseDetailView.as_view(),
            name='trix_student_course'),
    re_path(r'^permalink/(?P<permalink_id>\d+)$',
            permalink.PermalinkView.as_view(),
            name='trix_student_permalink'),
    re_path(r'^permalink/list/$',
            permalink.PermalinkListView.as_view(),
            name='trix_student_permalink_list_view'),
    re_path(r'^user/$',
            users.ProfilePageView.as_view(),
            name='trix_profile_page'),
    re_path(r'^user/delete/(?P<pk>\d+)$',
            users.UserDeleteView.as_view(),
            name="trix_delete_user"),
    re_path(r'^consent$',
            consent.ConsentFormView.as_view(),
            name='trix_consent_form'),
]
