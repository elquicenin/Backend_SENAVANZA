from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, EmpresaSerializer, ProgramaFormacionSerializer
from . import models
from rest_framework import status

#en este apartado hacemos las vistas de la API VIEW, que son para las peticion http,
# en este caso GET, POST, PUT, DELETE, y primero vamos a realizar al de administrador,
# que es la que se encarga de gestionar los usuarios, empresas y programas de formacion.

#----------------------PETICIONES GET,POST,PUT,DELETE PARA PROGRAMAS DE FORMACION-----------------------#
@api_view(['GET'])
def programa_list(request):
    if request.method == 'GET':
        programas = ProgramaFormacionSerializer(models.ProgramaFormacion.objects.all(), many=True)
        return Response(programas.data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def programa_create(request):
    if request.method == 'POST':
        serializer = ProgramaFormacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', 'DELETE'])
def programa_detail(request, pk):
    try:
        programa = models.ProgramaFormacion.objects.get(pk=pk)  # la pk es el id del programa que se va a eliminar
    except models.ProgramaFormacion.DoesNotExist:
        return Response({'error': 'Program not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        programa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        serializer = ProgramaFormacionSerializer(programa, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
#--------------------------TERMINAMOS LOS METODOS PARA LAS PETICIONES HTTP-------------------------------#
#-------------------------------------------------------------------------------------------------------#
###---------------------------PETICIONES DEL USUARIO NORMAL GET,POST,PUT,DELETE----------------------------#
@api_view(['POST'])
def user_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE', 'PUT'])
def user_detail(request):
    try:
        user = models.User.objects.get()  
    except models.User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#---------------------------PETICIONES DEL ADMINISTRADOR GET,POST,PUT,DELETE----------------------------#
@api_view(['GET'])
def user_empresa_list(request):
    if request.method == 'GET':
        empresas = UserSerializer(models.Empresa.objects.all(), many=True) #el many=True se usa para indicar que se van a serializar varios objetos
        return Response(empresas.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def user_empresa_create(request):
    if request.method == 'POST':
        serializer = EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', 'DELETE'])
def user_empresa_detail(request, pk):
    if request.method == 'DELETE':
        try:
            user = models.Empresa.objects.get(pk=pk)  # la pk es el id del usuario que se va a eliminar
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Empresa.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

def user_empresa_update(request, pk):
    try:
        user = models.Empresa.objects.get(pk=pk)#la pk es el id del usuario que se va a actualizar sirve para identificar el usuario en la base de datos
    except models.userAdmin.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = EmpresaSerializer(user, data=request.data, partial=True)  # partial=True permite actualizar solo algunos campos
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#-------------------------------------------------------------------------------------------------------#