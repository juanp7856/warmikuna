from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def ingreso(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            render(request, 'auth/registrar.html')
        
        else: 
            messages.error(request, "¡Usuario o contraseña incorrectos!")

    return(render(request, 'auth/ingreso.html'))

def registro(request):


    return(render(request, 'auth/registrar.html'))
