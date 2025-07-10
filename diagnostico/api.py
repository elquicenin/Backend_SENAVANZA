from .metodo_diagnostico import RecomendarPrograma
from rest_framework.decorators import api_view
from rest_framework.response import Response
import unicodedata
import re

# 🔹 Normaliza texto (nivel_programa)
def limpiar_texto(texto):
    if not texto:
        return ""
    texto = unicodedata.normalize("NFD", texto).encode('ascii', 'ignore').decode('utf-8')
    texto = texto.lower().replace(' ', '')
    return texto

# 🔸 Valida que el texto tenga sentido y no sea ruido
def entrada_valida(texto):
    if not texto:
        return False
    texto = texto.strip().lower()
    if len(texto) < 10:
        return False
    if len(set(texto)) <= 2:  # evita "aaaaaa", "111111", "zzzz"
        return False
    palabras = re.findall(r'\b\w+\b', texto)
    if len(palabras) < 2:
        return False
    return True

@api_view(['POST'])
def DiagnosticoEmpresarial(request):
    print('datos recibidos', request.data)

    Requirement = request.data.get('RequirementEmpresa')
    nivel_programa = request.data.get('nivel_programa')
    tools = request.data.get('tools')
    hards_kills = request.data.get('hards_kills')

    # Normaliza el campo estructurado
    nivel_programa = limpiar_texto(nivel_programa)

    # Validación de que existan los campos
    if not all([Requirement, nivel_programa, tools, hards_kills]):
        return Response({"error": "Faltan campos obligatorios."}, status=400)

    # Validación semántica de los textos
    if not (entrada_valida(Requirement) and entrada_valida(tools) and entrada_valida(hards_kills)):
        return Response({"error": "Por favor ingresa información válida y con sentido en todos los campos."}, status=400)

    recomend_program = RecomendarPrograma(Requirement, nivel_programa, tools, hards_kills)

    if "error" in recomend_program:
        return Response({"error": recomend_program["error"]}, status=404)

    return Response({
        "programa_recomendado": {
            "nombre": recomend_program["nombre"],
            "descripcion": recomend_program["descripcion"],
            "nivel_programa": recomend_program["nivel_programa"]
        }
    }, status=200)
