from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Usuario)
admin.site.register(models.Denuncia)
admin.site.register(models.Imagen)
admin.site.register(models.Taller)
admin.site.register(models.TallerXUsuario)