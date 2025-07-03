from .api import user_create, user_empresa_list, user_empresa_detail,user_empresa_create, user_empresa_update, programa_list, programa_create, programa_detail, user_detail, users_detail
from django.urls import path


# la URL que precede a las urls de la app Users es 'api/', por lo que las urls de la app Users quedarán bajo el prefijo 'api/empresa/' y 'api/programa/'
urlpatterns = [ 

    path('user/create/', user_create, name='user_create'),
    path('user/', user_detail, name='user_detail'),
    path('users/', users_detail, name='users_detail'),

    path('empresa/', user_empresa_list, name='user_empresa_list'),
    path('empresa/create/', user_empresa_create, name='user_empresa_create'),
    path('empresa/<str:pk>/', user_empresa_detail, name='user_empresa_detail'),
    path('empresa/update/<str:pk>/', user_empresa_update, name='user_empresa_update'),

    path('programas/', programa_list, name='programa_list'),
    path('programa/create/', programa_create, name='programa_create'),
    path('programa/<str:pk>/', programa_detail, name='programa_detail'),
]