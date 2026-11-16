# Playbook de Resposta a Incidentes — [TÍTULO DO CENÁRIO]

> **Modelo em branco para preenchimento após definição e validação do cenário.**  
> Documento de trabalho do projeto final de Cibersegurança. Não representa um incidente ocorrido ou um procedimento já testado.

| Campo | Informação |
|---|---|
| Código do playbook | [A preencher] |
| Versão | [A preencher] |
| Data de elaboração/revisão | [A preencher] |
| Responsável | [A preencher] |
| Estado | [Rascunho / Em revisão / Validado] |
| Ambiente autorizado para testes | [A preencher] |

## 1. Nome do Cenário

- **Tipo de incidente:** [A preencher]
- **Descrição do cenário:** [A preencher]
- **Sistemas e serviços potencialmente afetados:** [A preencher]
- **Objetivo do procedimento:** [A preencher]

## 2. Gatilho — Deteção / Alerta Wazuh

- **Fonte da deteção:** [A preencher]
- **Regra/ID e nível do alerta (se aplicável):** [A preencher após verificação]
- **Evento que inicia o playbook:** [A preencher]
- **Critérios para distinguir alerta real de falso positivo:** [A preencher]

## 3. Triagem

- **O que verificar inicialmente:** [A preencher]
- **Dados a registar (IP, host, utilizador, horário UTC):** [A preencher]
- **Como confirmar a ocorrência e avaliar a gravidade:** [A preencher]
- **Responsável pela confirmação:** [A preencher]

## 4. Contenção Imediata

- **Medidas de contenção propostas:** [A preencher]
- **Quem autoriza e quem executa cada medida:** [A preencher]
- **Impacto esperado e precauções para proteger a produção:** [A preencher]
- **Como confirmar que a contenção funcionou:** [A preencher]

## 5. Erradicação

- **Causa ou vulnerabilidade a corrigir:** [A preencher]
- **Ações corretivas:** [A preencher]
- **Equipa responsável pela correção:** [A preencher]
- **Forma de verificar a remoção da ameaça:** [A preencher]

## 6. Recuperação

- **Passos para restaurar o serviço:** [A preencher]
- **Testes de funcionamento e segurança:** [A preencher]
- **Condições para terminar o incidente:** [A preencher]
- **Monitorização após a recuperação:** [A preencher]

## 7. Evidências a Preservar

- **Registos, capturas e outros ficheiros necessários:** [A preencher]
- **Caminhos reais dos ficheiros/pastas:** [A preencher]
- **Data e hora da recolha em UTC:** [A preencher]
- **Hash SHA-256 de cada evidência (quando aplicável):** [A preencher]
- **Responsável pela recolha e cadeia de custódia:** [A preencher]
- **Local de armazenamento seguro:** [A preencher]

## 8. Comunicação e Registo do Incidente

- **Pessoas/equipas a informar:** [A preencher]
- **Critérios de escalonamento:** [A preencher]
- **Cronologia das ações e horários em UTC:** [A preencher]
- **Decisões e autorizações recebidas:** [A preencher]
- **Resultado dos testes/ocorrência:** [Não testado — preencher após execução]
- **Lições aprendidas e alterações propostas ao playbook:** [A preencher]
- **Referências técnicas e documentos consultados:** [A preencher]

---

**Nota de utilização:** duplicar este ficheiro para cada cenário aprovado pelo grupo. Preencher IDs de regras, comandos, endereços, responsáveis e resultados apenas depois de serem confirmados. Registar separadamente a diferença entre testes simulados e incidentes reais. Evitar publicar credenciais, dados pessoais ou logs sensíveis num repositório público.
