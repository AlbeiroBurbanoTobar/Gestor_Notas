from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Estudiante, Curso

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Estudiante, Curso, Profesor

class EstudianteForm(UserCreationForm):
    documento = forms.CharField(max_length=20)
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    direccion = forms.CharField(max_length=255)
    telefono_acudiente = forms.CharField(max_length=15)
    curso = forms.IntegerField(min_value=1, max_value=11)  # Permite ingresar un número

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = Usuario.ESTUDIANTE
        if commit:
            user.save()
            
            # Convertir el número ingresado en una instancia de Curso
            curso_id = self.cleaned_data['curso']
            try:
                curso = Curso.objects.get(id=curso_id)
            except Curso.DoesNotExist:
                raise ValueError(f"El curso con ID {curso_id} no existe.")

            estudiante = Estudiante.objects.create(
                usuario=user,
                documento=self.cleaned_data['documento'],
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                direccion=self.cleaned_data['direccion'],
                telefono_acudiente=self.cleaned_data['telefono_acudiente'],
                curso=curso  # Ahora es una instancia de Curso
            )


class ProfesorForm(UserCreationForm):
    direccion = forms.CharField(max_length=255)
    asignatura = forms.CharField(max_length=100)
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    telefono = forms.CharField(max_length=15)

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = Usuario.PROFESOR  
        if commit:
            user.save()
        return user
