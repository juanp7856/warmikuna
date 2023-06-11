from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from warmikuna_app.sendmail import send_forget_password_mail
from .forms import RegistroForm
from django.contrib import messages
from django.http import HttpResponse
from .models import Denuncia, Usuario, Imagen, Taller, TallerXUsuario
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
                print("es invalido")
                print(form.errors.items())

                for error in form.errors.items():
                    messages.error(request, error[1])
                    print(error[1])
    else: 
        return redirect('denuncia')

    form = RegistroForm()
    context = {"form": form}
    return render(request, 'auth/registrar.html', context)

def denuncia(request):
    tamano_max = 5
    MEGABYTE = 1024 * 1024

    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get("tipo")=="1":
                user = Usuario.objects.get(user=request.user)
                fecha = request.POST.get("fecha")
                denunciado = request.POST.get("denunciado")
                descripcion = request.POST.get("descripcion")
                imagenes = request.FILES.getlist('evidencia')
                nueva_denuncia = Denuncia(user=user, fecha=fecha, denunciado=denunciado, descripcion=descripcion)
                nueva_denuncia.save()

                for i in imagenes:
                    if i.size > tamano_max * MEGABYTE:
                        messages.error(request, 'Uno de los archivos excede el peso límite de 5MB')
                        return redirect('denuncia')

                    nuevaImagen = Imagen(denuncia=nueva_denuncia, imagen=i)
                    nuevaImagen.save()

                messages.success(request, 'Denuncia enviada')
                return redirect('denuncia')

            elif request.POST.get("tipo")=="2":
                fecha = request.POST.get("fecha")
                denunciado = request.POST.get("denunciado")
                descripcion = request.POST.get("descripcion")
                id_anonimo = str(uuid.uuid4())
                nueva_denuncia = Denuncia(fecha=fecha, denunciado=denunciado, descripcion=descripcion, id_anonimo=id_anonimo)
                nueva_denuncia.save()

                messages.success(request, f'Denuncia enviada, tu ID para la consulta es: {id_anonimo}')
                return redirect('denuncia')


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
                messages.success(request, 'No existe ese usuario.')
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
    return render(request , 'auth/recuperar_contrasena.html')

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
    return render(request , 'auth/reestablecer_contrasena.html' , context)

def consultaDenuncias(request):
    context = {}

    if request.user.is_authenticated:
        user = request.user
        usuario = Usuario.objects.get(user=user)
        denuncias = Denuncia.objects.filter(user=usuario)
        context = {'denuncias': denuncias}

        if request.method == 'POST':
            try:
                id = request.POST.get('id')
                denunciaBuscada = Denuncia.objects.get(id_anonimo=id)
                context = {'denuncias': denuncias, 'denunciabuscada': denunciaBuscada}
                
                return render(request, 'main/consulta.html', context)
            except Exception as e:
                messages.error(request, 'No existe esa ID de denuncia')
                return redirect('consulta')
            
    else:
        return redirect('ingreso')
    
    return render(request, 'main/consulta.html', context)
    

def listadoCursos(request):
    talleres = Taller.objects.all()
    context = {'talleres': talleres}

    if request.method=="POST":
        try:
            user = request.user
            taller_id = request.POST.get('taller_id')
            usuario = Usuario.objects.get(user=user)
            taller = Taller.objects.get(id=taller_id)
            nueva_inscripcion = TallerXUsuario(user=usuario, taller=taller)
            nueva_inscripcion.save()

            

        except Exception as e:
            return redirect('ingreso')

    return render(request, 'main/curso.html', context)