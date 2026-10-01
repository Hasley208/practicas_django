from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


# ==========================================
# 1. ONE-TO-ONE (Uno a Uno)
# ==========================================
# Regla: 1 Usuario tiene exactamente 1 Perfil. 1 Perfil pertenece a 1 solo Usuario.
class PerfilEstudiante(models.Model):
    # La relación OneToOne asegura que no haya dos perfiles apuntando al mismo User
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="perfil"
    )
    codigo_expediente = models.CharField(max_length=10, unique=True)
    biografia = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario}"


# ==========================================
# 2. ONE-TO-MANY / FK (Uno a Muchos)
# ==========================================
# Regla: 1 Profesor imparte MUCHOS Cursos. Pero 1 Curso lo dicta 1 solo Profesor.
class Profesor(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)

    def __str__(self):
        return f"Prof. {self.nombre}"


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    # La ForeignKey va en el lado del "Muchos" (Curso).
    # on_delete=models.SET_NULL evita borrar el curso si el profesor renuncia.
    profesor = models.ForeignKey(
        Profesor, on_delete=models.SET_NULL, null=True, related_name="cursos"
    )

    def __str__(self):
        return self.nombre


# ==========================================
# 3. MANY-TO-MANY (Muchos a Muchos)
# ==========================================
# Regla: 1 Estudiante se inscribe en MUCHOS Cursos. 1 Curso tiene MUCHOS Estudiantes.
class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    # ManyToManyField se puede poner en cualquiera de los dos modelos (aquí en Estudiante)
    cursos = models.ManyToManyField(Curso, related_name="estudiantes")

    def __str__(self):
        return self.nombre