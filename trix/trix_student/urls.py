from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from trix.trix_student.views import dashboard, assignments, course, howsolved, \
    permalink, users, consent, base


urlpatterns = [
    url('^$', dashboard.CourseListView.as_view(), name='trix_student_dashboard'),
    url('^assignment/howsolved/(?P<assignment_id>\d+)$',
        login_required(howsolved.HowsolvedView.as_view()),
        name='trix_student_howsolved'),
    url('^assignments/(?P<assignment_ids>[\d+&*]+)$',
        assignments.AssignmentListView.as_view(),
        name='trix_assignments_view'),
    url('^course/(?P<course_id>\d+)$',
        course.CourseDetailView.as_view(),
        name='trix_student_course'),
    url('^permalink/(?P<permalink_id>\d+)$',
        permalink.PermalinkView.as_view(),
        name='trix_student_permalink'),
    url('^permalink/list/$',
        permalink.PermalinkListView.as_view(),
        name='trix_student_permalink_list_view'),
    url('^user/$',
        users.ProfilePageView.as_view(),
        name='trix_profile_page'),
    url('^user/delete/(?P<pk>\d+)$',
        users.UserDeleteView.as_view(),
        name="trix_delete_user"),
    url(r'^consent$',
        consent.ConsentFormView.as_view(),
        name='trix_consent_form'),
    url(r'^wcag$', base.wcag_change, name="wcag")
]
