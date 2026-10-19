from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('comunidade/', views.comunidade, name='comunidade'),
    path('login/', views.login_view, name='login'),
    path('registo/', views.registo_view, name='registo'),
    path('torneios/', views.torneios, name='torneios'),
    path('teste/', views.teste_view, name='teste'),
]