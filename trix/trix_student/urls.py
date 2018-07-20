from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from trix.trix_student.views import login
from trix.trix_student.views import dashboard
from trix.trix_student.views import assignments
from trix.trix_student.views import course
from trix.trix_student.views import howsolved
from trix.trix_student.views import permalink
from trix.trix_admin.views.statistics import AssignmentStatsCsv

urlpatterns = [
    url('^$', dashboard.CourseListView.as_view(), name='trix_student_dashboard'),
    # url('^assignments/$', assignments.AssignmentListView.as_view(),
    #     name='trix_student_assignments'),
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
    # url(r'^statistics/ascsv$', AssignmentStatsCsv.as_view(), name='trix_stats_ascsv'),
    url(r'^login$', login.TrixLoginView.as_view(), name='trix-login'),
    url(r'^logout$',
        auth_views.logout,
        {'template_name': 'trix_student/logout.django.html'},
        name='trix-logout'),
]
