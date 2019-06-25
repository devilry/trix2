from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from trix.trix_auth.views import allauth_views, login


urlpatterns = [
    url('^login/$',
        login.TrixLoginView.as_view(),
        name='trix_login'),
    url('^logout/$',
        allauth_views.AllauthLogoutView.as_view(),
        name='trix_logout'),
    url('^allauth/login/$',
        allauth_views.AllauthLoginView.as_view(),
        name='account_login'),
    url('^allauth/logout/$',
        allauth_views.AllauthLogoutView.as_view(),
        name='account_logout'),
    url('^allauth/', include('allauth.urls')),
]
