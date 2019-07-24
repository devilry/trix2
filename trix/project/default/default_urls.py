from django.conf.urls import include, url
from django.contrib import admin

from trix.trix_admin.cradmin import CrAdminInstance

admin.autodiscover()

default_urls = [
    url(r'^authenticate/', include('trix.trix_auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^c/', include('trix.trix_course.urls')),
    url(r'^a/', include(CrAdminInstance.urls())),
    url(r'^', include('trix.trix_student.urls')),
]
