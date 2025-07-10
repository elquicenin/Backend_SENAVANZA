from rest_framework.decorators import api_view
from rest_framework.response import Response
from Users.models import ProgramaFormacion
from sentence_transformers import SentenceTransformer, util
import torch
import re
import unicodedata

# Modelo de embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')



def RecomendarPrograma(requirementEmpresa, nivel_programa, tools, hards_kills):
    programas = ProgramaFormacion.objects.filter(nivel_programa=nivel_programa)
    if not programas.exists():
        return {"error": "No se encontraron programas relacionados con el nivel de formación solicitado"}

    programas_filtrados = list(programas)
    descripciones = [p.descripcion for p in programas_filtrados]

    # Embeddings
    embeddings_descripciones = model.encode(descripciones, convert_to_tensor=True)
    embeddings_requirement = model.encode(requirementEmpresa, convert_to_tensor=True)
    embeddings_tools = model.encode(tools, convert_to_tensor=True)
    embeddings_hard_skills = model.encode(hards_kills, convert_to_tensor=True)

    # Similitudes
    similitud_programa_con_requirement = util.pytorch_cos_sim(embeddings_requirement, embeddings_descripciones)
    similitud_tools = util.pytorch_cos_sim(embeddings_tools, embeddings_descripciones)
    similitud_hard_skills = util.pytorch_cos_sim(embeddings_hard_skills, embeddings_descripciones)

    similitudes = (similitud_programa_con_requirement + similitud_tools + similitud_hard_skills) / 3

    recomend_program = torch.argmax(similitudes).item()
    mejor_programa = programas_filtrados[recomend_program]

    return {
        "nombre": mejor_programa.nombre,
        "descripcion": mejor_programa.descripcion,
        "nivel_programa": mejor_programa.nivel_programa,
    }