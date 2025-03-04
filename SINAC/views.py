from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Usuario, Estudiante
from .forms import EstudianteForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages

def registrar_estudiante(request):
    if request.method == "POST":
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Estudiante registrado correctamente.")
            return redirect("admin_home")  # Redirige a la página del administrador
        else:
            messages.error(request, "Error al registrar estudiante. Verifica los datos.")
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
