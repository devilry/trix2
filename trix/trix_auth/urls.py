from django.conf.urls import include, re_path
from trix.trix_auth.views import allauth_views, login

urlpatterns = [
    re_path(r'^login/$',
            login.TrixLoginView.as_view(),
            name='trix_login'),
    re_path(r'^logout/$',
            allauth_views.AllauthLogoutView.as_view(),
            name='trix_logout'),
    re_path(r'^allauth/login/$',
            allauth_views.AllauthLoginView.as_view(),
            name='account_login'),
    re_path(r'^allauth/logout/$',
            allauth_views.AllauthLogoutView.as_view(),
            name='account_logout'),
    re_path(r'^allauth/', include('allauth.urls')),
]
