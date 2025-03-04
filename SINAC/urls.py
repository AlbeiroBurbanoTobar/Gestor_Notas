from django.urls import path, include
from .views import home, home_admin, home_estudiante, registrar_estudiante

urlpatterns = [
    path('', home, name="home"),
    path('admin_home/', home_admin, name="home_admin"),
    path('estudiante_home/', home_estudiante, name="home_estudiante"),
    path('accounts/', include('django.contrib.auth.urls')),  
    path('registrar_estudiante/', registrar_estudiante, name='registrar_estudiante'),
]
