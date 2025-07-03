from Users.models import ProgramaFormacion
from sentence_transformers import SentenceTransformer, util
import torch
from rest_framework.views import APIView
from rest_framework.response import Response
model = SentenceTransformer('all-MiniLM-L6-v2')





def RecomendarPrograma(requirementEmpresa, nivel_programa):

    programas = ProgramaFormacion.objects.filter(nivel_programa=nivel_programa)
    if not programas.exists():
        return ({"error": "no se encontraron programas relacionados con lo requerido"})
    # Filtrar programas por el nivel proporcionado
    programas_filtrados = list(programas)

    # Extraemos las descripciones de los programas filtrados
    descripciones = [p.descripcion for p in programas_filtrados]

    # Convertimos las descripciones a embeddings
    embeddings_descripciones = model.encode(descripciones, convert_to_tensor=True)
    embeddings_requirement = model.encode(requirementEmpresa, convert_to_tensor=True)

    # Calculamos la similitud entre el embedding de la descripción del programa y el embedding de los requisitos de la empresa
    similitudes = util.pytorch_cos_sim(embeddings_requirement, embeddings_descripciones)


    
    # Obtenemos el índice del programa con la mayor similitud
    recomend_program = torch.argmax(similitudes).item()

    mejor_programa = programas_filtrados[recomend_program]

    

    return {
        "nombre": mejor_programa.nombre,
        "descripcion": mejor_programa.descripcion,
        "nivel_programa": mejor_programa.nivel_programa
    }
    


