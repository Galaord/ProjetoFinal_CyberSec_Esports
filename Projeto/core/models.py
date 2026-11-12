from django.db import models

class Equipa(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    tag = models.CharField(max_length=10, unique=True)
    pais = models.CharField(max_length=60, blank=True, null=True)
    vitorias = models.IntegerField(default=0)
    derrotas = models.IntegerField(default=0)

    class Meta:
        db_table = 'equipas'

    def __str__(self):
        return self.nome

class Utilizador(models.Model):
    nome = models.CharField(max_length=100)
    nickname = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)  # Palavra-passe encriptada (Hash)
    data_registo = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'utilizadores'

    def __str__(self):
        return self.nickname