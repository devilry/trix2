from django.conf.urls import include, url
from django.contrib import admin

# from trix.trix_admin.cradmin import CrAdminInstance


admin.autodiscover()

default_urls = [
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^a/', include(CrAdminInstance.urls())),
    #url(r'^$', HomepageView.as_view(), name='lokalt_home'),
]