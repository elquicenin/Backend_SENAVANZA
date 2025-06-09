# Login/serializers.py
from rest_framework import serializers
from Users.models import User

#traemos desde User.serializers el UserSerializer y el userAdminSerializer para poder usarlos en las vistas de Login 

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

