from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.db import connection
from .models import Equipa, Utilizador, Torneio, PartidaTorneio 

def pagina_inicial(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT j.nickname, 
                   (COALESCE(e.kills, 0) + COALESCE(e.assists, 0)) / GREATEST(COALESCE(e.deaths, 1), 1) AS kda
            FROM estatisticas_jogador e
            JOIN jogadores j ON e.jogador_id = j.id
            ORDER BY kda DESC 
            LIMIT 5
        """)
        top_jogadores = cursor.fetchall()

    top_equipas = Equipa.objects.all().extra(
        select={'winrate': 'vitorias / (vitorias + derrotas + 0.01) * 100'}
    ).order_by('-vitorias')[:5]

    torneios_recentes = Torneio.objects.all().order_by('-data_inicio')[:3]

    context = {
        'top_jogadores': top_jogadores,
        'top_equipas': top_equipas,
        'torneios_recentes': torneios_recentes,
    }
    
    return render(request, 'core/PaginaInicial.html', context)

def comunidade(request):
    return render(request, 'core/Comunidade.html')

def login_view(request):
    erro = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nickname, password FROM utilizadores WHERE email = %s", [email])
            row = cursor.fetchone()
            
            if row and check_password(password, row[2]):
                # Guarda o ID na sessão de forma segura e encriptada pelo Django
                request.session['utilizador_id'] = row[0]
                request.session['utilizador_nickname'] = row[1]
                return redirect('pagina_inicial')
            else:
                erro = "E-mail ou palavra-passe incorretos."
                
    return render(request, 'core/login.html', {'error': erro})

def registo_view(request):
    erro = None
    if request.method == 'POST':
        nome = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        
        if password != confirm_password:
            erro = "As palavras-passe não coincidem."
        else:
            with connection.cursor() as cursor:
                # Verifica se o e-mail ou nickname já existem
                cursor.execute("SELECT id FROM utilizadores WHERE email = %s OR nickname = %s", [email, username])
                if cursor.fetchone():
                    erro = "O e-mail ou o nome de jogador já estão em uso."
                else:
                    hashed_password = make_password(password)
                    # Inserção SQL direta na tabela personalizada
                    cursor.execute(
                        "INSERT INTO utilizadores (nome, nickname, email, password) VALUES (%s, %s, %s, %s)",
                        [nome, username, email, hashed_password]
                    )
                    # Redireciona imediatamente para a página inicial após criar conta
                    return redirect('pagina_inicial')
                    
    return render(request, 'core/registo.html', {'error': erro})

def logout_view(request):
    request.session.flush()
    return redirect('pagina_inicial')

def torneios(request):
    # Vai buscar todos os torneios à base de dados
    todos_torneios = Torneio.objects.all().order_by('data_inicio')
    
    context = {
        'torneios': todos_torneios,
    }
    return render(request, 'core/torneios.html', context)

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

def teste_view(request):
    # SELECT * FROM equipas
    equipas = Equipa.objects.all()
    return render(request, 'core/teste.html', {'equipas': equipas})