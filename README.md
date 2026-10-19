# Manual de Instalação do Django e Uso da Aplicação

## Base de Dados

Começar por importar a base de dados através do ficheiro *bd_torneios.sql* (Este ficheiro não tem uma query de create database, então precisam de criar a base de dados manualmente antes de executar ou adicionar *CREATE DATABASE bd_torneios;* antes do primeiro *CREATE TABLE*)

## Instalação do Django

Primeiro verificar se tem o Python instalado no computador. No CMD escreva:
```
python --version
```
Se não tiver instalado é necessário instalar.

Cria uma pasta para o projeto e navega até essa pasta no CMD (O vosso caminho e o nome da pasta pode ser diferente).
```
cd desktop/projeto
```

Ainda no CMD siga os seguintes passos:
```
python -m venv venv
```
```
venv\Scripts\activate
```
```
pip install django pymysql
```
```
django-admin startproject nexus_arena .
```
```
python manage.py startapp core
```

## Importar os Ficheiros da Aplicação

Depois adiciona dentro da pasta **core** cria uma nova pasta chamada **templates** e dentro dessa nova pasta outra chamada **core**.
A Estrutura deve ser a seguinte **core > templates > core**

Após isso copia todos os ficheiros disponíveis neste repositório para as suas correspondentes pastas, substituindo os ficheiros sempre que for pedido.

## Correr a aplicação

Por fim, voltar ao CMD e executar o comando:
```
python manage.py runserver
```

Para desligar o servidor do Django basta pressionar as teclas **Ctrl** + **C** no CMD. Para o voltar a ligar é só repetir o comando anterior desde que não feche o CMD.

Sempre que fecharem o CMD tem que executar os seguintes comandos:
Primeiro navegar até à pasta do projeto (O vosso caminho e o nome da pasta pode ser diferente).
```
cd desktop/projeto
```
```
venv\Scripts\activate
```
```
python manage.py runserver
```
