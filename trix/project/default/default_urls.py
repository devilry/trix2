from django.conf.urls import include, re_path
from django.contrib import admin

from trix.trix_admin.cradmin import CrAdminInstance

admin.autodiscover()

default_urls = [
    re_path(r'^authenticate/', include('trix.trix_auth.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^c/', include('trix.trix_course.urls')),
    re_path(r'^a/', include(CrAdminInstance.urls())),
    re_path(r'^', include('trix.trix_student.urls')),
]
