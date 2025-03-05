from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required,  user_passes_test
from .models import Usuario, Estudiante
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib import messages
from .models import Usuario, Estudiante, Profesor
from .forms import ProfesorForm, AsignaturaForm, EstudianteForm, GrupoForm, AsignarEstudiantesGrupoForm, VincularAsignaturasGrupoForm
from SINAC.models import Curso
from django import forms
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()

def es_admin(user):
    return user.is_superuser 


def registrar_estudiante(request):
    if request.method == "POST":
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Estudiante registrado correctamente.")
            
        else:
            messages.error(request, "Error al registrar el estudiante. Verifica los datos.")
    else:
        form = EstudianteForm()
    
    return render(request, "registrar_estudiante.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # Redirige al home según el rol
        else:
            return render(request, "login.html", {"error": "Usuario o contraseña incorrectos"})
    return render(request, "login.html")

@login_required
def home(request):
    """ Redirige a la página correspondiente según el rol del usuario """
    if request.user.rol == Usuario.ADMINISTRADOR:
        return redirect('home_admin')
    elif request.user.rol == Usuario.ESTUDIANTE:
        return redirect('home_estudiante')
    return redirect('login') 

@login_required
def home_admin(request):
    """ Página de inicio para Administradores """
    if request.user.rol != Usuario.ADMINISTRADOR:
        return redirect('home')
    
    return render(request, 'admin_home.html')

@login_required
def home_estudiante(request):
    """ Página de inicio para Estudiantes """
    if request.user.rol != Usuario.ESTUDIANTE:
        return redirect('home')

    return render(request, 'estudiante_home.html')

@login_required
def registrar_estudiante(request):
    """ Vista para que el administrador registre estudiantes """
    if request.user.rol != Usuario.ADMINISTRADOR:
        return redirect('home')

    if request.method == "POST":
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Profesor registrado exitosamente.")
    else:
        form = EstudianteForm()
    
    return render(request, 'registrar_estudiante.html', {'form': form})


@login_required
@user_passes_test(es_admin)
def lista_usuarios(request):
    usuarios = Usuario.objects.filter(is_superuser=False) 
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

@login_required
@user_passes_test(es_admin)
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if request.method == "POST":
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect('lista_usuarios')

    return render(request, 'eliminar_usuario.html', {'usuario': usuario})

def registrar_profesor(request):
    if request.method == "POST":
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Profesor registrado exitosamente.")
            
        else:
            messages.error(request, "Error al registrar el profesor. Verifica los datos ingresados.")
            print(form.errors) 
    else:
        form = ProfesorForm()
    return render(request, 'registrar_profesor.html', {'form': form})


@login_required
@user_passes_test(es_admin) 
def crear_asignatura(request):
    if request.method == "POST":
        form = AsignaturaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Asignatura creada exitosamente.")
            
        else:
            messages.error(request, "Error al crear la asignatura. Verifica los datos.")
    else:
        form = AsignaturaForm()

    return render(request, 'crear_asignatura.html', {'form': form})


@login_required
@user_passes_test(es_admin) 
def crear_grupo(request):
    if request.method == "POST":
        form = GrupoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Grupo creado exitosamente.")
            return redirect('home_admin') 
        else:
            messages.error(request, "Error al crear el grupo. Verifica los datos.")
    else:
        form = GrupoForm()

    return render(request, 'crear_grupo.html', {'form': form})


@login_required
@user_passes_test(es_admin) 
def asignar_estudiantes_a_grupo(request):
    if request.method == "POST":
        form = AsignarEstudiantesGrupoForm(request.POST)
        if form.is_valid():
            grupo = form.cleaned_data['grupo']
            estudiantes = form.cleaned_data['estudiantes']

      
            for estudiante in estudiantes:
                estudiante.grupo = grupo
                estudiante.save()

            messages.success(request, "Estudiantes asignados correctamente al grupo.")
            
        else:
            messages.error(request, "Error al asignar estudiantes. Verifica los datos.")
    else:
        form = AsignarEstudiantesGrupoForm()

    return render(request, 'asignar_estudiantes.html', {'form': form})


@login_required
@user_passes_test(es_admin) 
def vincular_asignaturas_a_grupo(request):
    if request.method == "POST":
        form = VincularAsignaturasGrupoForm(request.POST)
        if form.is_valid():
            grupo = form.cleaned_data['grupo']
            asignaturas = form.cleaned_data['asignaturas']

            for asignatura in asignaturas:
                asignatura.grupo = grupo
                asignatura.save()

            messages.success(request, "Asignaturas vinculadas correctamente al grupo.")
            
        else:
            messages.error(request, "Error al vincular asignaturas. Verifica los datos.")
    else:
        form = VincularAsignaturasGrupoForm()

    return render(request, 'vincular_asignaturas.html', {'form': form})


