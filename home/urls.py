from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path(r'login', auth_views.login),
    path(r'logout', auth_views.logout),
    path(r'Login', auth_views.login),
    path(r'Logout', auth_views.logout),
    path(r'register', views.register, name='register'),
    path(r'Register', views.register, name='Register'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
