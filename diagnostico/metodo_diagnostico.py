from Users.models import ProgramaFormacion
from sentence_transformers import SentenceTransformer, util
import torch
from rest_framework.views import APIView
from rest_framework.response import Response
model = SentenceTransformer('all-MiniLM-L6-v2')





def RecomendarPrograma(requirementEmpresa, nivel_programa, tools, hards_kills):

    programas = ProgramaFormacion.objects.filter(nivel_programa=nivel_programa)
    if not programas.exists():
        return {"error": "no se encontraron programas relacionados con lo requerido"}
    programas_filtrados = list(programas)
    descripciones = [p.descripcion for p in programas_filtrados]

    # Embeddings
    embeddings_descripciones = model.encode(descripciones, convert_to_tensor=True)
    embeddings_requirement = model.encode(requirementEmpresa, convert_to_tensor=True)
    embeddings_tools = model.encode(tools, convert_to_tensor=True)
    embeddings_hard_skills = model.encode(hards_kills, convert_to_tensor=True)

    # Calculamos la similitud entre el embedding de la descripción del programa y el embedding de los requisitos de la empresa
    similitud_programa_con_requirement = util.pytorch_cos_sim(embeddings_requirement, embeddings_descripciones)
    similitud_tools = util.pytorch_cos_sim(embeddings_tools, embeddings_descripciones)
    similitud_hard_skills = util.pytorch_cos_sim(embeddings_hard_skills, embeddings_descripciones)
    # Combinamos las similitudes
    similitudes = (similitud_programa_con_requirement + similitud_tools + similitud_hard_skills) / 3
    # Obtenemos el índice del programa con la mayor similitud
    
    recomend_program = torch.argmax(similitudes).item()

    mejor_programa = programas_filtrados[recomend_program]

    

    return {
        "nombre": mejor_programa.nombre,
        "descripcion": mejor_programa.descripcion,
        "nivel_programa": mejor_programa.nivel_programa,
        "porcentaje_similitud": round(similitud_total[idx_mejor] * 100, 2)
    }



