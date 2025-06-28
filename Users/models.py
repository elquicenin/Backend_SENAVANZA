import cuid 
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import timedelta, datetime
# Create your models here.

class User(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('empresa', 'Empresa'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES)
    password = models.CharField(max_length=128, null=False, blank=False)

    def set_password(self, raw_password):
        return super().set_password(raw_password)

class Empresa(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
    on_delete=models.CASCADE, related_name='empresa')
    id = models.CharField(primary_key=True, max_length=30, default=cuid.cuid, unique=True,editable=False)
    tipo_documento = [
        ('cc', 'CC'),
        ('nit', 'NIT'),
    ]
    documento = models.CharField(max_length=10, choices=tipo_documento, default='nit')
    numero_documento = models.IntegerField(null=False)
    razon_social = models.CharField(max_length=150, null=False, default='sin razon social')
    telefono = models.TextField(max_length=20)
    correo_electronico = models.EmailField(max_length=255, unique=True)
    direccion = models.CharField(max_length=255, null=False)
    actividad_economica = models.CharField(max_length=200, null=False)
    ESTADOS_CHOISES = [
        (1,'activo'),
        (2,'inactivo'),
        (3,'suspendido')
    ]
    estado = models.IntegerField(choices=ESTADOS_CHOISES, default=1)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=255, blank=True, null=True)

    def crear_token(self):
        import secrets
        self.token = secrets.token_hex(32)
        self.save()
        return self.token
    

class userAdmin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin')
    nombre = models.CharField(max_length=100, null=False,default='admin_sena',help_text='Nombre del administrador')
    apellido = models.CharField(max_length=100, null=False,default='admin_sena_apellido',help_text='Apellido del administrador')


class ProgramaFormacion(models.Model):
    id = models.CharField(primary_key=True, max_length=30, default=cuid.cuid, unique=True, editable=False)
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.TextField(null=False)
    ESTADOS_CHOISES = [
        (1, 'activo'),
        (2, 'inactivo'),
        (3, 'suspendido')
    ]
    estado = models.IntegerField(choices=ESTADOS_CHOISES, default=1)
    NIVEL_CHOICES = [
        ('tecnico', 'Técnico'),
        ('tecnologo', 'Tecnólogo'),
    ]
    nivel_programa = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='tecnologo')
    duracion = models.IntegerField(null=False, help_text='Duración en horas')
    modalidad = models.CharField(max_length=20, null=False, help_text='Modalidad del programa')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class DiagnosticoEmpresarial(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='diagnosticos')
    archivo = models.FileField(upload_to='diagnosticos/', null=False, blank=False)
    creation_at = models.DateTimeField(auto_now_add=True)

    def vencido(self):
        # tiempo de vencimiento del diagnostico es de 15 dias
        # si la fecha actual es mayor a la fecha de creacion mas 15 dias, entonces el diagnostico esta vencido
        return  datetime.now() > self.creation_at + timedelta(days=15) 