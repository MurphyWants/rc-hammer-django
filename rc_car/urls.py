from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rc/<uuid:unique_id>', views.by_uuid, name='by_uuid'),
    path('new_car', views.new_car, name='new_car'),
    path('rc/<uuid:unique_id>/edit/', views.edit_car, name='edit_car'),
    path('rc/<uuid:unique_id>/change_password/', views.change_password, name='change_password'),
    path('api/owned_cars/', views.RC_Car_ViewSet_Owned_by, name='api_owned_cars'),
    ]
