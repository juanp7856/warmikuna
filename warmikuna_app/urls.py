from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name="ingreso"),
    path('registro', views.register, name="registro"),
]