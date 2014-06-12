from django.conf.urls import patterns, include, url
from trix.trix_student.views import dashboard

urlpatterns = patterns('trix',
    url('^$', dashboard.CourseListView.as_view(), name='trix_student_dashboard' )


    )