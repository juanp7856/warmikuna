from django.forms import ModelForm
from django.contrib.auth.models import User

class Registro(ModelForm):
    class Meta:
        model = User
        

