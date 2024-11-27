from django.contrib.auth.models import AbstractUser
from django.db import models

class UsuarioPersonalizado(AbstractUser):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    # Campos requeridos al crear un superusuario
    REQUIRED_FIELDS = ['nombres', 'apellidos', 'telefono', 'email']

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.username})"
