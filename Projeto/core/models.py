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

class Torneio(models.Model):
    nome = models.CharField(max_length=100)
    jogo = models.CharField(max_length=30, default='CS2')
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    formato = models.CharField(max_length=10, default='BO3')
    estado = models.CharField(max_length=20, default='Planeado')

    class Meta:
        db_table = 'torneios'

    def __str__(self):
        return self.nome

class PartidaTorneio(models.Model):
    torneio = models.ForeignKey(Torneio, on_delete=models.CASCADE, db_column='torneio_id')
    equipa1 = models.ForeignKey(Equipa, on_delete=models.CASCADE, related_name='partidas_equipa1', db_column='equipa1_id')
    equipa2 = models.ForeignKey(Equipa, on_delete=models.CASCADE, related_name='partidas_equipa2', db_column='equipa2_id')
    vencedor = models.ForeignKey(Equipa, on_delete=models.SET_NULL, null=True, blank=True, related_name='partidas_vencidas', db_column='vencedor_id')
    data_jogo = models.DateTimeField()
    fase = models.CharField(max_length=50)
    formato = models.CharField(max_length=10, default='BO3')
    estado = models.CharField(max_length=20, default='Agendada')
    mapas_equipa1 = models.IntegerField(default=0)
    mapas_equipa2 = models.IntegerField(default=0)

    class Meta:
        db_table = 'partidas_torneio'

    def __str__(self):
        return f"{self.equipa1} vs {self.equipa2} ({self.fase})"

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