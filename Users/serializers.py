from rest_framework import serializers
from . import models

#serializer es utilizado para convertir instancias de modelos a formatos JSON o XML
# y viceversa, facilitando la comunicación entre el servidor y el cliente. 
# en este caso, para conectar el modelo con la API RESTful.
# Esto es útil para la creación, actualización y visualización de datos en aplicaciones web.

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Empresa
        fields = '__all__'  # Serializa todos los campos del modelo Empresa
        read_only_fields = ['id', 'create_at', 'update_at', 'token', 'password','user']  # Campos de solo lectura
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
        empresa_data = validated_data.pop('empresa', None)# el pop() elimina el campo 'empresa' de validated_data y lo asigna a empresa_data, si no existe, devuelve None
        # Actualiza los campos de la instancia del usuario que es empresa
        for atributo, value in validated_data.items(): 
            setattr(instance, atributo, value)
        instance.save()
        # Si hay datos de empresa, actualiza la empresa asociada
        if empresa_data and hasattr(instance, 'empresa'):# el hasattr() verifica si la instancia tiene el atributo 'empresa'
            # Si la instancia tiene una empresa asociada, actualiza sus campos
            empresa = instance.empresa
            for attr, value in empresa_data.items():#este ciclo recorre los atributos de la empresa y los actualiza por medio del setattr que es una funcion que permite asignar un valor a un atributo de un objeto
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


class ProgramaFormacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProgramaFormacion # Serializa todos los campos del modelo ProgramaFormacion 
        fields = '__all__'