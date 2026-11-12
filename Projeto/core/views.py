from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.db import connection
from .models import Equipa, Utilizador

def pagina_inicial(request):
    return render(request, 'core/PaginaInicial.html')

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
                # Login efetuado com sucesso (redireciona diretamente)
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
    return redirect('pagina_inicial')

def torneios(request):
    return render(request, 'core/torneios.html')

def teste_view(request):
    # SELECT * FROM equipas
    equipas = Equipa.objects.all()
    return render(request, 'core/teste.html', {'equipas': equipas})