from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from warmikuna_app.sendmail import send_forget_password_mail
from .forms import RegistroForm
from django.contrib import messages
from django.http import HttpResponse
from .models import Denuncia, Usuario
import uuid

# Create your views here.
def ingreso(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username = username, password = password)

            if user is not None:
                login(request, user)
                # fname = user.username
                return redirect('denuncia')
                # return render(request, "main/index.html", {'fname': fname})
            
            else: 
                messages.error(request, "¡Usuario o contraseña incorrectos!")
                return redirect('ingreso')
    else:
        return redirect('denuncia')

    return render(request, 'auth/ingreso.html')

def salir(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('ingreso')
    else:
        return redirect('denuncia')
    
def registro(request):
    errors = {}
    if request.user.is_anonymous:
        if request.method == "POST":
            form = RegistroForm(request.POST)
            if form.is_valid():
                username = form.clean_username("username")
                password = form.clean_password2("password1", "password2")
                form.save()
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request, user)
                    request.session['r_registro'] = True
                    return redirect('datos')
                return redirect('ingreso')
            else:
                errors = form.errors.as_json()
                print(form.errors.as_data())
    else: 
        return redirect('denuncia')

    form = RegistroForm()
    context = {"form": form, "errors": errors}
    return render(request, 'auth/registrar.html', context)

def denuncia(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get("tipo")=="1":
                user = Usuario.objects.get(user=request.user)
                fecha = request.POST.get("fecha")
                denunciado = request.POST.get("denunciado")
                descripcion = request.POST.get("descripcion")
                nueva_denuncia = Denuncia(user=user, fecha=fecha, denunciado=denunciado, descripcion=descripcion)
                nueva_denuncia.save()

            elif request.POST.get("tipo")=="2":
                fecha = request.POST.get("fecha")
                denunciado = request.POST.get("denunciado")
                descripcion = request.POST.get("descripcion")
                nueva_denuncia = Denuncia(fecha=fecha, denunciado=denunciado, descripcion=descripcion)
                nueva_denuncia.save()

    else:
        return redirect('ingreso')
                


    return render(request, 'main/denuncia.html')

def ingresar_datos(request):
    if request.user.is_authenticated:
        if 'r_registro' in request.session:
            if request.method == 'POST':
                user = request.user
                dni = request.POST.get("dni")
                nombre = request.POST.get("nombre")
                apellido = request.POST.get("apellido")
                numero = request.POST.get("numero")
                fnacim = request.POST.get("fnacim")

                if len(dni) != 8:
                    messages.error(request, "El DNI es incorrecto")
                    return redirect('datos')
                elif any(i.isnumeric() for i in nombre):
                    messages.error(request, "Nombre contiene números")
                    return redirect('datos')
                elif any(i.isnumeric() for i in apellido):
                    messages.error(request, "Apellido contiene números")
                    return redirect('datos')
                elif len(numero) != 9:
                    messages.error(request, "Número contiene menos de 9 dígitos")
                    return redirect('datos')
                usuario = Usuario.objects.get(user=user)
                usuario.dni = dni
                usuario.nombre = nombre
                usuario.apellido = apellido
                usuario.numero = numero
                usuario.fnacim = fnacim
                # nuevo_usuario = Usuario(user=user, dni=dni, nombre=nombre, apellido=apellido, numero=numero, fnacim=fnacim)
                usuario.save()

                del request.session['r_registro']
                return redirect('denuncia')
        else:
            return redirect('denuncia')
    else:
        return redirect('registro')

    return render(request, 'main/datos.html')

def olvidoContrasena(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username).first():
                messages.success(request, 'No eixste .')
                return redirect('password-forgot')
            
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            usuario_obj= Usuario.objects.get(user = user_obj)
            usuario_obj.passwordResetToken = token
            usuario_obj.save()
            send_forget_password_mail(user_obj.username , token)
            messages.success(request, 'Se envió el correo.')
            return redirect('password-forgot')
    
    except Exception as e:
        print(e)
    return render(request , 'auth/password-forgot.html')

def reestablecerContrasena(request, token):
    context = {}

    try:
        usuario_obj = Usuario.objects.filter(passwordResetToken = token).first()
        context = {'user_id' : usuario_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No se encontró id de usuario.')
                return redirect(f'password-reset/{token}/')
            
            if  new_password != confirm_password:
                messages.success(request, 'Contraseñas no coinciden.')
                return redirect(f'password-reset/{token}/')
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('ingreso')
            
    except Exception as e:
        print(e)
    return render(request , 'password-reset.html' , context)