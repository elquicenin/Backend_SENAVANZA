"""
URL configuration for SENAVANZA2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Users import urls 
from django.urls import include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urls.urlpatterns)),  # el include permite incluir las urls de la app Users bajo el prefijo 'api/'
    path('login/', include('Login.urls')),  # el include permite incluir las urls de la app Login bajo el prefijo 'api/login/'
    path('apidiagnos/', include('diagnostico.urls')),  # el include permite incluir las urls de la app diagnostico bajo el prefijo 'api/diagnostico/'
]
