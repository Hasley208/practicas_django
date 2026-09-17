from django.shortcuts import render
from django.http import HttpResponse
from utils import limpiar_texto

def index(request):
    return render(request,"code.html",{})

"""def get (request):
    hola = "B I E N V E N I D O"
    texto = limpiar_texto(hola)
    return HttpResponse(texto.encode("utf-8"), content_type="text/plain")"""

# Create your views here.
