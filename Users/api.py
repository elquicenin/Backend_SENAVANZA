from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, EmpresaSerializer, ProgramaFormacionSerializer, EmpresaUpdateSerializer, UserUpdateSerializer
from . import models

# ---------------- PETICIONES PARA PROGRAMAS DE FORMACIÓN ---------------- #

@api_view(['GET'])
def programa_list(request):
    programas = ProgramaFormacionSerializer(models.ProgramaFormacion.objects.all(), many=True)
    return Response(programas.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def programa_create(request):
    serializer = ProgramaFormacionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def programa_detail(request, pk):
    """
    Vista para actualizar (PUT) o eliminar (DELETE) un Programa de Formación
    """
    try:
        programa = models.ProgramaFormacion.objects.get(pk=pk)
    except models.ProgramaFormacion.DoesNotExist:
        return Response({'error': 'Programa no encontrado'}, status=status.HTTP_404_NOT_FOUND)


    if request.method == 'GET':
        serializer = ProgramaFormacionSerializer(programa)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = ProgramaFormacionSerializer(programa, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        programa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ---------------- CRUD PARA USUARIOS DEL SISTEMA ---------------- #

@api_view(['POST'])
def user_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_detail(request):
    try:
        user = models.User.objects.get()
    except models.User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        user = models.User.objects.get(pk=pk)
    except models.User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def users_detail(request):
    users = UserSerializer(models.User.objects.all(), many=True)
    return Response(users.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT'])
def user_detail_by_pk(request, pk):
    try:
        user = models.User.objects.get(pk=pk)
    except models.User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

# ---------------- CRUD PARA EMPRESAS ---------------- #

@api_view(['GET'])
def user_empresa_list(request):
    empresas = models.Empresa.objects.all()
    serializer = EmpresaSerializer(empresas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def user_empresa_create(request):
    serializer = EmpresaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def perfil_empresa(request):
    user = request.user
    try:
        empresa = models.Empresa.objects.get(user=user)
    except models.Empresa.DoesNotExist:
        return Response(
            {"error": "No se encontró una empresa asociada a este usuario"},
            status=status.HTTP_404_NOT_FOUND
        )
    if empresa.estado == 2:
        return Response({"error": "Empresa inactiva"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = EmpresaSerializer(empresa)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = EmpresaSerializer(empresa, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def user_empresa_update(request, pk):
    try:
        empresa = models.Empresa.objects.get(pk=pk)
    except models.Empresa.DoesNotExist:
        return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = EmpresaSerializer(empresa, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Sincroniza el correo en el usuario si fue actualizado
            nuevo_correo = serializer.validated_data.get('correo_electronico')  # Cambia 'correo' si tu campo se llama diferente
            if nuevo_correo:
                empresa.user.email = nuevo_correo
                empresa.user.save()
            if serializer.validated_data.get('estado') == 2:
                empresa.user.is_active = False
            else:
                empresa.user.is_active = True
            empresa.user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        empresa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def empresa_detail(request, pk):
    try:
        empresa = models.Empresa.objects.get(pk=pk)
    except models.Empresa.DoesNotExist:
        return Response({'error': 'Empresa no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if empresa.estado == 2:
        return Response({'error': 'Empresa inactiva'}, status=status.HTTP_403_FORBIDDEN)

    serializer = EmpresaSerializer(empresa)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_perfil_completo(request):
    """
    Endpoint para actualizar tanto datos del usuario como de la empresa
    Permite actualizar username, email, rol del usuario y todos los campos de empresa
    """
    user = request.user
    try:
        empresa = models.Empresa.objects.get(user=user)
    except models.Empresa.DoesNotExist:
        return Response(
            {"error": "No se encontró una empresa asociada a este usuario"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if empresa.estado == 2:
        return Response({"error": "Empresa inactiva"}, status=status.HTTP_403_FORBIDDEN)

    # Separar datos del usuario y empresa
    data = request.data.copy()
    user_data = {}
    empresa_data = {}
    
    # Campos del usuario que se pueden actualizar
    user_fields = ['username', 'email', 'rol']
    for field in user_fields:
        if field in data:
            user_data[field] = data.pop(field)
    
    # Los datos restantes son para la empresa
    empresa_data = data
    
    errors = {}
    
    # Actualizar usuario si hay datos
    if user_data:
        user_serializer = UserSerializer(user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            errors['user_errors'] = user_serializer.errors
    
    # Actualizar empresa si hay datos
    if empresa_data:
        empresa_serializer = EmpresaSerializer(empresa, data=empresa_data, partial=True)
        if empresa_serializer.is_valid():
            empresa_serializer.save()
            
            # Sincronizar correo si se actualizó en empresa
            nuevo_correo = empresa_serializer.validated_data.get('correo_electronico')
            if nuevo_correo and not user_data.get('email'):
                user.email = nuevo_correo
                user.save()
        else:
            errors['empresa_errors'] = empresa_serializer.errors
    
    # Si hay errores, retornarlos
    if errors:
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Retornar datos actualizados
    response_data = {
        'usuario': UserSerializer(user).data,
        'empresa': EmpresaSerializer(empresa).data,
        'message': 'Perfil actualizado exitosamente'
    }
    return Response(response_data, status=status.HTTP_200_OK)
