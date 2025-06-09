from django.contrib.auth.backends import ModelBackend
from .models import User,Empresa

class EmpresaEmailBackend(ModelBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        try:
            empresa = Empresa.objects.get(correo_electronico=username)
            user = empresa.user 
            if user.check_password(password):
                return user
        except Empresa.DoesNotExist:
            return None