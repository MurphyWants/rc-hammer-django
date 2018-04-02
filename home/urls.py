from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path(r'login$', auth_views.login),
    path(r'logout$', auth_views.logout),
    path(r'Login$', auth_views.login),
    path(r'Logout$', auth_views.logout),
    path(r'register$', views.register, name='register'),
    path(r'Register$', views.register, name='Register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
