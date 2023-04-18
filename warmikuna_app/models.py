from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.IntegerField(null=True)
    nombre = models.CharField(null=True, max_length=20)
    apellido = models.CharField(null=True, max_length=20)
    numero = models.CharField(null=True, max_length=9)
    fnacim = models.DateField(null=True)

    def __str__(self):
        return self.user.username

class Denuncia(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    descripcion = models.CharField(max_length=500)
    denunciado = models.CharField(max_length=40)
    imagenes = models.ImageField(null=True, blank=True, upload_to='images/') 


@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create(user=instance)
    else:
        return

@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
    # instance.usuario.save()
    return