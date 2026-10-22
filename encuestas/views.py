from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required  # Protege 
from django.contrib.auth import authenticate, login, logout
from utils import limpiar_texto
from django.http import JsonResponse, QueryDict
import json

from django.views.decorators.csrf import csrf_exempt
from .models import Profesor

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

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('index')

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
