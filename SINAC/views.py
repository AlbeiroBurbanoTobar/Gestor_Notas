from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib import messages
from .models import Usuario, Estudiante, Profesor, Asignatura,Nota
from .forms import (ProfesorForm, AsignaturaForm, EstudianteForm, GrupoForm, AsignarEstudiantesGrupoForm,
                     VincularAsignaturasGrupoForm, ModificarUsuarioForm, ModificarEstudianteForm, ModificarProfesorForm)
from SINAC.models import Grupo
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse


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
            return redirect("home")  
        else:
            return render(request, "login.html", {"error": "Usuario o contraseña incorrectos"})
    return render(request, "login.html")

@login_required
def home(request):
    if request.user.rol == Usuario.ADMINISTRADOR:
        return redirect('home_admin')
    elif request.user.rol == Usuario.ESTUDIANTE:
        return redirect('home_estudiante')
    elif request.user.rol == Usuario.PROFESOR:
        return redirect('home_profesor')
    
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


@login_required
@user_passes_test(es_admin)
def ver_grupo_por_nivel(request):
    if request.method == "POST":
        nivel = request.POST.get('nivel')
        grupos = Grupo.objects.filter(nivel=nivel)

    
        estudiantes = Estudiante.objects.filter(grupo__in=grupos)

   
        profesores = Profesor.objects.filter(asignatura__grupo__in=grupos)

        return render(request, 'ver_grupo_por_nivel.html', {
            'estudiantes': estudiantes,
            'profesores': profesores,
            'nivel': nivel
        })
    else:
        return render(request, 'ver_grupo_por_nivel.html', {'niveles': range(1, 12)})



@login_required
@user_passes_test(es_admin)
def modificar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if usuario.rol == Usuario.ESTUDIANTE:
        estudiante = get_object_or_404(Estudiante, usuario=usuario)
        form_usuario = ModificarUsuarioForm(request.POST or None, instance=usuario)
        form_detalles = ModificarEstudianteForm(request.POST or None, instance=estudiante)
    elif usuario.rol == Usuario.PROFESOR:
        profesor = get_object_or_404(Profesor, usuario=usuario)
        form_usuario = ModificarUsuarioForm(request.POST or None, instance=usuario)
        form_detalles = ModificarProfesorForm(request.POST or None, instance=profesor)
    else:
        form_usuario = ModificarUsuarioForm(request.POST or None, instance=usuario)
        form_detalles = None

    if request.method == "POST":
        if form_usuario.is_valid() and (form_detalles is None or form_detalles.is_valid()):
            form_usuario.save()
            if form_detalles:
                form_detalles.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect('lista_usuarios')
        else:
            messages.error(request, "Error al actualizar el usuario. Verifica los datos.")

    return render(request, 'modificar_usuario.html', {
        'form_usuario': form_usuario,
        'form_detalles': form_detalles,
        'usuario': usuario
    })

@login_required
def home_estudiante(request):
    if request.user.rol != Usuario.ESTUDIANTE:
        return redirect('home')
    
    return render(request, 'estudiante_home.html')


@login_required
def home_profesor(request):
    if request.user.rol != Usuario.PROFESOR:
        return redirect('home')
    
    return render(request, 'profesor_home.html')

@login_required
def registrar_notas(request):
    if request.user.rol != Usuario.PROFESOR:
        return redirect('home')

    profesor = Profesor.objects.get(usuario=request.user)
    asignaturas = Asignatura.objects.filter(profesor=profesor)

    if request.method == "POST":
        asignatura_id = request.POST.get("asignatura")
        estudiante_id = request.POST.get("estudiante")
        calificacion = request.POST.get("calificacion")

        if asignatura_id and estudiante_id and calificacion:
            try:
                estudiante = Estudiante.objects.get(id=estudiante_id)
                asignatura = Asignatura.objects.get(id=asignatura_id)

                nota, created = Nota.objects.update_or_create(
                    estudiante=estudiante,
                    asignatura=asignatura,
                    defaults={'calificacion': float(calificacion)}
                )

                messages.success(request, "Nota registrada exitosamente.")
            except Exception as e:
                messages.error(request, f"Error al registrar la nota: {str(e)}")
        else:
            messages.error(request, "Todos los campos son obligatorios.")

    return render(request, 'registrar_notas.html', {'asignaturas': asignaturas})

@login_required
def estudiantes_por_asignatura(request, asignatura_id):

    if request.user.rol != Usuario.PROFESOR:
        return JsonResponse({'error': 'No autorizado'}, status=403)

    asignatura = get_object_or_404(Asignatura, id=asignatura_id, profesor__usuario=request.user)
    estudiantes = Estudiante.objects.filter(grupo=asignatura.grupo)

    estudiantes_data = [{'id': estudiante.id, 'nombre': f"{estudiante.usuario.first_name} {estudiante.usuario.last_name}"} for estudiante in estudiantes]
    
    return JsonResponse({'estudiantes': estudiantes_data})

@login_required
def ver_notas_estudiante(request):
    if request.user.rol != Usuario.ESTUDIANTE:
        return redirect('home')

    estudiante = get_object_or_404(Estudiante, usuario=request.user)
    notas = Nota.objects.filter(estudiante=estudiante)

    return render(request, 'ver_notas.html', {'notas': notas})

@login_required
def ver_notas_docente(request):
    """Permite a los docentes ver las notas de sus estudiantes"""
    if request.user.rol != Usuario.PROFESOR:
        return redirect('home')

    profesor = get_object_or_404(Profesor, usuario=request.user)
    asignaturas = Asignatura.objects.filter(profesor=profesor)
    notas = Nota.objects.filter(asignatura__in=asignaturas).select_related('estudiante', 'asignatura')

    return render(request, 'ver_notas_docente.html', {'notas': notas, 'asignaturas': asignaturas})
