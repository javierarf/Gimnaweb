
## Proyecto Django con conexión a Oracle para manejar registro e inscripción

# 1. Estructura del proyecto:
# gimnaweb_backend/
# ├── gimnaweb_backend/
# │   ├── __init__.py
# │   ├── settings.py
# │   ├── urls.py
# │   └── wsgi.py
# ├── usuarios/
# │   ├── __init__.py
# │   ├── admin.py
# │   ├── apps.py
# │   ├── models.py
# │   ├── urls.py
# │   ├── views.py
# │   └── migrations/
# └── manage.py

# 2. models.py en 'usuarios'
from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=100)

class Inscripcion(models.Model):
    nombre = models.CharField(max_length=100)
    clase = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)

# 3. views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario, Inscripcion
import json

@csrf_exempt
def registrar_usuario(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        usuario = Usuario.objects.create(
            nombre=data['nombre'],
            email=data['email'],
            contrasena=data['contrasena']
        )
        return JsonResponse({'mensaje': 'Usuario registrado'})

@csrf_exempt
def inscribir_clase(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        inscripcion = Inscripcion.objects.create(
            nombre=data['nombre'],
            clase=data['clase']
        )
        return JsonResponse({'mensaje': 'Inscripción registrada'})

# 4. urls.py en 'usuarios'
from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registrar_usuario),
    path('inscripcion/', views.inscribir_clase),
]

# 5. urls.py en el proyecto principal
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('usuarios.urls')),
]

# 6. settings.py (fragmento conexión a Oracle)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'localhost:1521/XE',  # Ajustar según tu configuración
        'USER': 'usuario_oracle',
        'PASSWORD': 'contrasena_oracle',
    }
}
