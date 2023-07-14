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
    passwordResetToken = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.user.username

class Denuncia(models.Model):
    ESTADOS = [
        ("Enviado", "Enviado"),
        ("En investigación", "En investigación"),
        ("Archivado", "Archivado"),
        ("Cerrado", "Cerrado"),
        ("Requiere más datos", "Requiere más datos")
    ]

    MOTIVO = [
        ("Abuso", "Abuso"),
        ("Acoso", "Acoso"),
        ("Maltrato", "Maltrato")
    ]

    DEPARTAMENTOS = [
        ("Lima", "Lima"),
        ("Arequipa", "Arequipa"),
        ("Cusco", "Cusco"),
        ("La Libertad", "La Libertad"),
        ("Piura", "Piura"),
        ("Lambayeque", "Lambayeque"),
        ("Junín", "Junín"),
        ("Puno", "Puno"),
        ("Ancash", "Ancash"),
        ("Ica", "Ica"),
        ("Tacna", "Tacna"),
        ("Loreto", "Loreto"),
        ("Ucayali", "Ucayali"),
        ("San Martín", "San Martín"),
        ("Madre de Dios", "Madre de Dios"),
        ("Amazonas", "Amazonas"),
        ("Pasco", "Pasco"),
        ("Huancavelica", "Huancavelica"),
        ("Ayacucho", "Ayacucho"),
        ("Tumbes", "Tumbes"),
        ("Moquegua", "Moquegua"),
        ("Huánuco", "Huánuco"),
        ("Apurímac", "Apurímac"),
        ("Cajamarca", "Cajamarca"),
        ("Callao", "Callao"),
        ("Iquitos", "Iquitos"),
    ]

    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    descripcion = models.CharField(max_length=500)
    denunciado = models.CharField(max_length=40)
    departamento = models.CharField(choices=DEPARTAMENTOS, max_length=50, default="Lima")
    fecha = models.DateField(null=True)
    id_anonimo = models.CharField(null=True, blank=True, max_length=100)
    estado = models.CharField(choices=ESTADOS, max_length=20, default="Enviado")
    motivo = models.CharField(choices=MOTIVO, max_length=20, default="Abuso")

    def __str__(self):
        return 'Denunciado: {}'.format(self.denunciado)
    

class Imagen(models.Model):
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE, null=True)
    imagen = models.ImageField(null=True, blank=True, upload_to='images/') 

class Taller(models.Model):
    video = models.URLField(null=True, blank=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.titulo)
    
class TallerXUsuario(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=500, null=True)
    taller = models.ForeignKey(Taller, on_delete=models.CASCADE)


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