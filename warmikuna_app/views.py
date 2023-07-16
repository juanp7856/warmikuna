from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import folium
from funciones.get_coordenadas import get_coordenadas
from funciones.val_datos import valdatos
from funciones.val_reset import valreset
from patron_diseno.fabricaabstracta.fabricaAbstractaDenunciaAnonimo import FabricaDenunciaAnonima
from patron_diseno.fabricaabstracta.fabricaAbstractaDenunciaDatos import FabricaDenunciaDatos
from warmikuna_app.sendmail import send_forget_password_mail
from .forms import RegistroForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Denuncia, Usuario, Imagen, Taller, TallerXUsuario
import uuid
from django.db.models import Count
from folium.plugins import HeatMap

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
    is_colorblind = request.session.get('colorblind_mode', False)

    context = {'is_colorblind_mode': is_colorblind}

    if request.user.is_authenticated:
        if request.method == "POST":
            fecha = request.POST.get("fecha")
            denunciado = request.POST.get("denunciado")
            descripcion = request.POST.get("descripcion")
            imagenes = request.FILES.getlist('evidencia')
            motivo = request.FILES.get("motivo")
            
            if request.POST.get("tipo")=="1":
                user = Usuario.objects.get(user=request.user)

                fabricaDatos = FabricaDenunciaDatos()

                if(motivo == "1"):
                    denuncia = fabricaDatos.crearDenunciaAbuso()
                elif(motivo == "2"):
                    denuncia = fabricaDatos.crearDenunciaAcoso()
                else:
                    denuncia = fabricaDatos.crearDenunciaMaltrato()

                nueva_denuncia = denuncia.guardarDenuncia(user,descripcion,denunciado,fecha)
                denuncia.guardarImagenes(imagenes,nueva_denuncia)

                messages.success(request, 'Denuncia enviada')
                return redirect('denuncia')

            elif request.POST.get("tipo")=="2":
                fabricaAnonima = FabricaDenunciaAnonima()

                if(motivo == "1"):
                    denuncia = fabricaAnonima.crearDenunciaAbuso()
                elif(motivo == "2"):
                    denuncia = fabricaAnonima.crearDenunciaAcoso()
                else:
                    denuncia = fabricaAnonima.crearDenunciaMaltrato()
                
                denuncia.crearID()
                nueva_denuncia = denuncia.guardarDenuncia(None,descripcion,denunciado,fecha)
                denuncia.guardarImagenes(imagenes,nueva_denuncia)

                id_anonimo = denuncia.getID()

                messages.success(request, f'Denuncia enviada, tu ID para la consulta es: {id_anonimo}')
                return redirect('denuncia')
    else:
        return redirect('ingreso')
        
    return render(request, 'main/denuncia.html', context)

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
                
                error = valdatos(dni, nombre, apellido,numero)
                if(error != ""):
                    messages.error(request, error)
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
            
            error = valreset(user_id, new_password, confirm_password)

            if(error != ""):
                messages.error(request, error)
                return redirect(f'password-reset/{token}/')

            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('ingreso')
            
    except Exception as e:
        print(e)
    return render(request , 'auth/reestablecer_contrasena.html' , context)

def consultaDenuncias(request):
    is_colorblind = request.session.get('colorblind_mode', False)

    if request.user.is_authenticated:
        user = request.user
        usuario = Usuario.objects.get(user=user)
        denuncias = Denuncia.objects.filter(user=usuario)
        context = {'denuncias': denuncias, 'is_colorblind_mode': is_colorblind}

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
    is_colorblind = request.session.get('colorblind_mode', False)

    for taller in talleres:
        suscrito = False
        if request.user.is_authenticated:

            usuario = request.user
            usuarioObj = Usuario.objects.get(user=usuario)

            if TallerXUsuario.objects.filter(user=usuarioObj, taller_id=taller.id).exists():
                suscrito = True
        taller.suscrito = suscrito

    context = {'talleres': talleres, 'is_colorblind_mode': is_colorblind}

    if request.method == "POST":
        if 'subbutton' in request.POST:
            if request.user.is_authenticated:
                taller_id = request.POST.get('taller_id')
                usuario = request.user
                usuarioObj = Usuario.objects.get(user=usuario)

                try:
                    registro = TallerXUsuario.objects.get(user=usuarioObj, taller_id=taller_id)
                    registro.delete()
                except TallerXUsuario.DoesNotExist:
                    nuevo_registro = TallerXUsuario(user=usuarioObj, taller_id=taller_id)
                    nuevo_registro.save()
            else:
                return redirect('ingreso')
            return redirect('talleres')
        
        elif 'combutton' in request.POST:
            taller_id = request.POST.get('taller_id')
            comentario = request.POST.get('comentario')
            usuario = request.user
            usuarioObj = Usuario.objects.get(user=usuario)
            print(taller_id, comentario, usuario)
            tallerx = TallerXUsuario.objects.get(user=usuarioObj, taller_id=taller_id)
            tallerx.comentario = comentario
            tallerx.save()

    return render(request, 'main/curso.html', context)


def toggle_colorblind_mode(request):
    if 'colorblind_mode' in request.session:
        del request.session['colorblind_mode']
    else:
        request.session['colorblind_mode'] = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def generar_mapa(request):
    is_colorblind = request.session.get('colorblind_mode', False)

    peru_map = folium.Map(location=[-9.189967, -75.015152], zoom_start=6)

    departamentos_mas_comunes = Denuncia.objects.values('departamento').annotate(total=Count('departamento')).order_by('-total')[:10]

    datos_heatmap = []

    for departamento in departamentos_mas_comunes:
        coordenadas = get_coordenadas(departamento['departamento'])
        datos_heatmap.append(coordenadas + [departamento['total']])

    HeatMap(data=datos_heatmap, radius=15, blur=20, gradient={0.2: 'blue', 0.4: 'cyan', 0.6: 'lime', 0.8: 'yellow', 1: 'red'}).add_to(peru_map)

    mapa_html = peru_map._repr_html_()
    return render(request, 'main/index.html', {'mapa_html': mapa_html, 'is_colorblind_mode': is_colorblind})

def faq(request):
    is_colorblind = request.session.get('colorblind_mode', False)

    return render(request, 'main/faq.html', {'is_colorblind_mode': is_colorblind})