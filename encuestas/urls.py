from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), #Ruta para login
    path('home/', views.home, name='home'),  # Nueva ruta para el home
]