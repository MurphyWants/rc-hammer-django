from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rc/<uuid:unique_id>', views.by_uuid, name='by_uuid'),
    path('new_car', views.new_car, name='new_car'),
    ]
