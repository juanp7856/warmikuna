from django.urls import path
from django.contrib.auth.views import LogoutView

from warmikuna import settings

from . import views

urlpatterns = [
    path('login', views.ingreso, name="ingreso"),
    path('registro', views.registro, name="registro"),
    path('logout', views.salir, name="salir"),
    path('', views.denuncia, name="denuncia"),
    path('datos', views.ingresar_datos, name="datos"),
]