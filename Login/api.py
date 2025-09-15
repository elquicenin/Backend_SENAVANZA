#en este archivo de api.py vamos a realizar la validacion de la data ingresada para realizar el logeo de los usuarios y las empresas y generar el token de acceso,
# ademas de las vistas de la API VIEW, que son para las peticion http, en este caso GET, POST, PUT, DELETE, y primero vamos a realizar al de administrador, que es la que se encarga de gestionar los usuarios, empresas y programas de formacion.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserLoginSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Users.models import Empresa
from . import models


class CustomtokenObtainPairView(TokenObtainPairView):
    
    def post(self, request, *args, **kwargs):
        try:
            # Genera los tokens (acceso y refresh) usando SimpleJWT
            response = super().post(request, *args, **kwargs)
            tokens = response.data

            access_token = tokens['access']
            refresh_token = tokens['refresh']

            # Obtenemos al usuario autenticado
            user = authenticate(
                username=request.data.get('username'),
                password=request.data.get('password')
            )

            if not user:
                return Response({'detail': 'Credenciales incorrectas'}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_active:
                return Response({'detail': 'El usuario está desactivado'}, status=status.HTTP_403_FORBIDDEN)

            # Estado por defecto (usuarios/admins siempre tendrán 1)
            estado = 1

            # Si el rol es empresa, verificamos el estado real en la BD
            if user.rol == 'empresa':
                try:
                    empresa = user.empresa
                    estado = empresa.estado
                    if estado == 2:  # inactivo
                        return Response({'detail': 'La empresa está desactivada'}, status=status.HTTP_403_FORBIDDEN)
                except Empresa.DoesNotExist:
                    return Response({'detail': 'No existe una empresa asociada a este usuario'}, status=status.HTTP_404_NOT_FOUND)

            # Respuesta con tokens y datos de usuario
            res = Response()
            res.data = {
                'access': access_token,
                'refresh': refresh_token,
                'rol': user.rol,
                'is_active': user.is_active,
                'estado': estado  # nunca será null
            }

            # Guardamos tokens en cookies también (opcional si usas localStorage en React)
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            res.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            return res

        except Exception as e:
            return Response({'error': f'Error al obtener el token: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            request.data['refresh'] = refresh_token
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            access_token = tokens['access']
            res = Response()

            res.data = {
                'refreshed': True
            }

            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None', 
                path='/'
                )
            
            return res
            
        except:
            return Response({'error': 'Error al refrescar el token'}, status=status.HTTP_400_BAD_REQUEST)
            

@api_view(['POST'])
def login_admin(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user and user.is_active and user.rol == 'admin':
            return Response({'message': 'Login admin exitoso'}, status=status.HTTP_200_OK)
        return Response({'detail': 'No active account found with the given credentials'}, status=401)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def login_empresa(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user and user.rol == 'empresa':
            try:
                empresa = user.empresa  
            except models.Empresa.DoesNotExist:
                return Response(
                    {"error": "No se encontró una empresa asociada a este usuario"},
                    status=status.HTTP_404_NOT_FOUND
                )
            if empresa.estado == 2:  
                return Response(
                    {'detail': 'La empresa está desactivada'},
                    status=status.HTTP_403_FORBIDDEN
                )
            return Response(
                {'message': 'Login empresa exitoso'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'detail': 'Credenciales incorrectas'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def logout(request):
    try:
        res = Response()
        res.data = {'success': 'Logout exitoso'}
        res.delete_cookie('access_token', path='/', samesite='None')
        res.delete_cookie('refresh_token', path='/', samesite='None')
        return res
    except:
        return Response({'error': 'Error al cerrar sesión'}, status=status.HTTP_400_BAD_REQUEST)

#-----------------------------------------------------------------------------------------------------------###

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify(request):
    """
    Verifica la autenticidad del usuario leyendo la cookie access_token.
    Devuelve el rol, username y estado.
    """
    user = request.user  # Autenticado por JWT

    if user and user.is_authenticated:
        estado = 1  # valor por defecto para admin/usuarios

        if user.rol == 'empresa':
            try:
                empresa = user.empresa
                estado = empresa.estado
            except Empresa.DoesNotExist:
                return Response(
                    {"error": "No se encontró una empresa asociada a este usuario"},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response({
            'username': user.username,
            'rol': user.rol,
            'estado': estado
        }, status=status.HTTP_200_OK)

    return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    
# Aseguramos que el usuario esté autenticado para acceder a esta vista

#-----------------------------------------------------------------------------------------------------------###
#lo de abajo es otra forma de hacer el login, con diferente logica, pero no se esta usando en este momento
###---------------------------------------------------------------------------------------------------------###
# user = serializer.validated_data #asignamos los datos validados a la variable user
            # Verificamos si el rol del usuario es 'empresa'
            # if user['rol'] == 'empresa':
            #     return Response({'message': 'Login successful', 'empresa': user}, status=status.HTTP_200_OK)
            # else:
            #     return Response({'error': 'User nis not an empresa'}, status=status.HTTP_400_BAD_REQUEST)
###---------------------------------------------------------------------------------------------------------###


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify(request):
    """
    Verifica la autenticidad del usuario leyendo la cookie access_token.
    Devuelve el rol y el username.
    """
    user = request.user  # Autenticado por tu JWT Cookie
    if user and user.is_authenticated:
        return Response({
            'username': user.username,
            'rol': user.rol,
        }, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
## Recuperacion contraseña ##
@api_view(['POST'])
@permission_classes([AllowAny])
def send_reset_code(request):
    password_serializer = PasswordResetSerializer(data=request.data)
    if password_serializer.is_valid():
        password_serializer.save()
        return Response({'message': 'Código de restablecimiento enviado al correo electrónico registrado.'}, status=status.HTTP_200_OK)
    return Response(password_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def confirm_reset_code(request):
    confirm_serializer = PasswordResetConfirmSerializer(data=request.data)
    if confirm_serializer.is_valid():
        confirm_serializer.save()
        return Response({'message': 'Contraseña restablecida con éxito.'}, status=status.HTTP_200_OK)
    return Response(confirm_serializer.errors, status=status.HTTP_400_BAD_REQUEST)