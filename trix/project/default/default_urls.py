from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

from trix.trix_admin.cradmin import CrAdminInstance

admin.autodiscover()

default_urls = [
    url(r'^authenticate/', include('trix.trix_auth.urls')),
    url(r'^student/', include(urls.urlpatterns)),
    url(r'^course/', include('trix.trix_course.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^a/', include(CrAdminInstance.urls())),
    url(r'^$', RedirectView.as_view(pattern_name='trix_student_dashboard')),
]
