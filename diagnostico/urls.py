from django.urls import path
from .api import DiagnosticoEmpresarial

urlpatterns = [
    path('diagnostico/', DiagnosticoEmpresarial, name='diagnostico_empresarial'),

]

