from gettext import translation
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import folium
from funciones.get_coordenadas import get_coordenadas
from funciones.get_dep import get_dep
from funciones.val_datos import valdatos
from funciones.val_reset import valreset
from patron_diseno.fabricaabstracta.fabricaAbstractaDenunciaAnonimo import FabricaDenunciaAnonima
from patron_diseno.fabricaabstracta.fabricaAbstractaDenunciaDatos import FabricaDenunciaDatos
from warmikuna import settings
from warmikuna_app.sendmail import send_forget_password_mail
from .forms import RegistroForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Denuncia, Usuario, Imagen, Taller, TallerXUsuario
import uuid
from django.db.models import Count
from folium.plugins import HeatMap
from django.utils.translation import gettext_lazy as _
from django.utils.translation import activate, get_language

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
    
    context = {
        'Iniciar sesión': _('Iniciar sesión'),
        'No tienes una cuenta': _('No tienes una cuenta'),
        'Regístrate': _('Regístrate'),
        'Olvidaste tu contraseña': _('Olvidaste tu contraseña')
    }

    return render(request, 'auth/ingreso.html', context)

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
    context = {
        'form': form,
        'Registro': _('Registro'),
        'Registrate': _('Registrate'),
        'Ya tienes una cuenta': _('Ya tienes una cuenta'),
        'Iniciar Sesion': _('Iniciar Sesion')
    }
    return render(request, 'auth/registrar.html', context)

def denuncia(request):
    is_colorblind = request.session.get('colorblind_mode', False)
    print(_("Texto a traducir"))

    context = {
        'is_colorblind_mode': is_colorblind,
        'Denunciar': _('Denunciar'),
        'Tipo de denuncia': _('Tipo de denuncia'),
        'Con datos': _('Con datos'),
        'Anónima': _('Anónima'),
        'Motivo': _('Motivo'),
        'Abuso': _('Abuso'),
        'Acoso': _('Acoso'),
        'Maltrato': _('Maltrato'),
        'Regresar': _('Regresar'),
        'Inicio': _('Inicio'),
        'Realizar denuncia': _('Realizar denuncia'),
        'Cursos y Talleres': _('Cursos y Talleres'),
        'Consultas': _('Consultas'),
        'Preguntas frecuentes': _('Preguntas frecuentes'),
        'Lenguaje': _('Lenguaje'),
        'Quitar modo daltónico': _('Quitar modo daltónico'),
        'Modo daltónico': _('Modo daltónico'),
        'Cerrar sesión': _('Cerrar sesión')
    }

    if request.user.is_authenticated:
        if request.method == "POST":
            fecha = request.POST.get("fecha")
            denunciado = request.POST.get("denunciado")
            descripcion = request.POST.get("descripcion")
            imagenes = request.FILES.getlist('evidencia')
            motivo = request.POST.get("motivo")
            id = request.POST.get("departamento")
            departamento = get_dep(id)

            
            if request.POST.get("tipo")=="1":
                user = Usuario.objects.get(user=request.user)

                fabricaDatos = FabricaDenunciaDatos()

                if(motivo == "1"):
                    denuncia = fabricaDatos.crearDenunciaAbuso()
                elif(motivo == "2"):
                    denuncia = fabricaDatos.crearDenunciaAcoso()
                else:
                    denuncia = fabricaDatos.crearDenunciaMaltrato()

                nueva_denuncia = denuncia.guardarDenuncia(user,descripcion,denunciado,fecha,departamento)
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
                nueva_denuncia = denuncia.guardarDenuncia(None,descripcion,denunciado,fecha,departamento)
                denuncia.guardarImagenes(imagenes,nueva_denuncia)

                id_anonimo = denuncia.getID()

                messages.success(request, f'Denuncia enviada, tu ID para la consulta es: {id_anonimo}')
                return redirect('denuncia')
    else:
        return redirect('ingreso')
        
    return render(request, 'main/denuncia.html', context)

def ingresar_datos(request):
    is_colorblind = request.session.get('colorblind_mode', False)

    context = {
        'is_colorblind_mode': is_colorblind,
        'Datos': _('Datos'),
        'Datos personales': _('Datos personales')
    }

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

    return render(request, 'main/datos.html', context)

def olvidoContrasena(request):
    is_colorblind = request.session.get('colorblind_mode', False)

    context = {
        'is_colorblind_mode': is_colorblind,
        'Recuperar Contraseña': _('Recuperar Contraseña'),
        'Enviar': _('Enviar'),
        'Volver al inicio de sesión': _('Volver al inicio de sesión')
    }

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
    return render(request , 'auth/recuperar_contrasena.html', context)

def reestablecerContrasena(request, token):
    is_colorblind = request.session.get('colorblind_mode', False)

    try:
        usuario_obj = Usuario.objects.filter(passwordResetToken = token).first()
        context = {
            'user_id' : usuario_obj.user.id,
            'is_colorblind_mode': is_colorblind,
            'Reestablecer Contraseña': _('Reestablecer Contraseña'),
            'Reestablecer': _('Reestablecer'),
            'Volver al inicio de sesión': _('Volver al inicio de sesión')
        }

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
        context = {
            'denuncias': denuncias, 
            'is_colorblind_mode': is_colorblind,
            'Estado de Denuncia': _('Estado de Denuncia'),
            'Aquí puedes consultar en que estado se encuentran tus denuncias': _('Aquí puedes consultar en que estado se encuentran tus denuncias'),
            'Fecha': _('Fecha'),
            'Estado': _('Estado'),
            'Denunciado': _('Denunciado'),
            'Inicio': _('Inicio'),
            'Realizar denuncia': _('Realizar denuncia'),
            'Cursos y Talleres': _('Cursos y Talleres'),
            'Consultas': _('Consultas'),
            'Preguntas frecuentes': _('Preguntas frecuentes'),
            'Lenguaje': _('Lenguaje'),
            'Quitar modo daltónico': _('Quitar modo daltónico'),
            'Modo daltónico': _('Modo daltónico'),
            'Cerrar sesión': _('Cerrar sesión')
            }

        if request.method == 'POST':
            try:
                id = request.POST.get('id')
                denunciaBuscada = Denuncia.objects.get(id_anonimo=id)
                context = {
                    'denuncias': denuncias, 
                    'is_colorblind_mode': is_colorblind,
                    'denunciabuscada': denunciaBuscada,
                    'Estado de Denuncia': _('Estado de Denuncia'),
                    'Aquí puedes consultar en que estado se encuentran tus denuncias': _('Aquí puedes consultar en que estado se encuentran tus denuncias'),
                    'Fecha': _('Fecha'),
                    'Estado': _('Estado'),
                    'Denunciado': _('Denunciado'),
                    'Inicio': _('Inicio'),
                    'Realizar denuncia': _('Realizar denuncia'),
                    'Cursos y Talleres': _('Cursos y Talleres'),
                    'Consultas': _('Consultas'),
                    'Preguntas frecuentes': _('Preguntas frecuentes'),
                    'Lenguaje': _('Lenguaje'),
                    'Quitar modo daltónico': _('Quitar modo daltónico'),
                    'Modo daltónico': _('Modo daltónico'),
                    'Cerrar sesión': _('Cerrar sesión')
                }
                
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

    context = {
        'talleres': talleres, 
        'is_colorblind_mode': is_colorblind,
        'Talleres disponibles': _('Talleres disponibles'),
        'Desuscribirse': _('Desuscribirse'),
        'Suscribirse': _('Suscribirse'),
        'Comentario': _('Comentario'),
        'Enviar': _('Enviar'),
        'Inicio': _('Inicio'),
        'Realizar denuncia': _('Realizar denuncia'),
        'Cursos y Talleres': _('Cursos y Talleres'),
        'Consultas': _('Consultas'),
        'Preguntas frecuentes': _('Preguntas frecuentes'),
        'Lenguaje': _('Lenguaje'),
        'Quitar modo daltónico': _('Quitar modo daltónico'),
        'Modo daltónico': _('Modo daltónico'),
        'Cerrar sesión': _('Cerrar sesión')
    }

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

    context = {
        'mapa_html': mapa_html,
        'is_colorblind_mode': is_colorblind,
        'Mapa de calor': _('Mapa de calor'),
        'Denuncias por departamento': _('Denuncias por departamento'),
        'Inicio': _('Inicio'),
        'Realizar denuncia': _('Realizar denuncia'),
        'Cursos y Talleres': _('Cursos y Talleres'),
        'Consultas': _('Consultas'),
        'Preguntas frecuentes': _('Preguntas frecuentes'),
        'Lenguaje': _('Lenguaje'),
        'Quitar modo daltónico': _('Quitar modo daltónico'),
        'Modo daltónico': _('Modo daltónico'),
        'Cerrar sesión': _('Cerrar sesión')
    }

    return render(request, 'main/index.html', context)

def faq(request):

    is_colorblind = request.session.get('colorblind_mode', False)

    context = {
        'is_colorblind_mode': is_colorblind,
        'Preguntas frecuentes': _('Preguntas frecuentes'),
        '¿Cuáles son las acciones que el MIMP está tomando para prevenir y combatir la violencia de género?': _('¿Cuáles son las acciones que el MIMP está tomando para prevenir y combatir la violencia de género?'),
        'El MIMP está implementando diversas acciones para prevenir y combatir la violencia de género. Esto incluye la sensibilización y educación en temas de igualdad y prevención de la violencia, así como la promoción de normativas y políticas para proteger a las víctimas y sancionar a los agresores.': _('El MIMP está implementando diversas acciones para prevenir y combatir la violencia de género. Esto incluye la sensibilización y educación en temas de igualdad y prevención de la violencia, así como la promoción de normativas y políticas para proteger a las víctimas y sancionar a los agresores.'),
        '¿Qué servicios de atención y apoyo brinda el MIMP a las mujeres víctimas de violencia?': _('¿Qué servicios de atención y apoyo brinda el MIMP a las mujeres víctimas de violencia?'),
        'El MIMP brinda servicios de atención integral a las mujeres víctimas de violencia a través de los Centros de Emergencia Mujer (CEM) y las Casas de Acogida. Estos lugares proporcionan asistencia legal, atención psicológica, asesoría y acompañamiento durante el proceso de recuperación.': _('El MIMP brinda servicios de atención integral a las mujeres víctimas de violencia a través de los Centros de Emergencia Mujer (CEM) y las Casas de Acogida. Estos lugares proporcionan asistencia legal, atención psicológica, asesoría y acompañamiento durante el proceso de recuperación.'),
        '¿Cómo se puede denunciar casos de violencia contra la mujer? A parte de la web WARMIKUNA ¿Qué acciones toma el MIMP al recibir una denuncia?': _('¿Cómo se puede denunciar casos de violencia contra la mujer? A parte de la web WARMIKUNA ¿Qué acciones toma el MIMP al recibir una denuncia?'),
        'El MIMP cuenta con la Línea 100, donde se pueden realizar denuncias de violencia contra la mujer de manera confidencial y recibir orientación sobre los pasos a seguir. Al recibir una denuncia, el MIMP coordina con las autoridades competentes para brindar la protección necesaria a la víctima y tomar las acciones legales correspondientes contra el agresor.': _('El MIMP cuenta con la Línea 100, donde se pueden realizar denuncias de violencia contra la mujer de manera confidencial y recibir orientación sobre los pasos a seguir. Al recibir una denuncia, el MIMP coordina con las autoridades competentes para brindar la protección necesaria a la víctima y tomar las acciones legales correspondientes contra el agresor.'),
        '¿Qué medidas se están implementando para garantizar la seguridad de las mujeres en espacios públicos?': _('¿Qué medidas se están implementando para garantizar la seguridad de las mujeres en espacios públicos?'),
        'El MIMP está trabajando en la implementación de políticas y programas para garantizar la seguridad de las mujeres en espacios públicos. Esto incluye la promoción de entornos seguros, la instalación de sistemas de vigilancia, el fortalecimiento de la iluminación y la capacitación de personal de seguridad en enfoques de género.': _('El MIMP está trabajando en la implementación de políticas y programas para garantizar la seguridad de las mujeres en espacios públicos. Esto incluye la promoción de entornos seguros, la instalación de sistemas de vigilancia, el fortalecimiento de la iluminación y la capacitación de personal de seguridad en enfoques de género.'),
        '¿Qué programas y campañas se están llevando a cabo para concientizar sobre la violencia de género?': '¿Qué programas y campañas se están llevando a cabo para concientizar sobre la violencia de género?',
        'El MIMP desarrolla diversas campañas de sensibilización y prevención sobre la violencia de género, como Ni una menos y 16 días de activismo contra la violencia de género. Además, se promueven programas educativos en escuelas y comunidades para generar conciencia sobre la importancia de la igualdad y el respeto.': _('El MIMP desarrolla diversas campañas de sensibilización y prevención sobre la violencia de género, como Ni una menos y 16 días de activismo contra la violencia de género. Además, se promueven programas educativos en escuelas y comunidades para generar conciencia sobre la importancia de la igualdad y el respeto.'),
        'Inicio': _('Inicio'),
        'Realizar denuncia': _('Realizar denuncia'),
        'Cursos y Talleres': _('Cursos y Talleres'),
        'Consultas': _('Consultas'),
        'Preguntas frecuentes': _('Preguntas frecuentes'),
        'Lenguaje': _('Lenguaje'),
        'Quitar modo daltónico': _('Quitar modo daltónico'),
        'Modo daltónico': _('Modo daltónico'),
        'Cerrar sesión': _('Cerrar sesión')
    }

    return render(request, 'main/faq.html', context)

# def cambiar_idioma(request):
#     if request.method == "POST":
#         nuevo_idioma = request.POST.get('idioma')

#         del request.session[settings.LANGUAGE_SESSION_KEY]

#         # translation.activate(nuevo_idioma)
#         # request.session[settings.LANGUAGE_SESSION_KEY] = nuevo_idioma

#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def cambiar_idioma(request):
    if request.method == 'POST':
        idioma = request.POST.get('idioma')
        if idioma in [lang_code for lang_code, _ in settings.LANGUAGES]:
            request.session[settings.LANGUAGE_SESSION_KEY] = idioma
            activate(idioma)
    return redirect(request.META.get('HTTP_REFERER', '/'))