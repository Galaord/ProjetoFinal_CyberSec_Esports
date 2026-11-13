from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('comunidade/', views.comunidade, name='comunidade'),
    path('login/', views.login_view, name='login'),
    path('registo/', views.registo_view, name='registo'),
    path('logout/', views.logout_view, name='logout'),
    path('torneios/', views.torneios, name='torneios'),
    path('torneios/<int:torneio_id>/', views.detalhe_torneio_view, name='detalhe_torneio'),
    path('teste/', views.teste_view, name='teste'),
]