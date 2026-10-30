from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required  # Protege 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from utils import limpiar_texto
from django.http import JsonResponse, QueryDict
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from .models import Profesor

def index(request):
    # Si el formulario se envió con el botón (método POST)
    error = None
    if request.method == 'POST':
        usuario_req = request.POST.get('identifier', '').strip()
        clave_req = request.POST.get('password')
        
        
        user = authenticate(request, username=usuario_req, password=clave_req)
        
        if user is not None:
            login(request, user)  
            return redirect('home')  
        error = 'Usuario o contraseña incorrectos.'
            
    return render(request, "code.html", {"error": error})

@login_required 
def home(request):
    return render(request, "home.html") 

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('index')

def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirmacion = request.POST.get('password_confirm', '')
        error = None

        if not nombre or not email or not password or not confirmacion:
            error = 'Completa todos los campos para crear tu cuenta.'
        elif 'terms' not in request.POST:
            error = 'Debes aceptar los términos para crear tu cuenta.'
        elif password != confirmacion:
            error = 'Las contraseñas no coinciden.'
        else:
            try:
                validate_email(email)
            except ValidationError:
                error = 'Introduce una dirección de correo válida.'
            if error is None:
                User = get_user_model()
                if User.objects.filter(username__iexact=email).exists():
                    error = 'Ya existe una cuenta con ese correo.'
                else:
                    nuevo_usuario = User(
                        username=email,
                        email=email,
                        first_name=nombre,
                    )
                    try:
                        password_validation.validate_password(password, nuevo_usuario)
                    except ValidationError as validation_error:
                        error = ' '.join(validation_error.messages)
                    else:
                        nuevo_usuario.set_password(password)
                        nuevo_usuario.save()
                        login(request, nuevo_usuario)
                        return redirect('home')

        return render(request, "registro.html", {"error": error})

    return render(request, "registro.html")

  

"""def get (request):
    hola = "B I E N V E N I D O"
    texto = limpiar_texto(hola)
    return HttpResponse(texto.encode("utf-8"), content_type="text/plain")"""

@csrf_exempt
def profesor_view(request):
    print("-.--->", request.method)
    if request.method == "POST":
        print("Profesor......", request.POST)
        nombre = request.POST.get("nombre")
        especialidad = request.POST.get("especialidad")

        print(nombre, especialidad)
        profesor = Profesor.objects.create(nombre=nombre, especialidad=especialidad)
        print("Profesor creado:", profesor)

        return JsonResponse({"status": "ok", "profesor_name": profesor.nombre})
    if request.method == "GET":
        print(request.GET)
        profesor = Profesor.objects.filter(nombre=request.GET.get("nombre"))
        print(profesor)
        data = []
        for p in profesor:
            data.append({"nombre": p.nombre, "especialidad": p.especialidad})
        return JsonResponse({"status": "ok", "message": data})
    
    if request.method == "PUT":
        put_data = QueryDict(request.body)
        nombre = put_data.get("nombre")
        especialidad = put_data.get("especialidad")
        print("paso al put", nombre, especialidad)
        # Aquí podrías manejar la actualización de un profesor
        profesor = Profesor.objects.filter(nombre=nombre).first()
        print("---", profesor)
        if profesor:
            profesor.especialidad = especialidad
            profesor.save()
            return JsonResponse({"status": "ok", "message": "Profesor actualizado"})
        else:
            return JsonResponse(
                {"status": "error", "message": "Profesor no encontrado"}
            )

@csrf_exempt 
def musico_view(request):
    print("-.--->", request.method)
    if request.method == "POST":
        print("Músico......", request.POST)
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        instrument = request.POST.get("instrument")

        print(first_name, last_name, instrument)
        musico = Musician.objects.create(first_name=first_name, last_name=last_name, instrument=instrument)
        print("Músico creado:", musico)

        return JsonResponse({"status": "ok", "musico_name": musico.first_name})

    if request.method == "GET":
            print(request.GET)
            musico = Musician.objects.filter(first_name=request.GET.get("first_name"))
            print(musico)
            data = []
            for p in musico:
                data.append({"first_name": p.first_name, "last_name": p.last_name, "instrument": p.instrument})
            return JsonResponse({"status": "ok", "message": data})
    
    if request.method == "PUT":
        put_data = QueryDict(request.body)
        first_name = put_data.get("first_name")
        last_name = put_data.get("last_name")
        instrument = put_data.get("instrument")
        print("paso al put", first_name, last_name, instrument)
        # Aquí podrías manejar la actualización de un músico
        musico = Musician.objects.filter(first_name=first_name).first()
        print("---", musico)
        if musico:
            musico.last_name = last_name
            musico.instrument = instrument
            musico.save()
            return JsonResponse({"status": "ok", "message": "Músico actualizado"})
        else:
            return JsonResponse(
                {"status": "error", "message": "Músico   no encontrado"}
            )