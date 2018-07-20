from django.conf.urls import include, url
from django.contrib import admin

from trix.trix_admin.cradmin import CrAdminInstance
from trix.trix_student import urls


admin.autodiscover()

default_urls = [
    url(r'^admin/', admin.site.urls),
    url(r'^a/', include(CrAdminInstance.urls())),
    url(r'^', include(urls.urlpatterns)),
]
