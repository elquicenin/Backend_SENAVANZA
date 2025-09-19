from rest_framework.decorators import api_view
from rest_framework.response import Response
from Users.models import ProgramaFormacion
from sentence_transformers import SentenceTransformer, util
import torch

# Modelo de embeddings más preciso
model = SentenceTransformer('all-mpnet-base-v2')

def RecomendarPrograma(requirementEmpresa, nivel_programa, tools, hards_kills):
    # Filtrar programas según nivel
    programas = ProgramaFormacion.objects.filter(nivel_programa=nivel_programa)
    if not programas.exists():
        return {"error": "No se encontraron programas relacionados con el nivel de formación solicitado"}

    programas_filtrados = list(programas)
    descripciones = [p.descripcion for p in programas_filtrados]

    #  Embeddings de todos los elementos
    embeddings_descripciones = model.encode(descripciones, convert_to_tensor=True)
    embeddings_requirement = model.encode(requirementEmpresa, convert_to_tensor=True)
    embeddings_tools = model.encode(tools, convert_to_tensor=True)
    embeddings_hard_skills = model.encode(hards_kills, convert_to_tensor=True)

    #  Calcular similitudes
    similitud_programa_con_requirement = util.pytorch_cos_sim(embeddings_requirement, embeddings_descripciones)
    similitud_tools = util.pytorch_cos_sim(embeddings_tools, embeddings_descripciones)
    similitud_hard_skills = util.pytorch_cos_sim(embeddings_hard_skills, embeddings_descripciones)

    # porcentaje similitudes#
    peso_requirement = 0.3
    peso_tools = 0.4
    peso_skills = 0.3

    # Promedio simple de similitudes
    similitudes = (similitud_programa_con_requirement*peso_requirement + similitud_tools*peso_tools + similitud_hard_skills*peso_skills) 

    #  Programa con mayor similitud
    recomend_program = torch.argmax(similitudes).item()
    mejor_programa = programas_filtrados[recomend_program]

    
    return {
        "nombre": mejor_programa.nombre,
        "descripcion": mejor_programa.descripcion,
        "nivel_programa": mejor_programa.nivel_programa,
    }
