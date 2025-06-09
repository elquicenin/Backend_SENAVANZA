from Users.models import ProgramaFormacion
from sentence_transformers import SentenceTransformer, util
import torch
from rest_framework.views import APIView
from rest_framework.response import Response
model = SentenceTransformer('all-MiniLM-L6-v2')





def RecomendarPrograma(requirementEmpresa, nivel_programa):

    programas = ProgramaFormacion.objects.filter(nivel_programa=nivel_programa)
    if not programas:
        return None
    # Filtrar programas por el nivel proporcionado
    programas_filtrados = [p for p in programas if p.nivel_programa == nivel_programa]

    # Extraemos las descripciones de los programas filtrados
    descripciones = [p.descripcion for p in programas_filtrados]
    # Convertimos las descripciones a embeddings
    embeddings_descripciones = model.encode(descripciones, convert_to_tensor=True)
    embeddings_requirement = model.encode(requirementEmpresa, convert_to_tensor=True)

    # Calculamos la similitud entre el embedding de la descripción del programa y el embedding de los requisitos de la empresa
    similitudes = util.pytorch_cos_sim(embeddings_requirement, embeddings_descripciones)

    # Obtenemos el índice del programa con la mayor similitud
    recomend_program = torch.argmax(similitudes, dim=1).item()

    return programas_filtrados[recomend_program]
    


