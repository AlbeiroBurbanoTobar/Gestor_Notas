from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ADMINISTRADOR = 'ADMINISTRADOR'
    ESTUDIANTE = 'ESTUDIANTE'
    PROFESOR = 'profesor'
    
    ROLES = [
        (ADMINISTRADOR, 'Administrador'),
        (ESTUDIANTE, 'Estudiante'),
        (PROFESOR, 'Profesor'),
    ]
    
    rol = models.CharField(max_length=20, choices=ROLES, default=ESTUDIANTE)

class Curso(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Estudiante(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    documento = models.CharField(max_length=20, unique=True, default="0000000000")
    fecha_nacimiento = models.DateField()
    telefono_acudiente = models.CharField(max_length=15, default="0000000000")
    direccion = models.CharField(max_length=255, default="Sin dirección")

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"


class Profesor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15)
    documento = models.CharField(max_length=20, unique=True)  
    email = models.EmailField(unique=True)  

    def __str__(self):
        return f"{self.usuario.first_name} {self.usuario.last_name}"


class Nota(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    calificacion = models.FloatField()

    def __str__(self):
        return f"{self.estudiante.usuario.first_name} {self.estudiante.usuario.last_name} - {self.curso.nombre}: {self.calificacion}"

class Asignatura(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)  
    def __str__(self):
        return f"{self.nombre} - {self.profesor.usuario.first_name} {self.profesor.usuario.last_name}"
    

class Grupo(models.Model):
    NIVELES = [(i, str(i)) for i in range(1, 12)]  # Niveles de 1 a 11

    nombre = models.CharField(max_length=100, unique=True)
    nivel = models.IntegerField(choices=NIVELES)  # Nivel entre 1 y 11

    def __str__(self):
        return f"{self.nombre} - Nivel {self.nivel}"


