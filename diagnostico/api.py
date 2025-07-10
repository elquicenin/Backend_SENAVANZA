from .metodo_diagnostico import RecomendarPrograma
from rest_framework.decorators import api_view
from rest_framework.response import Response
import unicodedata

def limpiar_texto(texto):
    if not texto:
        return ""
    # quitar las tildes
    texto = unicodedata.normalize("NFD", texto).encode('ascii', 'ignore').decode('utf-8')
    # quitar caracteres especiales y espacios en blanco
    texto = texto.lower().replace(' ','')
    return texto

@api_view(['POST'])
def DiagnosticoEmpresarial(request):
    
    Requirement = request.data.get('RequirementEmpresa')
    nivel_programa = request.data.get('nivel_programa')
    tools = request.data.get('tools')
    hards_kills = request.data.get('hards_kills')
    #en la variables superiores se esperan las los datos ingresados desde el front end para poder usarlos mas abajo

    #normalizo el nivel de programa 
    nivel_programa = limpiar_texto(nivel_programa)

    if not Requirement or not nivel_programa: #Verificamos negando los datos para no tener que poner elif o else, lo cual permite que los datos si se ingresen y no pueda ser ejecutado o tener un crash
        return Response({"error": "Datos incompletos"}, status=400)
    
    #declaramos la variable recomend_program para invocar el metodo que le pasaramemos como parametros lo enviado por le frontend
    recomend_program = RecomendarPrograma(Requirement, nivel_programa, tools, hards_kills)

    if "error" in recomend_program:#usamos la negacion para validar si el metodo RecomendarPrograma arroja un error de coincidencia no accedera a los atributos de los programas de formacion 
        return Response({"error": recomend_program["error"]}, status=404)
    
    return Response({
        "programa_recomendado": {
        "nombre": recomend_program["nombre"],
        "descripcion": recomend_program["descripcion"],
        "nivel_programa": recomend_program["nivel_programa"]
                }
            }, status=200)
            
            