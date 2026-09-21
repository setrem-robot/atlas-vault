---
title: "Como funciona — do toque à informação"
tipo: arquitetura
estado_documental: revisado
atualizado: 2026-09-09
tags:
  - atlas
  - arquitetura
---

# Como funciona — do toque à informação

## Um comando de frente

1. O operador pressiona frente no app. `RobotConnection` envia `{"cmd":"F"}` em UTF-8 com quebra de linha e repete o movimento a cada 300 ms.
2. A ponte BLE no Raspberry Pi recebe e valida a linha. O limite é 512 bytes. `EntregaMqtt` publica em `robo/comando/entrada` com QoS 1.
3. O roteador transforma `F` em `{"acao":"frente","velocidade":60}` e publica no tópico `robo/motores/comando`.
4. `ServicoMotores` converte a ação em velocidades esquerda/direita, renova o vigia e pede o alvo à rampa.
5. O laço de 50 ms avança a rampa e chama o backend. No modo simulado, registra os comandos; no real, ajusta STEP/DIR/EN.
6. Ao soltar/cancelar, o app envia `S`. O serviço zera a rampa imediatamente. Se as mensagens param de chegar, o vigia de 1 s também manda parar.

Não foram medidas latências entre essas etapas nesta sessão. O tick de 50 ms é frequência do laço, não taxa fixa de telemetria.

## Uma leitura até o banco

1. O GPS interpreta NMEA e produz `robo/gps/posicao`.
2. O orquestrador espelha para `robo/telemetria/gps`.
3. A bridge leva esse prefixo ao broker remoto; comandos não descem pela bridge configurada.
4. O ingestor extrai o tipo do tópico e usa `ts` numérico do payload, ou o instante de chegada se esse campo for ausente/inválido.
5. O registro entra na tabela `telemetria`, mantendo o payload JSONB.
6. A API consulta o histórico. O app distingue estado atual, trajeto, série e eventos; `idade_s` ajuda a identificar dados antigos.

## Três informações diferentes

| Informação | O que comprova | O que não comprova |
|---|---|---|
| Último botão pressionado | Intenção do operador | Recepção ou movimento |
| Comando observado no MQTT/painel | Entrada chegou ao barramento | Roda girou ou posição mudou |
| Status do serviço de motores | Alvo de ação e velocidades calculadas | Velocidade física medida por encoder |

O código atual não mede posição/encoder dos motores. A navegação, o GPS real e o retorno de execução pertencem às etapas de integração em [[wiki/planejamento/backlog]].

## Fontes e conferência

- [app/lib/services/robot_connection.dart](https://github.com/setrem-robot/aplicativo/blob/44d500160ecf13d7d1db2a4fe0c54052d352c0aa/lib/services/robot_connection.dart)
- [orquestrador/pi/services/motores/src/motores/main.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/pi/services/motores/src/motores/main.py)
- [orquestrador/cloud/ingestor/main.py](https://github.com/setrem-robot/orquestrador/blob/98ee681498e05426ff47041ae7f8e7ec97d0ffaf/cloud/ingestor/main.py)

---
[[INICIO|Início]] · [[wiki/meta/fontes|Fontes e limites da documentação]]
