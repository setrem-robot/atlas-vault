---
title: "Decisões — por que o projeto é assim"
tipo: decisao
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - decisao
---

# Decisões — por que o projeto é assim

| ID | Decisão | Estado | Motivo / consequência |
|---|---|---|---|
| DEC-01 | Raspberry Pi como único computador/controlador principal, retirando a ponte ESP32 | Direção confirmada pelo usuário; BLE já implementado | Menos uma placa e uma serial no caminho de comando |
| DEC-02 | Preservar NUS/JSON e tópico de entrada ao trocar transporte | Implementada no código | App e serviços mantêm contrato apesar de mudar a ponte |
| DEC-03 | Mensagens MQTT entre componentes | Implementada | Serviços separados por responsabilidade |
| DEC-04 | API de leitura separada da ingestão | Implementada | Aplicativo consulta dados sem acesso direto ao banco |
| DEC-05 | Movimento precisa ser renovado; silêncio dispara parada | Implementada, pendente de validação física atual | Tratar perda de comunicação sem depender do último `S` |
| DEC-06 | Cinemática separada do hardware, com simulação | Implementada | Permitir desenvolvimento e testes sem robô |
| DEC-07 | IA/voz de rede com alternativa local configurável | Código implementado e uso relatado | Continuar interagindo sem rede, com diferenças de qualidade |
| DEC-08 | Vosk como padrão de escuta | Implantada em `producao` `43a6fe0` e medida no Pi; precisão com voz humana pendente | Reconhecer durante a fala corta 1,7–2,3 s de silêncio depois da pergunta. Custa precisão; trocar de volta é uma variável. Ver [[wiki/revisoes/2026-09-09-escuta-vosk-hardware]] |
| DEC-09 | Um único broker local | Necessidade documentada; configuração efetiva pendente | Evitar conflito apt/Docker na porta 1883 |
| DEC-10 | Rota planejada sem assumir navegação pronta | Estado atual documentado | Não confundir envio de pontos com execução autônoma |
| DEC-11 | Separar evidência histórica, código, implantação e proposta | Adotada neste vault | Manter narrativa verificável e atualizável |
| DEC-12 | Nuvem hospedada na VM do LARCC, Pi alcançando-a por Tailscale | Implantada em 02/10/2026 | Tirar a nuvem do servidor doméstico; telemetria sobe de qualquer rede sem expor MQTT à internet. Ver [[wiki/historico/registro-de-trabalho]] |

O motivo de uma decisão implementada foi extraído das fontes quando descrito. Não foi atribuída autoria individual a decisões coletivas sem evidência. Para novas decisões, usar [[modelos/Decisao]] com alternativas, impactos, fonte e status.

DEC-01 não estabelece que o banco ou toda IA precisam rodar exclusivamente no Pi: o objetivo explicitado foi retirar o ESP32 da eletrônica embarcada. Ver [[wiki/planejamento/onde-queremos-ir]].

## Fontes e conferência

- [RobotEye/src/roboteye/ble/nus.py](https://github.com/setrem-robot/atlas_ai_v2/blob/43a6fe025ab5474cc1120d0a71d731392d1234b4/src/roboteye/ble/nus.py)
- [orquestrador/README.md](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/README.md)
- [orquestrador/pi/services/motores/src/motores/main.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/motores/src/motores/main.py)
- [[wiki/diario/2026-09-09]]

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]
