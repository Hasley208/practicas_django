from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), #Ruta para login
    path('home/', views.home, name='home'),  # Nueva ruta para el home
    path('logout/', views.logout_view, name='logout'),
    path('profesor/', views.profesor_view, name='profesor'),
    path('musico/', views.musico_view, name='musico')
]