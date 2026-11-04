from django.shortcuts import render, get_object_or_404
from .models import Equipa, Torneio, PartidaTorneio 

def pagina_inicial(request):
    return render(request, 'core/PaginaInicial.html')

def comunidade(request):
    return render(request, 'core/Comunidade.html')

def login_view(request):
    return render(request, 'core/login.html')

def registo_view(request):
    return render(request, 'core/registo.html')

def torneios(request):
    # Vai buscar todos os torneios à base de dados
    todos_torneios = Torneio.objects.all().order_by('data_inicio')
    
    context = {
        'torneios': todos_torneios,
    }
    return render(request, 'core/torneios.html', context)

def teste_view(request):  # Eliminar mais tarde
    # SELECT * FROM equipas
    equipas = Equipa.objects.all()
    return render(request, 'core/teste.html', {'equipas': equipas})

def detalhe_torneio_view(request, torneio_id):
    # Vai buscar o torneio específico ou retorna erro 404
    torneio = get_object_or_404(Torneio, pk=torneio_id)
    
    # Filtra diretamente as partidas associadas a este torneio de forma segura e otimizada
    partidas = PartidaTorneio.objects.filter(torneio=torneio).select_related('equipa1', 'equipa2', 'vencedor').order_by('data_jogo')

    # Equipas inscritas no torneio
    inscricoes = torneio.inscricoes_torneio_set.all() if hasattr(torneio, 'inscricoes_torneio_set') else []

    context = {
        'torneio': torneio,
        'partidas': partidas,
        'inscricoes': inscricoes,
    }
    return render(request, 'core/detalhe_torneio.html', context)