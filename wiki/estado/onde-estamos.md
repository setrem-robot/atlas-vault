---
title: "Onde estamos — estado atual do projeto"
tipo: estado
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - estado
---

# Onde estamos — estado atual do projeto

## Leitura correta do estado

**Implementado** significa encontrado no código. **Relatado** significa descrito por uma fonte, sem repetição do teste nesta sessão. **Pendente** significa lacuna documentada ou confirmação necessária. Um recurso pode estar implementado e ainda pendente de validação física.

| Subsistema | Evidência atual | Limite / próximo passo |
|---|---|---|
| Mecânica | Estrutura híbrida e ensaios manuais nos PDFs | Confirmar estado físico, medidas, rodas e alimentação atuais |
| BLE direto no Pi | `RobotEye/ble/nus.py`, serviço e publicação MQTT | Código e relatos de conexão; consolidar instalação sem ESP32 |
| Controle Flutter | Direcional, repetição de 300 ms e parada | Testar desconexão, troca de tela e comportamento real |
| Motores | Backend STEP/DIR, simulação, rampa, vigia de 1 s, RLock | README informa ausência de teste do motor real com esse código |
| Rota segura | Planejamento, persistência local, envio fatiado e roteamento | Não há consumidor de navegação; não segue a rota sozinho |
| GPS | Serviço NMEA e contrato prontos | Montagem e coleta atual não comprovadas; fontes divergem |
| Bateria | Contrato, banco e telas preparados | Não foi encontrado produtor físico de bateria |
| Wi-Fi | Serviço `nmcli`, status e roteamento | Testar aplicação e retorno; confirmar broker único |
| Face e conversa | Pipeline de IA/voz, painel, persona, reservas e recuperação de áudio | Métricas atuais e qualidade com usuários ainda precisam de coleta |
| Escuta | Vosk padrão; alternativa Whisper | Mudanças publicadas em 09/09; validar no ambiente de uso |
| MQTT e nuvem | Broker, bridge, ingestor, TimescaleDB e FastAPI | Disputa apt/Docker documentada; confirmar implantação e perdas |
| Visualização | App, site público e painel local do RobotEye | Distinguir dado simulado, comando recebido e estado medido |
| IA ligada à telemetria | Há integração MQTT para controle/painel | Não há consumo de `robo/voz/falar` pela fala nem contexto de bateria integrado |
| Relatório acadêmico | LaTeX com proposta e capítulos | Capítulo de resultados e estatística em desenvolvimento |

## Versões observadas

- App: `main`, HEAD `44d5001`, versão declarada `1.2.2+9`.
- Orquestrador: `main`, HEAD `98ee681`.
- RobotEye: `producao`, HEAD `43a6fe0`; `main` em `e1b26d7`.
- As três árvores de trabalho estavam limpas e as branches ativas em 0 à frente / 0 atrás do upstream após fetch.

Há histórico local adicional, detalhado em [[wiki/estado/git-local-e-remoto]]. O nome `producao` não prova que esse SHA está instalado no Raspberry Pi.

## Prioridade prática

Consolidar o caminho app → BLE no Pi → broker único → motores, em paralelo à melhoria da IA. Instalar o GPS e comprovar sua chegada ao banco e às telas. Registrar o que é real, simulado, atrasado ou ainda não medido. Ver [[wiki/planejamento/backlog]].

## Fontes e conferência

- [app/pubspec.yaml](https://github.com/setrem-robot/aplicativo/blob/44d500160ecf13d7d1db2a4fe0c54052d352c0aa/pubspec.yaml)
- [orquestrador/README.md](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/README.md)
- [RobotEye/README.md](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/README.md)
- [RobotEye/src/roboteye/config.py](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/src/roboteye/config.py)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]
