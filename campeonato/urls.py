"""
URL configuration for campeonato project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# campeonato/urls.py
from django.contrib import admin
from django.urls import path
from tabela import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('standings/', views.standings_view, name='standings'),
    path('add-team/', views.add_team_view, name='add_team'),
    path('add-match/', views.add_match_view, name='add_match'),
    path('update-result/<int:match_id>/', views.update_result_view, name='update_result'),
    path('reset-championship/', views.reset_championship, name='reset_championship'), # Defina a URL nomeada corretamente aqui
    path('', views.standings_view),
]

