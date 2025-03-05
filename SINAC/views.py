from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required,  user_passes_test
from .models import Usuario, Estudiante
from .forms import EstudianteForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib import messages
from .models import Usuario, Estudiante, Profesor
from .forms import ProfesorForm
from SINAC.models import Curso


User = get_user_model()

def es_admin(user):
    return user.is_superuser 


def registrar_estudiante(request):
    if request.method == "POST":
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Estudiante registrado correctamente.")
            return redirect("home_admin")  # Redirigir al panel del administrador
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
    return redirect('login')  # En caso de que no tenga rol asignado

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
            return redirect('home_admin')
    else:
        form = EstudianteForm()
    
    return render(request, 'registrar_estudiante.html', {'form': form})


def registrar_profesor(request):
    if request.method == "POST":
        form = ProfesorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Profesor registrado exitosamente.")
            return redirect('home_admin')  # Redirigir al panel de admin
    else:
        form = ProfesorForm()
    return render(request, 'registrar_profesor.html', {'form': form})

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