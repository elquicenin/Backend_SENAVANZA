from .metodo_diagnostico import RecomendarPrograma
from rest_framework.decorators import api_view
from rest_framework.response import Response



@api_view(['POST'])
def DiagnosticoEmpresarial(request):
    if request.method != 'POST':
        return Response({"error": "Método no permitido"}, status=405)
    Requirement = request.data.get('RequirementEmpresa')
    nivel_programa = request.data.get('nivel_programa')
    if not nivel_programa:
        return Response({"error": "Nivel de programa no proporcionado"}, status=400)
    recomend_program = RecomendarPrograma(Requirement, nivel_programa)
    if not recomend_program:
        return Response({"error": "No se encontraron programas de formación para lo requerido"}, status=404)
    return Response({
        "programa_recomendado": {
        "id": recomend_program.id,
        "nombre": recomend_program.nombre,
        "descripcion": recomend_program.descripcion,
        "nivel_programa": recomend_program.nivel_programa
                }
            }, status=200)
            
            