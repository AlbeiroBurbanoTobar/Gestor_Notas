from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Estudiante, Curso

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Estudiante, Asignatura, Profesor

class EstudianteForm(UserCreationForm):  # Heredamos de UserCreationForm para incluir usuario y contraseña
    documento = forms.CharField(max_length=20, required=True, label="Documento de Identidad")
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    telefono_acudiente = forms.CharField(max_length=15, required=True, label="Teléfono del Acudiente")
    direccion = forms.CharField(max_length=255, required=True, label="Dirección")

    class Meta:
        model = Usuario
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'documento', 'fecha_nacimiento', 'telefono_acudiente', 'direccion']

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.rol = Usuario.ESTUDIANTE  # Asignamos el rol de estudiante
        if commit:
            usuario.save()
            # Creamos el perfil del estudiante
            estudiante = Estudiante.objects.create(
                usuario=usuario,
                documento=self.cleaned_data['documento'],
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                telefono_acudiente=self.cleaned_data['telefono_acudiente'],
                direccion=self.cleaned_data['direccion']
            )
        return usuario

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password"])
        usuario.rol = Usuario.ESTUDIANTE  # Asignar el rol de estudiante
        if commit:
            usuario.save()
            estudiante = Estudiante.objects.create(
                usuario=usuario,
                documento=self.cleaned_data.get('documento'),
                fecha_nacimiento=self.cleaned_data.get('fecha_nacimiento'),
                telefono_acudiente=self.cleaned_data.get('telefono_acudiente'),
                direccion=self.cleaned_data.get('direccion')
            )
            estudiante.save()
        return usuario

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = Usuario.ESTUDIANTE
        if commit:
            user.save()
            

            estudiante = Estudiante.objects.create(
                usuario=user,
                documento=self.cleaned_data['documento'],
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                direccion=self.cleaned_data['direccion'],
                telefono_acudiente=self.cleaned_data['telefono_acudiente'],
        
            )

class ProfesorForm(UserCreationForm):
    direccion = forms.CharField(max_length=255, required=True)
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    telefono = forms.CharField(max_length=15, required=True)
    documento = forms.CharField(max_length=20, required=True, label="Documento de Identidad")  
    email = forms.EmailField(required=True, label="Correo Electrónico")  

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = Usuario.PROFESOR
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profesor.objects.create(
                usuario=user,
                direccion=self.cleaned_data['direccion'],
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                telefono=self.cleaned_data['telefono'],
                documento=self.cleaned_data['documento'],
                email=self.cleaned_data['email'],
            )
        return user


class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['nombre', 'profesor']  # Campos que se mostrarán

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profesor'].queryset = Profesor.objects.all()  # Solo mostrar profesores registrados
