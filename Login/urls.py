from django .urls import path
from .api import login_admin, login_empresa
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api import login_admin, login_empresa, logout, verify ,CustomtokenObtainPairView, CustomTokenRefreshView


urlpatterns = [
    path('loginAdmin/', login_admin, name='login_admin'),
    path('loginEmpresa/', login_empresa, name='login_empresa'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout, name='logout'),
    path('token/', CustomtokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', verify, name='verify'),
]