from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('<h1>Hola, esta es la pagina principal de encuestas!</h1')

# Create your views here.
