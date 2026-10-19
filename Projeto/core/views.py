from django.shortcuts import render
from .models import Equipa

def pagina_inicial(request):
    return render(request, 'core/PaginaInicial.html')

def comunidade(request):
    return render(request, 'core/Comunidade.html')

def login_view(request):
    return render(request, 'core/login.html')

def registo_view(request):
    return render(request, 'core/registo.html')

def torneios(request):
    return render(request, 'core/torneios.html')

def teste_view(request):
    # SELECT * FROM equipas
    equipas = Equipa.objects.all()
    return render(request, 'core/teste.html', {'equipas': equipas})