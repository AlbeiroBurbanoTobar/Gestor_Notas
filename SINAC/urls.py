from django.urls import path, include
from .views import (home, home_admin, home_estudiante, registrar_estudiante,
                     registrar_profesor, eliminar_usuario, lista_usuarios, 
                     crear_asignatura, crear_grupo, asignar_estudiantes_a_grupo,
                     vincular_asignaturas_a_grupo, ver_grupo_por_nivel)

urlpatterns = [
    path('', home, name="home"),
    path('admin_home/', home_admin, name="home_admin"),
    path('estudiante_home/', home_estudiante, name="home_estudiante"),
    path('accounts/', include('django.contrib.auth.urls')),  
    path('registrar_estudiante/', registrar_estudiante, name='registrar_estudiante'),
    path('registrar_profesor/', registrar_profesor, name='registrar_profesor'),
    path('usuarios/', lista_usuarios, name='lista_usuarios'),
    path('eliminar_usuario/<int:usuario_id>/', eliminar_usuario, name='eliminar_usuario'),
    path('crear_asignatura/', crear_asignatura, name='crear_asignatura'),
    path('crear_grupo/', crear_grupo, name='crear_grupo'),
    path('asignar_estudiantes/', asignar_estudiantes_a_grupo, name='asignar_estudiantes'),
    path('vincular_asignaturas/', vincular_asignaturas_a_grupo, name='vincular_asignaturas'),
    path('ver_grupo_por_nivel/', ver_grupo_por_nivel, name='ver_grupo_por_nivel'),




]

