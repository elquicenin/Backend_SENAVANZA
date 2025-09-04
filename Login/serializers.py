# Login/serializers.py
from rest_framework import serializers
from Users import  models
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from random import randint
#traemos desde User.serializers el UserSerializer y el userAdminSerializer para poder usarlos en las vistas de Login 

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



User = settings.AUTH_USER_MODEL # el User que creamos aca se trae desde el settings el AUTH_USER_MODEL que es el abstracto que creamos en Users/models.py 

class PasswordResetSerializer(serializers.Serializer):
    nit = serializers.IntegerField() # Asegúrate de que el NIT sea un campo entero para poder validar correctamente ya que en el modelo es IntegerField porque si lo dejo normal como CharField no me valida bien

    def validate_nit(self, value): # este metodo valida que el nit exista en la base de datos y guarda el valor en value
        if not models.Empresa.objects.filter(numero_documento=value).exists(): # si no existe el nit en la base de datos
            raise serializers.ValidationError("El NIT proporcionado no está registrado.") # el raise es para lanzar una excepcion y el serializers.ValidationError es para devolver un error de validacion
        return value

    def create(self, validated_data): # este metodo crea el codigo de restablecimiento y lo guarda en la base de datos donde ya se encuentra el modelo PasswordResetCode
        nit = validated_data['nit'] # obtenemos el nit del diccionario validated_data
        empresa = models.Empresa.objects.get(numero_documento=nit) # comparamos el nit con el numero_documento de la empresa 
        user = empresa.user # obtenemos el usuario asociado a la empresa
        

        # creamos el codigo de restablecimiento con ramdom.randint para que sea un numero entre 1000 y 9999
        new_codee = randint(1000, 9999)

        # guardamos el codigo en la base de datos, si ya existe un codigo para ese usuario lo actualiza, si no lo crea
        reset, created = models.PasswordResetCode.objects.update_or_create( # el created del inicio es para saber si se creo o se actualizo
            user=user,
            defaults={'code': new_codee, 'created_at': timezone.now()}
        )

        # print("DEBUG RESET:", reset, reset.code)  
        # # esto es para ver en la consola el codigo de restablecimiento que se creo o se actualizo

        user.email_user(
            subject="Código de restablecimiento de contraseña",
            message=f"Su código de restablecimiento de contraseña es: {reset}"
        ) # enviamos el codigo al email del usuario importante todo se saca de la base de datos

        return reset # retornamos el codigo de restablecimiento

class PasswordResetConfirmSerializer(serializers.Serializer):
    nit = serializers.IntegerField()
    code = serializers.CharField(max_length=4)
    new_password = serializers.CharField(min_length=8, max_length=128)
    # en los campos anteriores se definen los campos que se van a recibir en el request

    def validate(self, data): # el metodo validate valida que el nit y el codigo existan en la base de datos y que el codigo no haya expirado y guarda los valores en data
        nit = data.get('nit')
        code = data.get('code')

        try:
            empresa = models.Empresa.objects.get(numero_documento=nit) # validamos que el nit ingresado coincida con el numero_documento de la empresa
            user = empresa.user
        except models.Empresa.DoesNotExist:
            raise serializers.ValidationError("NIT no encontrado.")

        try:
            reset_code = models.PasswordResetCode.objects.get(user=user, code=code) # validamos que el codigo ingresado coincida con el codigo de restablecimiento de la base de datos
            # verificamos si el codigo ha expirado (10 minutos de validez) igual el modelo lo hace de manera automatica pero lo dejo por si acaso
            if not reset_code.is_valid(): # negamos el metodo is_valid para que entre al if si el codigo no es valido
                raise serializers.ValidationError("El código ha expirado.")
        except models.PasswordResetCode.DoesNotExist:
            raise serializers.ValidationError("El código de restablecimiento es inválido o ya fue utilizado.")

        data['user'] = user
        data['reset_code'] = reset_code
        return data # los datos anteriores se guardan en el diccionario data

    def save(self, **kwargs):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        self.validated_data['reset_code'].delete()
        return user
        # el metodo save guarda la nueva contraseña en la base de datos y elimina el codigo de restablecimiento para que no se pueda volver a usar
        # importante desde el front hay que enviar un request con el siguiente formato: 
        # {
        # "nit": 108827233,
        # "code": "1234",  
        # "new_password": "Holamundo1"}

