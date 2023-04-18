from django.urls import path

from . import views

urlpatterns = [
    path('', views.ingreso, name="ingreso"),
    path('registro', views.registro, name="registro"),
]