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
    path('password-forgot', views.olvidoContrasena, name="password-forgot"),
    path('password-reset/<token>/', views.reestablecerContrasena, name="password-reset"),
    path('consulta', views.consultaDenuncias, name="consulta"),
    path('talleres', views.listadoCursos, name="talleres")
]