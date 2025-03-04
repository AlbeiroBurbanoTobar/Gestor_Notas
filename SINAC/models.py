from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ADMINISTRADOR = 'ADMINISTRADOR'
    ESTUDIANTE = 'ESTUDIANTE'
    
    ROLES = [
        (ADMINISTRADOR, 'Administrador'),
        (ESTUDIANTE, 'Estudiante'),
    ]
    
    rol = models.CharField(max_length=20, choices=ROLES, default=ESTUDIANTE)

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nombre

class Estudiante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE,  null=True, blank=True)
    documento = models.CharField(max_length=20, unique=True, default="0000000000")
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=255, default="Sin dirección")
    telefono_acudiente = models.CharField(max_length=15, default="0000000000")  # Se agrega un valor predeterminado
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name} - Curso {self.curso.nombre}"


class Nota(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    calificacion = models.FloatField()

    def __str__(self):
        return f"{self.estudiante.usuario.first_name} {self.estudiante.usuario.last_name} - {self.curso.nombre}: {self.calificacion}"
