cat << 'EOF' > correlacionar.py
import pandas as pd
import json

# 1. Carregar os carimbos temporais da Telemetria do Sistema Operativo (CSV) em UTC
ataques = pd.read_csv('ataques_teste.csv')
ataques['timestamp_utc'] = pd.to_datetime(ataques['timestamp_utc'])

# 2. Carregar os alertas do Wazuh SIEM (JSON) em UTC
with open('alertas_teste.json') as f:
    alertas = json.load(f)

alertas_df = pd.DataFrame(alertas)
alertas_df['timestamp'] = pd.to_datetime(alertas_df['timestamp'])

resultados = []

# 3. Procurar correspondência numa janela de 10 segundos após a execução no Sistema Operativo
for idx, ataque in ataques.iterrows():
    candidatos = alertas_df[
        (alertas_df['timestamp'] >= ataque['timestamp_utc']) &
        (alertas_df['timestamp'] <= ataque['timestamp_utc'] + pd.Timedelta(seconds=10))
    ]

    if len(candidatos) > 0:
        alerta = candidatos.iloc[0]
        latencia = (alerta['timestamp'] - ataque['timestamp_utc']).total_seconds()
        resultados.append({
            'ferramenta': ataque['ferramenta'],
            'hora_ataque': ataque['timestamp_utc'],
            'hora_alerta': alerta['timestamp'],
            'latencia_segundos': round(latencia, 3),
            'detetado': True
        })
    else:
        resultados.append({
            'ferramenta': ataque['ferramenta'],
            'hora_ataque': ataque['timestamp_utc'],
            'hora_alerta': None,
            'latencia_segundos': None,
            'detetado': False
        })

# 4. Mostrar tabela final, Taxa de Deteção Global e MTTD
df_final = pd.DataFrame(resultados)
print(df_final.to_string(index=False))
print("\nTaxa de deteção global: " + str(round(df_final['detetado'].mean() * 100, 2)) + "%")
print("MTTD (Tempo Médio de Deteção): " + str(round(df_final['latencia_segundos'].mean(), 3)) + " segundos")
EOF

python3 correlacionar.py | tee resultado_correlacao.txt

#PROIBIDA A UTILIZAÇÃO EM PORTFÓLIO
#O código e os artefatos contidos neste repositório pertencem ao Projeto Final do curso Técnico em Cibersegurança e servem estritamente para fins de validação interna de métricas. Fica vedada a publicação, cópia ou exibição deste trabalho em portfólios, sites pessoais ou redes profissionais por terceiros. O uso não autorizado constitui violação de propriedade intelectual dos colaboradores.



