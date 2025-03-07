from django.contrib import admin
from .models import Usuario, Estudiante, Grupo, Asignatura, Nota

admin.site.register(Usuario)
admin.site.register(Estudiante)
admin.site.register(Asignatura) 
admin.site.register(Grupo) 
admin.site.register(Nota) 
