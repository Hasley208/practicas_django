from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required  # Protege 
from django.contrib.auth import authenticate, login
from utils import limpiar_texto

def index(request):
    # Si el formulario se envió con el botón (método POST)
    error = None
    if request.method == 'POST':
        usuario_req = request.POST.get('username')
        clave_req = request.POST.get('password')
        
        
        user = authenticate(request, username=usuario_req, password=clave_req)
        
        if user is not None:
            login(request, user)  # Inicia la sesión oficialmente en Django
            return redirect('home')  # Te lleva al Home automáticamente
        error = 'Usuario o contraseña incorrectos.'
            
    return render(request, "code.html", {"error": error})

@login_required  # Si no han iniciado sesión, Django los rebota
def home(request):
    return render(request, "home.html") 

"""def get (request):
    hola = "B I E N V E N I D O"
    texto = limpiar_texto(hola)
    return HttpResponse(texto.encode("utf-8"), content_type="text/plain")"""

# Create your views here.

