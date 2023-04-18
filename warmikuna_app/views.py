from django.shortcuts import render

# Create your views here.
def login(request):
    return(render(request, 'auth/ingreso.html'))

def register(request):
    return(render(request, 'auth/registrar.html'))

def create_user(request):
    if request.method == 'POST':
        pass
    pass