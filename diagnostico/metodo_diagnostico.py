from Users.models import ProgramaFormacion
from sentence_transformers import SentenceTransformer, util
import torch
from rest_framework.views import APIView
from rest_framework.response import Response
model = SentenceTransformer('all-MiniLM-L6-v2')





def RecomendarPrograma(requirementEmpresa, nivel_programa):
    programas = ProgramaFormacion.objects.all()
    if not programas.exists():
        return {"error": "no se encontraron programas relacionados con lo requerido"}
    programas_filtrados = list(programas)
    descripciones = [p.descripcion for p in programas_filtrados]

    # Embeddings
    embeddings_descripciones = model.encode(descripciones, convert_to_tensor=True)
    embeddings_requirement = model.encode(requirementEmpresa, convert_to_tensor=True)

    # Similitud de descripción (coseno)
    similitudes_desc = util.pytorch_cos_sim(embeddings_requirement, embeddings_descripciones).cpu().numpy().flatten()

    # Similitud de nivel_programa (1 si coincide, 0 si no)
    similitudes_nivel = [1.0 if p.nivel_programa == nivel_programa else 0.0 for p in programas_filtrados]

    # Ponderación: 70% descripción, 30% nivel_programa
    similitud_total = [0.7 * desc + 0.3 * nivel for desc, nivel in zip(similitudes_desc, similitudes_nivel)]

    # Mejor programa
    idx_mejor = int(torch.tensor(similitud_total).argmax())
    mejor_programa = programas_filtrados[idx_mejor]

    return {
        "nombre": mejor_programa.nombre,
        "descripcion": mejor_programa.descripcion,
        "nivel_programa": mejor_programa.nivel_programa,
        "porcentaje_similitud": round(similitud_total[idx_mejor] * 100, 2)
    }



