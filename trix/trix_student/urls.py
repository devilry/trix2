from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from trix.trix_student.views import dashboard
from trix.trix_student.views import assignments
from trix.trix_student.views import course
from trix.trix_student.views import howsolved

urlpatterns = patterns('trix',
    url('^$', dashboard.CourseListView.as_view(), name='trix_student_dashboard' ),
    url('^assignments/$', assignments.AssignmentListView.as_view(), name='trix_student_assignments'),
    url('^assignment/howsolved/(?P<assignment_id>\d+)$',
        login_required(howsolved.HowsolvedView.as_view()),
        name='trix_student_howsolved'),
    url('^course/(?P<course_id>\d+)$', course.CourseDetailView.as_view(), name='trix_student_course'),
    url('^permalink/(?P<permalink_id>\d+)$', course.PermalinkView.as_view(), name='trix_student_permalink'),
    url(r'^login$', 'trix_student.views.login.loginview', name='trix-login'),
    url(r'^logout$', 'trix_student.views.logout.logoutview', name='trix-logout'),
)