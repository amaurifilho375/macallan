from django.urls import path
from . import views

urlpatterns = [
    path('', views.macallan_form, name='macallan_form'),
    path('success/', views.macallan_success, name='macallan_success'),
]
