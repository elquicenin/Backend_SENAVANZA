from rest_framework import serializers
from . import models
from django.conf import settings
import random

#serializer es utilizado para convertir instancias de modelos a formatos JSON o XML
# y viceversa, facilitando la comunicación entre el servidor y el cliente. 
# en este caso, para conectar el modelo con la API RESTful.
# Esto es útil para la creación, actualización y visualización de datos en aplicaciones web.

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Empresa
        fields = '__all__'  # Serializa todos los campos del modelo Empresa
        read_only_fields = ['id', 'create_at', 'update_at', 'token', 'user']  # Solo campos técnicos son de solo lectura
## EMPRESA 

class UserSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer(required=False)

    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'rol', 'empresa', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        empresa_data = validated_data.pop('empresa', None)
        user = models.User.objects.create_user(**validated_data)
        if user.rol == 'empresa' and empresa_data:
            models.Empresa.objects.create(user=user, **empresa_data)
        return user
    

    def update(self, instance, validated_data):
            # 1. Extraer los datos de 'empresa' (OneToOne/Nested)
            empresa_data = validated_data.pop('empresa', None)
            
            # 2. Extraer los datos de 'groups' (ManyToManyField)
            groups_data = validated_data.pop('groups', None)

            # 3. Extraer los datos de 'user_permissions' (ManyToManyField)
            # ESTA ES LA NUEVA CLAVE PARA SOLUCIONAR EL ERROR
            user_permissions_data = validated_data.pop('user_permissions', None) 
            
            # 4. Actualiza los campos de la instancia del usuario que NO son ManyToMany
            # El error ocurre en la línea 48 de tu traceback, que es este ciclo:
            for atributo, value in validated_data.items(): 
                setattr(instance, atributo, value)
                
            instance.save()
            
            # 5. Actualizar la relación ManyToMany 'groups'
            if groups_data is not None:
                instance.groups.set(groups_data)
            
            # 6. Actualizar la relación ManyToMany 'user_permissions' usando .set()
            if user_permissions_data is not None:
                # Es vital usar .set() para actualizar esta relación M2M
                instance.user_permissions.set(user_permissions_data)
                
            # 7. Actualizar la empresa asociada (si aplica)
            if empresa_data and hasattr(instance, 'empresa'):
                empresa = instance.empresa
                for attr, value in empresa_data.items():
                    setattr(empresa, attr, value)
                empresa.save()
                
            return instance
    def create_user(self, validated_data):
        """
        Crea un usuario admin cuando su rol sea 'admin'
        """
        admin_data = validated_data.pop('admin', None)
        user = models.User.objects.create_user(**validated_data)
        if user.rol == 'admin' and admin_data:
            models.userAdmin.objects.create(user=user, **admin_data)
        return user
    
    
###-----------------------------COMO SE USA LO ANTERIOR ---------------------------------------###
# {
#   "username": "empresa_nueva",
#   "password": "ContraseñaSegura123",
#   "rol": "empresa",
#   "email": "empresa_nueva@correo.com",
#   "empresa": {
#     "documento": "nit",
#     "numero_documento": 900123456,
#     "razon_social": "Empresa Nueva S.A.S.",
#     "telefono": "3001234567",
#     "correo_electronico": "contacto@empresanueva.com",
#     "direccion": "Calle 123 #45-67",
#     "actividad_economica": "Servicios",
#     "estado": 1
#   }
# }
###-------------------------------------------------------------------------------------------###
class EmpresaUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer específico para actualizaciones de empresa que permite todos los campos editables
    """
    class Meta:
        model = models.Empresa
        fields = [
            'documento', 'numero_documento', 'razon_social', 'telefono', 
            'correo_electronico', 'direccion', 'actividad_economica', 'estado'
        ]
        # No incluye read_only_fields para permitir actualización de todos los campos

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer específico para actualizaciones de usuario que permite todos los campos editables
    """
    class Meta:
        model = models.User
        fields = ['username', 'email', 'rol']
        # No incluye campos técnicos como id, password, etc.

class ProgramaFormacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProgramaFormacion # Serializa todos los campos del modelo ProgramaFormacion 
        fields = '__all__'