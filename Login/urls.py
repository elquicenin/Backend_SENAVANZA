from django .urls import path
from .api import login_admin, login_empresa, logout, verify ,CustomtokenObtainPairView, CustomTokenRefreshView
from .api import login_admin, login_empresa, logout , verify,CustomtokenObtainPairView, CustomTokenRefreshView


urlpatterns = [
    # el path que precede a estas rutas es login/
    path('loginAdmin/', login_admin, name='login_admin'),
    path('loginEmpresa/', login_empresa, name='login_empresa'),
    path('logout/', logout, name='logout'),
    path('token/', CustomtokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', verify, name='verify'),
]