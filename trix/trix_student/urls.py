from django.conf.urls import patterns, include, url
from trix.trix_student.views import dashboard
from trix.trix_student.views import assignments

urlpatterns = patterns('trix',
    url('^$', dashboard.CourseListView.as_view(), name='trix_student_dashboard' ),
    url('^assignments/$', assignments.AssignmentListView.as_view(), name='trix_student_assignments')


    )