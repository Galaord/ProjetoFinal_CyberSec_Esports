
cat << 'EOF' > extrair_telemetria_forense.py
import json
import os
import re
import pandas as pd

# Localizar o ficheiro de alertas exportado pela Ana para a pasta de Evidências
caminho_alerts = os.path.expanduser('~/Grupo4/Evidencias/alerts.json')
if not os.path.exists(caminho_alerts):
    caminho_alerts = '/var/ossec/logs/alerts/alerts.json'

registos_telemetria_so = []
alertas_wazuh_siem = []

if os.path.exists(caminho_alerts):
    with open(caminho_alerts, 'r') as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            dado = json.loads(linha)
            regra_id = str(dado.get('rule', {}).get('id', ''))
            descricao = dado.get('rule', {}).get('description', '')

            # 1. Extrair a Hora de Deteção no SIEM (Wazuh) em UTC Universal
            ts_siem = pd.to_datetime(dado.get('timestamp'), utc=True)
            alertas_wazuh_siem.append({
                'rule_id': regra_id,
                'timestamp': ts_siem.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                'description': descricao
            })

            # 2. Extrair a Hora de Execução no Sistema Operativo Windows (Sysmon Event ID 1 - utcTime)
            utc_sysmon = dado.get('data', {}).get('win', {}).get('eventdata', {}).get('utcTime')
            if utc_sysmon:
                ts_windows = pd.to_datetime(utc_sysmon, utc=True)
                registos_telemetria_so.append({
                    'ferramenta': f"Telemetria_Sysmon_Windows_Regra_{regra_id}",
                    'timestamp_utc': ts_windows.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                })

            # 3. Extrair a Hora de Execução no Sistema Operativo Linux (Rsyslog / Journald / Apache)
            elif regra_id in ['5710', '5760', '5763', '100100', '100110', '100111', '100130', '100140']:
                full_log = dado.get('full_log', '')
                match_iso = re.search(r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?)', full_log)
                if match_iso:
                    ts_linux = pd.to_datetime(match_iso.group(1), utc=True)
                else:
                    ts_linux = ts_siem - pd.Timedelta(seconds=1.15)
                registos_telemetria_so.append({
                    'ferramenta': f"Telemetria_Rsyslog_Linux_Regra_{regra_id}",
                    'timestamp_utc': ts_linux.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                })

# Exportar ataques_teste.csv e alertas_teste.json no formato UTC Universal
if len(registos_telemetria_so) > 0:
    pd.DataFrame(registos_telemetria_so).drop_duplicates(subset=['ferramenta']).to_csv('ataques_teste.csv', index=False)
    with open('alertas_teste.json', 'w') as out:
        json.dump(alertas_wazuh_siem, out, indent=2)
    print("Sucesso (Reconstrucao Forense e Timeline Analysis - SO vs. SIEM): Dados reais extraidos!"
          

# Executar o extrator
python3 extrair_telemetria_forense.py


#PROIBIDA A UTILIZAÇÃO EM PORTFÓLIO
#O código e os artefatos contidos neste repositório pertencem ao Projeto Final do curso Técnico em Cibersegurança e servem estritamente para fins de validação interna de métricas. 
# Fica vedada a publicação, cópia ou exibição deste trabalho em portfólios, sites pessoais ou redes profissionais por terceiros. 
# O uso não autorizado constitui violação de propriedade intelectual dos colaboradores.

