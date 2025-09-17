from django .urls import path
from .api import login_admin, login_empresa, logout ,verify ,CustomtokenObtainPairView, CustomTokenRefreshView, send_reset_code, confirm_reset_code, confirm_password


urlpatterns = [
    # el path que precede a estas rutas es login/
    path('loginAdmin/', login_admin, name='login_admin'),
    path('loginEmpresa/', login_empresa, name='login_empresa'),
    path('logout/', logout, name='logout'),
    path('token/', CustomtokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', verify, name='verify'),
    path('verify/', verify, name='verify'),
    path('code-reset/', send_reset_code, name='reset_password'), #el include permite incluir las urls de la app Login bajo el prefijo login/'
    path('confirm-code/', confirm_reset_code, name='confirm_code'), #el include permite incluir las urls de la app Login bajo el prefijo login/'
    path('confirm-password/', confirm_password, name='confirm_reset'), #el include permite incluir las urls de la app Login bajo el prefijo login/'
]