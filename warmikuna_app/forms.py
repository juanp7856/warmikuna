from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'type': 'text',
            'id' : 'username',
            'name' : 'username',
            'placeholder' : 'Correo Electronico'
        })
        self.fields["password1"].widget.attrs.update({
            'type': 'text',
            'id' : 'password1',
            'name' : 'password1',
            'placeholder' : 'Contraseña'
        })
        self.fields["password2"].widget.attrs.update({
            'type': 'text',
            'id' : 'password2',
            'name' : 'password2',
            'placeholder' : 'Confirmar contraseña'
        })

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get("username")

        if not ("@" and ".") in username:
            raise forms.ValidationError("No es un correo")
        
        return username
    
    def clean_password2(self, *args, **kwargs):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Contraseñas no coinciden")
        elif len(password1) <8:
            raise forms.ValidationError("Contraseña muy corta")
        elif password1.isnumeric():
            raise forms.ValidationError("Contraseña solo contiene números")
        
        return password2
        




